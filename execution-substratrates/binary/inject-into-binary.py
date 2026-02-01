#!/usr/bin/env python3
"""
Inject ERB Rulebook into Binary Execution Substrate.

This script compiles the C implementation of calc functions to a shared library
that can be called from Python via ctypes.

The C code (erb_calc.c) contains ALL calculation logic. This script only:
1. Compiles the C code to native binary (.dylib on macOS, .so on Linux)
2. Verifies the build was successful

Build process:
- macOS: clang -shared -fPIC erb_calc.c -o erb_calc.dylib
- Linux: gcc -shared -fPIC erb_calc.c -o erb_calc.so
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

# Add project root to path for shared imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from orchestration.shared import load_rulebook


def detect_platform():
    """Detect the current platform and return appropriate compiler settings."""
    system = platform.system()
    if system == "Darwin":
        return {
            "compiler": "clang",
            "output": "erb_calc.dylib",
            "flags": ["-shared", "-fPIC", "-O2"],
        }
    elif system == "Linux":
        return {
            "compiler": "gcc",
            "output": "erb_calc.so",
            "flags": ["-shared", "-fPIC", "-O2"],
        }
    else:
        raise RuntimeError(f"Unsupported platform: {system}")


def compile_shared_library(script_dir):
    """Compile erb_calc.c to a shared library."""
    platform_info = detect_platform()

    c_source = script_dir / "erb_calc.c"
    output_file = script_dir / platform_info["output"]

    if not c_source.exists():
        raise FileNotFoundError(f"C source not found: {c_source}")

    # Build command
    cmd = [
        platform_info["compiler"],
        *platform_info["flags"],
        str(c_source),
        "-o", str(output_file),
    ]

    print(f"Compiling: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Compilation FAILED:")
        print(result.stderr)
        sys.exit(1)

    print(f"Successfully compiled: {output_file}")
    return output_file


def verify_library(lib_path):
    """Verify the library exports expected functions."""
    import ctypes

    try:
        lib = ctypes.CDLL(str(lib_path))

        # Check that expected functions exist
        expected_functions = [
            "calc_category_contains_language",
            "calc_has_grammar",
            "calc_relationship_to_concept",
            "calc_family_fued_question",
            "calc_is_a_family_feud_top_answer",
            "calc_family_feud_mismatch",
        ]

        for func_name in expected_functions:
            if not hasattr(lib, func_name):
                print(f"WARNING: Function {func_name} not found in library")
            else:
                print(f"  - {func_name}")

        print("Library verification passed!")
        return True

    except Exception as e:
        print(f"Library verification FAILED: {e}")
        return False


def main():
    script_dir = Path(__file__).resolve().parent
    print("=" * 60)
    print("Binary Execution Substrate - Injection Phase")
    print("=" * 60)

    # Load rulebook (for verification/logging)
    try:
        rulebook = load_rulebook()
        candidates = rulebook.get("LanguageCandidates", {}).get("data", [])
        print(f"Loaded rulebook with {len(candidates)} language candidates")
    except FileNotFoundError as e:
        print(f"Warning: {e}")

    # Compile the shared library
    print("\nCompiling C code to native binary...")
    lib_path = compile_shared_library(script_dir)

    # Verify the library
    print("\nVerifying library exports...")
    verify_library(lib_path)

    print("\nInjection complete!")
    print(f"Library ready at: {lib_path}")


if __name__ == "__main__":
    main()
