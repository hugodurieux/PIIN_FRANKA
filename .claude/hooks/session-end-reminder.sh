#!/bin/bash
# Hook: fires at session end (SessionEnd event)
# Reminds the user to update SESSION.md if session-scribe wasn't run.

SESSION_FILE="$(pwd)/SESSION.md"
[ ! -f "$SESSION_FILE" ] && exit 0

LAST_MODIFIED=$(stat -f "%m" "$SESSION_FILE" 2>/dev/null || stat -c "%Y" "$SESSION_FILE" 2>/dev/null)
NOW=$(date +%s)
AGE=$(( NOW - LAST_MODIFIED ))

if [ "$AGE" -gt 1800 ]; then
  echo ""
  echo "WARNING: SESSION.md was not updated this session."
  echo "         Run: 'Update SESSION.md' before closing."
  echo ""
fi
