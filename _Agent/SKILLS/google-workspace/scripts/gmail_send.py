#!/usr/bin/env python3
"""Send an email through Gmail.

This is a write-capable script. It requires --send to actually send.
"""

from __future__ import annotations

import argparse
import base64
from email.message import EmailMessage
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google_auth import get_credentials, gmail_send_token_path

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def _body_from_args(body: str | None, body_file: str | None) -> str:
    if body and body_file:
        raise SystemExit("Use either --body or --body-file, not both.")
    if body_file:
        return Path(body_file).expanduser().read_text(encoding="utf-8")
    if body:
        return body
    raise SystemExit("Email body is required. Use --body or --body-file.")


def _build_message(to: str, subject: str, body: str, sender: str = "me") -> dict:
    message = EmailMessage()
    message["To"] = to
    message["From"] = sender
    message["Subject"] = subject
    message.set_content(body)
    encoded = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return {"raw": encoded}


def main() -> None:
    parser = argparse.ArgumentParser(description="Send an email through Gmail.")
    parser.add_argument("--to", required=True, help="Recipient email address.")
    parser.add_argument("--subject", required=True, help="Email subject.")
    parser.add_argument("--body", help="Plain text email body.")
    parser.add_argument("--body-file", help="Path to a plain text body file.")
    parser.add_argument("--send", action="store_true", help="Actually send the email.")
    parser.add_argument("--dry-run", action="store_true", help="Preview without sending.")
    args = parser.parse_args()

    body = _body_from_args(args.body, args.body_file)

    if args.dry_run or not args.send:
        print("Gmail send dry run")
        print(f"- To: {args.to}")
        print(f"- Subject: {args.subject}")
        print("")
        print(body)
        if not args.send:
            print("\nNot sent. Add --send to send this email.")
        return

    try:
        service = build("gmail", "v1", credentials=get_credentials(SCOPES, token_file=gmail_send_token_path()))
        result = (
            service.users()
            .messages()
            .send(userId="me", body=_build_message(args.to, args.subject, body))
            .execute()
        )
    except HttpError as error:
        raise SystemExit(f"Gmail API error: {error}") from error

    print("Gmail message sent")
    print(f"- To: {args.to}")
    print(f"- Subject: {args.subject}")
    print(f"- Message ID: {result.get('id', '')}")


if __name__ == "__main__":
    main()
