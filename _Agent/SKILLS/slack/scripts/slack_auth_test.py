#!/usr/bin/env python3
"""Verify Slack token access with auth.test."""

from __future__ import annotations

from slack_auth import slack_api


def main() -> None:
    payload = slack_api("auth.test")
    print("Slack auth ok")
    print(f"- Team: {payload.get('team', '')}")
    print(f"- User: {payload.get('user', '')}")
    print(f"- Team ID: {payload.get('team_id', '')}")
    print(f"- User ID: {payload.get('user_id', '')}")


if __name__ == "__main__":
    main()
