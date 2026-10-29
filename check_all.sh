#!/bin/sh
# GuardKit one-command check: demo + suite tests + selfcheck.
# Usage: sh check_all.sh
# Requires: python3. For pytest, use a venv with pytest installed.
set -e
echo "1. Suite demo..."
python3 kit.py demo
echo ""
echo "2. Suite smoke tests..."
python3 kit.py test
echo ""
echo "3. Selfcheck (secrets)..."
python3 kit.py selfcheck
echo ""
echo "4. Per-tool pytest (if pytest is available)..."
for d in semver-diff tracelock wattshift safeoffer checkfirst secretscan shmpipe; do
  if [ -d "$d/tests" ]; then
    echo "--- $d ---"
    (cd "$d" && python3 -m pytest tests/ -q 2>&1 | tail -2) || echo "(pytest not available or failed for $d — see above)"
  fi
done
echo ""
echo "ALL CHECKS DONE — see above for any failures."
