# Article 12: Go and Golang — Compiled Performance, Generated Safety

For production systems that need speed, ERB generates Go code. This article examines the generated structs, calculation functions, and test harness. We explore how Go's type system catches errors that dynamic languages miss, and benchmark the performance difference. Special attention to the conditional `main.go` generation that preserves custom code while regenerating business logic.

---

## Detailed Table of Contents

### 1. Why Go?
- **Compiled Performance**: Faster than Python, safer than C
- **Static Types**: Catch errors at compile time
- **Single Binary**: No runtime dependencies
- **Test Time**: 201ms (includes compilation)

### 2. The Generated Files

```
execution-substratrates/golang/
├── erb_sdk.go             # Generated structs + calc methods (10KB)
├── main.go                # Test runner (conditionally generated)
├── erb_test               # Compiled binary (2.98MB)
├── go.mod                 # Go module definition
├── inject-into-golang.py  # Code generator
├── take-test.sh           # Shell wrapper
├── test-answers.json      # Output for grading
└── README.md
```

### 3. The Generated Struct — `erb_sdk.go`

```go
package main

import (
    "encoding/json"
    "os"
)

// LanguageCandidate represents a language classification candidate
type LanguageCandidate struct {
    LanguageCandidateID       *string `json:"language_candidate_id"`
    Name                      *string `json:"name"`
    Category                  *string `json:"category"`
    HasSyntax                 *bool   `json:"has_syntax"`
    HasIdentity               *bool   `json:"has_identity"`
    CanBeHeld                 *bool   `json:"can_be_held"`
    RequiresParsing           *bool   `json:"requires_parsing"`
    ResolvesToAnAST           *bool   `json:"resolves_to_an_ast"`
    HasLinearDecodingPressure *bool   `json:"has_linear_decoding_pressure"`
    IsStableOntologyReference *bool   `json:"is_stable_ontology_reference"`
    IsLiveOntologyEditor      *bool   `json:"is_live_ontology_editor"`
    IsOpenWorld               *bool   `json:"is_open_world"`
    IsClosedWorld             *bool   `json:"is_closed_world"`
    DistanceFromConcept       *int    `json:"distance_from_concept"`
    DimensionalityWhileEditing *string `json:"dimensionality_while_editing"`
    ModelObjectFacilityLayer  *string `json:"model_object_facility_layer"`
    ChosenLanguageCandidate   *bool   `json:"chosen_language_candidate"`
    SortOrder                 *int    `json:"sort_order"`

    // Computed fields (populated by Calc methods)
    FamilyFuedQuestion            *string `json:"family_fued_question"`
    HasGrammar                    *bool   `json:"has_grammar"`
    IsDescriptionOf               *bool   `json:"is_description_of"`
    IsOpenClosedWorldConflicted   *bool   `json:"is_open_closed_world_conflicted"`
    RelationshipToConcept         *string `json:"relationship_to_concept"`
    TopFamilyFeudAnswer           *bool   `json:"top_family_feud_answer"`
    FamilyFeudMismatch            *string `json:"family_feud_mismatch"`
}
```

### 4. Pointer Types for NULL Handling

Go uses pointer types to represent nullable values:

| Type | Meaning |
|------|---------|
| `*bool` | Boolean that can be `nil` (NULL) |
| `*string` | String that can be `nil` |
| `*int` | Integer that can be `nil` |

```go
// Safe boolean check with nil handling
func boolValue(b *bool) bool {
    if b == nil {
        return false
    }
    return *b
}
```

### 5. The Calculation Methods

#### 5.1 Level 1 Methods
```go
// CalcFamilyFuedQuestion calculates the family feud question
func (c *LanguageCandidate) CalcFamilyFuedQuestion() *string {
    if c.Name == nil {
        return nil
    }
    result := "Is " + *c.Name + " a language?"
    return &result
}

// CalcHasGrammar calculates has_grammar from has_syntax
func (c *LanguageCandidate) CalcHasGrammar() *bool {
    result := boolValue(c.HasSyntax)
    return &result
}

// CalcIsDescriptionOf calculates is_description_of from distance_from_concept
func (c *LanguageCandidate) CalcIsDescriptionOf() *bool {
    if c.DistanceFromConcept == nil {
        result := false
        return &result
    }
    result := *c.DistanceFromConcept > 1
    return &result
}

// CalcIsOpenClosedWorldConflicted checks for logical conflict
func (c *LanguageCandidate) CalcIsOpenClosedWorldConflicted() *bool {
    result := boolValue(c.IsOpenWorld) && boolValue(c.IsClosedWorld)
    return &result
}

// CalcRelationshipToConcept derives relationship from distance
func (c *LanguageCandidate) CalcRelationshipToConcept() *string {
    var result string
    if c.DistanceFromConcept != nil && *c.DistanceFromConcept == 1 {
        result = "IsMirrorOf"
    } else {
        result = "IsDescriptionOf"
    }
    return &result
}
```

#### 5.2 Level 2 Methods
```go
// CalcTopFamilyFeudAnswer implements the 8-condition AND formula
func (c *LanguageCandidate) CalcTopFamilyFeudAnswer() *bool {
    // Compute Level 1 dependency
    isDescriptionOf := boolValue(c.CalcIsDescriptionOf())

    result := boolValue(c.HasSyntax) &&
        boolValue(c.RequiresParsing) &&
        isDescriptionOf &&
        boolValue(c.HasLinearDecodingPressure) &&
        boolValue(c.ResolvesToAnAST) &&
        boolValue(c.IsStableOntologyReference) &&
        !boolValue(c.CanBeHeld) &&
        !boolValue(c.HasIdentity)

    return &result
}
```

#### 5.3 Level 3 Methods
```go
// CalcFamilyFeudMismatch reports discrepancies
func (c *LanguageCandidate) CalcFamilyFeudMismatch() *string {
    topAnswer := boolValue(c.CalcTopFamilyFeudAnswer())
    chosen := boolValue(c.ChosenLanguageCandidate)
    conflicted := boolValue(c.CalcIsOpenClosedWorldConflicted())

    var result string
    if topAnswer != chosen {
        isWord := "Isn't"
        if topAnswer {
            isWord = "Is"
        }
        markedWord := "Is Not"
        if chosen {
            markedWord = "Is"
        }
        name := ""
        if c.Name != nil {
            name = *c.Name
        }
        result = name + " " + isWord + " a Family Feud Language, but " +
                 markedWord + " marked as a 'Language Candidate.'"
    }
    if conflicted {
        result += " - Open World vs. Closed World Conflict."
    }
    if result == "" {
        return nil
    }
    return &result
}
```

### 6. The Composite Method

```go
// ComputeAllCalculatedFields computes all calculated fields in DAG order
func (c *LanguageCandidate) ComputeAllCalculatedFields() {
    // Level 1 (can run in parallel)
    c.FamilyFuedQuestion = c.CalcFamilyFuedQuestion()
    c.HasGrammar = c.CalcHasGrammar()
    c.IsDescriptionOf = c.CalcIsDescriptionOf()
    c.IsOpenClosedWorldConflicted = c.CalcIsOpenClosedWorldConflicted()
    c.RelationshipToConcept = c.CalcRelationshipToConcept()

    // Level 2 (depends on Level 1)
    c.TopFamilyFeudAnswer = c.CalcTopFamilyFeudAnswer()

    // Level 3 (depends on Level 2)
    c.FamilyFeudMismatch = c.CalcFamilyFeudMismatch()
}
```

### 7. The Test Runner — `main.go`

```go
package main

import (
    "encoding/json"
    "fmt"
    "os"
)

func main() {
    // 1. Read blank test
    data, err := os.ReadFile("../../testing/blank-test.json")
    if err != nil {
        fmt.Println("Error reading blank-test.json:", err)
        os.Exit(1)
    }

    // 2. Parse JSON
    var candidates []LanguageCandidate
    if err := json.Unmarshal(data, &candidates); err != nil {
        fmt.Println("Error parsing JSON:", err)
        os.Exit(1)
    }

    // 3. Compute all calculated fields
    for i := range candidates {
        candidates[i].ComputeAllCalculatedFields()
    }

    // 4. Write results
    output, err := json.MarshalIndent(candidates, "", "  ")
    if err != nil {
        fmt.Println("Error marshaling JSON:", err)
        os.Exit(1)
    }

    if err := os.WriteFile("test-answers.json", output, 0644); err != nil {
        fmt.Println("Error writing test-answers.json:", err)
        os.Exit(1)
    }

    fmt.Printf("Computed %d records\n", len(candidates))
}
```

### 8. The Conditional `main.go` Generation

The injector preserves existing `main.go` if it exists:

```python
def inject_into_golang():
    # Always regenerate erb_sdk.go
    write_file('erb_sdk.go', generate_sdk())

    # Only generate main.go if it doesn't exist
    if not os.path.exists('main.go'):
        write_file('main.go', generate_main())
    else:
        print("main.go exists, preserving custom code")
```

This allows developers to:
- Add custom functions to `main.go`
- Modify the test runner
- Re-run injection without losing changes

### 9. Building and Running

```bash
# Build
go build -o erb_test

# Run
./erb_test
# Output: Computed 125 records

# Or in one step:
go run . > test-answers.json
```

### 10. Test Results

- **Pass Rate**: 100% (0 failures)
- **Execution Time**: 201ms (includes go build)
- **Binary Size**: 2.98MB (includes runtime)

### 11. Go's Type System Advantages

| Python | Go |
|--------|-----|
| `has_syntax = True` | `HasSyntax: &trueVal` |
| Runtime type errors | Compile-time type checks |
| `None` confusion | Explicit `*bool` vs `bool` |
| Duck typing | Structural interfaces |

### 12. Formula → Go Translation

| Formula | Go Code |
|---------|---------|
| `={{HasSyntax}} = TRUE()` | `boolValue(c.HasSyntax)` |
| `=NOT({{CanBeHeld}})` | `!boolValue(c.CanBeHeld)` |
| `=AND(A, B)` | `a && b` |
| `="Is " & {{Name}} & "..."` | `"Is " + *c.Name + "..."` |
| `=IF(X = 1, "A", "B")` | `if x == 1 { "A" } else { "B" }` |

### 13. Performance Comparison

| Substrate | Execution Time | Notes |
|-----------|----------------|-------|
| Python | 115ms | Interpreted |
| Go | 201ms | Includes compilation |
| Go (pre-built) | ~50ms | Binary only |

---

## Key Files Referenced in This Article

| File | Purpose |
|------|---------|
| [erb_sdk.go](../../execution-substratrates/golang/erb_sdk.go) | Generated structs + methods |
| [main.go](../../execution-substratrates/golang/main.go) | Test runner |
| [inject-into-golang.py](../../execution-substratrates/golang/inject-into-golang.py) | Generator |

---

*Article content to be written...*
