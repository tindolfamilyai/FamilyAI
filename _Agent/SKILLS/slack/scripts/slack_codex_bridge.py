#!/usr/bin/env python3
"""Poll a Slack channel for explicit Codex prompts and reply in-thread.

Default trigger in General:

    codex: run daily brief chat-only

This script intentionally polls Slack Web API instead of requiring a public
inbound webhook URL. It stores processing state under _Reports/Slack_Codex/.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

from slack_auth import slack_api

PROJECT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CHANNEL = "C0AUWRU29V5"
DEFAULT_STATE = PROJECT_ROOT / "_Reports" / "Slack_Codex" / "state.json"
DEFAULT_LOG_DIR = PROJECT_ROOT / "_Reports" / "Slack_Codex" / "logs"
DEFAULT_TRIGGER = "codex:"
MAX_REPLY_CHARS = 3500


SLACK_FORMATTING_RULES = """Slack response formatting rules:
- Keep the answer concise and directly actionable.
- Use Slack mrkdwn: *bold* for labels, bullets with "- ", and inline code with backticks.
- Slack does not render Markdown tables. If a table is useful, put it inside a fenced code block so columns stay aligned.
- Avoid dumping command logs, tool traces, or raw file reads.
- End with file paths only when they matter to the user.
"""


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def _find_codex() -> str:
    for path in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(path) / "codex"
        if candidate.exists() and os.access(candidate, os.X_OK):
            return str(candidate)

    extension_root = Path.home() / ".vscode" / "extensions"
    candidates = sorted(extension_root.glob("*/bin/macos-aarch64/codex"))
    for candidate in reversed(candidates):
        if candidate.exists() and os.access(candidate, os.X_OK):
            return str(candidate)

    raise FileNotFoundError("codex CLI not found in PATH or VS Code extension bins.")


def _load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _append_log(log_dir: Path, text: str) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{time.strftime('%Y-%m-%d')}.log"
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(text.rstrip() + "\n")


def _post_reply(channel: str, thread_ts: str, text: str, *, dry_run: bool) -> None:
    if dry_run:
        print("Slack reply dry run")
        print(f"- Channel: {channel}")
        print(f"- Thread: {thread_ts}")
        print(f"- Text: {text[:500]}")
        return
    slack_api(
        "chat.postMessage",
        {"channel": channel, "thread_ts": thread_ts, "text": text},
        http_method="POST",
    )


def _run_codex(prompt: str, timeout_seconds: int) -> tuple[int, str]:
    codex = _find_codex()
    env = os.environ.copy()
    env["TZ"] = "America/New_York"
    env["PATH"] = (
        f"{Path.home() / '.local' / 'bin'}:/opt/homebrew/bin:/usr/local/bin:"
        f"{env.get('PATH', '')}"
    )
    bridge_prompt = (
        "You are being invoked from the Tindol Family Slack General channel via "
        "the local slack_codex_bridge.py runner. Follow the repository AGENTS.md "
        "and safety rules. Keep Slack replies concise. Do not expose secrets or "
        "token contents. If an action would require a destructive or sensitive "
        "external change, refuse or draft only.\n\n"
        f"{SLACK_FORMATTING_RULES}\n"
        f"Slack request:\n{prompt}"
    )
    with tempfile.NamedTemporaryFile(prefix="slack-codex-", suffix=".txt", delete=False) as handle:
        output_path = Path(handle.name)
    try:
        command = [
            codex,
            "--ask-for-approval",
            "never",
            "exec",
            "-C",
            str(PROJECT_ROOT),
            "--skip-git-repo-check",
            "--ephemeral",
            "--sandbox",
            "workspace-write",
            "--output-last-message",
            str(output_path),
            bridge_prompt,
        ]
        completed = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout_seconds,
            check=False,
        )
        final_message = ""
        if output_path.exists():
            final_message = output_path.read_text(encoding="utf-8").strip()
        if final_message:
            return completed.returncode, final_message
        return completed.returncode, completed.stdout.strip()
    finally:
        try:
            output_path.unlink()
        except FileNotFoundError:
            pass


def _format_reply(exit_code: int, output: str) -> str:
    if not output:
        output = "(Codex returned no output.)"
    if len(output) > MAX_REPLY_CHARS:
        output = output[-MAX_REPLY_CHARS:]
        output = f"...output truncated to last {MAX_REPLY_CHARS} chars...\n{output}"
    if exit_code == 0:
        return output
    return f"Codex exited with code {exit_code}.\n\n{output}"


def _message_prompt(message: dict[str, Any], trigger: str) -> str | None:
    if message.get("subtype") or message.get("bot_id"):
        return None
    text = (message.get("text") or "").strip()
    if not text.lower().startswith(trigger.lower()):
        return None
    prompt = text[len(trigger) :].strip()
    return prompt or None


def process_once(args: argparse.Namespace) -> int:
    state = _load_state(args.state_file)
    latest_seen = state.get(args.channel, "0")
    payload = slack_api(
        "conversations.history",
        {
            "channel": args.channel,
            "oldest": latest_seen,
            "limit": str(args.limit),
            "inclusive": "false",
        },
    )
    messages = sorted(payload.get("messages", []), key=lambda item: float(item.get("ts", "0")))
    processed = 0
    newest = latest_seen

    for message in messages:
        ts = message.get("ts")
        if not ts:
            continue
        newest = max(newest, ts, key=lambda value: float(value))
        prompt = _message_prompt(message, args.trigger)
        if not prompt:
            continue

        processed += 1
        thread_ts = message.get("thread_ts") or ts
        user = message.get("user", "unknown")
        _append_log(args.log_dir, f"{_now()} request ts={ts} user={user}: {prompt}")
        state[args.channel] = newest
        _save_state(args.state_file, state)
        _post_reply(args.channel, thread_ts, "Codex received this. Running now...", dry_run=args.dry_run)
        try:
            exit_code, output = _run_codex(prompt, args.timeout_seconds)
            reply = _format_reply(exit_code, output)
        except subprocess.TimeoutExpired:
            reply = f"Codex timed out after {args.timeout_seconds} seconds."
            exit_code = 124
        except Exception as exc:
            reply = f"Codex bridge error: {exc}"
            exit_code = 1
        _append_log(args.log_dir, f"{_now()} result ts={ts} exit={exit_code}")
        _post_reply(args.channel, thread_ts, reply, dry_run=args.dry_run)

    if newest != latest_seen:
        state[args.channel] = newest
        _save_state(args.state_file, state)

    return processed


def mark_now(args: argparse.Namespace) -> None:
    payload = slack_api(
        "conversations.history",
        {
            "channel": args.channel,
            "limit": "1",
        },
    )
    messages = payload.get("messages", [])
    if not messages:
        print(f"No messages found in {args.channel}; state unchanged.")
        return
    latest = messages[0].get("ts")
    if not latest:
        print(f"Latest message in {args.channel} had no timestamp; state unchanged.")
        return
    state = _load_state(args.state_file)
    state[args.channel] = latest
    _save_state(args.state_file, state)
    print(f"Marked {args.channel} current through Slack ts {latest}.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--channel", default=DEFAULT_CHANNEL, help="Slack channel id to watch.")
    parser.add_argument("--trigger", default=DEFAULT_TRIGGER, help="Required message prefix.")
    parser.add_argument("--interval", type=int, default=15, help="Polling interval in seconds.")
    parser.add_argument("--limit", type=int, default=50, help="Max Slack messages to inspect per poll.")
    parser.add_argument("--timeout-seconds", type=int, default=600, help="Max Codex runtime per request.")
    parser.add_argument("--state-file", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--log-dir", type=Path, default=DEFAULT_LOG_DIR)
    parser.add_argument("--once", action="store_true", help="Process one poll and exit.")
    parser.add_argument("--mark-now", action="store_true", help="Set state to the latest channel message and exit.")
    parser.add_argument("--dry-run", action="store_true", help="Do not post replies to Slack.")
    args = parser.parse_args()

    args.state_file = args.state_file.expanduser()
    args.log_dir = args.log_dir.expanduser()

    if args.mark_now:
        mark_now(args)
        return 0

    if args.once:
        processed = process_once(args)
        print(f"Processed {processed} Slack Codex request(s).")
        return 0

    startup = f"Slack Codex bridge watching channel {args.channel} for prefix {args.trigger!r}."
    print(startup, flush=True)
    _append_log(args.log_dir, f"{_now()} {startup}")
    while True:
        try:
            process_once(args)
        except KeyboardInterrupt:
            raise
        except Exception as exc:
            _append_log(args.log_dir, f"{_now()} bridge error: {exc}")
            print(f"Bridge error: {exc}", file=sys.stderr)
        time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())
