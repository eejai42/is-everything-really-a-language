#!/bin/bash

# take-test.sh for explain-dag execution substrate
# Evaluates formulas and produces derivation explanations
#
# Reads from shared testing/blank-tests/ and writes to:
#   - test-answers/ (for grading)
#   - test-explanations/ (derivation DAGs)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Ensure output directories exist
mkdir -p "$SCRIPT_DIR/test-answers"
mkdir -p "$SCRIPT_DIR/test-explanations"

# Run ExplainDAG substrate
python3 "$SCRIPT_DIR/take-test.py"

echo "explain-dag: test completed"
