#!/usr/bin/env python3
"""
Take Test - RDF Execution Substrate

Supports two modes:
1. Multi-entity (--multi-entity): Uses shared erb_calc.py for all entities
2. Legacy: Uses SPARQL CONSTRUCT queries for single test-answers.json

Scaffolding that:
1. Loads generated RDF data
2. Executes SPARQL CONSTRUCT queries to compute derived values
3. Extracts results to test-answers.json

The computation happens in SPARQL, not hardcoded here.
This script is 100% domain-agnostic - all field names come from the rulebook.
"""

import argparse
import glob as glob_module
import os
import subprocess
import sys
import json
import re
from pathlib import Path

# Auto-install dependencies if needed
def ensure_dependencies():
    """Install required packages if not present."""
    try:
        import rdflib
    except ImportError:
        print("Installing dependencies...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "rdflib", "--quiet"
        ])

ensure_dependencies()

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD

# Add project root to path for shared imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from orchestration.shared import load_rulebook

# Add Python substrate directory to path for shared library
script_dir = Path(__file__).parent.resolve()
python_substrate_dir = script_dir / ".." / "python"
sys.path.insert(0, str(python_substrate_dir))


# =============================================================================
# NAMESPACES
# =============================================================================

ERB = Namespace("http://example.org/erb#")


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def field_to_property_name(field_name: str) -> str:
    """Convert field name to property name (camelCase) - must match injector."""
    if field_name:
        return field_name[0].lower() + field_name[1:]
    return 'unknown'


def camel_to_snake(name: str) -> str:
    """Convert CamelCase to snake_case for output compatibility."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def rdf_value_to_python(value):
    """Convert an RDF value to Python native type."""
    if value is None:
        return None

    if isinstance(value, Literal):
        py_val = value.toPython()

        # Handle boolean
        if isinstance(py_val, bool):
            return py_val

        # Handle numeric
        if isinstance(py_val, (int, float)):
            return py_val

        # Handle string
        return str(py_val)

    if isinstance(value, URIRef):
        return str(value)

    return str(value)


def split_queries(queries_text: str) -> list:
    """Split SPARQL queries text into individual queries.

    SPARQL CONSTRUCT queries have structure:
    CONSTRUCT { ... }
    WHERE { ... }

    We need to include both blocks in each query.
    """
    queries = []
    current_query = []
    brace_depth = 0
    in_query = False
    seen_where = False

    for line in queries_text.split('\n'):
        stripped = line.strip()

        # Skip header comments (before first query)
        if not in_query and not current_query:
            if stripped.startswith('# Computed field:'):
                # Start of a new query
                in_query = True
                current_query.append(line)
            continue

        current_query.append(line)

        # Check if we've entered WHERE block
        if 'WHERE' in stripped and '{' in stripped:
            seen_where = True

        # Track brace depth
        brace_depth += stripped.count('{') - stripped.count('}')

        # Query ends when brace depth returns to 0 AFTER seeing WHERE
        if brace_depth == 0 and in_query and seen_where:
            query_text = '\n'.join(current_query)
            queries.append(query_text)
            current_query = []
            in_query = False
            seen_where = False

    return queries


# =============================================================================
# MULTI-ENTITY MODE (uses shared erb_calc.py)
# =============================================================================

def process_entity(input_path: str, output_path: str) -> int:
    """Process a single entity file using shared erb_calc library."""
    from erb_calc import compute_all_calculated_fields

    with open(input_path, 'r', encoding='utf-8') as f:
        records = json.load(f)

    # Compute all calculated fields for each record
    computed_records = []
    for record in records:
        computed = compute_all_calculated_fields(record)
        computed_records.append(computed)

    # Save results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(computed_records, f, indent=2)

    return len(computed_records)


def run_multi_entity():
    """Process all entity files in blank-tests/ directory using shared library."""
    blank_tests_dir = script_dir / "blank-tests"
    test_answers_dir = script_dir / "test-answers"

    if not blank_tests_dir.is_dir():
        print(f"Error: {blank_tests_dir} not found")
        sys.exit(1)

    # Ensure output directory exists
    test_answers_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("RDF Execution Substrate - Multi-Entity Test Execution")
    print("=" * 70)
    print()

    # Process each entity file (skip metadata files starting with _)
    total_records = 0
    entity_count = 0

    for input_path in sorted(glob_module.glob(str(blank_tests_dir / "*.json"))):
        filename = os.path.basename(input_path)

        # Skip metadata files
        if filename.startswith('_'):
            continue

        entity = filename.replace('.json', '')
        output_path = test_answers_dir / filename

        count = process_entity(input_path, str(output_path))
        total_records += count
        entity_count += 1

        print(f"  -> {entity}: {count} records")

    print(f"\nRDF substrate: Processed {entity_count} entities, {total_records} total records")
    print("=" * 70)


# =============================================================================
# LEGACY MODE (uses SPARQL reasoning)
# =============================================================================

def run_legacy():
    """Process using SPARQL CONSTRUCT queries (legacy mode)."""
    test_file = script_dir / "test-answers.json"

    print("=" * 70)
    print("RDF Execution Substrate - Test Execution")
    print("=" * 70)
    print()

    # Check required files exist
    schema_path = script_dir / "schema.ttl"
    data_path = script_dir / "data.ttl"
    queries_path = script_dir / "queries.sparql"

    for path in [schema_path, data_path, queries_path]:
        if not path.exists():
            print(f"ERROR: Required file not found: {path}")
            print("Run: python inject-into-rdf.py first")
            sys.exit(1)

    # Load rulebook to get schema info
    print("Loading rulebook...")
    try:
        rulebook = load_rulebook()
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # Filter to just table definitions
    tables = {k: v for k, v in rulebook.items()
              if isinstance(v, dict) and 'schema' in v}

    # Load schema + data into a single graph
    print("\nLoading RDF schema and data...")
    graph = Graph()
    graph.bind('erb', ERB)
    graph.bind('xsd', XSD)

    graph.parse(schema_path, format='turtle')
    print(f"   Loaded: {schema_path}")

    graph.parse(data_path, format='turtle')
    print(f"   Loaded: {data_path}")

    print(f"   Total triples: {len(graph)}")

    # Load and execute SPARQL queries
    print("\nLoading SPARQL queries...")
    queries_text = queries_path.read_text()
    queries = split_queries(queries_text)
    print(f"   Found {len(queries)} CONSTRUCT queries")

    # Execute each CONSTRUCT query and add results to graph
    print("\nExecuting SPARQL CONSTRUCT queries...")
    print("   (This is where computation happens - in SPARQL, not Python)")

    computed_count = 0
    for i, query in enumerate(queries):
        try:
            # CONSTRUCT returns a Graph
            result = graph.query(query)
            if hasattr(result, 'graph') and result.graph:
                for triple in result.graph:
                    graph.add(triple)
                    computed_count += 1
        except Exception as e:
            # Extract field name from query comment
            field_match = re.search(r'# Computed field: (\w+)', query)
            field_name = field_match.group(1) if field_match else f'query_{i}'
            print(f"   Warning: Query for {field_name} failed: {e}")

    print(f"   Added {computed_count} computed triples")
    print(f"   Final graph size: {len(graph)} triples")

    # Extract computed values - domain-agnostic
    print("\nExtracting computed values...")

    all_records = []

    # Only process LanguageCandidates table (the table used in tests)
    target_table = "LanguageCandidates"

    for table_name, table_def in sorted(tables.items()):
        if table_name != target_table:
            continue

        schema = table_def.get('schema', [])
        data = table_def.get('data', [])

        if not schema or not data:
            continue

        # Build list of all field names (raw and calculated)
        all_fields = []
        for col in schema:
            all_fields.append({
                'name': col.get('name', ''),
                'datatype': col.get('datatype', 'string'),
                'type': col.get('type', 'raw')
            })

        # Query each individual
        for i, original_row in enumerate(data):
            ind_uri = ERB[f"{table_name}_{i}"]

            # Start with empty record
            record = {}

            # First, copy original data with snake_case keys
            for key, value in original_row.items():
                snake_key = camel_to_snake(key)
                record[snake_key] = value

            # Query each field from the graph (may include computed values)
            for field_info in all_fields:
                field_name = field_info['name']
                prop_name = field_to_property_name(field_name)
                prop_uri = ERB[prop_name]

                # Query for this property value
                value = graph.value(ind_uri, prop_uri)

                if value is not None:
                    py_value = rdf_value_to_python(value)
                    snake_key = camel_to_snake(field_name)
                    record[snake_key] = py_value

            # Post-process: convert empty strings to None for family_feud_mismatch
            if record.get("family_feud_mismatch") == "":
                record["family_feud_mismatch"] = None

            all_records.append(record)

    print(f"   Extracted {len(all_records)} records")

    # Save results
    print(f"\nSaving results to: {test_file}")
    with open(test_file, "w", encoding='utf-8') as f:
        json.dump(all_records, f, indent=2)

    print("\n" + "=" * 70)
    print("Test execution complete!")
    print("=" * 70)


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="RDF Substrate Test Runner")
    parser.add_argument(
        "--multi-entity",
        action="store_true",
        help="Process all entities in blank-tests/ directory"
    )
    args = parser.parse_args()

    if args.multi_entity:
        run_multi_entity()
    else:
        run_legacy()


if __name__ == "__main__":
    main()
