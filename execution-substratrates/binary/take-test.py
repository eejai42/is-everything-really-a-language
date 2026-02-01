#!/usr/bin/env python3
"""
Take Test - Binary Execution Substrate

This script:
1. Loads test-answers.json (copied from blank-test.json)
2. For each record, calls the native binary calc functions via ctypes
3. Updates the JSON with computed values
4. Saves test-answers.json

CRITICAL BOUNDARY:
- Python handles ONLY: JSON loading/saving, field name access, calling functions
- Python NEVER contains: computation logic, string concatenation for results,
  boolean comparisons, conditional string building

ALL computation happens in the native binary (erb_calc.dylib / erb_calc.so).
"""

import ctypes
import json
import platform
from pathlib import Path


def load_library():
    """Load the native calc library."""
    script_dir = Path(__file__).resolve().parent

    # Determine library name based on platform
    system = platform.system()
    if system == "Darwin":
        lib_name = "erb_calc.dylib"
    elif system == "Linux":
        lib_name = "erb_calc.so"
    else:
        raise RuntimeError(f"Unsupported platform: {system}")

    lib_path = script_dir / lib_name

    if not lib_path.exists():
        raise FileNotFoundError(
            f"Library not found: {lib_path}\n"
            "Run inject-into-binary.py first to compile the library."
        )

    lib = ctypes.CDLL(str(lib_path))

    # Setup function signatures
    # -------------------------

    # calc_category_contains_language(category: str) -> bool
    lib.calc_category_contains_language.argtypes = [ctypes.c_char_p]
    lib.calc_category_contains_language.restype = ctypes.c_bool

    # calc_has_grammar(has_syntax: bool) -> bool
    lib.calc_has_grammar.argtypes = [ctypes.c_bool]
    lib.calc_has_grammar.restype = ctypes.c_bool

    # calc_relationship_to_concept(distance: int) -> str
    lib.calc_relationship_to_concept.argtypes = [ctypes.c_int]
    lib.calc_relationship_to_concept.restype = ctypes.c_char_p

    # calc_family_fued_question(name: str) -> str
    lib.calc_family_fued_question.argtypes = [ctypes.c_char_p]
    lib.calc_family_fued_question.restype = ctypes.c_char_p

    # calc_is_a_family_feud_top_answer(...) -> bool
    lib.calc_is_a_family_feud_top_answer.argtypes = [
        ctypes.c_char_p,  # category
        ctypes.c_bool,    # has_syntax
        ctypes.c_bool,    # can_be_held
        ctypes.c_bool,    # meaning_is_serialized
        ctypes.c_bool,    # requires_parsing
        ctypes.c_bool,    # is_ongology_descriptor
        ctypes.c_bool,    # has_identity
        ctypes.c_int,     # distance_from_concept
    ]
    lib.calc_is_a_family_feud_top_answer.restype = ctypes.c_bool

    # calc_family_feud_mismatch(name, is_top, chosen) -> str or NULL
    lib.calc_family_feud_mismatch.argtypes = [
        ctypes.c_char_p,  # name
        ctypes.c_bool,    # is_top_answer
        ctypes.c_bool,    # chosen_language_candidate
    ]
    lib.calc_family_feud_mismatch.restype = ctypes.c_char_p

    return lib


def to_bytes(value):
    """Convert a string to bytes for ctypes, handling None."""
    if value is None:
        return b""
    return str(value).encode("utf-8")


def to_bool(value):
    """Convert a value to boolean, treating None as False."""
    if value is None:
        return False
    return bool(value)


def to_int(value, default=0):
    """Convert a value to int, with a default for None."""
    if value is None:
        return default
    return int(value)


def main():
    script_dir = Path(__file__).resolve().parent
    test_file = script_dir / "test-answers.json"

    print("=" * 60)
    print("Binary Execution Substrate - Test Execution Phase")
    print("=" * 60)

    # Load the library
    print("\nLoading native binary library...")
    lib = load_library()
    print("Library loaded successfully!")

    # Load test data
    print(f"\nLoading test data from: {test_file}")
    with open(test_file, "r") as f:
        data = json.load(f)

    print(f"Loaded {len(data)} records")

    # Process each record
    print("\nComputing calculated fields...")
    for i, record in enumerate(data):
        # Extract raw field values (Python just accesses JSON, no computation)
        name = record.get("name")
        category = record.get("category")
        has_syntax = record.get("has_syntax")
        can_be_held = record.get("can_be_held")
        meaning_is_serialized = record.get("meaning_is_serialized")
        requires_parsing = record.get("requires_parsing")
        is_ongology_descriptor = record.get("is_ongology_descriptor")
        has_identity = record.get("has_identity")
        distance_from_concept = record.get("distance_from_concept")
        chosen_language_candidate = record.get("chosen_language_candidate")

        # Call native binary functions for ALL computations
        # -------------------------------------------------

        # Level 1: family_fued_question
        question_result = lib.calc_family_fued_question(to_bytes(name))
        record["family_fued_question"] = question_result.decode("utf-8") if question_result else ""

        # Level 1: has_grammar
        record["has_grammar"] = lib.calc_has_grammar(to_bool(has_syntax))

        # Level 1: relationship_to_concept
        relationship_result = lib.calc_relationship_to_concept(to_int(distance_from_concept))
        record["relationship_to_concept"] = relationship_result.decode("utf-8") if relationship_result else ""

        # Level 2: top_family_feud_answer (is_a_family_feud_top_answer)
        is_top_answer = lib.calc_is_a_family_feud_top_answer(
            to_bytes(category),
            to_bool(has_syntax),
            to_bool(can_be_held),
            to_bool(meaning_is_serialized),
            to_bool(requires_parsing),
            to_bool(is_ongology_descriptor),
            to_bool(has_identity),
            to_int(distance_from_concept)
        )
        record["top_family_feud_answer"] = is_top_answer

        # Level 3: family_feud_mismatch
        mismatch_result = lib.calc_family_feud_mismatch(
            to_bytes(name),
            is_top_answer,
            to_bool(chosen_language_candidate)
        )
        if mismatch_result:
            record["family_feud_mismatch"] = mismatch_result.decode("utf-8")
        else:
            record["family_feud_mismatch"] = None

    # Save results
    print(f"\nSaving results to: {test_file}")
    with open(test_file, "w") as f:
        json.dump(data, f, indent=2)

    print("\nTest execution complete!")
    print(f"Computed {len(data)} records with native binary functions.")


if __name__ == "__main__":
    main()
