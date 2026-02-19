#!/bin/bash

# take-test.sh for binary execution substrate
# Executes the ARM64 assembly substrate to compute calculated fields
#
# Supports two modes:
# 1. Multi-entity: Processes all files in blank-tests/ -> test-answers/
# 2. Legacy: Uses single blank-test.json -> test-answers.json

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check for new multi-entity structure
if [ -d "$SCRIPT_DIR/blank-tests" ] && [ -n "$(ls -A "$SCRIPT_DIR/blank-tests" 2>/dev/null)" ]; then
    # Multi-entity mode: blank-tests/ exists and has files
    echo "binary: Using multi-entity mode (blank-tests/ -> test-answers/)"

    # Ensure test-answers directory exists
    mkdir -p "$SCRIPT_DIR/test-answers"

    # Run binary substrate in multi-entity mode
    python3 "$SCRIPT_DIR/take-test.py" --multi-entity
else
    # Legacy mode: Use single blank-test.json
    echo "binary: Using legacy mode (blank-test.json -> test-answers.json)"

    # Delete previous test-answers.json to prevent stale results
    rm -f "$SCRIPT_DIR/test-answers.json"

    # Copy blank test template to this folder as test-answers.json
    cp "$SCRIPT_DIR/../../testing/blank-test.json" "$SCRIPT_DIR/test-answers.json"

    # Run binary substrate
    python3 "$SCRIPT_DIR/take-test.py"
fi

echo "binary: test completed"
