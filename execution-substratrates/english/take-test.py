#!/usr/bin/env python3
"""
Take test for the English execution substrate.

Supports two modes:
1. Multi-entity (--multi-entity): Uses shared erb_calc.py for all entities
2. Legacy: Uses LLM to infer values from English specifications

This script reads the generated English markdown files (specification.md,
candidate-profiles.md, glossary.md) and uses an LLM to infer the values
for the computed columns in test-answers.json.

The test validates whether natural language specifications can be used
to correctly compute derived fields - essentially testing if an LLM can
"execute" English as a programming language.
"""

import argparse
import glob as glob_module
import json
import os
import sys
from pathlib import Path

# Get script directory
script_dir = Path(__file__).parent.resolve()

# Add Python substrate directory to path for shared library
python_substrate_dir = script_dir / ".." / "python"
sys.path.insert(0, str(python_substrate_dir))


COMPUTED_COLUMNS = [
    "family_fued_question",
    "top_family_feud_answer",
    "family_feud_mismatch",
    "has_grammar",
    "is_open_closed_world_conflicted",
    "relationship_to_concept"
]


def has_computed_values(test_answers):
    """Check if any computed columns have non-null values."""
    for record in test_answers:
        for col in COMPUTED_COLUMNS:
            if record.get(col) is not None:
                return True
    return False


def load_markdown_files(script_dir):
    """Load all generated markdown files."""
    md_files = {}

    for filename in ['specification.md', 'candidate-profiles.md', 'glossary.md']:
        filepath = script_dir / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                md_files[filename] = f.read()
        else:
            print(f"Warning: {filename} not found")
            md_files[filename] = ""

    return md_files


def extract_raw_predicates(glossary_text):
    """Extract only the Raw Predicates section from the glossary (skip Calculated Predicates)."""
    if not glossary_text:
        return ""
    # Find the start of Calculated Predicates and cut there
    calc_idx = glossary_text.find("## Calculated Predicates")
    if calc_idx > 0:
        return glossary_text[:calc_idx].strip()
    return glossary_text


def build_prompt(md_files, test_answers):
    """Build the prompt for the LLM to fill in computed columns."""
    # Only include raw predicate definitions (input field meanings), not the calculated formulas
    # which are already in the specification
    raw_predicates = extract_raw_predicates(md_files.get('glossary.md', ''))

    prompt = f"""You are taking a test. Your task is to fill in the computed columns for each language candidate based on the specification provided.

## The Specification (How to compute each field)

{md_files.get('specification.md', '')}

## Field Definitions (Input Fields Only)

{raw_predicates}

## Your Task

Below is a JSON array of language candidates. Each candidate has raw input fields already filled in, but the following computed columns are null and need to be calculated:

- family_fued_question (string): Apply the formula from the spec
- top_family_feud_answer (boolean): Apply the 7-condition AND formula
- family_feud_mismatch (string or null): Apply the IF formula - returns null if TopFamilyFeudAnswer equals ChosenLanguageCandidate
- has_grammar (boolean): Equals HasSyntax
- is_open_closed_world_conflicted (boolean): IsOpenWorld AND IsClosedWorld
- relationship_to_concept (string): "IsMirrorOf" if DistanceFromConcept=1, else "IsDescriptionOf"

## Input Data (test-answers.json with nulls)

```json
{json.dumps(test_answers, indent=2)}
```

## Instructions

1. For EACH candidate in the array, compute the 6 null fields using the formulas from the specification
2. Return ONLY the complete JSON array with all computed fields filled in
3. Use exact field names as shown (snake_case)
4. Boolean values should be true/false (lowercase, no quotes)
5. String values should be in quotes
6. family_feud_mismatch should be null (not "null") when there's no mismatch

Return ONLY valid JSON - no markdown code blocks, no explanations, just the JSON array."""

    return prompt


def extract_json_from_response(response_text):
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


def call_llm(prompt):
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
    model = "gpt-4o-mini"  # Smaller model with 8k tokens - should get some right but not all

    # Log first 2 lines of prompt
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
        temperature=0.3,  # Higher temp for more variability
        max_tokens=8096,  # gpt-3.5-turbo limit
    )

    response_text = response.choices[0].message.content

    # Log first 2 lines of response
    response_lines = response_text.split('\n')
    print("=" * 60)
    print("RESPONSE (first 2 lines):")
    for line in response_lines[:2]:
        print(f"  {line[:100]}")
    print(f"  ... ({len(response_lines)} total lines, {len(response_text)} chars)")
    print("=" * 60)
    sys.stdout.flush()

    return response_text


def copy_blank_test(script_dir, answers_path):
    """Copy blank-test.json to test-answers.json."""
    import shutil
    blank_path = script_dir / '..' / '..' / 'testing' / 'blank-test.json'
    if not blank_path.exists():
        print(f"Error: {blank_path} not found")
        sys.exit(1)
    shutil.copy(blank_path, answers_path)
    print(f"Copied blank test to {answers_path.name}")


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
    print("English Execution Substrate - Multi-Entity Test Execution")
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

        count = process_entity(input_path, str(output_path), entity)
        total_records += count
        entity_count += 1

        print(f"  -> {entity}: {count} records")

    print(f"\nEnglish substrate: Processed {entity_count} entities, {total_records} total records")
    print("=" * 70)


# =============================================================================
# LEGACY MODE (uses LLM)
# =============================================================================

def run_legacy(args):
    """Process using LLM inference (legacy mode)."""
    answers_path = script_dir / 'test-answers.json'

    # Load markdown files first (needed regardless)
    md_files = load_markdown_files(script_dir)

    if not md_files.get('specification.md'):
        print("Error: specification.md not found - run inject-into-english.py first")
        sys.exit(1)

    # Ask user if they want to run the LLM test (unless --regenerate)
    if not args.regenerate:
        if args.no_prompt:
            print("Skipping LLM test (use --regenerate to force).")
            return 0

        if not sys.stdin.isatty():
            print("Non-interactive mode detected. Skipping LLM test (use --regenerate to force).")
            return 0

        sys.stdout.flush()
        try:
            response = input("Run LLM test for english? [y/N]: ").strip().lower()
        except EOFError:
            print("\nNon-interactive mode detected (EOF). Skipping LLM test (use --regenerate to force).")
            return 0
        if response not in ('y', 'yes'):
            print("Skipping LLM test. Use --regenerate to force.")
            return 0

    # User said yes - delete old answers and copy fresh blank test
    if answers_path.exists():
        answers_path.unlink()
    copy_blank_test(script_dir, answers_path)

    # Load the fresh blank test
    with open(answers_path, 'r', encoding='utf-8') as f:
        test_answers = json.load(f)

    print(f"Loaded {len(test_answers)} candidates from test-answers.json")

    # Build prompt
    prompt = build_prompt(md_files, test_answers)

    # Call LLM
    response = call_llm(prompt)

    # Parse response
    filled_answers = extract_json_from_response(response)

    if filled_answers is None:
        print("Error: Could not parse LLM response as JSON")
        print("Response was:")
        print(response[:1000])
        sys.exit(1)

    if len(filled_answers) != len(test_answers):
        print(f"Warning: LLM returned {len(filled_answers)} records, expected {len(test_answers)}")

    # Write updated answers
    with open(answers_path, 'w', encoding='utf-8') as f:
        json.dump(filled_answers, f, indent=2)

    print(f"english: test-answers.json updated with {len(filled_answers)} computed records")

    # Count filled fields
    filled_count = 0
    for record in filled_answers:
        for col in COMPUTED_COLUMNS:
            if record.get(col) is not None:
                filled_count += 1

    print(f"Filled {filled_count} computed fields across {len(filled_answers)} records")


# =============================================================================
# MAIN
# =============================================================================

def main():
    run_multi_entity()


if __name__ == "__main__":
    main()
