#!/bin/bash

# take-test.sh for graphql execution substrate
# Executes the GraphQL resolver logic to compute calculated fields
#
# Reads from shared testing/blank-tests/ and writes to local test-answers/

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Ensure test-answers directory exists
mkdir -p "$SCRIPT_DIR/test-answers"

# Run GraphQL substrate (reads from shared testing/blank-tests/)
python3 "$SCRIPT_DIR/take-test.py"

echo "graphql: test completed"
