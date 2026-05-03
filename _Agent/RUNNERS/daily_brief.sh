#!/bin/bash
set -euo pipefail

PROJECT_ROOT="/Users/tindolhouse/Documents/Claude/Projects/Tindol Family Codex Claude"
LOG_DIR="$PROJECT_ROOT/_Reports/Daily_Briefs/logs"
DATE_STAMP="$(date +%F)"
LOG_FILE="$LOG_DIR/${DATE_STAMP}_daily_brief_runner.log"
ENGINE="codex"
MODE="saved-slack"

usage() {
  echo "Usage: $0 [--engine codex|gemini] [--mode saved-slack|chat-only]" >&2
}

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --engine)
      ENGINE="${2:-}"
      shift 2
      ;;
    --mode)
      MODE="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage
      exit 2
      ;;
  esac
done

case "$ENGINE" in
  codex|gemini) ;;
  *)
    echo "ERROR: --engine must be codex or gemini" >&2
    exit 2
    ;;
esac

case "$MODE" in
  saved-slack|chat-only) ;;
  *)
    echo "ERROR: --mode must be saved-slack or chat-only" >&2
    exit 2
    ;;
esac

mkdir -p "$LOG_DIR"
cd "$PROJECT_ROOT"

# Ensure consistent timezone
export TZ="America/New_York"
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
for node_bin in "$HOME"/.nvm/versions/node/*/bin; do
  if [[ -d "$node_bin" ]]; then
    export PATH="$node_bin:$PATH"
  fi
done

find_codex() {
  local found
  found="$(command -v codex || true)"
  if [[ -z "$found" ]]; then
    found="$(find "/Users/tindolhouse/.vscode/extensions" -path '*/bin/macos-aarch64/codex' -type f 2>/dev/null | sort | tail -n 1 || true)"
  fi
  printf '%s\n' "$found"
}

find_gemini() {
  local found
  found="$(command -v gemini || true)"
  if [[ -z "$found" ]]; then
    found="$(find "$HOME/.nvm/versions/node" -path '*/bin/gemini' -type f 2>/dev/null | sort | tail -n 1 || true)"
  fi
  printf '%s\n' "$found"
}

saved_slack_prompt="Run skill daily-brief for today's date using the default saved-and-Slack behavior. Save the brief to _Reports/Daily_Briefs/YYYY-MM-DD_daily_brief.md. Then send that same saved brief to Slack channel C0AUWRU29V5 using _Agent/SKILLS/slack/scripts/slack_send_message.py with --text-file and --send. Do not ask for approval. If Google or Slack fails, still save the brief and include failures under Notes / Gaps."
chat_only_prompt="Run skill daily-brief for today's date in chat-only mode. Do not save a file. Do not send or post to Slack. Do not ask for approval. If Google or Slack access is unavailable, still produce the local brief in chat and include failures under Notes / Gaps."

if [[ "$MODE" == "chat-only" ]]; then
  PROMPT="$chat_only_prompt"
else
  PROMPT="$saved_slack_prompt"
fi

if [[ "${FAMILY_DAILY_BRIEF_DRY_RUN:-}" == "1" ]]; then
  if [[ "$ENGINE" == "gemini" ]]; then
    TOOL_BIN="$(find_gemini)"
  else
    TOOL_BIN="$(find_codex)"
  fi
  echo "Daily brief dry run"
  echo "- Engine: $ENGINE"
  echo "- Tool: ${TOOL_BIN:-missing}"
  echo "- Mode: $MODE"
  echo "- Project: $PROJECT_ROOT"
  echo "- Log: $LOG_FILE"
  echo "- Approval mode: no prompts"
  echo "- Network access: enabled"
  echo "- Extra writable roots: /Users/tindolhouse/.config/tindol-family-google, /Users/tindolhouse/.config/tindol-family-slack"
  echo "- Slack channel: C0AUWRU29V5"
  if [[ "$ENGINE" == "gemini" ]]; then
    echo "- Command: gemini --skip-trust --approval-mode=yolo --sandbox -p \"$PROMPT\""
  else
    echo "- Command: codex --ask-for-approval never exec -C \"$PROJECT_ROOT\" --skip-git-repo-check --sandbox workspace-write --add-dir ... -c sandbox_workspace_write.network_access=true \"$PROMPT\""
  fi
  exit 0
fi

if [[ "$ENGINE" == "gemini" ]]; then
  GEMINI_BIN="$(find_gemini)"
  if [[ -z "$GEMINI_BIN" ]]; then
    echo "ERROR: gemini CLI not found in PATH" >> "$LOG_FILE"
    exit 1
  fi
  if [[ "$MODE" == "chat-only" ]]; then
    exec "$GEMINI_BIN" --skip-trust --approval-mode=yolo --sandbox -p "$PROMPT"
  fi
  "$GEMINI_BIN" --skip-trust --approval-mode=yolo --sandbox -p "$PROMPT" >> "$LOG_FILE" 2>&1
  exit $?
fi

CODEX_BIN="$(find_codex)"
if [[ -z "$CODEX_BIN" ]]; then
  echo "ERROR: codex CLI not found in PATH" >> "$LOG_FILE"
  exit 1
fi

if [[ "$MODE" == "chat-only" ]]; then
  exec "$CODEX_BIN" --ask-for-approval never exec \
    -C "$PROJECT_ROOT" \
    --skip-git-repo-check \
    --sandbox workspace-write \
    --add-dir "/Users/tindolhouse/.config/tindol-family-google" \
    --add-dir "/Users/tindolhouse/.config/tindol-family-slack" \
    -c sandbox_workspace_write.network_access=true \
    "$PROMPT"
fi

"$CODEX_BIN" --ask-for-approval never exec \
  -C "$PROJECT_ROOT" \
  --skip-git-repo-check \
  --sandbox workspace-write \
  --add-dir "/Users/tindolhouse/.config/tindol-family-google" \
  --add-dir "/Users/tindolhouse/.config/tindol-family-slack" \
  -c sandbox_workspace_write.network_access=true \
  "$PROMPT" >> "$LOG_FILE" 2>&1
