#!/usr/bin/env python3
"""Shared read-only Slack API helper.

The Slack token lives outside the project repo by default.
This module never prints token contents.
"""

from __future__ import annotations

import json
import os
import ssl
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

DEFAULT_TOKEN_FILE = Path.home() / ".config" / "tindol-family-slack" / "slack.env"


def _ssl_context() -> ssl.SSLContext:
    try:
        import certifi  # type: ignore

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def token_file_path() -> Path:
    return Path(os.environ.get("TINDOL_SLACK_TOKEN_FILE", DEFAULT_TOKEN_FILE)).expanduser()


def _load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def get_token() -> str:
    token = os.environ.get("SLACK_BOT_TOKEN")
    if token:
        return token

    values = _load_env_file(token_file_path())
    token = values.get("SLACK_BOT_TOKEN")
    if token:
        return token

    raise FileNotFoundError(
        "Slack token not found. Expected SLACK_BOT_TOKEN in the environment "
        f"or in {token_file_path()}."
    )


def slack_api(
    method: str,
    params: dict[str, Any] | None = None,
    *,
    http_method: str = "GET",
) -> dict[str, Any]:
    query = urllib.parse.urlencode(params or {})
    url = f"https://slack.com/api/{method}"
    body = None
    normalized_method = http_method.upper()
    if query and normalized_method == "GET":
        url = f"{url}?{query}"
    elif query:
        body = query.encode("utf-8")

    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {get_token()}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method=normalized_method,
    )

    with urllib.request.urlopen(request, timeout=30, context=_ssl_context()) as response:
        payload = json.loads(response.read().decode("utf-8"))

    if not payload.get("ok"):
        error = payload.get("error", "unknown_error")
        needed = payload.get("needed")
        provided = payload.get("provided")
        details = f"Slack API error for {method}: {error}"
        if needed:
            details += f" (needed: {needed}; provided: {provided})"
        raise RuntimeError(details)

    return payload
