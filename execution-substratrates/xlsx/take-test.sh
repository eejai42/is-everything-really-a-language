#!/bin/bash

# take-test.sh for xlsx execution substrate
# This script reads the xlsx file and produces test answers
#
# Reads from shared testing/blank-tests/ and writes to local test-answers/

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Ensure test-answers directory exists
mkdir -p "$SCRIPT_DIR/test-answers"

# Run Python script (reads from shared testing/blank-tests/)
python3 take-test.py

echo "xlsx: test completed"
