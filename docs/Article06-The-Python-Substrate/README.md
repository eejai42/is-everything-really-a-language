# Article 6: The Python Substrate — Readable, Testable, Shareable

Python serves as the most accessible execution substrate—readable code that matches the formulas almost 1:1. This article walks through the generated `erb_calc.py` module, shows how it implements the calculation DAG, and demonstrates the test harness. We also explore how other substrates (like YAML) can import and reuse Python calculations, proving that substrates can collaborate rather than exist in isolation.

---

## Detailed Table of Contents

### 1. Why Python Is the "Reference" Readable Substrate
- **Human Readability**: Python code maps almost directly to the formulas
- **Zero Compilation**: Edit and run immediately
- **Ecosystem**: Rich testing tools, debuggers, type hints
- **Sharing**: Send a `.py` file to anyone; they can run it
- **Test Time**: 115ms — among the fastest substrates

### 2. The Generated File Structure

```
execution-substrates/python/
├── erb_calc.py          # Generated calculation functions (5.6KB)
├── erb_sdk.py           # Dataclass + methods (reusable SDK)
├── take-test.py         # Test runner
├── take-test.sh         # Shell wrapper
├── inject-into-python.py # Injector script
├── test-answers.json    # Output from test
├── test-results.md      # Grade report
└── README.md            # Documentation
```

### 3. The `erb_calc.py` Module — Pure Functions

#### 3.1 Level 1 Functions
```python
def calc_family_fued_question(name: str) -> str:
    """Calculate family_fued_question from raw fields."""
    return f"Is {name} a language?"

def calc_has_grammar(has_syntax: bool) -> bool:
    """Calculate has_grammar from raw fields."""
    return (has_syntax is True)

def calc_is_description_of(distance_from_concept: int) -> bool:
    """Calculate is_description_of from raw fields."""
    return (distance_from_concept or 0) > 1

def calc_is_open_closed_world_conflicted(
    is_open_world: bool,
    is_closed_world: bool
) -> bool:
    """Calculate is_open_closed_world_conflicted from raw fields."""
    return (is_open_world is True) and (is_closed_world is True)

def calc_relationship_to_concept(distance_from_concept: int) -> str:
    """Calculate relationship_to_concept from raw fields."""
    return "IsMirrorOf" if (distance_from_concept == 1) else "IsDescriptionOf"
```

#### 3.2 Level 2 Functions (Depend on Level 1)
```python
def calc_top_family_feud_answer(
    has_syntax: bool,
    requires_parsing: bool,
    is_description_of: bool,  # ← Level 1 result
    has_linear_decoding_pressure: bool,
    resolves_to_an_ast: bool,
    is_stable_ontology_reference: bool,
    can_be_held: bool,
    has_identity: bool
) -> bool:
    """Calculate top_family_feud_answer (Level 2 - depends on is_description_of)."""
    return (
        (has_syntax is True) and
        (requires_parsing is True) and
        (is_description_of is True) and  # Level 1 dependency
        (has_linear_decoding_pressure is True) and
        (resolves_to_an_ast is True) and
        (is_stable_ontology_reference is True) and
        not (can_be_held is True) and
        not (has_identity is True)
    )
```

#### 3.3 Level 3 Functions (Depend on Level 2)
```python
def calc_family_feud_mismatch(
    name: str,
    top_family_feud_answer: bool,  # ← Level 2 result
    chosen_language_candidate: bool,
    is_open_closed_world_conflicted: bool  # ← Level 1 result
) -> str:
    """Calculate family_feud_mismatch (Level 3)."""
    result = ""
    if top_family_feud_answer != chosen_language_candidate:
        is_word = "Is" if top_family_feud_answer else "Isn't"
        marked_word = "Is" if chosen_language_candidate else "Is Not"
        result = f"{name} {is_word} a Family Feud Language, but {marked_word} marked as a 'Language Candidate.'"
    if is_open_closed_world_conflicted:
        result += " - Open World vs. Closed World Conflict."
    return result if result else ""
```

### 4. The Composite Function — `compute_all_calculated_fields()`

```python
def compute_all_calculated_fields(record: dict) -> dict:
    """Compute all calculated fields in DAG order."""
    result = dict(record)

    # Level 1 (parallel - no dependencies between these)
    result['family_fued_question'] = calc_family_fued_question(
        result.get('name')
    )
    result['has_grammar'] = calc_has_grammar(
        result.get('has_syntax')
    )
    result['is_description_of'] = calc_is_description_of(
        result.get('distance_from_concept')
    )
    result['is_open_closed_world_conflicted'] = calc_is_open_closed_world_conflicted(
        result.get('is_open_world'),
        result.get('is_closed_world')
    )
    result['relationship_to_concept'] = calc_relationship_to_concept(
        result.get('distance_from_concept')
    )

    # Level 2 (depends on Level 1)
    result['top_family_feud_answer'] = calc_top_family_feud_answer(
        result.get('has_syntax'),
        result.get('requires_parsing'),
        result['is_description_of'],  # From Level 1
        result.get('has_linear_decoding_pressure'),
        result.get('resolves_to_an_ast'),
        result.get('is_stable_ontology_reference'),
        result.get('can_be_held'),
        result.get('has_identity')
    )

    # Level 3 (depends on Level 2)
    result['family_feud_mismatch'] = calc_family_feud_mismatch(
        result.get('name'),
        result['top_family_feud_answer'],  # From Level 2
        result.get('chosen_language_candidate'),
        result['is_open_closed_world_conflicted']  # From Level 1
    )

    return result
```

### 5. The `erb_sdk.py` — Object-Oriented Interface

```python
@dataclass
class LanguageCandidate:
    language_candidate_id: str
    name: Optional[str] = None
    category: Optional[str] = None
    has_syntax: Optional[bool] = None
    has_identity: Optional[bool] = None
    can_be_held: Optional[bool] = None
    # ... all 19 raw fields

    def calc_top_family_feud_answer(self) -> bool:
        """Calculate classification using instance fields."""
        return (
            (self.has_syntax is True) and
            (self.requires_parsing is True) and
            (self.calc_is_description_of() is True) and  # Method call
            (self.has_linear_decoding_pressure is True) and
            (self.resolves_to_an_ast is True) and
            (self.is_stable_ontology_reference is True) and
            not (self.can_be_held is True) and
            not (self.has_identity is True)
        )

    def calc_is_description_of(self) -> bool:
        """Calculate is_description_of."""
        return (self.distance_from_concept or 0) > 1
```

### 6. The Test Runner — `take-test.py`

```python
#!/usr/bin/env python3
import json
import sys
sys.path.insert(0, '../../orchestration')
from erb_calc import compute_all_calculated_fields

def main():
    # 1. Load blank test
    with open('../../testing/blank-test.json') as f:
        blank_test = json.load(f)

    # 2. Compute all calculated fields
    results = []
    for record in blank_test:
        computed = compute_all_calculated_fields(record)
        results.append(computed)

    # 3. Write results
    with open('test-answers.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"Computed {len(results)} records")

if __name__ == '__main__':
    main()
```

### 7. The Injection Script — `inject-into-python.py`

The injector is **100% domain-agnostic**:

```python
def inject():
    # 1. Load rulebook
    with open('../../effortless-rulebook/effortless-rulebook.json') as f:
        rulebook = json.load(f)

    # 2. For each table, for each calculated field:
    #    - Parse the formula
    #    - Extract dependencies
    #    - Generate Python function

    # 3. Build compute_all_calculated_fields() with proper DAG order

    # 4. Write erb_calc.py
```

### 8. Formula → Python Translation Examples

| Formula | Python |
|---------|--------|
| `={{HasSyntax}} = TRUE()` | `has_syntax is True` |
| `=NOT({{CanBeHeld}})` | `not (can_be_held is True)` |
| `=AND(A, B)` | `(a is True) and (b is True)` |
| `="Is " & {{Name}} & " a language?"` | `f"Is {name} a language?"` |
| `=IF({{X}} = 1, "A", "B")` | `"A" if x == 1 else "B"` |

### 9. The NULL Handling Strategy

```python
# Pattern: Use `is True` for boolean checks (handles None gracefully)
(has_syntax is True)  # None is True → False

# Pattern: Use `or default` for numeric operations
(distance_from_concept or 0) > 1  # None or 0 → 0 > 1 → False

# Pattern: Use .get() for dict access
result.get('name')  # Missing key → None
```

### 10. Substrate Collaboration — YAML Imports Python

The YAML substrate doesn't implement its own calculations—it imports Python:

```python
# In execution-substrates/yaml/take-test.py:
sys.path.insert(0, '../python')
from erb_calc import compute_all_calculated_fields

# YAML just stores data; Python does the math
```

### 11. Test Results

- **Pass Rate**: 100% (0 failures)
- **Execution Time**: 115ms
- **Records Processed**: 125
- **Fields Tested**: 5 computed columns × 125 records = 625 assertions

### 12. Debugging Tips

```python
# To debug a specific candidate:
record = {'name': 'English', 'has_syntax': True, ...}
result = compute_all_calculated_fields(record)
print(f"is_description_of: {result['is_description_of']}")
print(f"top_family_feud_answer: {result['top_family_feud_answer']}")
```

---

## Key Files Referenced in This Article

| File | Purpose |
|------|---------|
| [erb_calc.py](../../execution-substrates/python/erb_calc.py) | Generated calculation functions |
| [erb_sdk.py](../../execution-substrates/python/erb_sdk.py) | Dataclass-based SDK |
| [take-test.py](../../execution-substrates/python/take-test.py) | Test runner |
| [inject-into-python.py](../../execution-substrates/python/inject-into-python.py) | Code generator |

---

*Article content to be written...*
