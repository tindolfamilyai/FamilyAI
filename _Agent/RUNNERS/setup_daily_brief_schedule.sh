#!/bin/bash
set -euo pipefail

PROJECT_ROOT="/Users/tindolhouse/Documents/Claude/Projects/Tindol Family Codex Claude"
RUNNER_DIR="$PROJECT_ROOT/_Agent/RUNNERS"
LOG_DIR="$PROJECT_ROOT/_Reports/Daily_Briefs/logs"
AGENT_LABEL="com.tindolfamily.dailybrief"
PLIST_SOURCE="$RUNNER_DIR/$AGENT_LABEL.plist"
PLIST_TARGET="/Users/tindolhouse/Library/LaunchAgents/$AGENT_LABEL.plist"
KICKSTART=0

if [[ "${1:-}" == "--kickstart" ]]; then
  KICKSTART=1
elif [[ "${1:-}" != "" ]]; then
  echo "Usage: $0 [--kickstart]" >&2
  exit 2
fi

mkdir -p "$LOG_DIR"
mkdir -p "/Users/tindolhouse/Library/LaunchAgents"

cp "$PLIST_SOURCE" "$PLIST_TARGET"
chmod 644 "$PLIST_TARGET"

launchctl unload "$PLIST_TARGET" 2>/dev/null || true
launchctl load "$PLIST_TARGET"

if [[ "$KICKSTART" == "1" ]]; then
  launchctl kickstart -k "gui/$(id -u)/$AGENT_LABEL"
  echo "Installed and triggered $AGENT_LABEL"
else
  echo "Installed $AGENT_LABEL"
  echo "Not triggered. Run with --kickstart to start the scheduled brief immediately."
fi
echo "Plist: $PLIST_TARGET"
echo "Logs: $LOG_DIR"
