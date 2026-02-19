#!/bin/bash

# take-test.sh for xlsx execution substrate
# This script reads the xlsx file and produces test answers
#
# Supports two modes:
# 1. Multi-entity: Reads xlsx worksheets, writes to test-answers/{entity}.json
# 2. Legacy: Uses single test-answers.json

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check for new multi-entity structure
if [ -d "$SCRIPT_DIR/blank-tests" ] && [ -n "$(ls -A "$SCRIPT_DIR/blank-tests" 2>/dev/null)" ]; then
    # Multi-entity mode
    echo "xlsx: Using multi-entity mode (blank-tests/ -> test-answers/)"

    # Ensure test-answers directory exists
    mkdir -p "$SCRIPT_DIR/test-answers"

    # Run Python script in multi-entity mode
    python3 take-test.py --multi-entity
else
    # Legacy mode: Use single test-answers.json
    echo "xlsx: Using legacy mode (blank-test.json -> test-answers.json)"

    # Delete previous test-answers.json to prevent stale results
    rm -f "$SCRIPT_DIR/test-answers.json"

    # Copy blank test template
    cp "$SCRIPT_DIR/../../testing/blank-test.json" "$SCRIPT_DIR/test-answers.json"

    # Run the Python script
    python3 take-test.py
fi

echo "xlsx: test completed"
