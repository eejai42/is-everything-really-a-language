#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Run the SDK demo
echo "=== Go ERB SDK ==="
go run erb_sdk.go main.go

# Run the test for this substrate
"$SCRIPT_DIR/take-test.sh"
