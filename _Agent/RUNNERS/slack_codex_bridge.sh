#!/bin/bash
set -euo pipefail

PROJECT_ROOT="/Users/tindolhouse/Documents/Claude/Projects/Tindol Family Codex Claude"
LOG_DIR="$PROJECT_ROOT/_Reports/Slack_Codex/logs"
LOG_FILE="$LOG_DIR/bridge_stdout.log"

mkdir -p "$LOG_DIR"
cd "$PROJECT_ROOT"

export TZ="America/New_York"
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

exec python3 "$PROJECT_ROOT/_Agent/SKILLS/slack/scripts/slack_codex_bridge.py" "$@" >> "$LOG_FILE" 2>&1
