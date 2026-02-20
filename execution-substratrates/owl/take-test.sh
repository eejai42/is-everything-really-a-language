#!/bin/bash

# take-test.sh for owl execution substrate
# Executes the SHACL reasoner to compute derived values
#
# Reads from shared testing/blank-tests/ and writes to local test-answers/

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Ensure test-answers directory exists
mkdir -p "$SCRIPT_DIR/test-answers"

# Run OWL substrate (reads from shared testing/blank-tests/)
python3 "$SCRIPT_DIR/take-test.py"

echo "owl: test completed"
