#!/usr/bin/env python3
"""Print recent Slack messages from a conversation id."""

from __future__ import annotations

import argparse
import datetime as dt

from slack_auth import slack_api


def _format_ts(value: str) -> str:
    try:
        seconds = float(value)
    except (TypeError, ValueError):
        return value
    return dt.datetime.fromtimestamp(seconds, tz=dt.timezone.utc).isoformat()


def main() -> None:
    parser = argparse.ArgumentParser(description="Read recent Slack messages from a conversation.")
    parser.add_argument("channel_id", help="Slack conversation id, e.g. C123 or D123")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    payload = slack_api(
        "conversations.history",
        {
            "channel": args.channel_id,
            "limit": str(args.limit),
        },
    )

    messages = payload.get("messages", [])
    print(f"Slack recent messages for {args.channel_id}")
    if not messages:
        print("No messages found.")
        return

    for message in messages:
        user = message.get("user") or message.get("username") or message.get("bot_id") or "unknown"
        text = (message.get("text") or "").replace("\n", " ").strip()
        print(f"- {_format_ts(message.get('ts', ''))} | {user} | {text}")


if __name__ == "__main__":
    main()
