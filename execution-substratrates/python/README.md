# Python SDK - Language Candidates Rulebook

Python implementation of the ERB calculation functions as an in-memory SDK.

## Role in Three-Phase Contract

Python serves as a **SDK runtime** — dataclass objects with `calc_*` methods that compute derived fields in-memory without a database.

### Phase 1: Inject

Generate `erb_sdk.py` with:

| Component | Purpose |
|-----------|---------|
| Model classes | Dataclasses for each entity type |
| `calc_*` methods | Methods implementing each derived field formula |
| Dependency ordering | Lazy evaluation or explicit DAG-safe call order |

The injection script reads `effortless-rulebook.json` and generates Python code that mirrors the PostgreSQL calc functions.

### Phase 2: Execute

1. Read `blank-test.json`
2. For each record:
   - Instantiate object with raw fields
   - Compute derived fields (call calc methods)
   - Materialize complete record dict

```bash
./take-test.sh  # Loads blank-test.json, computes via SDK, writes results
```

### Phase 3: Emit

Write computed values to `test-answers.json`:

| Output | Content |
|--------|---------|
| `test-answers.json` | All raw fields + SDK-computed values |

### Grade

Compare `test-answers.json` against `answer-key.json` field-by-field to verify SDK correctness.

## Technology

**Python** is a dynamically-typed, interpreted language known for readability and extensive libraries. Its class system with `@property` decorators and dataclasses makes it natural for implementing ERB's entity/calculation pattern.

Key characteristics:
- **Classes with methods**: Python classes group data and behavior; `self` provides instance access
- **Dynamic typing**: No compile-time type checking, but type hints available for documentation
- **JSON support**: Built-in `json` module for loading/dumping rulebook data
- **Dataclasses**: `@dataclass` decorator auto-generates `__init__`, `__repr__`, etc.

The Python SDK mirrors the PostgreSQL calc functions as class methods, enabling the same DAG of calculations to run in-memory without a database. Useful for data analysis, scripting, and rapid prototyping.

## Files

| File | Description |
|------|-------------|
| `erb_sdk.py` | Entity classes with calc functions mirroring PostgreSQL |
| `inject-substrate.sh` | Generates the SDK from rulebook |
| `take-test.sh` | Runs the test (load data, compute, extract) |
| `test-answers.json` | Computed results for grading |

## Usage

```python
from erb_sdk import LanguageCandidate, load_from_rulebook, is_language

# Load from rulebook
candidates, arguments = load_from_rulebook("../../effortless-rulebook/effortless-rulebook.json")

# Use calculated fields (DAG-aware)
for c in candidates:
    view = c.to_view()  # All raw + calculated fields
    print(f"{view['name']}: is_language={view['is_a_family_feud_top_answer']}")

# Or use individual calc methods
candidate = candidates[0]
print(candidate.calc_category_contains_language())
print(candidate.calc_is_a_family_feud_top_answer())
print(candidate.calc_family_feud_mismatch())
```

## DAG Execution Order

```
Level 0: Raw fields (from rulebook)
Level 1: category_contains_language, has_grammar, relationship_to_concept, family_fued_question
Level 2: is_a_family_feud_top_answer (depends on category_contains_language)
Level 3: family_feud_mismatch (depends on is_a_family_feud_top_answer)
```

## Calc Method Examples

```python
def calc_category_contains_language(self) -> bool:
    """Level 1: Check if category contains 'language'"""
    if self.category is None:
        return False
    return "language" in self.category.lower()

def calc_is_a_family_feud_top_answer(self) -> bool:
    """Level 2: The full language classification formula"""
    category_contains_language = self.calc_category_contains_language()
    return (
        category_contains_language
        and (self.has_syntax or False)
        and not (self.can_be_held or False)
        and (self.meaning_is_serialized or False)
        and (self.requires_parsing or False)
        and (self.is_ongology_descriptor or False)
        and not (self.has_identity or False)
        and self.distance_from_concept == 2
    )
```

## Source

Mirrors: `postgres/02-create-functions.sql`
Generated from: `effortless-rulebook/effortless-rulebook.json`
