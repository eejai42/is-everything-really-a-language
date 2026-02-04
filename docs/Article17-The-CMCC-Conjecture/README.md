# Article 17: The CMCC Conjecture

The CMCC (Conditions, Mutability, Calculations, and Constraints) Conjecture proposes a fundamental classification of all business logic into four orthogonal categories. This article explores the theoretical foundations of CMCC, how it maps to the ERB architecture, and why separating these concerns enables the multi-substrate projection that powers this system. We examine how each category manifests differently across execution environments—from spreadsheet formulas to SQL constraints to SHACL shapes—while preserving semantic equivalence.

---

## Detailed Table of Contents

### 1. The CMCC Conjecture Statement

> **All business logic can be classified into four orthogonal categories:**
> - **C**onditions (predicates about current state)
> - **M**utability (which fields can change and how)
> - **C**alculations (derived values from other fields)
> - **C**onstraints (rules that must hold true)

### 2. Why Four Categories?

| Category | Question Answered | Example |
|----------|-------------------|---------|
| **Conditions** | What is true right now? | `HasSyntax = true` |
| **Mutability** | What can change? | `Name` is editable, `LanguageCandidateId` is not |
| **Calculations** | What values are derived? | `TopFamilyFeudAnswer = AND(...)` |
| **Constraints** | What must always hold? | `DistanceFromConcept >= 1` |

### 3. Conditions — State Predicates

Conditions are facts about the current state:

```json
{
  "has_syntax": true,
  "requires_parsing": true,
  "distance_from_concept": 2,
  "chosen_language_candidate": true
}
```

**In ERB WikiData**:
- 19 raw fields in `LanguageCandidates` table
- Each represents a current truth about a candidate
- No derivation logic—pure observation

**Manifestation Across Substrates**:
| Substrate | Representation |
|-----------|----------------|
| PostgreSQL | Table columns |
| Python | Dataclass fields |
| Go | Struct fields |
| OWL | Data properties |
| RDF | Triples |

### 4. Mutability — Change Control

Mutability defines which fields can be edited:

| Field | Mutable? | Notes |
|-------|----------|-------|
| `language_candidate_id` | No | Primary key |
| `name` | Yes | Can be renamed |
| `has_syntax` | Yes | Can change classification |
| `top_family_feud_answer` | No | Calculated, not editable |

**In ERB**:
- Raw fields → Mutable (edited in Airtable)
- Calculated fields → Immutable (derived from formulas)

**Manifestation Across Substrates**:
| Substrate | Mutable | Immutable |
|-----------|---------|-----------|
| PostgreSQL | Base table | View columns |
| Airtable | Input columns | Formula columns |
| Excel | Data cells | Formula cells |

### 5. Calculations — Derived Values

Calculations produce new values from existing ones:

```
Level 0 (Raw):        has_syntax, distance_from_concept, ...
    ↓
Level 1 (Derived):    is_description_of = distance > 1
    ↓
Level 2 (Derived):    top_family_feud_answer = AND(has_syntax, is_description_of, ...)
    ↓
Level 3 (Derived):    family_feud_mismatch = IF(top_answer != chosen, ...)
```

**The ERB Approach**:
- Formulas defined in Excel-dialect syntax
- Parsed to AST, compiled to 12 different languages
- DAG ensures correct evaluation order

**Manifestation Across Substrates**:
| Substrate | Calculation Mechanism |
|-----------|----------------------|
| PostgreSQL | `calc_*()` functions |
| Python | `calc_*()` methods |
| Excel | `=AND(...)` formulas |
| SPARQL | CONSTRUCT queries |
| OWL | SHACL-SPARQL rules |

### 6. Constraints — Validation Rules

Constraints define what must always be true:

```
∀ candidate:
    distance_from_concept ∈ {1, 2}
    NOT(is_open_world AND is_closed_world) OR is_flagged
    has_grammar → has_syntax
```

**In ERB WikiData**:
- `IsOpenClosedWorldConflicted` flags impossible states
- `FamilyFeudMismatch` catches formula/human disagreement
- Schema types enforce data validity

**Manifestation Across Substrates**:
| Substrate | Constraint Mechanism |
|-----------|---------------------|
| PostgreSQL | CHECK constraints, RLS policies |
| OWL | OWL axioms |
| SHACL | sh:NodeShape constraints |
| GraphQL | Type system (non-null, enums) |

### 7. The Orthogonality Claim

**Orthogonal** means: each category is independent.

- You can have conditions without calculations
- You can have calculations without constraints
- You can have constraints without mutability rules

**Why This Matters**:
- Separating concerns enables independent projection
- Each substrate implements all four categories differently
- The *semantics* remain identical across substrates

### 8. Mapping CMCC to ERB Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AIRTABLE RULEBOOK                         │
│                                                              │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐ │
│  │ Conditions│  │ Mutability│  │ Calcul-   │  │Constraints│ │
│  │  (Fields) │  │  (Config) │  │ ations    │  │  (Logic)  │ │
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘ │
└────────┼──────────────┼──────────────┼──────────────┼───────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────┐
│                effortless-rulebook.json                      │
│   {                                                          │
│     "schema": [                                              │
│       { "name": "HasSyntax", "type": "raw" },     // C      │
│       { "name": "TopFamilyFeudAnswer",                       │
│         "type": "calculated",                                │
│         "formula": "=AND(...)" }                  // C      │
│     ],                                                       │
│     "data": [...]                                            │
│   }                                                          │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│              12 EXECUTION SUBSTRATES                         │
│  Each implements all four CMCC categories differently        │
└─────────────────────────────────────────────────────────────┘
```

### 9. The Schema Field Types

The rulebook schema distinguishes:

```json
{
  "name": "HasSyntax",
  "datatype": "boolean",
  "type": "raw",         // ← Condition (editable)
  "nullable": true
},
{
  "name": "TopFamilyFeudAnswer",
  "datatype": "boolean",
  "type": "calculated",  // ← Calculation (derived)
  "nullable": true,
  "formula": "=AND(...)"
}
```

### 10. Why CMCC Enables Multi-Substrate Projection

Without CMCC separation:
- Logic mixed with data
- Constraints embedded in code
- Calculations scattered across layers

With CMCC separation:
- Clear mapping to any target
- PostgreSQL: conditions → columns, calculations → functions
- Excel: conditions → cells, calculations → formulas
- OWL: conditions → properties, calculations → rules

### 11. The Theoretical Foundation

CMCC relates to established concepts:

| CMCC | Related Concept |
|------|-----------------|
| Conditions | Relational database state |
| Mutability | CQRS write model |
| Calculations | Functional derivations |
| Constraints | Formal verification, contracts |

### 12. Open Questions

- Is CMCC *complete*? (Are there business logic types outside CMCC?)
- Is CMCC *minimal*? (Could we reduce to fewer categories?)
- What is the relationship between calculations and constraints?

---

## Key Files Referenced in This Article

| File | Purpose |
|------|---------|
| [effortless-rulebook.json](../../effortless-rulebook/effortless-rulebook.json) | Schema with type annotations |
| [README.md](../../README.md) | Architecture overview |

---

*Article content to be written...*
