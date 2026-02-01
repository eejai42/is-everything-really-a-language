#!/bin/bash

# take-test.sh for docx execution substrate
# This script will eventually run the docx substrate to produce test answers

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Step 1: Copy blank test template to this folder as test-answers.json
cp "$SCRIPT_DIR/../../testing/blank-test.json" "$SCRIPT_DIR/test-answers.json"

# TODO: Step 2: Run the docx substrate solution to populate answers
# (Future implementation will go here)

echo "docx: test-answers.json created from blank template"
