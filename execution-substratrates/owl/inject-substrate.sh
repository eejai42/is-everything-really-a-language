#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Inject data into the owl substrate
python3 "$SCRIPT_DIR/inject-into-owl.py"

# Run the test for this substrate
"$SCRIPT_DIR/take-test.sh"
