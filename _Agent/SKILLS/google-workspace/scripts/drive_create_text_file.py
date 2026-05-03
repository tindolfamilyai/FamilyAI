#!/usr/bin/env python3
"""Create a Google Drive folder and upload a text file.

This is a write-capable script. It defaults to dry-run and requires --create to
actually create a Drive file.
"""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from google_auth import drive_file_token_path, get_credentials

FOLDER_MIME = "application/vnd.google-apps.folder"
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def _find_or_create_folder(service, name: str) -> str:
    escaped = name.replace("\\", "\\\\").replace("'", "\\'")
    query = f"mimeType = '{FOLDER_MIME}' and name = '{escaped}' and trashed = false"
    result = (
        service.files()
        .list(
            q=query,
            pageSize=10,
            fields="files(id, name)",
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
        )
        .execute()
    )
    folders = result.get("files", [])
    if folders:
        return folders[0]["id"]

    metadata = {"name": name, "mimeType": FOLDER_MIME}
    folder = service.files().create(body=metadata, fields="id").execute()
    return folder["id"]


def _upload_text_file(service, folder_id: str, filename: str, contents: str) -> dict:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as handle:
        temp_path = Path(handle.name)
        handle.write(contents)

    try:
        media = MediaFileUpload(str(temp_path), mimetype="text/plain", resumable=False)
        metadata = {"name": filename, "parents": [folder_id], "mimeType": "text/plain"}
        return (
            service.files()
            .create(body=metadata, media_body=media, fields="id, name, webViewLink")
            .execute()
        )
    finally:
        temp_path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Drive folder and text file.")
    parser.add_argument("--folder", required=True)
    parser.add_argument("--filename", required=True)
    parser.add_argument("--text", required=True)
    parser.add_argument("--create", action="store_true", help="Actually create the Drive folder/file.")
    parser.add_argument("--dry-run", action="store_true", help="Preview without creating.")
    args = parser.parse_args()

    if args.dry_run or not args.create:
        print("Google Drive create dry run")
        print(f"- Folder: {args.folder}")
        print(f"- Filename: {args.filename}")
        print(f"- Text length: {len(args.text)} chars")
        print(f"- Preview: {args.text[:160].strip()}")
        if not args.create:
            print("\nNot created. Add --create to create this Drive file.")
        return

    try:
        service = build("drive", "v3", credentials=get_credentials(SCOPES, token_file=drive_file_token_path()))
        folder_id = _find_or_create_folder(service, args.folder)
        file_info = _upload_text_file(service, folder_id, args.filename, args.text)
    except HttpError as error:
        raise SystemExit(f"Google Drive API error: {error}") from error

    print("Google Drive text file created")
    print(f"- Folder: {args.folder}")
    print(f"- Folder ID: {folder_id}")
    print(f"- File: {file_info.get('name', args.filename)}")
    print(f"- File ID: {file_info.get('id', '')}")
    print(f"- Link: {file_info.get('webViewLink', '')}")


if __name__ == "__main__":
    main()
