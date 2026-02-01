#!/bin/bash

# take-test.sh for graphql execution substrate
# This script will eventually run the graphql substrate to produce test answers

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Step 1: Copy blank test template to this folder as test-answers.json
cp "$SCRIPT_DIR/../../testing/blank-test.json" "$SCRIPT_DIR/test-answers.json"

# TODO: Step 2: Run the graphql substrate solution to populate answers
# (Future implementation will go here)

echo "graphql: test-answers.json created from blank template"
