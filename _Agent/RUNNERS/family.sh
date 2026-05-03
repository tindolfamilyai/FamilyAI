#!/bin/bash
set -euo pipefail

# family.sh - launch Claude Code, Codex CLI, or Gemini CLI from the Tindol Family Hub root.

PROJECT="/Users/tindolhouse/Documents/Claude/Projects/Tindol Family Codex Claude"
STATE_FILE="$HOME/.family-ai-tool"

find_tool() {
  local tool="$1"
  local found=""

  if found="$(command -v "$tool" 2>/dev/null)"; then
    printf '%s\n' "$found"
    return 0
  fi

  if [[ "$tool" == "codex" ]]; then
    found="$(find "$HOME/.vscode/extensions" -path '*/bin/macos-aarch64/codex' -type f 2>/dev/null | sort | tail -n 1 || true)"
    if [[ -n "$found" && -x "$found" ]]; then
      printf '%s\n' "$found"
      return 0
    fi
  fi

  if [[ "$tool" == "gemini" ]]; then
    found="$(find "$HOME/.nvm/versions/node" -path '*/bin/gemini' -type f 2>/dev/null | sort | tail -n 1 || true)"
    if [[ -n "$found" && -x "$found" ]]; then
      printf '%s\n' "$found"
      return 0
    fi
  fi

  return 1
}

active_tool() {
  local saved
  saved="$(cat "$STATE_FILE" 2>/dev/null || true)"
  case "$saved" in
    claude|codex|gemini) printf '%s\n' "$saved" ;;
    *) printf '%s\n' "codex" ;;
  esac
}

fallback_tool() {
  local tool
  for tool in codex gemini; do
    if find_tool "$tool" >/dev/null; then
      printf '%s\n' "$tool"
      return 0
    fi
  done
  return 1
}

show_status() {
  local active="$1"
  printf 'Project: %s\n' "$PROJECT"
  printf 'Active tool: %s\n' "$active"
  for tool in claude codex gemini; do
    if path="$(find_tool "$tool")"; then
      printf '%s: installed at %s\n' "$tool" "$path"
    else
      printf '%s: missing\n' "$tool"
    fi
  done
}

if [[ "${1:-}" == "status" ]]; then
  show_status "$(active_tool)"
  exit 0
fi

if [[ "${1:-}" == "use" ]]; then
  case "${2:-}" in
    claude|codex|gemini)
      printf '%s\n' "$2" > "$STATE_FILE"
      printf 'Now using %s\n' "$2"
      if ! find_tool "$2" >/dev/null; then
        printf 'WARNING: %s is not installed or not on PATH.\n' "$2" >&2
      fi
      exit 0
      ;;
    *)
      printf 'Usage: family use claude|codex|gemini\n' >&2
      exit 2
      ;;
  esac
fi

is_daily_brief_prompt() {
  local prompt
  prompt="$(printf '%s' "$*" | tr '[:upper:]' '[:lower:]')"
  case "$prompt" in
    *"daily brief"*|*"daily-brief"*|*"morning brief"*|*"start my day"*|*"/daily-brief"*)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

daily_brief_mode() {
  local prompt
  prompt="$(printf '%s' "$*" | tr '[:upper:]' '[:lower:]')"
  case "$prompt" in
    *"chat-only"*|*"chat only"*|*"do not save"*|*"don't save"*|*"no-save"*|*"no save"*|*"do not send"*|*"don't send"*|*"no-slack"*|*"no slack"*)
      printf '%s\n' "chat-only"
      ;;
    *)
      printf '%s\n' "saved-slack"
      ;;
  esac
}

requested_tool=""
explicit_tool=0
if [[ "${1:-}" == "claude" || "${1:-}" == "codex" || "${1:-}" == "gemini" ]]; then
  requested_tool="$1"
  explicit_tool=1
  shift
else
  requested_tool="$(active_tool)"
fi

if [[ "$#" -gt 0 ]] && is_daily_brief_prompt "$@"; then
  cd "$PROJECT" || { printf 'ERROR: project root not found at %s\n' "$PROJECT" >&2; exit 1; }
  mode="$(daily_brief_mode "$@")"
  engine="codex"
  if [[ "$requested_tool" == "gemini" ]]; then
    engine="gemini"
  fi
  if [[ "$engine" == "gemini" ]] && ! find_tool "gemini" >/dev/null; then
    if [[ "$explicit_tool" == "1" ]]; then
      printf 'ERROR: gemini is not installed or not on PATH.\n' >&2
      exit 127
    fi
    fallback="$(fallback_tool || true)"
    if [[ -z "$fallback" ]]; then
      printf 'ERROR: no supported fallback tool is installed.\n' >&2
      exit 127
    fi
    printf 'WARNING: gemini is missing; falling back to %s.\n' "$fallback" >&2
    engine="$fallback"
  fi
  printf '[family] using: daily brief runner via %s engine (%s)\n' "$engine" "$mode"
  exec "$PROJECT/_Agent/RUNNERS/daily_brief.sh" --engine "$engine" --mode "$mode"
fi

tool_path=""
if ! tool_path="$(find_tool "$requested_tool")"; then
  if [[ "$explicit_tool" == "1" ]]; then
    printf 'ERROR: %s is not installed or not on PATH.\n' "$requested_tool" >&2
    exit 127
  elif fallback="$(fallback_tool || true)" && [[ -n "$fallback" ]]; then
    printf 'WARNING: %s is missing; falling back to %s.\n' "$requested_tool" "$fallback" >&2
    requested_tool="$fallback"
    tool_path="$(find_tool "$requested_tool")"
  else
    printf 'ERROR: %s is not installed or not on PATH.\n' "$requested_tool" >&2
    exit 127
  fi
fi

cd "$PROJECT" || { printf 'ERROR: project root not found at %s\n' "$PROJECT" >&2; exit 1; }
printf '[family] using: %s\n' "$requested_tool"
if [[ "$requested_tool" == "gemini" ]]; then
  exec "$tool_path" --skip-trust "$@"
fi
exec "$tool_path" "$@"
