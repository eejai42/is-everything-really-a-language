#!/usr/bin/env python3
"""
GraphQL Substrate Test Runner

This script computes all calculated fields using the shared erb_calc.py library
(same as Python and YAML substrates).

Supports two modes:
1. Multi-entity (--multi-entity): Processes all files in blank-tests/ -> test-answers/
2. Legacy: Processes single blank-test.json -> test-answers.json

The resolvers.js file contains the same logic for GraphQL runtime,
but for testing we use the shared Python library to ensure consistency.
"""

import argparse
import glob
import json
import os
import sys
from pathlib import Path

# Get script directory
script_dir = Path(__file__).parent.resolve()

# Add Python substrate directory to path for shared library
python_substrate_dir = script_dir / ".." / "python"
sys.path.insert(0, str(python_substrate_dir))

from erb_calc import compute_all_calculated_fields


def process_entity(input_path: str, output_path: str, entity_name: str) -> int:
    """Process a single entity file, computing all calculated fields."""
    with open(input_path, 'r', encoding='utf-8') as f:
        records = json.load(f)

    # Compute all calculated fields for each record
    computed_records = []
    for record in records:
        computed = compute_all_calculated_fields(record, entity_name)
        computed_records.append(computed)

    # Save results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(computed_records, f, indent=2)

    return len(computed_records)


def run_multi_entity():
    """Process all entity files from shared testing/blank-tests/ directory."""
    # Use shared blank-tests directory at project root
    project_root = script_dir.parent.parent
    blank_tests_dir = project_root / "testing" / "blank-tests"
    test_answers_dir = script_dir / "test-answers"

    if not blank_tests_dir.is_dir():
        print(f"Error: {blank_tests_dir} not found")
        sys.exit(1)

    # Ensure output directory exists
    test_answers_dir.mkdir(parents=True, exist_ok=True)

    # Process each entity file (skip metadata files starting with _)
    total_records = 0
    entity_count = 0

    for input_path in sorted(glob.glob(str(blank_tests_dir / "*.json"))):
        filename = os.path.basename(input_path)

        # Skip metadata files
        if filename.startswith('_'):
            continue

        entity = filename.replace('.json', '')
        output_path = test_answers_dir / filename

        count = process_entity(input_path, str(output_path), entity)
        total_records += count
        entity_count += 1

        print(f"  -> {entity}: {count} records")

    print(f"GraphQL substrate: Processed {entity_count} entities, {total_records} total records")


def run_legacy():
    """Process single blank-test.json file (legacy mode)."""
    blank_test_path = script_dir / '..' / '..' / 'testing' / 'blank-test.json'
    answers_path = script_dir / 'test-answers.json'

    # Load blank test data
    with open(blank_test_path, 'r', encoding='utf-8') as f:
        candidates = json.load(f)

    print(f"GraphQL substrate: Processing {len(candidates)} candidates...")

    # Compute answers for each candidate using shared library
    computed = []
    for candidate in candidates:
        computed.append(compute_all_calculated_fields(candidate))

    # Save test answers
    with open(answers_path, 'w', encoding='utf-8') as f:
        json.dump(computed, f, indent=2)

    print(f"GraphQL substrate: Saved results to {answers_path}")


def main():
    run_multi_entity()


if __name__ == "__main__":
    main()
