# Go SDK - Language Candidates Rulebook

Go implementation of the ERB calculation functions as a compiled, typed SDK.

## Role in Three-Phase Contract

Go serves as a **compiled typed runtime** — struct types with `Calc*()` methods that compute derived fields in-memory with compile-time type safety.

### Phase 1: Inject

Generate Go structs + `Calc*()` methods mirroring the formula DAG:

| Component | Purpose |
|-----------|---------|
| Entity structs | Go structs with JSON tags for each entity type |
| `Calc*()` methods | Methods implementing each derived field formula |
| Pointer receivers | Methods that can access/modify struct state |

The injection script reads `effortless-rulebook.json` and generates Go code that mirrors the PostgreSQL calc functions.

### Phase 2: Execute

1. Read `blank-test.json` into structs
2. For each record:
   - Unmarshal JSON into struct with raw fields
   - Compute derived fields (call Calc methods)
3. Marshal structs back to JSON

```bash
./take-test.sh  # Compiles, loads blank-test.json, computes, writes results
```

### Phase 3: Emit

Write computed values to `test-answers.json`:

| Output | Content |
|--------|---------|
| `test-answers.json` | All raw fields + Go-computed values |

### Grade

Compare `test-answers.json` against `answer-key.json` field-by-field to verify SDK correctness.

## Technology

**Go (Golang)** is Google's statically-typed, compiled language designed for simplicity, concurrency, and fast compilation. Its struct-based type system and method receivers make it well-suited for implementing ERB's entity/calculation pattern.

Key characteristics:
- **Structs with methods**: Go uses struct types with attached methods rather than classes
- **Pointer receivers**: Methods can modify struct state via pointer receivers (`func (c *Candidate) Calc...`)
- **JSON marshaling**: Built-in `encoding/json` with struct tags for field mapping
- **No inheritance**: Composition over inheritance; interfaces for polymorphism

The Go SDK mirrors the PostgreSQL calc functions as methods on entity structs, enabling the same DAG of calculations to run in-memory without a database.

## Files

| File | Description |
|------|-------------|
| `erb_sdk.go` | Entity structs with calc methods mirroring PostgreSQL |
| `main.go` | Demo application |
| `inject-substrate.sh` | Generates the SDK from rulebook |
| `take-test.sh` | Runs the test (compile, load data, compute, extract) |
| `test-answers.json` | Computed results for grading |

## Usage

```go
import erb "execution-substratrates/golang"

// Load from rulebook
rulebook, err := erb.LoadFromRulebook("../../effortless-rulebook/effortless-rulebook.json")

// Use calculated fields (DAG-aware)
for _, c := range rulebook.LanguageCandidates.Data {
    view := c.ToView()
    fmt.Printf("%s: is_language=%v\n", *view.Name, view.IsAFamilyFeudTopAnswer)
}

// Or use individual calc methods
candidate := rulebook.LanguageCandidates.Data[0]
fmt.Println(candidate.CalcCategoryContainsLanguage())
fmt.Println(candidate.CalcIsAFamilyFeudTopAnswer())
fmt.Println(candidate.CalcFamilyFeudMismatch())
```

## DAG Execution Order

```
Level 0: Raw fields (from rulebook)
Level 1: CategoryContainsLanguage, HasGrammar, RelationshipToConcept, FamilyFuedQuestion
Level 2: IsAFamilyFeudTopAnswer (depends on CategoryContainsLanguage)
Level 3: FamilyFeudMismatch (depends on IsAFamilyFeudTopAnswer)
```

## Calc Method Examples

```go
func (c *LanguageCandidate) CalcCategoryContainsLanguage() bool {
    if c.Category == nil {
        return false
    }
    return strings.Contains(strings.ToLower(*c.Category), "language")
}

func (c *LanguageCandidate) CalcIsAFamilyFeudTopAnswer() bool {
    categoryContainsLanguage := c.CalcCategoryContainsLanguage()
    return categoryContainsLanguage &&
        boolOrFalse(c.HasSyntax) &&
        !boolOrFalse(c.CanBeHeld) &&
        boolOrFalse(c.MeaningIsSerialized) &&
        boolOrFalse(c.RequiresParsing) &&
        boolOrFalse(c.IsOngologyDescriptor) &&
        !boolOrFalse(c.HasIdentity) &&
        intOrZero(c.DistanceFromConcept) == 2
}
```

## Source

Mirrors: `postgres/02-create-functions.sql`
Generated from: `effortless-rulebook/effortless-rulebook.json`
