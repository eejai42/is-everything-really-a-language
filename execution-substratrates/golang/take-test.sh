#!/bin/bash

# take-test.sh for golang execution substrate
# Runs the Go SDK to compute test answers
#
# Supports two modes:
# 1. Multi-entity: Processes all files in blank-tests/ -> test-answers/
# 2. Legacy: Uses single blank-test.json -> test-answers.json

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check for new multi-entity structure
if [ -d "$SCRIPT_DIR/blank-tests" ] && [ -n "$(ls -A "$SCRIPT_DIR/blank-tests" 2>/dev/null)" ]; then
    # Multi-entity mode
    echo "golang: Using multi-entity mode (blank-tests/ -> test-answers/)"

    # Ensure test-answers directory exists
    mkdir -p "$SCRIPT_DIR/test-answers"

    # Run Go test runner in multi-entity mode
    go run erb_sdk.go main.go --multi-entity
else
    # Legacy mode: Use single blank-test.json
    echo "golang: Using legacy mode (blank-test.json -> test-answers.json)"

    # Delete previous test-answers.json to prevent stale results
    rm -f "$SCRIPT_DIR/test-answers.json"

    # Run the Go test runner
    go run erb_sdk.go main.go take-test
fi

echo "golang: test completed"
