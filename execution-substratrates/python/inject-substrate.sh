#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Run the SDK demo
echo "=== Python ERB SDK ==="
python3 erb_sdk.py

# Run the test for this substrate
"$SCRIPT_DIR/take-test.sh"
