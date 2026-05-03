#!/usr/bin/env python3
"""List today's Google Calendar events from the primary calendar."""

from __future__ import annotations

import datetime as dt
import os
from zoneinfo import ZoneInfo

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google_auth import READONLY_SCOPES, get_credentials


def main() -> None:
    timezone_name = os.environ.get("TINDOL_GOOGLE_TIMEZONE", "America/New_York")
    tz = ZoneInfo(timezone_name)
    today = dt.datetime.now(tz).date()
    time_min = dt.datetime.combine(today, dt.time.min, tzinfo=tz).isoformat()
    time_max = dt.datetime.combine(today + dt.timedelta(days=1), dt.time.min, tzinfo=tz).isoformat()

    try:
        service = build("calendar", "v3", credentials=get_credentials(READONLY_SCOPES))
        result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
    except HttpError as error:
        raise SystemExit(f"Google Calendar API error: {error}") from error

    events = result.get("items", [])
    print(f"Google Calendar events for {today.isoformat()} ({timezone_name})")
    if not events:
        print("No events found.")
        return

    for event in events:
        start = event.get("start", {})
        start_value = start.get("dateTime") or start.get("date") or "unknown time"
        summary = event.get("summary", "(no title)")
        print(f"- {start_value}: {summary}")


if __name__ == "__main__":
    main()
