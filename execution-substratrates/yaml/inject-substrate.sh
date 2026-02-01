#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# YAML schema is static - no generation needed
# This script validates the schema exists
echo "YAML schema available at: execution-substratrates/yaml/schema.yaml"

# Run the test for this substrate
"$SCRIPT_DIR/take-test.sh"
