#!/usr/bin/env python3
"""Print Gmail message summaries for a specific date in Markdown."""

from __future__ import annotations

import argparse
from datetime import date, timedelta
from email.utils import parsedate_to_datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google_auth import READONLY_SCOPES, get_credentials


def _header(headers: list[dict], name: str) -> str:
    for header in headers:
        if header.get("name", "").lower() == name.lower():
            return header.get("value", "")
    return ""


def _short_date(value: str) -> str:
    if not value:
        return ""
    try:
        return parsedate_to_datetime(value).isoformat()
    except (TypeError, ValueError):
        return value


def _gmail_date(value: date) -> str:
    return value.strftime("%Y/%m/%d")


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize Gmail arrivals for a date.")
    parser.add_argument("--date", required=True, help="Date in YYYY-MM-DD format.")
    parser.add_argument("--max-results", type=int, default=25)
    args = parser.parse_args()

    target = date.fromisoformat(args.date)
    next_day = target + timedelta(days=1)
    query = f"after:{_gmail_date(target)} before:{_gmail_date(next_day)}"

    try:
        service = build("gmail", "v1", credentials=get_credentials(READONLY_SCOPES))
        search = (
            service.users()
            .messages()
            .list(userId="me", q=query, maxResults=args.max_results)
            .execute()
        )
        messages = search.get("messages", [])
        print(f"## Email Arrivals — {target.isoformat()}\n")
        print(f"Query: `{query}`\n")
        if not messages:
            print("- None found")
            return

        for item in messages:
            msg = (
                service.users()
                .messages()
                .get(
                    userId="me",
                    id=item["id"],
                    format="metadata",
                    metadataHeaders=["From", "Subject", "Date"],
                )
                .execute()
            )
            payload = msg.get("payload", {})
            headers = payload.get("headers", [])
            sender = _header(headers, "From") or "(unknown sender)"
            subject = _header(headers, "Subject") or "(no subject)"
            sent_time = _short_date(_header(headers, "Date"))
            snippet = msg.get("snippet", "").strip() or "(no snippet)"
            print(f"- **From:** {sender}")
            print(f"  **Date:** {sent_time}")
            print(f"  **Subject:** {subject}")
            print(f"  **Snippet:** {snippet}")
    except HttpError as error:
        raise SystemExit(f"Gmail API error: {error}") from error


if __name__ == "__main__":
    main()
