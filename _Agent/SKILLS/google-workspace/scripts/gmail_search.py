#!/usr/bin/env python3
"""Search Gmail using Gmail query syntax and print message summaries."""

from __future__ import annotations

import argparse
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Search Gmail read-only.")
    parser.add_argument("query", help="Gmail search query, e.g. 'from:target newer_than:30d'")
    parser.add_argument("--max-results", type=int, default=10)
    args = parser.parse_args()

    try:
        service = build("gmail", "v1", credentials=get_credentials(READONLY_SCOPES))
        search = (
            service.users()
            .messages()
            .list(userId="me", q=args.query, maxResults=args.max_results)
            .execute()
        )
        messages = search.get("messages", [])
        print(f"Gmail search: {args.query}")
        if not messages:
            print("No messages found.")
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
            sender = _header(headers, "From")
            subject = _header(headers, "Subject") or "(no subject)"
            date = _short_date(_header(headers, "Date"))
            snippet = msg.get("snippet", "")
            print(f"- {date} | {sender} | {subject} | {snippet}")
    except HttpError as error:
        raise SystemExit(f"Gmail API error: {error}") from error


if __name__ == "__main__":
    main()
