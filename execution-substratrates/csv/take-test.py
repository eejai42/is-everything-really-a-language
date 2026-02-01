#!/usr/bin/env python3
"""
Read test answers from the CSV substrate.

This script reads the language_candidates.csv file and populates test-answers.json
by matching CSV columns to JSON fields.

Unlike the xlsx substrate which reads from rulebook.xlsx, this substrate
reads from the flat CSV export, demonstrating that the CSV format contains
all the information needed to populate test answers.
"""

import csv
import json
import re
import sys
from pathlib import Path


def to_snake_case(name):
    """Convert PascalCase or camelCase to snake_case."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def convert_csv_value(value, field_name=None):
    """Convert CSV string value to appropriate Python type."""
    if value is None or value == '':
        return None

    # Handle boolean strings
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False

    # Try numeric conversion
    try:
        if '.' in value:
            return float(value)
        return int(value)
    except (ValueError, TypeError):
        pass

    return value


def load_csv_as_lookup(csv_path, pk_field):
    """Load CSV file and return a lookup dict keyed by primary key.

    Args:
        csv_path: Path to the CSV file
        pk_field: Name of the primary key field (snake_case)

    Returns:
        Dict mapping primary key values to row dicts
    """
    lookup = {}

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Convert all values to appropriate types
            converted_row = {}
            for field_name, value in row.items():
                converted_row[field_name] = convert_csv_value(value, field_name)

            # Get primary key value
            pk_value = converted_row.get(pk_field)
            if pk_value is not None:
                lookup[pk_value] = converted_row

    return lookup


def fill_null_fields_from_csv(csv_path, answers_path):
    """Read test-answers.json and fill null fields from CSV values.

    Args:
        csv_path: Path to the language_candidates.csv file
        answers_path: Path to test-answers.json
    """
    # Load test answers
    with open(answers_path, 'r', encoding='utf-8') as f:
        answers = json.load(f)

    if not answers:
        print("Error: test-answers.json is empty")
        sys.exit(1)

    json_fields = list(answers[0].keys())
    print(f"Found {len(json_fields)} fields in test answers")

    # Find primary key field (first field ending in _id)
    pk_field = next((f for f in json_fields if f.endswith('_id')), json_fields[0])
    print(f"Primary key field: {pk_field}")

    # Load CSV as lookup
    csv_lookup = load_csv_as_lookup(csv_path, pk_field)
    print(f"Loaded {len(csv_lookup)} rows from CSV")

    # Fill null fields
    fields_filled = 0
    records_updated = 0

    for answer in answers:
        pk_value = answer.get(pk_field)
        if pk_value is None or pk_value not in csv_lookup:
            continue

        csv_row = csv_lookup[pk_value]
        record_updated = False

        for field in json_fields:
            if answer.get(field) is None and csv_row.get(field) is not None:
                answer[field] = csv_row[field]
                fields_filled += 1
                record_updated = True

        if record_updated:
            records_updated += 1

    print(f"Filled {fields_filled} null fields across {records_updated} records")

    # Write updated answers
    with open(answers_path, 'w', encoding='utf-8') as f:
        json.dump(answers, f, indent=2)

    print(f"Updated {answers_path}")


def main():
    script_dir = Path(__file__).parent
    csv_path = script_dir / 'language_candidates.csv'
    answers_path = script_dir / 'test-answers.json'

    if not csv_path.exists():
        print(f"Error: {csv_path} not found")
        print("Run inject-into-csv.py first to generate the CSV file")
        sys.exit(1)

    if not answers_path.exists():
        print(f"Error: {answers_path} not found")
        print("Ensure blank-test.json was copied to test-answers.json")
        sys.exit(1)

    fill_null_fields_from_csv(csv_path, answers_path)
    print("csv: test-answers.json updated with values from language_candidates.csv")


if __name__ == "__main__":
    main()
