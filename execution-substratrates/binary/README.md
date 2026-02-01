# Binary - x86-64 Assembly Execution Substrate

x86-64 assembly implementation where ALL calculation functions are implemented at the register level.

## Overview

This substrate compiles the ERB rulebook into raw x86-64 assembly. Every calculated field is computed by CPU instructions. Python handles only file I/O (loading and saving JSON); all business logic executes in assembly.

## The Critical Boundary: Computation Logic

The boundary is **computation logic**, not domain awareness.

### Python Layer (`take-test.py`) — CAN have:
- Field names like `category`, `has_syntax`, `name` (for JSON access)
- Data structures and JSON loading/saving
- Calling assembly functions with the right field values
- Everything from the Python substrate EXCEPT the `calc_*` methods

### Python Layer — CANNOT have:
- `"language" in category.lower()` — this is computation
- `"true" if has_syntax else ""` — this is computation
- `f"Is {name} a language?"` — this is computation
- Boolean AND chains — this is computation
- Conditional string building — this is computation

### Assembly Layer (`erb_calc.asm`) — MUST have:
- All 6 `calc_*` functions from the rulebook
- The actual logic that decides outputs from inputs
- Uses libc for string primitives (strlen, strcat, strstr, etc.)

### Why This Matters

If Python contained `if "language" in category.lower()`, we'd just be running Python with assembly as decoration. The assembly must own the actual decision-making.

## libc Usage: Allowed and Expected

This substrate does **NOT** require reimplementing string primitives. Using libc is expected:

| libc Function | Used For |
|---------------|----------|
| `strlen` | Get string length |
| `strcpy`, `strcat` | String concatenation |
| `strstr` | Substring search |
| `tolower` | Case conversion |
| `malloc`, `free` | Buffer allocation |
| `sprintf` | Formatted string building |

The assembly implements the **decision logic** — checking boolean flags, comparing integers, deciding which strings to concatenate. The libc functions are just tools, like how SQL uses built-in `LOWER()` and `CONCAT()`.

## Comparison: SQL vs Assembly Verbosity

In PostgreSQL, each calculated field is typically **1 line**:

```sql
-- calc_category_contains_language
POSITION('language' IN LOWER(category)) > 0

-- calc_family_fued_question
'Is ' || name || ' a language?'
```

In assembly, the same logic requires **many more lines** — setting up registers, calling libc, handling the calling convention, etc. A simple string concatenation might be 20-30 lines. This is expected and acceptable; the goal is proving the contract works, not code golf.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  inject-into-binary.py                                      │
│  (Generic rulebook-to-assembly generator)                   │
│                                                             │
│  Reads:  effortless-rulebook.json                           │
│  Writes: erb_calc.asm (generated assembly source)           │
│          erb_calc.so  (compiled shared library)             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  take-test.py                                               │
│                                                             │
│  1. Load test-answers.json (contains nulls)                 │
│  2. For each record, for each null calculated field:        │
│     → Call the corresponding assembly function via ctypes   │
│  3. Update the JSON with computed values                    │
│  4. Save test-answers.json                                  │
└─────────────────────────────────────────────────────────────┘
```

## Role in Three-Phase Contract

### Phase 1: Inject

`inject-into-binary.py` reads the rulebook and generates:

1. **erb_calc.asm** — Assembly source with all calc functions:
   - `calc_category_contains_language` (string search)
   - `calc_has_grammar` (bool to string)
   - `calc_relationship_to_concept` (conditional string)
   - `calc_family_fued_question` (string concatenation)
   - `calc_is_a_family_feud_top_answer` (8-way boolean AND)
   - `calc_family_feud_mismatch` (conditional string concatenation)

2. **erb_calc.so** — Compiled shared library (via NASM + linker)

### Phase 2: Execute

`take-test.py` runs the test:

```bash
./take-test.sh
```

Which executes:
1. Copy `blank-test.json` → `test-answers.json`
2. Run `take-test.py`:
   - Load `test-answers.json`
   - For each null field, call the assembly function
   - Update with computed result
   - Save `test-answers.json`

### Phase 3: Emit

`test-answers.json` contains all computed values, produced by assembly execution.

### Grade

Compare `test-answers.json` against `answer-key.json` — assembly must produce identical results to all other substrates.

## Generated Assembly Functions

Each calc function from the rulebook becomes an assembly function:

| Calculated Field | Assembly Function | Operations |
|------------------|-------------------|------------|
| `category_contains_language` | `calc_category_contains_language` | String lowercase, substring search |
| `has_grammar` | `calc_has_grammar` | Boolean to string conversion |
| `relationship_to_concept` | `calc_relationship_to_concept` | Integer compare, return string pointer |
| `family_fued_question` | `calc_family_fued_question` | String concatenation |
| `is_a_family_feud_top_answer` | `calc_is_a_family_feud_top_answer` | 8-way boolean AND |
| `family_feud_mismatch` | `calc_family_feud_mismatch` | Conditional string building |

## Python/Assembly Interface

Python calls assembly via `ctypes`. Python knows field names but delegates all computation:

```python
import ctypes
import json

lib = ctypes.CDLL("./erb_calc.dylib")

# Setup function signatures
lib.calc_category_contains_language.argtypes = [ctypes.c_char_p]
lib.calc_category_contains_language.restype = ctypes.c_bool

lib.calc_family_fued_question.argtypes = [ctypes.c_char_p]
lib.calc_family_fued_question.restype = ctypes.c_char_p

# Load JSON
with open("test-answers.json") as f:
    data = json.load(f)

for record in data["LanguageCandidates"]["data"]:
    # Python knows field names, but computation happens in assembly
    category = (record.get("Category") or "").encode('utf-8')
    record["CategoryContainsLanguage"] = lib.calc_category_contains_language(category)

    name = (record.get("Name") or "").encode('utf-8')
    result = lib.calc_family_fued_question(name)
    record["FamilyFuedQuestion"] = result.decode('utf-8') if result else ""

with open("test-answers.json", "w") as f:
    json.dump(data, f, indent=2)
```

The key: Python never contains `"language" in x.lower()` or string concatenation logic — that's all in assembly.

## Files

| File | Description |
|------|-------------|
| `inject-into-binary.py` | Generates assembly from rulebook |
| `erb_calc.asm` | Generated assembly source (all calc functions) |
| `erb_calc.o` | Assembled object file |
| `erb_calc.so` / `erb_calc.dylib` | Compiled shared library |
| `take-test.py` | Test runner (JSON I/O + assembly calls) |
| `inject-substrate.sh` | Runs injection + compilation |
| `take-test.sh` | Runs the test |
| `test-answers.json` | Computed results for grading |

## Build Process

```bash
# 1. Generate assembly from rulebook
python inject-into-binary.py

# 2. Assemble to object file
nasm -f elf64 erb_calc.asm -o erb_calc.o      # Linux
nasm -f macho64 erb_calc.asm -o erb_calc.o    # macOS

# 3. Link to shared library
ld -shared -o erb_calc.so erb_calc.o          # Linux
ld -dylib -o erb_calc.dylib erb_calc.o        # macOS
```

## DAG Execution Order

```
Level 0: Raw fields (from JSON)
Level 1: category_contains_language, has_grammar, relationship_to_concept, family_fued_question
Level 2: is_a_family_feud_top_answer (depends on category_contains_language)
Level 3: family_feud_mismatch (depends on is_a_family_feud_top_answer)
```

Assembly functions respect this order — Level 2+ functions call Level 1 functions internally.

## Why Assembly?

This substrate proves the ERB contract holds at the lowest practical level of abstraction. The same business rules that work in a spreadsheet, in SQL, in Python — work as raw CPU instructions.

The `inject-into-binary.py` generator is domain-agnostic: it reads any ERB rulebook and produces assembly. The pattern is identical to other substrates — only the target language changes.

## Status

Planned implementation.

## Expected Difficulty

This substrate is intentionally harder than higher-level substrates. A score below 100% is meaningful data:

- **Python/SQL**: High-level abstractions handle edge cases automatically
- **Assembly**: Every edge case must be handled explicitly

If binary scores 80% while Python scores 100%, that demonstrates something real about abstraction levels and their trade-offs. The contract is *possible* at the CPU level, but *harder* — and quantifying that difficulty is part of the experiment.

## Source

Generated from: `effortless-rulebook/effortless-rulebook.json`
