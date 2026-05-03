#!/usr/bin/env python3
"""Print recent Gmail messages with full body in Markdown."""

from __future__ import annotations

import argparse
import base64
import re
from email.utils import parsedate_to_datetime
from html import unescape

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


def _decode_body(data: str | None) -> str:
    if not data:
        return ""
    padded = data + "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(padded.encode("utf-8")).decode("utf-8", errors="replace")


def _html_to_text(value: str) -> str:
    text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", "", value)
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)</p\s*>", "\n\n", text)
    text = re.sub(r"(?s)<[^>]+>", "", text)
    text = unescape(text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def _walk_parts(payload: dict) -> list[dict]:
    parts = []
    stack = [payload]
    while stack:
        part = stack.pop(0)
        parts.append(part)
        stack.extend(part.get("parts", []))
    return parts


def _message_body(payload: dict) -> str:
    plain_bodies: list[str] = []
    html_bodies: list[str] = []

    for part in _walk_parts(payload):
        mime_type = part.get("mimeType", "")
        filename = part.get("filename", "")
        if filename:
            continue
        body = _decode_body(part.get("body", {}).get("data"))
        if not body:
            continue
        if mime_type == "text/plain":
            plain_bodies.append(body.strip())
        elif mime_type == "text/html":
            html_bodies.append(_html_to_text(body))

    body = "\n\n".join(item for item in plain_bodies if item).strip()
    if body:
        return body
    return "\n\n".join(item for item in html_bodies if item).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Print recent Gmail messages as Markdown.")
    parser.add_argument("--query", default="in:inbox", help="Gmail query. Defaults to latest inbox messages.")
    parser.add_argument("--max-results", type=int, default=3)
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
        print(f"# Gmail Recent Messages\n\nQuery: `{args.query}`\n")

        if not messages:
            print("No messages found.")
            return

        for index, item in enumerate(messages, start=1):
            msg = service.users().messages().get(userId="me", id=item["id"], format="full").execute()
            payload = msg.get("payload", {})
            headers = payload.get("headers", [])
            sender = _header(headers, "From")
            subject = _header(headers, "Subject") or "(no subject)"
            date = _short_date(_header(headers, "Date"))
            body = _message_body(payload) or msg.get("snippet", "")

            print(f"## {index}. {subject}\n")
            print(f"- **From:** {sender}")
            print(f"- **Date:** {date}")
            print(f"- **Message ID:** `{msg.get('id', '')}`\n")
            print("### Body\n")
            print(body.strip() or "_No body text found._")
            print("\n---\n")
    except HttpError as error:
        raise SystemExit(f"Gmail API error: {error}") from error


if __name__ == "__main__":
    main()
