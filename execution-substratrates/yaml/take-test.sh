#!/bin/bash

# take-test.sh for yaml execution substrate
# Executes the YAML schema deterministically using Python
#
# Supports two modes:
# 1. Multi-entity: Processes all files in blank-tests/ -> test-answers/
# 2. Legacy: Uses single blank-test.json -> test-answers.json

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check for new multi-entity structure
if [ -d "$SCRIPT_DIR/blank-tests" ] && [ -n "$(ls -A "$SCRIPT_DIR/blank-tests" 2>/dev/null)" ]; then
    # Multi-entity mode
    echo "yaml: Using multi-entity mode (blank-tests/ -> test-answers/)"

    # Ensure test-answers directory exists
    mkdir -p "$SCRIPT_DIR/test-answers"

    # Run YAML substrate in multi-entity mode
    python3 "$SCRIPT_DIR/take-test.py" --multi-entity
else
    # Legacy mode
    echo "yaml: Using legacy mode (blank-test.json -> test-answers.json)"

    # Delete previous test-answers.json to prevent stale results
    rm -f "$SCRIPT_DIR/test-answers.json"

    # Copy blank test template
    cp "$SCRIPT_DIR/../../testing/blank-test.json" "$SCRIPT_DIR/test-answers.json"

    # Run YAML substrate
    python3 "$SCRIPT_DIR/take-test.py"
fi

echo "yaml: test completed"
