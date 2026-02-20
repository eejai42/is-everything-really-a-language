#!/bin/bash

# take-test.sh for golang execution substrate
# Runs the Go SDK to compute test answers
#
# Reads from shared testing/blank-tests/ and writes to local test-answers/

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Ensure test-answers directory exists
mkdir -p "$SCRIPT_DIR/test-answers"

# Run Go test runner (reads from shared testing/blank-tests/)
go run erb_sdk.go main.go

echo "golang: test completed"
