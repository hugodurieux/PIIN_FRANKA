#!/bin/bash
# PreToolUse hook (matcher: Bash)
# Intercepts any attempt to EXECUTE Python code and blocks it,
# forcing explicit human authorization.
#
# BLOCKED (execution):   python x.py, python3 -m training.train, pytest...
# ALLOWED (editing):     creating/modifying .py files, reading them, py_compile (syntax)
#
# Exit 2 = block the call and return the message to Claude.
# Exit 0 = let it pass (fall back to the normal permission flow).

input=$(cat)
cmd=$(echo "$input" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"command"[[:space:]]*:[[:space:]]*"//;s/"$//')

# Python EXECUTION patterns (not editing, not syntax check).
# py_compile (syntax check only, does NOT execute code) is explicitly allowed.
if echo "$cmd" | grep -Eq '(^|[;&| ])(python3?|pytest|ipython)([[:space:]]|$)'; then
  if echo "$cmd" | grep -q 'py_compile'; then
    exit 0   # syntax check only -> allowed
  fi
  echo "BLOCKED: running Python code is not allowed without your explicit authorization." >&2
  echo "Attempted command: $cmd" >&2
  echo "Claude can write/modify code, but YOU run it." >&2
  exit 2   # really blocks, even in bypass mode
fi

exit 0
