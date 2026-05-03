#!/usr/bin/env python3
"""List recent Google Drive file metadata."""

from __future__ import annotations

import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google_auth import READONLY_SCOPES, get_credentials


def main() -> None:
    parser = argparse.ArgumentParser(description="List recent Drive files read-only.")
    parser.add_argument("--max-results", type=int, default=10)
    args = parser.parse_args()

    try:
        service = build("drive", "v3", credentials=get_credentials(READONLY_SCOPES))
        result = (
            service.files()
            .list(
                pageSize=args.max_results,
                orderBy="modifiedTime desc",
                fields="files(id, name, mimeType, modifiedTime)",
            )
            .execute()
        )
    except HttpError as error:
        raise SystemExit(f"Google Drive API error: {error}") from error

    files = result.get("files", [])
    print("Recent Google Drive files")
    if not files:
        print("No files found.")
        return

    for file in files:
        print(
            f"- {file.get('modifiedTime', '')} | {file.get('name', '')} | "
            f"{file.get('mimeType', '')} | {file.get('id', '')}"
        )


if __name__ == "__main__":
    main()
