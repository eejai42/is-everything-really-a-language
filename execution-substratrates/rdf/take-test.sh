#!/bin/bash

# take-test.sh for RDF execution substrate
# Executes SPARQL-based computation to produce test answers
#
# Reads from shared testing/blank-tests/ and writes to local test-answers/

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Ensure test-answers directory exists
mkdir -p "$SCRIPT_DIR/test-answers"

# Run RDF substrate (reads from shared testing/blank-tests/)
python3 "$SCRIPT_DIR/take-test.py"

echo "rdf: test completed"
