#!/bin/sh
# GuardKit install check — no coding needed to run this.
# Usage: sh install.sh
# It checks Python, optionally installs pyarrow for ShmPipe, and runs the suite demo.
set -e
echo "GuardKit install check"
python3 --version || { echo "Python 3 is required. Install it from python.org, then run this again."; exit 1; }
echo "Python OK. Five of seven tools need no extra install."
echo "Optional: install pyarrow for ShmPipe? (y/N)"
read -r ans
if [ "$ans" = "y" ] || [ "$ans" = "Y" ]; then
  python3 -m pip install pyarrow || echo "pyarrow install failed — ShmPipe will be SKIPPED in the demo, other tools still run."
fi
echo "Running suite demo..."
python3 kit.py demo
echo "Done. Open web/index.html in a browser to try CheckFirst + SafeOffer."
