#!/bin/bash

# take-test.sh for xlsx execution substrate
# This script reads the xlsx file and produces test-answers.json

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR"

# Run the Python script to read from rulebook.xlsx and produce test-answers.json
python3 take-test.py
