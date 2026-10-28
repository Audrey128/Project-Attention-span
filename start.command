#!/bin/bash
# Double-click on Mac to launch Attention Tracker.
cd "$(dirname "$0")"
if command -v python3 >/dev/null 2>&1; then
  python3 run.py
else
  echo "Python 3 isn't installed. Get it from https://www.python.org/downloads/"
  read -n 1 -s -r -p "Press any key to close."
fi
