#!/usr/bin/env python3
"""Create a Google Calendar event.

This is a write-capable script. It defaults to dry-run and requires --create to
actually create a calendar event.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
from zoneinfo import ZoneInfo

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google_auth import calendar_event_token_path, get_credentials

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def _parse_local_datetime(value: str, timezone_name: str) -> dt.datetime:
    tz = ZoneInfo(timezone_name)
    parsed = dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=tz)
    return parsed.astimezone(tz)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Google Calendar event.")
    parser.add_argument("--summary", required=True)
    parser.add_argument("--start", required=True, help="Local ISO datetime, e.g. 2026-04-30T12:00:00")
    parser.add_argument("--duration-minutes", type=int, default=60)
    parser.add_argument("--calendar-id", default="primary")
    parser.add_argument("--timezone", default=os.environ.get("TINDOL_GOOGLE_TIMEZONE", "America/New_York"))
    parser.add_argument("--description", default="")
    parser.add_argument("--create", action="store_true", help="Actually create the calendar event.")
    parser.add_argument("--dry-run", action="store_true", help="Preview without creating.")
    args = parser.parse_args()

    start = _parse_local_datetime(args.start, args.timezone)
    end = start + dt.timedelta(minutes=args.duration_minutes)
    body = {
        "summary": args.summary,
        "description": args.description,
        "start": {"dateTime": start.isoformat(), "timeZone": args.timezone},
        "end": {"dateTime": end.isoformat(), "timeZone": args.timezone},
    }

    if args.dry_run or not args.create:
        print("Google Calendar create dry run")
        print(f"- Calendar ID: {args.calendar_id}")
        print(f"- Summary: {args.summary}")
        print(f"- Start: {start.isoformat()}")
        print(f"- End: {end.isoformat()}")
        if args.description:
            print(f"- Description: {args.description}")
        if not args.create:
            print("\nNot created. Add --create to create this event.")
        return

    try:
        service = build("calendar", "v3", credentials=get_credentials(SCOPES, token_file=calendar_event_token_path()))
        result = service.events().insert(calendarId=args.calendar_id, body=body).execute()
    except HttpError as error:
        raise SystemExit(f"Google Calendar API error: {error}") from error

    print("Google Calendar event created")
    print(f"- Summary: {result.get('summary', args.summary)}")
    print(f"- Start: {result.get('start', {}).get('dateTime', '')}")
    print(f"- End: {result.get('end', {}).get('dateTime', '')}")
    print(f"- Link: {result.get('htmlLink', '')}")


if __name__ == "__main__":
    main()
