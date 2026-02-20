#!/bin/bash

# take-test.sh for python execution substrate
# Executes the Python substrate to compute calculated fields
#
# Reads from shared testing/blank-tests/ and writes to local test-answers/

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Ensure test-answers directory exists
mkdir -p "$SCRIPT_DIR/test-answers"

# Run Python substrate (reads from shared testing/blank-tests/)
python3 "$SCRIPT_DIR/take-test.py"

echo "python: test completed"
