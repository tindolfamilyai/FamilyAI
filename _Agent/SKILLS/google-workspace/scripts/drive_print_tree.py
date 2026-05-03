#!/usr/bin/env python3
"""Print a Google Drive folder tree by folder name or id."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google_auth import READONLY_SCOPES, get_credentials

FOLDER_MIME = "application/vnd.google-apps.folder"


@dataclass
class DriveItem:
    id: str
    name: str
    mime_type: str

    @property
    def is_folder(self) -> bool:
        return self.mime_type == FOLDER_MIME


def escape_query(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def find_folder(service, folder_name: str) -> DriveItem:
    query = (
        "mimeType = 'application/vnd.google-apps.folder' "
        f"and name contains '{escape_query(folder_name)}' and trashed = false"
    )
    result = (
        service.files()
        .list(
            q=query,
            pageSize=20,
            fields="files(id, name, mimeType)",
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
        )
        .execute()
    )
    folders = [
        DriveItem(id=item["id"], name=item["name"], mime_type=item["mimeType"])
        for item in result.get("files", [])
    ]
    if not folders:
        raise SystemExit(f"No Drive folder found matching: {folder_name}")

    exact = [folder for folder in folders if folder.name.lower() == folder_name.lower()]
    return exact[0] if exact else folders[0]


def list_children(service, parent_id: str) -> list[DriveItem]:
    children: list[DriveItem] = []
    page_token = None
    while True:
        result = (
            service.files()
            .list(
                q=f"'{parent_id}' in parents and trashed = false",
                pageSize=100,
                pageToken=page_token,
                fields="nextPageToken, files(id, name, mimeType)",
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                orderBy="name",
            )
            .execute()
        )
        children.extend(
            DriveItem(id=item["id"], name=item["name"], mime_type=item["mimeType"])
            for item in result.get("files", [])
        )
        page_token = result.get("nextPageToken")
        if not page_token:
            break
    return sorted(children, key=lambda item: (not item.is_folder, item.name.lower()))


def print_tree(service, item: DriveItem, depth: int, max_depth: int, folders_only: bool) -> None:
    indent = "  " * depth
    marker = "[folder]" if item.is_folder else "[file]"
    print(f"{indent}- {item.name} {marker}")

    if not item.is_folder or depth >= max_depth:
        return

    for child in list_children(service, item.id):
        if folders_only and not child.is_folder:
            continue
        print_tree(service, child, depth + 1, max_depth, folders_only)


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a Google Drive folder tree.")
    parser.add_argument("folder", help="Folder name to search for, or folder id with --id")
    parser.add_argument("--id", action="store_true", help="Treat folder argument as a Drive folder id")
    parser.add_argument("--max-depth", type=int, default=5)
    parser.add_argument("--folders-only", action="store_true")
    args = parser.parse_args()

    try:
        service = build("drive", "v3", credentials=get_credentials(READONLY_SCOPES))
        root = (
            DriveItem(id=args.folder, name=args.folder, mime_type=FOLDER_MIME)
            if args.id
            else find_folder(service, args.folder)
        )
        print_tree(service, root, depth=0, max_depth=args.max_depth, folders_only=args.folders_only)
    except HttpError as error:
        raise SystemExit(f"Google Drive API error: {error}") from error


if __name__ == "__main__":
    main()
