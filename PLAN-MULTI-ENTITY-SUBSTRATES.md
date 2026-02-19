# Plan: Convert All Substrates to Multi-Entity Support

## Overview

Convert the 6 remaining substrates to support multi-entity testing, and remove all legacy single-entity code paths from the codebase.

## Current State

### Substrates WITH multi-entity support (5):
- `csv` - ✅ Has `--multi-entity` flag, auto-detects `blank-tests/`
- `golang` - ✅ Has `--multi-entity` flag, auto-detects `blank-tests/`
- `python` - ✅ Has `--multi-entity` flag, auto-detects `blank-tests/`
- `xlsx` - ✅ Has `--multi-entity` flag, auto-detects `blank-tests/`
- `yaml` - ✅ Has `--multi-entity` flag, auto-detects `blank-tests/`

### Substrates NEEDING multi-entity support (6):
- `binary` - Python-based, straightforward conversion
- `english` - Python-based, has hardcoded columns + LLM logic
- `graphql` - Python-based, straightforward conversion
- `owl` - Python-based, straightforward conversion
- `rdf` - Python-based, straightforward conversion
- `uml` - Python-based, straightforward conversion

### Legacy files to remove:
- `testing/blank-test.json` - single-entity blank test
- `testing/answer-key.json` - single-entity answer key
- Legacy code paths in `test-orchestrator.py` that generate these files
- Legacy code paths in all `take-test.sh` scripts that check for single files

---

## Phase 1: Update Remaining Substrates

### Task 1.1: Update `binary` substrate

**Files to modify:**
- `execution-substratrates/binary/take-test.sh`
- `execution-substratrates/binary/take-test.py`

**Changes:**
1. Update `take-test.sh` to use the standard multi-entity detection pattern:
```bash
if [ -d "$SCRIPT_DIR/blank-tests" ] && [ -n "$(ls -A "$SCRIPT_DIR/blank-tests" 2>/dev/null)" ]; then
    python3 take-test.py --multi-entity
else
    # Legacy fallback (will be removed in Phase 2)
    ...
fi
```

2. Update `take-test.py` to:
   - Add `--multi-entity` argument
   - Add `run_multi_entity()` function that loops through `blank-tests/*.json`
   - Read computed columns from `blank-tests/_metadata.json` instead of hardcoding
   - Write output to `test-answers/{entity}.json`

---

### Task 1.2: Update `graphql` substrate

**Files to modify:**
- `execution-substratrates/graphql/take-test.sh`
- `execution-substratrates/graphql/take-test.py`

**Changes:** Same pattern as Task 1.1

---

### Task 1.3: Update `owl` substrate

**Files to modify:**
- `execution-substratrates/owl/take-test.sh`
- `execution-substratrates/owl/take-test.py`

**Changes:** Same pattern as Task 1.1

---

### Task 1.4: Update `rdf` substrate

**Files to modify:**
- `execution-substratrates/rdf/take-test.sh`
- `execution-substratrates/rdf/take-test.py`

**Changes:** Same pattern as Task 1.1

---

### Task 1.5: Update `uml` substrate

**Files to modify:**
- `execution-substratrates/uml/take-test.sh`
- `execution-substratrates/uml/take-test.py`

**Changes:** Same pattern as Task 1.1

---

### Task 1.6: Update `english` substrate (special case)

**Files to modify:**
- `execution-substratrates/english/take-test.sh`
- `execution-substratrates/english/take-test.py`

**Changes:**
1. Update `take-test.sh` with standard multi-entity detection
2. Update `take-test.py`:
   - Remove hardcoded `COMPUTED_COLUMNS` list
   - Read computed columns from `blank-tests/_metadata.json`
   - Add entity loop for multi-entity mode
   - Update `build_prompt()` to be entity-agnostic (use metadata instead of hardcoded field descriptions)
   - Process each entity file separately with its own LLM call

**Additional consideration:** The English substrate uses LLM to "execute" the English specification. For multi-entity support, it needs to:
- Load entity-specific markdown files (if they exist) OR use a generic prompt
- Handle entities that may not have English specifications yet

---

## Phase 2: Remove Legacy Single-Entity Support

### Task 2.1: Update `test-orchestrator.py`

**File:** `orchestration/test-orchestrator.py`

**Changes:**
1. Remove lines 267-272 (legacy `answer-key.json` generation)
2. Remove lines 333-337 (legacy `blank-test.json` generation)
3. Remove `get_substrate_answers()` fallback for old single-file structure (lines 455-476)
4. Simplify `distribute_blank_tests_to_substrate()` - always use multi-entity mode

---

### Task 2.2: Remove legacy files

**Files to delete:**
- `testing/blank-test.json`
- `testing/answer-key.json`

---

### Task 2.3: Simplify all `take-test.sh` scripts

**Files to modify:** All 11 `take-test.sh` files

**Changes:**
- Remove the legacy `else` branch that handles single-file mode
- Always use multi-entity mode (the `if` branch becomes the only path)
- Remove `cp blank-test.json test-answers.json` fallback logic

Example simplified `take-test.sh`:
```bash
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "substrate_name: Processing multi-entity tests..."
mkdir -p "$SCRIPT_DIR/test-answers"
python3 take-test.py --multi-entity

echo "substrate_name: test completed"
```

---

### Task 2.4: Clean up substrate `take-test.py` files

**Files to modify:** All 11 `take-test.py` files

**Changes:**
- Remove `run_legacy()` function
- Remove the `if args.multi_entity: ... else: run_legacy()` branching
- Make multi-entity the default (no flag needed, but keep for compatibility)

---

## Phase 3: Validation

### Task 3.1: Run full test suite

```bash
./start.sh test
```

**Expected results:**
- All 11 substrates should run in multi-entity mode
- All entities should be tested (not just `language_candidates`)
- No references to legacy files in output

### Task 3.2: Verify file cleanup

```bash
# These should NOT exist
ls testing/blank-test.json 2>/dev/null && echo "ERROR: legacy file exists"
ls testing/answer-key.json 2>/dev/null && echo "ERROR: legacy file exists"

# These SHOULD exist
ls testing/blank-tests/*.json
ls testing/answer-keys/*.json
```

### Task 3.3: Verify substrate outputs

```bash
# Each substrate should have test-answers/ directory with per-entity files
for substrate in execution-substratrates/*/; do
    echo "=== $substrate ==="
    ls "$substrate/test-answers/" 2>/dev/null || echo "  (no test-answers yet)"
done
```

---

## Implementation Order

1. **Phase 1** (Tasks 1.1-1.6): Update all 6 substrates - can be done in parallel
2. **Phase 2** (Tasks 2.1-2.4): Remove legacy support - do after Phase 1 is verified working
3. **Phase 3** (Tasks 3.1-3.3): Validate everything works

---

## Shared Helper: Reading Metadata

All substrates should use a common pattern for reading computed columns:

```python
def load_entity_metadata(blank_tests_dir):
    """Load _metadata.json to get computed columns per entity."""
    metadata_path = os.path.join(blank_tests_dir, "_metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            return json.load(f)
    return {}

# Usage in run_multi_entity():
metadata = load_entity_metadata(blank_tests_dir)
for entity, info in metadata.items():
    computed_columns = info.get("computed_columns", [])
    primary_key = info.get("primary_key")
    # ... process entity
```

---

## Estimated Effort

| Phase | Tasks | Effort |
|-------|-------|--------|
| Phase 1.1-1.5 | 5 simple substrates | ~30 min each (copy pattern) |
| Phase 1.6 | English substrate | ~1 hour (LLM logic changes) |
| Phase 2 | Remove legacy | ~30 min |
| Phase 3 | Validation | ~15 min |
| **Total** | | ~4-5 hours |

---

## Rollback Plan

If issues arise:
1. The orchestrator still generates legacy files during Phase 1
2. Substrates still have legacy fallback during Phase 1
3. Full rollback = `git checkout` to pre-Phase-2 commit
