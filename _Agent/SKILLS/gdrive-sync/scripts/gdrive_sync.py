#!/usr/bin/env python3
"""Sync Tindol Family domain folders and Docs to Google Drive.

Defaults to dry-run. Add --sync to actually upload files.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Reuse the shared google_auth helper from the google-workspace skill.
GOOGLE_WS_SCRIPTS = Path(__file__).resolve().parents[2] / "google-workspace" / "scripts"
sys.path.insert(0, str(GOOGLE_WS_SCRIPTS))

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from google_auth import drive_file_token_path, get_credentials

PROJECT_ROOT = Path(__file__).resolve().parents[4]
FOLDER_MIME = "application/vnd.google-apps.folder"
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
SKIP_DIRS = {".claude", ".agents", ".gemini", "_Agent", ".git"}
SKIP_EXTENSIONS = {".pyc", ".pyo"}
DOMAIN_PREFIXES = tuple(f"{i:02d}_" for i in range(10))
DEFAULT_TOP_LEVEL_FOLDERS = ("Docs",)


def find_sync_folders(root: Path, domains: list[str] | None) -> list[Path]:
    folders = [
        item
        for item in sorted(root.iterdir())
        if item.is_dir() and item.name.startswith(DOMAIN_PREFIXES)
    ]
    if domains:
        return [f for f in folders if any(f.name.startswith(f"{d}_") for d in domains)]

    for name in DEFAULT_TOP_LEVEL_FOLDERS:
        folder = root / name
        if folder.is_dir():
            folders.append(folder)
    return folders


def _find_or_create_folder(service, name: str, parent_id: str | None = None) -> str:
    escaped = name.replace("\\", "\\\\").replace("'", "\\'")
    parent_clause = f" and '{parent_id}' in parents" if parent_id else ""
    query = f"mimeType = '{FOLDER_MIME}' and name = '{escaped}' and trashed = false{parent_clause}"
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
    metadata: dict = {"name": name, "mimeType": FOLDER_MIME}
    if parent_id:
        metadata["parents"] = [parent_id]
    folder = service.files().create(body=metadata, fields="id").execute()
    return folder["id"]


def _find_file(service, name: str, parent_id: str) -> str | None:
    escaped = name.replace("\\", "\\\\").replace("'", "\\'")
    query = (
        f"name = '{escaped}' and '{parent_id}' in parents"
        f" and trashed = false and mimeType != '{FOLDER_MIME}'"
    )
    result = (
        service.files()
        .list(q=query, pageSize=5, fields="files(id)")
        .execute()
    )
    files = result.get("files", [])
    return files[0]["id"] if files else None


def _upload_file(service, local_path: Path, parent_id: str) -> dict:
    media = MediaFileUpload(str(local_path), resumable=False)
    existing_id = _find_file(service, local_path.name, parent_id)
    if existing_id:
        return (
            service.files()
            .update(fileId=existing_id, media_body=media, fields="id, name, webViewLink")
            .execute()
        )
    metadata: dict = {"name": local_path.name, "parents": [parent_id]}
    return (
        service.files()
        .create(body=metadata, media_body=media, fields="id, name, webViewLink")
        .execute()
    )


def _sync_folder_recursive(
    service,
    local_folder: Path,
    parent_drive_id: str,
    stats: dict,
    prefix: str,
) -> None:
    drive_folder_id = _find_or_create_folder(service, local_folder.name, parent_drive_id)
    for item in sorted(local_folder.iterdir()):
        if item.name.startswith(".") or item.name in SKIP_DIRS:
            continue
        if item.is_dir():
            _sync_folder_recursive(service, item, drive_folder_id, stats, prefix + "  ")
        elif item.is_file():
            if item.suffix in SKIP_EXTENSIONS:
                continue
            try:
                _upload_file(service, item, drive_folder_id)
                rel = item.relative_to(PROJECT_ROOT)
                print(f"{prefix}  synced: {rel}")
                stats["uploaded"] += 1
            except HttpError as exc:
                rel = item.relative_to(PROJECT_ROOT)
                print(f"{prefix}  ERROR: {rel}: {exc}", file=sys.stderr)
                stats["errors"] += 1


def _dry_run_folder(local_folder: Path, stats: dict, prefix: str = "") -> None:
    for item in sorted(local_folder.iterdir()):
        if item.name.startswith(".") or item.name in SKIP_DIRS:
            continue
        if item.is_dir():
            _dry_run_folder(item, stats, prefix + "  ")
        elif item.is_file():
            if item.suffix in SKIP_EXTENSIONS:
                continue
            rel = item.relative_to(PROJECT_ROOT)
            print(f"  [dry run] {rel}")
            stats["would_upload"] += 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", default="Tindol Family Hub", help="Root Drive folder name.")
    parser.add_argument("--sync", action="store_true", help="Actually upload files to Drive.")
    parser.add_argument("--dry-run", dest="force_dry", action="store_true", help="Preview only.")
    parser.add_argument(
        "--domains",
        nargs="*",
        metavar="NN",
        help="Two-digit domain numbers to sync, e.g. 00 06. Default: all domains plus Docs.",
    )
    args = parser.parse_args()

    sync_folders = find_sync_folders(PROJECT_ROOT, args.domains)
    if not sync_folders:
        raise SystemExit("No matching sync folders found.")

    is_dry_run = args.force_dry or not args.sync

    print(f"Google Drive sync {'(DRY RUN)' if is_dry_run else ''}")
    print(f"Root Drive folder: {args.folder}")
    print(f"Sync folders: {[f.name for f in sync_folders]}")
    print()

    if is_dry_run:
        stats: dict = {"would_upload": 0}
        for folder in sync_folders:
            print(f"{folder.name}/")
            _dry_run_folder(folder, stats)
            print()
        print(f"Would upload {stats['would_upload']} file(s).")
        print("\nNot synced. Add --sync to upload files to Google Drive.")
        return

    try:
        creds = get_credentials(SCOPES, token_file=drive_file_token_path())
        service = build("drive", "v3", credentials=creds)
    except Exception as exc:
        raise SystemExit(f"Google Drive auth error: {exc}") from exc

    try:
        root_id = _find_or_create_folder(service, args.folder)
    except HttpError as exc:
        raise SystemExit(f"Could not find or create root Drive folder: {exc}") from exc

    stats = {"uploaded": 0, "errors": 0}
    for folder in sync_folders:
        print(f"{folder.name}/")
        try:
            _sync_folder_recursive(service, folder, root_id, stats, "")
        except HttpError as exc:
            print(f"  ERROR in {folder.name}: {exc}", file=sys.stderr)
            stats["errors"] += 1
        print()

    print(f"Sync complete: {stats['uploaded']} file(s) uploaded, {stats['errors']} error(s).")
    if stats["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
