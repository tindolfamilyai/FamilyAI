#!/usr/bin/env python3
"""List visible Slack conversations."""

from __future__ import annotations

import argparse

from slack_auth import slack_api


def main() -> None:
    parser = argparse.ArgumentParser(description="List Slack conversations read-only.")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument(
        "--types",
        default="public_channel,private_channel,mpim,im",
        help="Comma-separated Slack conversation types.",
    )
    args = parser.parse_args()

    payload = slack_api(
        "conversations.list",
        {
            "exclude_archived": "true",
            "limit": str(args.limit),
            "types": args.types,
        },
    )

    channels = payload.get("channels", [])
    print("Slack conversations")
    if not channels:
        print("No conversations found.")
        return

    for channel in channels:
        name = channel.get("name") or channel.get("user") or channel.get("id")
        private = "private" if channel.get("is_private") else "public"
        member = "member" if channel.get("is_member") else "not-member"
        print(f"- {name} | {channel.get('id')} | {private} | {member}")


if __name__ == "__main__":
    main()
