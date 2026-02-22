#!/usr/bin/env python3
"""
Generate Python calculation library from the Effortless Rulebook.

This script reads formulas from the rulebook and generates erb_calc.py
with proper calculation functions for ALL entities with calculated fields.

Generated file is shared by Python, English, YAML, and other substrates.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Set

# Add project root to path for shared imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from orchestration.shared import (
    load_rulebook, get_candidate_name_from_cwd, handle_clean_arg,
    discover_entities, get_entity_schema, to_snake_case,
    get_calculated_fields, get_raw_fields
)
from orchestration.formula_parser import (
    parse_formula, compile_to_python, get_field_dependencies,
    ASTNode, FieldRef, FuncCall, Concat, LiteralString
)


def build_dag_levels(calculated_fields: List[Dict], raw_field_names: Set[str]) -> List[List[Dict]]:
    """
    Build DAG levels for calculated fields based on dependencies.

    Level 0: Raw fields (not returned, just used as base)
    Level 1+: Calculated fields ordered by dependency
    """
    # Parse formulas and get dependencies
    field_deps = {}
    for field in calculated_fields:
        formula = field.get('formula', '')
        try:
            ast = parse_formula(formula)
            deps = get_field_dependencies(ast)
            field_deps[field['name']] = set(to_snake_case(d) for d in deps)
        except Exception as e:
            print(f"Warning: Failed to parse formula for {field['name']}: {e}")
            field_deps[field['name']] = set()

    # Build levels
    levels = []
    assigned = set(to_snake_case(name) for name in raw_field_names)
    remaining = {f['name']: f for f in calculated_fields}

    while remaining:
        # Find fields whose dependencies are all assigned
        current_level = []
        for name, field in list(remaining.items()):
            deps = field_deps.get(name, set())
            if deps <= assigned:
                current_level.append(field)

        if not current_level:
            # Circular dependency or missing field - add remaining to final level
            print(f"Warning: Could not resolve dependencies for: {list(remaining.keys())}")
            levels.append(list(remaining.values()))
            break

        # Add to level and mark as assigned
        levels.append(current_level)
        for field in current_level:
            assigned.add(to_snake_case(field['name']))
            del remaining[field['name']]

    return levels


def generate_function_signature(entity_name: str, field_name: str, deps: List[str]) -> str:
    """Generate function signature with entity-namespaced function name."""
    entity_snake = to_snake_case(entity_name)
    field_snake = to_snake_case(field_name)
    func_name = f"calc_{entity_snake}_{field_snake}"
    params = [to_snake_case(d) for d in deps]
    params_str = ", ".join(params) if params else ""
    return f"def {func_name}({params_str}):"


def generate_calc_function(entity_name: str, field: Dict) -> str:
    """Generate a calculation function for a field, namespaced by entity."""
    name = field['name']
    formula = field.get('formula', '')
    entity_snake = to_snake_case(entity_name)
    field_snake = to_snake_case(name)

    try:
        ast = parse_formula(formula)
        deps = get_field_dependencies(ast)
        python_expr = compile_to_python(ast)
    except Exception as e:
        return f'''
def calc_{entity_snake}_{field_snake}():
    """ERROR: Could not parse formula: {formula}
    Error: {e}
    """
    raise NotImplementedError("Formula parsing failed")
'''

    # Generate function
    lines = []
    sig = generate_function_signature(entity_name, name, deps)
    lines.append(sig)

    # Docstring with formula (escape triple quotes and trailing double quotes)
    formula_escaped = formula.replace('\\', '\\\\').replace('"""', "'''")
    # If formula ends with a quote, add space to prevent """"
    if formula_escaped.endswith('"'):
        formula_escaped = formula_escaped + ' '
    lines.append(f'    """Formula: {formula_escaped}"""')

    # Return expression
    lines.append(f'    return {python_expr}')

    return '\n'.join(lines)


def generate_entity_compute_function(
    entity_name: str,
    calculated_fields: List[Dict],
    dag_levels: List[List[Dict]],
    string_fields: List[str]
) -> str:
    """Generate compute function for a specific entity."""
    entity_snake = to_snake_case(entity_name)

    lines = []
    lines.append(f'def compute_{entity_snake}_fields(record: dict) -> dict:')
    lines.append(f'    """Compute all calculated fields for {entity_name}."""')
    lines.append('    result = dict(record)')
    lines.append('')

    # Process each level
    for level_idx, level_fields in enumerate(dag_levels):
        lines.append(f'    # Level {level_idx + 1} calculations')
        for field in level_fields:
            name = field['name']
            snake_name = to_snake_case(name)

            try:
                ast = parse_formula(field.get('formula', ''))
                deps = get_field_dependencies(ast)
            except:
                deps = []

            # Generate function call
            func_name = f"calc_{entity_snake}_{snake_name}"
            if deps:
                args = [f"result.get('{to_snake_case(dep)}')" for dep in deps]
                args_str = ', '.join(args)
                lines.append(f"    result['{snake_name}'] = {func_name}({args_str})")
            else:
                lines.append(f"    result['{snake_name}'] = {func_name}()")
        lines.append('')

    # Post-process: convert empty strings to None for string fields
    if string_fields:
        lines.append('    # Convert empty strings to None for string fields')
        fields_list = ', '.join(f"'{f}'" for f in string_fields)
        lines.append(f"    for key in [{fields_list}]:")
        lines.append("        if result.get(key) == '':")
        lines.append('            result[key] = None')
        lines.append('')

    lines.append('    return result')

    return '\n'.join(lines)


def generate_dispatcher_function(entities_with_calcs: List[str]) -> str:
    """Generate a dispatcher that routes to the correct entity's compute function."""
    lines = []
    lines.append('def compute_all_calculated_fields(record: dict, entity_name: str = None) -> dict:')
    lines.append('    """')
    lines.append('    Compute all calculated fields for a record.')
    lines.append('    ')
    lines.append('    Args:')
    lines.append('        record: The record dict with raw field values')
    lines.append('        entity_name: Entity name (snake_case or PascalCase)')
    lines.append('    ')
    lines.append('    Returns:')
    lines.append('        Record dict with calculated fields filled in')
    lines.append('    """')
    lines.append('    if entity_name is None:')
    lines.append('        # Try to infer from record keys')
    lines.append('        return dict(record)')
    lines.append('')
    lines.append('    # Normalize to snake_case')
    lines.append("    entity_lower = entity_name.lower().replace('-', '_')")
    lines.append('')

    # Generate dispatch logic
    for i, entity in enumerate(entities_with_calcs):
        entity_snake = to_snake_case(entity)
        prefix = 'if' if i == 0 else 'elif'
        lines.append(f"    {prefix} entity_lower == '{entity_snake}':")
        lines.append(f"        return compute_{entity_snake}_fields(record)")

    lines.append('    else:')
    lines.append('        # Unknown entity, return as-is')
    lines.append('        return dict(record)')

    return '\n'.join(lines)


def generate_erb_calc(rulebook: Dict) -> str:
    """Generate the complete erb_calc.py content for ALL entities."""
    lines = []

    # Header
    lines.append('"""')
    lines.append('ERB Calculation Library (GENERATED - DO NOT EDIT)')
    lines.append('=================================================')
    lines.append('Generated from: effortless-rulebook/effortless-rulebook.json')
    lines.append('')
    lines.append('This file contains pure functions that compute calculated fields')
    lines.append('from raw field values. Supports multiple entities.')
    lines.append('"""')
    lines.append('')
    lines.append('from typing import Optional, Any')
    lines.append('')

    # Discover all entities
    entities = discover_entities(rulebook)
    entities_with_calcs = []

    # Process each entity
    for entity_name in entities:
        schema = get_entity_schema(rulebook, entity_name)
        calculated_fields = get_calculated_fields(schema)

        if not calculated_fields:
            continue  # Skip entities with no calculated fields

        entities_with_calcs.append(entity_name)
        raw_fields = get_raw_fields(schema)
        raw_field_names = {f['name'] for f in raw_fields}

        # Find string calculated fields (for empty string -> None conversion)
        string_fields = [
            to_snake_case(f['name'])
            for f in calculated_fields
            if f.get('datatype') == 'string'
        ]

        # Build DAG levels
        dag_levels = build_dag_levels(calculated_fields, raw_field_names)

        # Section header for this entity
        entity_snake = to_snake_case(entity_name)
        lines.append('')
        lines.append('# ' + '=' * 77)
        lines.append(f'# {entity_name.upper()} CALCULATIONS')
        lines.append('# ' + '=' * 77)

        # Generate calculation functions for each level
        for level_idx, level_fields in enumerate(dag_levels):
            lines.append('')
            lines.append(f'# Level {level_idx + 1}')

            for field in level_fields:
                lines.append('')
                lines.append(generate_calc_function(entity_name, field))

        # Generate entity-specific compute function
        lines.append('')
        lines.append('')
        lines.append(generate_entity_compute_function(
            entity_name, calculated_fields, dag_levels, string_fields
        ))

    # Generate dispatcher function
    lines.append('')
    lines.append('')
    lines.append('# ' + '=' * 77)
    lines.append('# DISPATCHER FUNCTION')
    lines.append('# ' + '=' * 77)
    lines.append('')
    lines.append(generate_dispatcher_function(entities_with_calcs))

    return '\n'.join(lines)


def main():
    # Files actually generated by THIS script
    GENERATED_FILES = [
        'erb_calc.py',
    ]

    # Handle --clean argument
    if handle_clean_arg(GENERATED_FILES, "Python substrate: Removes generated calculation library"):
        return

    script_dir = Path(__file__).resolve().parent

    print("=" * 70)
    print("Python Execution Substrate - Multi-Entity Formula Compiler")
    print("=" * 70)
    print()

    # Load the rulebook
    print("Loading rulebook...")
    try:
        rulebook = load_rulebook()
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # Discover entities
    entities = discover_entities(rulebook)
    print(f"Discovered {len(entities)} entities: {', '.join(entities)}")
    print()

    # Show calculated fields per entity
    total_fields = 0
    for entity_name in entities:
        schema = get_entity_schema(rulebook, entity_name)
        calculated_fields = get_calculated_fields(schema)
        if calculated_fields:
            print(f"  {entity_name}: {len(calculated_fields)} calculated fields")
            for field in calculated_fields:
                print(f"    - {field['name']}")
            total_fields += len(calculated_fields)

    print()
    print(f"Total: {total_fields} calculated fields to compile")
    print()
    print("-" * 70)
    print()

    # Generate erb_calc.py
    print("Generating erb_calc.py...")
    erb_calc_content = generate_erb_calc(rulebook)

    erb_calc_path = script_dir / "erb_calc.py"
    erb_calc_path.write_text(erb_calc_content, encoding='utf-8')
    print(f"Wrote: {erb_calc_path} ({len(erb_calc_content)} bytes)")

    print()
    print("=" * 70)
    print("Generation complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
