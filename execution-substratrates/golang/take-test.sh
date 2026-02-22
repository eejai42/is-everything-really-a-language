#!/bin/bash
set -e  # Exit immediately on ANY error - FAIL LOUDLY!
set -o pipefail  # Catch errors in pipes

# take-test.sh for golang execution substrate
# Runs the Go SDK to compute test answers
#
# Reads from shared testing/blank-tests/ and writes to local test-answers/
#
# IMPORTANT: This script WILL fail loudly if:
#   - Go compilation fails (type mismatches, syntax errors)
#   - Input files are missing
#   - Output cannot be written

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "golang: Starting test..."

# Verify required source files exist
if [[ ! -f "erb_sdk.go" ]]; then
    echo "FATAL: erb_sdk.go not found! Run inject-into-golang.py first." >&2
    exit 1
fi

if [[ ! -f "main.go" ]]; then
    echo "FATAL: main.go not found! Run inject-into-golang.py first." >&2
    exit 1
fi

# Ensure test-answers directory exists
mkdir -p "$SCRIPT_DIR/test-answers"

# Run Go test runner - compilation errors will cause immediate exit due to set -e
echo "golang: Compiling and running..."
go run erb_sdk.go main.go

echo "golang: test completed successfully"
