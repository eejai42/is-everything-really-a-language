#!/usr/bin/env python3
"""
Take test for the English execution substrate.

This substrate uses an LLM to "execute" English language specifications.
It reads the schema from the rulebook and asks the LLM to compute the
calculated fields for each record based on the formula descriptions.

This tests whether natural language specifications can be used to correctly
compute derived fields - essentially testing if an LLM can "execute" English
as a programming language.

DOMAIN-AGNOSTIC: Works with any Airtable schema, not hardcoded to any specific domain.
"""

import glob as glob_module
import json
import os
import sys
from pathlib import Path

# Get script directory
script_dir = Path(__file__).parent.resolve()

# Add project root to path for shared imports
sys.path.insert(0, str(script_dir.parent.parent))

from orchestration.shared import (
    load_rulebook,
    discover_entities,
    get_entity_schema,
    get_calculated_fields,
    get_raw_fields,
    to_snake_case,
    to_pascal_case
)


# =============================================================================
# MODEL CONFIGURATION
# =============================================================================

DEFAULT_PROVIDER = os.environ.get("LLM_PROVIDER", "openai")
DEFAULT_MODEL = os.environ.get("LLM_MODEL", "gpt-4o-mini")


def call_llm(prompt: str) -> str:
    """Call the OpenAI API to get computed values."""
    try:
        import openai
    except ImportError:
        print("Error: openai package not installed")
        print("Run: pip install openai")
        sys.exit(1)

    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)

    client = openai.OpenAI()
    model = DEFAULT_MODEL

    # Log prompt info
    prompt_lines = prompt.split('\n')
    print("=" * 60)
    print("PROMPT (first 2 lines):")
    for line in prompt_lines[:2]:
        print(f"  {line[:100]}")
    print(f"  ... ({len(prompt_lines)} total lines, {len(prompt)} chars)")
    print("=" * 60)
    print(f"Calling OpenAI ({model})... please wait...")
    sys.stdout.flush()

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=8096,
    )

    response_text = response.choices[0].message.content

    # Log response info
    response_lines = response_text.split('\n')
    print("=" * 60)
    print("RESPONSE (first 2 lines):")
    for line in response_lines[:2]:
        print(f"  {line[:100]}")
    print(f"  ... ({len(response_lines)} total lines, {len(response_text)} chars)")
    print("=" * 60)
    sys.stdout.flush()

    return response_text


# =============================================================================
# PROMPT BUILDING (Domain-Agnostic)
# =============================================================================

def build_schema_description(schema: list) -> str:
    """Build a human-readable description of the schema for the LLM."""
    raw_fields = get_raw_fields(schema)
    calc_fields = get_calculated_fields(schema)

    lines = []

    # Raw fields section
    lines.append("## Input Fields (Raw Data)")
    lines.append("")
    for field in raw_fields:
        name = field.get('name', 'Unknown')
        datatype = field.get('datatype', 'string')
        desc = field.get('Description', '')
        snake_name = to_snake_case(name)
        lines.append(f"- **{snake_name}** ({datatype}): {desc if desc else 'Input field'}")
    lines.append("")

    # Calculated fields section
    lines.append("## Calculated Fields (To Be Computed)")
    lines.append("")
    for field in calc_fields:
        name = field.get('name', 'Unknown')
        datatype = field.get('datatype', 'string')
        formula = field.get('formula', '')
        desc = field.get('Description', '')
        snake_name = to_snake_case(name)
        lines.append(f"### {snake_name}")
        lines.append(f"- **Type:** {datatype}")
        lines.append(f"- **Formula:** `{formula}`")
        if desc:
            lines.append(f"- **Description:** {desc}")
        lines.append("")

    return "\n".join(lines)


def build_computed_columns_list(schema: list) -> list:
    """Get list of calculated column names in snake_case."""
    calc_fields = get_calculated_fields(schema)
    return [to_snake_case(f.get('name', '')) for f in calc_fields]


def build_prompt(schema: list, entity_name: str, test_data: list) -> str:
    """Build the prompt for the LLM to fill in computed columns."""
    schema_description = build_schema_description(schema)
    calc_fields = get_calculated_fields(schema)
    computed_columns = build_computed_columns_list(schema)

    # Build bullet list of computed columns with their types and formulas
    computed_cols_desc = []
    for field in calc_fields:
        name = to_snake_case(field.get('name', ''))
        datatype = field.get('datatype', 'string')
        formula = field.get('formula', '')
        computed_cols_desc.append(f"- {name} ({datatype}): {formula}")

    prompt = f"""You are taking a test. Your task is to fill in the computed columns for each record in the "{entity_name}" entity based on the schema and formulas provided.

## Schema Definition

{schema_description}

## Your Task

Below is a JSON array of {entity_name} records. Each record has raw input fields already filled in, but the following computed columns are null and need to be calculated:

{chr(10).join(computed_cols_desc)}

## Input Data (with null values for computed fields)

```json
{json.dumps(test_data, indent=2)}
```

## Instructions

1. For EACH record in the array, compute the null fields using the formulas provided above
2. Return ONLY the complete JSON array with all computed fields filled in
3. Use exact field names as shown (snake_case)
4. Boolean values should be true/false (lowercase, no quotes)
5. String values should be in quotes
6. null should remain null (not "null") if the formula cannot be computed
7. Preserve ALL other fields exactly as they appear in the input

Return ONLY valid JSON - no markdown code blocks, no explanations, just the JSON array."""

    return prompt


def extract_json_from_response(response_text: str) -> list:
    """Extract JSON array from LLM response."""
    # Try to parse directly first
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass

    # Try to find JSON array in the response
    text = response_text.strip()

    # Remove markdown code blocks if present
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    # Find the array bounds
    start = text.find('[')
    end = text.rfind(']')

    if start != -1 and end != -1:
        try:
            return json.loads(text[start:end+1])
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            print(f"Attempted to parse: {text[start:start+200]}...")

    return None


# =============================================================================
# MULTI-ENTITY PROCESSING
# =============================================================================

def process_entity(input_path: str, output_path: str, entity_name: str,
                   schema: list) -> tuple:
    """
    Process a single entity file using the LLM.

    Returns: (record_count, filled_field_count)
    """
    # Load input data
    with open(input_path, 'r', encoding='utf-8') as f:
        test_data = json.load(f)

    if not test_data:
        # Empty file - just copy it
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2)
        return (0, 0)

    computed_columns = build_computed_columns_list(schema)

    if not computed_columns:
        # No calculated fields - just copy the data
        print(f"    No calculated fields for {entity_name}, copying as-is")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2)
        return (len(test_data), 0)

    # Build and send prompt
    prompt = build_prompt(schema, entity_name, test_data)
    response = call_llm(prompt)

    # Parse response
    filled_answers = extract_json_from_response(response)

    if filled_answers is None:
        print(f"Error: Could not parse LLM response as JSON for {entity_name}")
        print("Response was:")
        print(response[:1000])
        # Write empty result
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2)
        return (len(test_data), 0)

    if len(filled_answers) != len(test_data):
        print(f"Warning: LLM returned {len(filled_answers)} records, expected {len(test_data)}")

    # Count filled fields
    filled_count = 0
    for record in filled_answers:
        for col in computed_columns:
            if record.get(col) is not None:
                filled_count += 1

    # Write results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(filled_answers, f, indent=2)

    return (len(filled_answers), filled_count)


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
    print("English Execution Substrate - LLM Test Execution (Domain-Agnostic)")
    print("=" * 70)
    print()

    # Load rulebook to get schemas
    print("Loading rulebook...")
    try:
        rulebook = load_rulebook()
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # Discover all entities
    entities = discover_entities(rulebook)
    print(f"Discovered {len(entities)} entities: {', '.join(entities)}")

    # Process each entity file (skip metadata files starting with _)
    total_records = 0
    total_filled = 0
    entity_count = 0

    for input_path in sorted(glob_module.glob(str(blank_tests_dir / "*.json"))):
        filename = os.path.basename(input_path)

        # Skip metadata files
        if filename.startswith('_'):
            continue

        entity_snake = filename.replace('.json', '')
        output_path = test_answers_dir / filename

        # Find matching rulebook entity (case-insensitive)
        rulebook_entity = None
        for e in entities:
            if to_snake_case(e) == entity_snake:
                rulebook_entity = e
                break

        if not rulebook_entity:
            print(f"  -> {entity_snake}: No matching entity in rulebook, copying as-is")
            with open(input_path, 'r') as f:
                data = json.load(f)
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
            continue

        # Get schema for this entity
        schema = get_entity_schema(rulebook, rulebook_entity)
        calc_fields = get_calculated_fields(schema)

        print(f"\nProcessing {entity_snake}...")
        print(f"  Schema: {len(schema)} fields, {len(calc_fields)} calculated")

        # Process the entity
        record_count, filled_count = process_entity(
            input_path, output_path, entity_snake, schema
        )

        total_records += record_count
        total_filled += filled_count
        entity_count += 1

        print(f"  -> {entity_snake}: {record_count} records, {filled_count} computed fields filled")

    print()
    print("=" * 70)
    print(f"English substrate: Processed {entity_count} entities, {total_records} total records")
    print(f"Filled {total_filled} computed fields total")
    print("=" * 70)


def main():
    """Main entry point."""
    run_multi_entity()


if __name__ == "__main__":
    main()
