#!/usr/bin/env python3
"""Shared read-only Google Workspace OAuth helper.

Credentials and tokens live outside the project repo by default.
This module never prints credential or token contents.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Sequence

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

DEFAULT_CONFIG_DIR = Path.home() / ".config" / "tindol-family-google"
DEFAULT_CREDENTIALS = DEFAULT_CONFIG_DIR / "credentials.json"
DEFAULT_TOKEN = DEFAULT_CONFIG_DIR / "token.json"

READONLY_SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/drive.metadata.readonly",
]


def credential_path() -> Path:
    return Path(os.environ.get("TINDOL_GOOGLE_CREDENTIALS", DEFAULT_CREDENTIALS)).expanduser()


def token_path() -> Path:
    return Path(os.environ.get("TINDOL_GOOGLE_TOKEN", DEFAULT_TOKEN)).expanduser()


def gmail_send_token_path() -> Path:
    default_path = DEFAULT_CONFIG_DIR / "token_gmail_send.json"
    return Path(os.environ.get("TINDOL_GOOGLE_SEND_TOKEN", default_path)).expanduser()


def drive_file_token_path() -> Path:
    default_path = DEFAULT_CONFIG_DIR / "token_drive_file.json"
    return Path(os.environ.get("TINDOL_GOOGLE_DRIVE_FILE_TOKEN", default_path)).expanduser()


def calendar_event_token_path() -> Path:
    default_path = DEFAULT_CONFIG_DIR / "token_calendar_event.json"
    return Path(os.environ.get("TINDOL_GOOGLE_CALENDAR_EVENT_TOKEN", default_path)).expanduser()


def get_credentials(scopes: Sequence[str] | None = None, token_file: Path | None = None) -> Credentials:
    """Return valid OAuth credentials for the requested scopes."""
    active_scopes = list(scopes or READONLY_SCOPES)
    creds_file = credential_path()
    active_token_file = token_file or token_path()

    if not creds_file.exists():
        raise FileNotFoundError(
            "Google credentials file not found. Expected it at "
            f"{creds_file}. Move your OAuth desktop credentials.json there."
        )

    creds = None
    if active_token_file.exists():
        creds = Credentials.from_authorized_user_file(str(active_token_file), active_scopes)

    missing_scopes = bool(creds and hasattr(creds, "has_scopes") and not creds.has_scopes(active_scopes))

    if missing_scopes:
        creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                creds = None
                flow = InstalledAppFlow.from_client_secrets_file(str(creds_file), active_scopes)
                creds = flow.run_local_server(port=0)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_file), active_scopes)
            creds = flow.run_local_server(port=0)

        # Attempt to persist the token, but handle sandbox/permission restrictions gracefully.
        try:
            active_token_file.parent.mkdir(parents=True, exist_ok=True)
            active_token_file.write_text(creds.to_json(), encoding="utf-8")
            active_token_file.chmod(0o600)
        except PermissionError:
            # In some sandboxed environments (like macOS Seatbelt), writing outside the project
            # may be blocked even if read access is allowed. We continue with the valid
            # in-memory credentials so the calling script can still complete.
            pass
        except Exception as e:
            # Log other unexpected errors but try to proceed.
            print(f"Warning: Could not save token to {active_token_file}: {e}")

    return creds
