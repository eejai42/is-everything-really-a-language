# Implementation Deep Dive

**README.TECHNICAL.md** — The complete technical documentation for developers who want to understand, extend, or contribute to the Effortless Rulebook project.

For a quick overview, see the main [README.md](README.md). For the philosophical foundation, see [README.ARGUMENT.md](README.ARGUMENT.md).

---

## Table of Contents

1. [Independent Execution Substrates](#1-independent-execution-substrates)
2. [Testing Architecture](#2-testing-architecture)
3. [Fuzzy Evaluation Layer](#3-fuzzy-evaluation-layer)
4. [Transpilers](#4-transpilers)
5. [Download Artifacts](#5-download-artifacts)
6. [Known Quirks](#6-known-quirks)

---

## 1. Independent Execution Substrates

Each execution substrate is a fully independent host that consumes the same rulebook and computes results using domain-agnostic, reusable tooling.

No substrate is privileged.
Disagreement is therefore about definitions, not implementations.

> **No execution substrate defines truth; all substrates merely project and compute from the rulebook.**

### For Instance: `top_family_feud_answer` in Three Languages

**PostgreSQL** ([postgres/02-create-functions.sql](postgres/02-create-functions.sql)):
```sql
CREATE OR REPLACE FUNCTION calc_language_candidates_top_family_feud_answer(p_language_candidate_id TEXT)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN (
    COALESCE((SELECT has_syntax FROM language_candidates WHERE language_candidate_id = p_language_candidate_id), FALSE)
    AND NOT COALESCE((SELECT can_be_held FROM language_candidates WHERE language_candidate_id = p_language_candidate_id), FALSE)
    AND COALESCE((SELECT has_linear_decoding_pressure FROM language_candidates WHERE language_candidate_id = p_language_candidate_id), FALSE)
    AND COALESCE((SELECT requires_parsing FROM language_candidates WHERE language_candidate_id = p_language_candidate_id), FALSE)
    AND COALESCE((SELECT stable_ontology_reference FROM language_candidates WHERE language_candidate_id = p_language_candidate_id), FALSE)
    AND NOT COALESCE((SELECT has_identity FROM language_candidates WHERE language_candidate_id = p_language_candidate_id), FALSE)
    AND COALESCE((SELECT distance_from_concept FROM language_candidates WHERE language_candidate_id = p_language_candidate_id) = 2, FALSE)
  )::boolean;
END;
$$ LANGUAGE plpgsql STABLE;
```

**Python** ([execution-substrates/python/erb_sdk.py](execution-substrates/python/erb_sdk.py)):
```python
def calc_top_family_feud_answer(self) -> bool:
    return (
        (self.has_syntax or False)
        and not (self.can_be_held or False)
        and (self.has_linear_decoding_pressure or False)
        and (self.requires_parsing or False)
        and (self.stable_ontology_reference or False)
        and not (self.has_identity or False)
        and self.distance_from_concept == 2
    )
```

**English Specification** ([execution-substrates/english/specification.md](execution-substrates/english/specification.md)):
```
TopFamilyFeudAnswer = AND(
  HasSyntax,
  NOT(CanBeHeld),
  HasLinearDecodingPressure,
  RequiresParsing,
  StableOntologyReference,
  NOT(HasIdentity),
  DistanceFromConcept = 2
)
```

### Substrate Roles in the Three-Phase Contract

All substrates follow the same **three-phase contract**:

1. **Inject** (domain-agnostic): Take the rulebook (schema + formulas) and generate a runnable "substrate" artifact (SDK / schema / workbook / ontology / etc.)
2. **Execute test**: Load `blank-test.json` (raw fields + null computed fields), run the generated rules to compute derived fields, and emit `test-answers.json`
3. **Grade**: Compare that substrate's `test-answers.json` to the canonical `answer-key.json` field-by-field and report mismatches

The *thing that changes per substrate* is: **what "injection" produces**, **how execution computes**, and **what kind of runtime you need**.

| Substrate | Role | Injection Produces (Domain-Agnostic) | Executable? |
|-----------|------|--------------------------------------|:-----------:|
| **PostgreSQL** | Source of truth — canonical computation engine | Tables (1:1 with entities), `calc_*()` functions (1:1 with computed columns), views | ✓ (generates `answer-key.json`) |
| **XLSX** | Spreadsheet runtime for formulas | Worksheets (1:1 with entities), formula columns (1:1 with computed columns) | ✓ |
| **Python** | SDK runtime (dataclass + methods) | `@dataclass` classes (1:1 with entities), `calc_*()` methods (1:1 with computed columns) | ✓ |
| **Go** | Compiled typed runtime (structs + methods) | Go `struct` types (1:1 with entities), `Calc*()` methods (1:1 with computed columns) | ✓ |
| **GraphQL** | Computation via resolvers | Type definitions (1:1 with entities), resolvers (1:1 with computed columns) | ✓ |
| **RDF/Turtle** | Semantic-web schema + rules | Classes/properties (1:1 with entities/fields), optional SPARQL rules | ✓ (with rules engine) / 🔮 Fuzzy |
| **OWL** | Ontology + reasoning | OWL classes (1:1 with entities), optional SWRL rules | ✓ (limited) / 🔮 Fuzzy |
| **YAML** | LLM-friendly schema serialization | Schema definitions (1:1 with entities/fields) | ✓ (requires runner) |
| **CSV** | Tabular schema export | Field definitions (1:1 with entities/fields) | ✓ (requires runner) |
| **UML** | Structural model / diagrams | Class diagrams (1:1 with entities) | 🔮 Fuzzy |
| **DOCX** | Human-readable document export | Document sections (1:1 with entities/formulas) | 🔮 Fuzzy |
| **English** | Human-readable specification | Prose descriptions (1:1 with entities/formulas) | 🔮 Fuzzy |
| **Binary** | Compiled native execution | C structs (1:1 with entities), C functions (1:1 with computed columns) | ✓ |

**Legend**: ✓ = Native execution, 🔮 = LLM Fuzzy Grading (see [Fuzzy Evaluation Layer](#3-fuzzy-evaluation-layer))

### All Execution Substrates

| Layer | Description | Run | README |
|-------|-------------|-----|--------|
| **PostgreSQL** | Source of truth — tables, calc functions, views | [init-db.sh](postgres/init-db.sh) | [README](postgres/README.md) |
| **XLSX** | Excel workbook with native formulas | [run.sh](execution-substrates/xlsx/run.sh) | [README](execution-substrates/xlsx/README.md) |
| **Python** | SDK with dataclasses and calc methods | [run.sh](execution-substrates/python/run.sh) | [README](execution-substrates/python/README.md) |
| **Go** | Structs with calculation methods | [run.sh](execution-substrates/golang/run.sh) | [README](execution-substrates/golang/README.md) |
| **GraphQL** | Schema with resolvers | [run.sh](execution-substrates/graphql/run.sh) | [README](execution-substrates/graphql/README.md) |
| **RDF/Turtle** | Linked data ontology | [run.sh](execution-substrates/rdf/run.sh) | [README](execution-substrates/rdf/README.md) |
| **OWL** | Semantic web ontology | [run.sh](execution-substrates/owl/run.sh) | [README](execution-substrates/owl/README.md) |
| **YAML** | LLM-friendly schema | [run.sh](execution-substrates/yaml/run.sh) | [README](execution-substrates/yaml/README.md) |
| **CSV** | Tabular field definitions | [run.sh](execution-substrates/csv/run.sh) | [README](execution-substrates/csv/README.md) |
| **UML** | Entity relationship diagrams | [run.sh](execution-substrates/uml/run.sh) | [README](execution-substrates/uml/README.md) |
| **DOCX** | Word document export | [run.sh](execution-substrates/docx/run.sh) | [README](execution-substrates/docx/README.md) |
| **English** | Human-readable specification | — | [specification.md](execution-substrates/english/specification.md) |
| **Binary** | Encoded schema representation | [run.sh](execution-substrates/binary/run.sh) | [README](execution-substrates/binary/README.md) |

---

## 2. Testing Architecture

The project includes a comprehensive testing framework that validates each execution substrate produces identical computed results.

### The Key Insight

**Injection code must be 100% domain-agnostic, general-purpose, and reusable.**

The injector script (`inject-into-*.py`) for any substrate:
- **NEVER** contains words like "language", "syntax", "grammar", or any domain concept
- **ONLY** translates generic rulebook structures into target language constructs
- **Generates** entity structures (structs/classes/tables) and computation functions (1:1 with computed columns)

The test runner (`take-test.py`) for any substrate:
- **NEVER** knows what the data represents
- **ONLY** reads JSON → populates structures → calls generated functions → emits JSON

This means **when the rulebook changes** (different domain, different entities, different formulas), the infrastructure "follows along" automatically. The same `inject-into-golang.py` script that generates code for language classification would work identically for inventory management, financial calculations, or any other domain.

### The Three-Phase Testing Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TESTING ARCHITECTURE                                │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────┐
  │   PostgreSQL View   │  ← Source of Truth
  │  (vw_language_...   │    (all computed fields included)
  └──────────┬──────────┘
             │
             ▼
  ┌─────────────────────┐     ┌─────────────────────┐
  │   answer-key.json   │     │   blank-test.json   │
  │  (complete answers) │     │  (nulled computed   │
  └─────────────────────┘     │   columns)          │
             │                └──────────┬──────────┘
             │                           │
             │    ┌──────────────────────┼──────────────────────┐
             │    │                      │                      │
             │    ▼                      ▼                      ▼
             │  ┌─────────┐         ┌─────────┐           ┌─────────┐
             │  │  XLSX   │         │ Python  │    ...    │ Golang  │
             │  │Substrate│         │Substrate│           │Substrate│
             │  └────┬────┘         └────┬────┘           └────┬────┘
             │       │                   │                     │
             │       ▼                   ▼                     ▼
             │  ┌─────────┐         ┌─────────┐           ┌─────────┐
             │  │  test-  │         │  test-  │           │  test-  │
             │  │answers. │         │answers. │           │answers. │
             │  │  json   │         │  json   │           │  json   │
             │  └────┬────┘         └────┬────┘           └────┬────┘
             │       │                   │                     │
             └───────┼───────────────────┼─────────────────────┤
                     │                   │                     │
                     ▼                   ▼                     ▼
              ┌────────────────────────────────────────────────────┐
              │              TEST ORCHESTRATOR                     │
              │         (field-by-field comparison)                │
              │                                                    │
              │   For each substrate:                              │
              │     test-answers.json  vs  answer-key.json         │
              │                    ↓                               │
              │            PASS / FAIL + Score                     │
              └────────────────────────────────────────────────────┘
```

### Phase 1: Substrate Injection (Domain-Agnostic)

Each substrate has an `inject-substrate.sh` that calls `inject-into-*.py`:

```bash
inject-substrate.sh → inject-into-*.py
```

The injection script is **100% domain-agnostic**—it reads the generic `effortless-rulebook.json` and generates the runtime execution substrate/SDK. **The injector knows nothing about "languages", "grammar", "syntax", or any domain concepts.** It simply:

1. **Reads the rulebook schema** — entity names, field names, field types, formula definitions
2. **Generates entity structures** — structs/classes/tables with fields matching the schema
3. **Generates computation functions** — one function per computed column, exactly mirroring the formula DAG

When the rulebook changes (new entities, new fields, new formulas), re-running the injector regenerates the substrate artifacts. The injector never needs modification—it's a generic translator.

| Substrate | Entity Structure | Computed Column Functions |
|-----------|------------------|---------------------------|
| **postgres** | `CREATE TABLE` statements | `calc_entityname_fieldname()` SQL functions |
| **xlsx** | Worksheet rows/columns | Excel formula cells (e.g., `=AND(...)`) |
| **python** | `@dataclass` classes | `calc_fieldname()` methods on the class |
| **golang** | Go `struct` types | `Calc*()` methods on the struct |
| **graphql** | GraphQL type definitions | Resolver functions for computed fields |
| **owl/rdf** | Class/property definitions | SPARQL rules or embedded formula comments |
| **binary** | C struct definitions | C functions for computed fields |

### Example: Go Substrate Injection

The injector reads the rulebook and generates:

```go
// GENERATED: Entity struct (one per rulebook entity)
type LanguageCandidate struct {
    LanguageCandidateID         *string `json:"language_candidate_id"`
    Name                        *string `json:"name"`
    Category                    *string `json:"category"`
    HasSyntax                   *bool   `json:"has_syntax"`
    CanBeHeld                   *bool   `json:"can_be_held"`
    HasLinearDecodingPressure   *bool   `json:"has_linear_decoding_pressure"`
    RequiresParsing             *bool   `json:"requires_parsing"`
    StableOntologyReference     *bool   `json:"stable_ontology_reference"`
    HasIdentity                 *bool   `json:"has_identity"`
    DistanceFromConcept         *int    `json:"distance_from_concept"`
    // ... all raw fields from rulebook
}

// GENERATED: Calc function (one per computed column in rulebook)
func (c *LanguageCandidate) CalcTopFamilyFeudAnswer() bool {
    // Implements the 7-condition formula from the rulebook
}

func (c *LanguageCandidate) CalcIsOpenClosedWorldConflicted() bool {
    // Implements: is_open_world AND is_closed_world
}
```

**Note:** The struct field names (`HasSyntax`, `CanBeHeld`) and method names (`CalcTopFamilyFeudAnswer`) come directly from the rulebook schema. The injector doesn't know these fields relate to linguistics—it just translates whatever entities/fields/formulas the rulebook defines.

### Phase 2: Test Execution (main())

Each substrate has a `take-test.sh` that runs the test:

```bash
take-test.sh → take-test.py (or take-test.go, etc.)
```

The `main()` function is **also domain-agnostic**. It follows a simple pattern:

1. **Read** `blank-test.json` — JSON array of records with raw fields + null computed fields
2. **Populate** structs/objects — unmarshal each JSON record into the generated entity structure
3. **Compute** derived fields — call the generated `Calc*()` functions to fill in nulled computed columns
4. **Emit** `test-answers.json` — marshal the fully-computed records back to JSON

```
┌─────────────────────┐     ┌─────────────────────┐
│   blank-test.json   │     │  Generated SDK      │
│  (raw fields only)  │     │  (structs + funcs)  │
└──────────┬──────────┘     └──────────┬──────────┘
           │                           │
           └───────────┬───────────────┘
                       ▼
              ┌─────────────────┐
              │    main()       │
              │                 │
              │  1. Read JSON   │
              │  2. Populate    │
              │  3. Calc*()     │
              │  4. Emit JSON   │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ test-answers.json│
              │ (all fields)    │
              └─────────────────┘
```

### Example: Go Test Runner

```go
func main() {
    // 1. Read blank test input
    data, _ := os.ReadFile("../../testing/blank-test.json")
    var candidates []LanguageCandidate
    json.Unmarshal(data, &candidates)

    // 2. For each record, compute derived fields using generated Calc functions
    for i := range candidates {
        c := &candidates[i]
        topAnswer := c.CalcTopFamilyFeudAnswer()
        conflicted := c.CalcIsOpenClosedWorldConflicted()
        mismatch := c.CalcFamilyFeudMismatch()
        // ... assign computed values back to struct
    }

    // 3. Emit computed results
    output, _ := json.MarshalIndent(candidates, "", "  ")
    os.WriteFile("test-answers.json", output, 0644)
}
```

**The main() function has no domain knowledge.** It doesn't know what a "language" is or what "syntax" means. It just:
- Loads whatever JSON structure the rulebook defines
- Calls whatever `Calc*()` functions were generated
- Writes the results

When the rulebook changes (new fields, new formulas, new test data), the same `main()` pattern continues to work—only the generated SDK changes.

### Phase 3: Grading

The test orchestrator compares each substrate's `test-answers.json` against the `answer-key.json`:

```
For each computed column:
    expected = answer-key.json[record][column]
    actual   = test-answers.json[record][column]

    if expected == actual: PASS
    else: FAIL
```

### Running the Tests

```bash
# Run full orchestration (all substrates)
cd orchestration
./orchestrate.sh

# Run a single substrate
cd execution-substrates/xlsx
./inject-substrate.sh
```

### Test Artifacts

| File | Location | Purpose |
|------|----------|---------|
| `answer-key.json` | `testing/` | Ground truth from PostgreSQL |
| `blank-test.json` | `testing/` | Test input (nulled computed columns) |
| `test-answers.json` | `execution-substrates/*/` | Substrate's computed answers |
| `test-results.md` | `execution-substrates/*/` | Per-substrate grade report |
| `all-tests-results.md` | `orchestration/` | Summary across all substrates |

### Why This Architecture?

1. **Separation of Concerns**: Injection is purely structural (schema → SDK). Testing is purely functional (compute → compare).

2. **100% Domain Agnosticism**: The injection and test-runner scripts work for ANY rulebook. They contain:
   - **Zero domain-specific words** (no "language", "grammar", "syntax", etc.)
   - **Zero domain-specific logic** (no special cases for this rulebook)
   - **Only generic translation** (rulebook entities → target language constructs)

3. **"Follow Along" Principle**: When the rulebook changes, everything else automatically follows:
   - **New entity?** Injector generates new struct/class/table
   - **New field?** Injector adds it to the entity structure
   - **New formula?** Injector generates new `Calc*()` function
   - **New test data?** Test runner processes it without modification

   The infrastructure never needs domain-specific updates—it just translates whatever the rulebook defines.

4. **Falsifiability**: If a substrate computes a different answer, we know immediately which field failed.

5. **Extensibility**: Adding a new substrate means implementing:
   - `inject-into-*.py` — generic rulebook → SDK translator
   - `take-test.py` — generic JSON → SDK → JSON runner

   No changes to the orchestrator, no domain knowledge required.

---

## 3. Fuzzy Evaluation Layer

Some substrates cannot directly execute computations—they produce **human-readable specifications**, **diagrams**, or **semantic definitions** instead of runnable code. For these substrates, we introduce an **LLM Fuzzy Grading** layer.

### Concept

The fuzzy evaluation layer uses a Large Language Model (LLM) to:

1. **Read** the substrate's specification/output (prose, ontology, diagrams)
2. **Interpret** the instructions to understand the computation logic
3. **Infer** what the computed field values should be for each candidate
4. **Compare** the LLM's inferences against the canonical `answer-key.json`

This tests whether the non-computational substrate **accurately describes** the computation, even though it cannot execute it directly.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FUZZY EVALUATION LAYER                               │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────┐     ┌─────────────────────┐
  │   Substrate Output  │     │   blank-test.json   │
  │  (prose, ontology,  │     │  (raw field values) │
  │   diagrams, etc.)   │     └──────────┬──────────┘
  └──────────┬──────────┘                │
             │                           │
             ▼                           ▼
  ┌────────────────────────────────────────────────────┐
  │                    LLM                              │
  │                                                     │
  │  "Based on this specification, what should the     │
  │   computed values be for this candidate?"           │
  │                                                     │
  └──────────────────────┬─────────────────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────────────┐
  │              test-answers.json                       │
  │            (LLM-inferred values)                     │
  └──────────────────────┬──────────────────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────────────┐
  │              Standard Grading                        │
  │     (compare against answer-key.json)               │
  └─────────────────────────────────────────────────────┘
```

### Why Fuzzy Evaluation?

| Question | Answer |
|----------|--------|
| Why not just skip non-computational substrates? | We want to verify that the specification **accurately describes** the computation—a prose description that leads to wrong answers is a bad specification |
| What does a high score mean? | The specification is clear and precise enough that an LLM can correctly interpret and apply the formulas |
| What does a low score mean? | The specification may be ambiguous, incomplete, or use terminology that differs from the implementation |
| Is this deterministic? | No—LLM outputs can vary. Use low temperature (0.1) for consistency. Multiple runs may yield slightly different scores |

### Substrates Using Fuzzy Evaluation

| Substrate | Why Fuzzy? | What Gets Evaluated |
|-----------|------------|---------------------|
| **English** | Prose cannot execute | Whether the prose clearly describes formulas an LLM can follow |
| **DOCX** | Documents cannot execute | Whether the formatted spec accurately describes the computation |
| **UML** | Diagrams cannot execute | Whether class/method signatures imply correct computation |
| **OWL** | Limited expressivity (no string ops) | Whether the ontology semantics capture the logic |
| **RDF** | Limited without SPARQL | Whether the schema + comments describe correct formulas |

### Running Fuzzy Evaluation

The `llm-fuzzy-grader.py` tool in the orchestration folder handles fuzzy evaluation:

```bash
cd orchestration

# Evaluate a specific substrate
python llm-fuzzy-grader.py english --provider openai --write-answers
python llm-fuzzy-grader.py docx --provider anthropic --write-answers
python llm-fuzzy-grader.py uml --provider ollama --write-answers

# Options:
#   --provider: openai | anthropic | ollama
#   --write-answers: Generate test-answers.json for standard grading
#   --sample N: Only evaluate N records (for testing)
#   --verbose: Show detailed progress
```

### Supported LLM Providers

| Provider | Model | Requires |
|----------|-------|----------|
| `openai` | GPT-4o | `OPENAI_API_KEY` environment variable |
| `anthropic` | Claude Sonnet | `ANTHROPIC_API_KEY` environment variable |
| `ollama` | Llama 3.2 (local) | Ollama running on localhost:11434 |

### Fuzzy Grading Output

Each fuzzy-evaluated substrate receives:

| File | Purpose |
|------|---------|
| `test-answers.json` | LLM-inferred values (integrates with standard grading) |
| `fuzzy-grading-report.md` | Detailed report showing inferences and mismatches |

---

## 4. Transpilers

The build pipeline uses `ssotme` transpilers to generate all execution layers from the single source of truth. Each transpiler reads from `effortless-rulebook.json` and produces a specific output format.

### Source Sync

| Transpiler | Direction | Description |
|------------|-----------|-------------|
| `airtabletorulebook` | Airtable → JSON | Pulls schema + data from Airtable into [effortless-rulebook.json](effortless-rulebook/effortless-rulebook.json) |
| `rulebooktoairtable` | JSON → Airtable | Pushes local changes back to Airtable (disabled by default) |

### Code Generation

| Transpiler | Output | README |
|------------|--------|--------|
| `rulebooktopostgres` | PostgreSQL DDL (tables, functions, views, policies, data) | [postgres/README.md](postgres/README.md) |
| `rulebooktopython` | Python SDK with dataclasses | [execution-substrates/python/README.md](execution-substrates/python/README.md) |
| `rulebooktogolang` | Go structs with calc methods | [execution-substrates/golang/README.md](execution-substrates/golang/README.md) |
| `rulebooktoenglish` | Human-readable specification | [execution-substrates/english/README.md](execution-substrates/english/README.md) |
| `rulebooktographql` | GraphQL schema + resolvers | [execution-substrates/graphql/README.md](execution-substrates/graphql/README.md) |
| `rulebooktordf` | RDF/Turtle linked data | [execution-substrates/rdf/README.md](execution-substrates/rdf/README.md) |
| `rulebooktoowl` | OWL semantic web ontology | [execution-substrates/owl/README.md](execution-substrates/owl/README.md) |
| `rulebooktoyaml` | YAML schema (LLM-friendly) | [execution-substrates/yaml/README.md](execution-substrates/yaml/README.md) |
| `rulebooktocsv` | CSV field definitions | [execution-substrates/csv/README.md](execution-substrates/csv/README.md) |
| `rulebooktouml` | UML entity diagrams | [execution-substrates/uml/README.md](execution-substrates/uml/README.md) |
| `rulebooktodocx` | Word document export | [execution-substrates/docx/README.md](execution-substrates/docx/README.md) |
| `rulebooktobinary` | Binary schema encoding | [execution-substrates/binary/README.md](execution-substrates/binary/README.md) |

### Utility

| Transpiler | Description |
|------------|-------------|
| `init-db` | Runs [postgres/init-db.sh](postgres/init-db.sh) to initialize the database |
| `JsonHbarsTransform` | Generates [README.SCHEMA.md](README.SCHEMA.md) from Handlebars template |

### Running Transpilers

```bash
# Build all transpilers
ssotme -buildall

# Build a specific transpiler
ssotme -build rulebooktopython

# Build with dependencies disabled (faster)
ssotme -build -id
```

See [ssotme.json](ssotme.json) for full configuration.

---

## 5. Download Artifacts

| Artifact | Description |
|----------|-------------|
| [`effortless-rulebook.json`](effortless-rulebook/effortless-rulebook.json) | The canonical rulebook (JSON) — all schema, formulas, and data |
| [`rulebook.xlsx`](execution-substrates/xlsx/rulebook.xlsx) | Excel workbook with live formulas |
| [`language_candidates.csv`](execution-substrates/csv/language_candidates.csv) | Flat CSV of all candidates with computed values |
| [`column_formulas.csv`](execution-substrates/csv/column_formulas.csv) | CSV of all field definitions and formulas |
| [`specification.md`](execution-substrates/english/specification.md) | Human-readable English specification |
| [`glossary.md`](execution-substrates/english/glossary.md) | Glossary of terms and predicates |

---

## 6. Known Quirks

### The "fued" Typo

The field `family_fued_question` contains a typo ("fued" instead of "feud"), while `top_family_feud_answer` uses the correct spelling. This inconsistency originates from the Airtable source of truth and is preserved across all substrates for consistency.

---

## Quick Start Examples

### Run the Python SDK

```bash
cd execution-substrates/python
./run.sh
```

Or directly:
```bash
python erb_sdk.py
```

Output:
```
Loaded 25 language candidates

First candidate: English
  language_candidate_id: english
  name: English
  top_family_feud_answer: True
  family_feud_mismatch: None
  ...
```

### Query the PostgreSQL View

```sql
-- See all candidates with computed classification
SELECT name, category, top_family_feud_answer, family_feud_mismatch
FROM vw_language_candidates
ORDER BY sort_order;

-- Find mismatches between computed and marked
SELECT name, family_feud_mismatch
FROM vw_language_candidates
WHERE family_feud_mismatch IS NOT NULL;
```

---

## Architecture Summary

This project follows the **Effortless Rulebook (ERB)** pattern:

```
Airtable (Source of Truth)
         ↓
effortless-rulebook.json (CMCC format)
         ↓
Code Generation (ssotme transpilers)
         ↓
12+ Execution Layers (all implementing the same logic)
```

For schema details, see [README.SCHEMA.md](README.SCHEMA.md).

---

*Back to [README.md](README.md) | See also [README.ARGUMENT.md](README.ARGUMENT.md)*
