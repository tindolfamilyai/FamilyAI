#!/usr/bin/env python3
"""Send a Slack message to a channel id or user id.

This is a write-capable script. It defaults to dry-run and requires --send to
actually post to Slack.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from slack_auth import slack_api


def _open_dm(user_id: str) -> str:
    payload = slack_api("conversations.open", {"users": user_id}, http_method="POST")
    channel = payload.get("channel", {})
    channel_id = channel.get("id")
    if not channel_id:
        raise RuntimeError("Slack did not return a DM channel id.")
    return channel_id


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a Slack message.")
    destination = parser.add_mutually_exclusive_group(required=True)
    destination.add_argument("--channel", help="Slack channel/conversation id, e.g. C123 or D123.")
    destination.add_argument("--user", help="Slack user id to open a DM with, e.g. U123.")
    message_input = parser.add_mutually_exclusive_group(required=True)
    message_input.add_argument("--text", help="Message text to send.")
    message_input.add_argument("--text-file", help="Path to UTF-8 text file to send.")
    parser.add_argument("--send", action="store_true", help="Actually send the Slack message.")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be sent without sending.")
    args = parser.parse_args()

    destination_label = args.channel or f"DM with {args.user}"
    message_text = args.text
    if args.text_file:
        text_path = Path(args.text_file).expanduser()
        if not text_path.exists():
            raise FileNotFoundError(f"Text file not found: {text_path}")
        message_text = text_path.read_text(encoding="utf-8")
    if not message_text or not message_text.strip():
        raise ValueError("Message text is empty.")

    if args.dry_run or not args.send:
        print("Slack send dry run")
        print(f"- Destination: {destination_label}")
        print(f"- Text length: {len(message_text)} chars")
        print(f"- Preview: {message_text[:160].strip()}")
        if not args.send:
            print("\nNot sent. Add --send to post this message.")
        return

    channel_id = args.channel or _open_dm(args.user)
    payload = slack_api(
        "chat.postMessage",
        {"channel": channel_id, "text": message_text},
        http_method="POST",
    )
    print("Slack message sent")
    print(f"- Channel: {payload.get('channel', channel_id)}")
    print(f"- Timestamp: {payload.get('ts', '')}")


if __name__ == "__main__":
    main()
