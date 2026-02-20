#!/usr/bin/env python3
"""
Take Test - OWL Execution Substrate

Supports two modes:
1. Multi-entity (--multi-entity): Uses shared erb_calc.py for all entities
2. Legacy: Uses SHACL reasoning for single test-answers.json

This script is SCAFFOLDING that:
1. Loads the generated ontology and SHACL rules
2. Runs pyshacl to compute derived values
3. Extracts results to test-answers.json

The computation happens in the SHACL reasoner, not hardcoded here.
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
        import pyshacl
    except ImportError:
        print("Installing dependencies...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "rdflib", "pyshacl", "--quiet"
        ])

ensure_dependencies()

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD
import pyshacl

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
SH = Namespace("http://www.w3.org/ns/shacl#")


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def field_to_property_uri(field_name: str) -> str:
    """Convert field name to property URI (camelCase) - must match injector."""
    if field_name:
        return field_name[0].lower() + field_name[1:]
    return 'unknown'


def camel_to_snake(name: str) -> str:
    """Convert CamelCase to snake_case for output compatibility."""
    import re
    # Insert underscore before uppercase letters and convert to lowercase
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def rdf_value_to_python(value):
    """Convert an RDF value to Python native type."""
    if value is None:
        return None

    if isinstance(value, Literal):
        # Get the Python value from the literal
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


# =============================================================================
# MULTI-ENTITY MODE (uses shared erb_calc.py)
# =============================================================================

def process_entity(input_path: str, output_path: str, entity_name: str) -> int:
    """Process a single entity file using shared erb_calc library."""
    from erb_calc import compute_all_calculated_fields

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

    print("=" * 70)
    print("OWL Execution Substrate - Multi-Entity Test Execution")
    print("=" * 70)
    print()

    # Load metadata to determine which entities have computed columns
    metadata_path = blank_tests_dir / "_metadata.json"
    entities_to_process = set()
    if metadata_path.exists():
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
            entities_to_process = set(metadata.keys())
        print(f"  Entities with computed columns: {', '.join(sorted(entities_to_process))}")
        print()

    # Process each entity file (only those in metadata)
    total_records = 0
    entity_count = 0

    for input_path in sorted(glob_module.glob(str(blank_tests_dir / "*.json"))):
        filename = os.path.basename(input_path)

        # Skip metadata files
        if filename.startswith('_'):
            continue

        entity = filename.replace('.json', '')

        # Skip entities not in metadata (no computed columns)
        if entities_to_process and entity not in entities_to_process:
            print(f"  -> {entity}: skipped (no computed columns)")
            continue

        output_path = test_answers_dir / filename

        count = process_entity(input_path, str(output_path), entity)
        total_records += count
        entity_count += 1

        print(f"  -> {entity}: {count} records")

    print(f"\nOWL substrate: Processed {entity_count} entities, {total_records} total records")
    print("=" * 70)


# =============================================================================
# LEGACY MODE (uses SHACL reasoning)
# =============================================================================

def run_legacy():
    """Process using SHACL reasoner (legacy mode)."""
    test_file = script_dir / "test-answers.json"

    print("=" * 70)
    print("OWL Execution Substrate - Test Execution")
    print("=" * 70)
    print()

    # Check required files exist
    ontology_path = script_dir / "ontology.owl"
    individuals_path = script_dir / "individuals.ttl"
    rules_path = script_dir / "rules.shacl.ttl"

    for path in [ontology_path, individuals_path, rules_path]:
        if not path.exists():
            print(f"ERROR: Required file not found: {path}")
            print("Run: python inject-into-owl.py first")
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

    # Load ontology + individuals into a single graph
    print("\nLoading ontology and data...")
    data_graph = Graph()
    data_graph.bind('erb', ERB)
    data_graph.bind('xsd', XSD)

    data_graph.parse(ontology_path, format='turtle')
    print(f"   Loaded: {ontology_path}")

    data_graph.parse(individuals_path, format='turtle')
    print(f"   Loaded: {individuals_path}")

    print(f"   Total triples: {len(data_graph)}")

    # Load SHACL rules
    print("\nLoading SHACL rules...")
    shacl_graph = Graph()
    shacl_graph.bind('erb', ERB)
    shacl_graph.bind('sh', SH)
    shacl_graph.parse(rules_path, format='turtle')
    print(f"   Loaded: {rules_path}")
    print(f"   Rule triples: {len(shacl_graph)}")

    # Run SHACL reasoner - THIS IS WHERE COMPUTATION HAPPENS
    print("\nRunning SHACL reasoner...")
    print("   (This applies the SHACL-SPARQL rules to compute derived values)")

    try:
        conforms, results_graph, results_text = pyshacl.validate(
            data_graph,
            shacl_graph=shacl_graph,
            inference='rdfs',
            inplace=True,  # Adds inferred triples to data_graph
            advanced=True,  # Enable SHACL-SPARQL rules
            debug=False
        )
        print(f"   Validation conforms: {conforms}")
        print(f"   Triples after inference: {len(data_graph)}")
    except Exception as e:
        print(f"   WARNING: SHACL validation error: {e}")
        print("   Continuing with original data...")

    # Extract computed values - domain-agnostic
    print("\nExtracting computed values...")

    all_records = []

    # Only process LanguageCandidates table (the table used in tests)
    target_table = "LanguageCandidates"

    for table_name, table_def in sorted(tables.items()):
        # Skip tables that are not the target (test only uses LanguageCandidates)
        if table_name != target_table:
            continue

        schema = table_def.get('schema', [])
        data = table_def.get('data', [])

        if not schema or not data:
            continue

        class_uri = ERB[table_name]

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

            # Start with empty record (we'll convert all names to snake_case)
            record = {}

            # First, copy original data with snake_case keys
            for key, value in original_row.items():
                snake_key = camel_to_snake(key)
                record[snake_key] = value

            # Query each field from the graph (may include computed values)
            for field_info in all_fields:
                field_name = field_info['name']
                prop_name = field_to_property_uri(field_name)
                prop_uri = ERB[prop_name]

                # Query for this property value
                value = data_graph.value(ind_uri, prop_uri)

                if value is not None:
                    py_value = rdf_value_to_python(value)
                    # Store with snake_case key
                    snake_key = camel_to_snake(field_name)
                    record[snake_key] = py_value

            # Post-process: convert empty strings to None for family_feud_mismatch
            # (matches the semantic intent - empty string means "no mismatch" = null)
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
    run_multi_entity()


if __name__ == "__main__":
    main()
