# Article 2: The Airtable Rulebook — Where Truth Lives

The entire system begins in Airtable—a spreadsheet-like interface that non-programmers can understand and edit. This article walks through every table, column, and relationship in the ERB_WikiData rulebook. We examine how language candidates are defined, how evaluation criteria become formula columns, and how the DAG (Directed Acyclic Graph) of calculations is implicitly encoded in cell references. By the end, you'll understand that this "simple spreadsheet" contains everything needed to generate a dozen different implementations.

---

## Detailed Table of Contents

### 1. Why Airtable? (A Controversial Choice)
- **The Case Against Code as Source of Truth**: Developers aren't the only stakeholders
- **The Spreadsheet Lingua Franca**: Everyone understands rows and columns
- **What Airtable Adds**: Types, relationships, formulas, views, and an API
- **The Link**: [Airtable Base appC8XTj95lubn6hz](https://airtable.com/appC8XTj95lubn6hz/shro5WGKLfkfxltQK)
- **The Tradeoff**: Vendor dependency vs. universal accessibility

### 2. The Two Tables in This Rulebook
- **Table: LanguageCandidates** — 125 records, 24 fields (19 raw + 5 calculated)
- **Table: IsEverythingALanguage** — 16 records documenting the philosophical argument
- **Why Two Tables?**: Data (candidates) vs. Metadata (the argument about classification)

### 3. The LanguageCandidates Schema — Raw Fields
Walking through each field that humans edit directly:

| Field | Type | Description |
|-------|------|-------------|
| `LanguageCandidateId` | string (PK) | Unique identifier: `english`, `a-coffee-mug`, `falsifier-a` |
| `Name` | string | Display name: "English", "A Coffee Mug", "Python" |
| `Category` | string | Classification bucket: "Natural Language", "Physical Object", "Running Software", "Formal Language" |
| `ChosenLanguageCandidate` | boolean | Human assertion: "I claim this IS a language" |
| `HasSyntax` | boolean | Does it have explicit grammar rules? |
| `HasIdentity` | boolean | Could it have a globally unique identifier (like a GUID)? |
| `CanBeHeld` | boolean | Is it physical/material? |
| `RequiresParsing` | boolean | Must it be parsed to extract meaning? |
| `ResolvesToAnAST` | boolean | Does parsing produce an abstract syntax tree? |
| `HasLinearDecodingPressure` | boolean | Must it be decoded sequentially? |
| `IsStableOntologyReference` | boolean | Does it provide stable concept references? |
| `IsLiveOntologyEditor` | boolean | Does it allow real-time ontology editing? |
| `IsOpenWorld` | boolean | Open-world assumption? |
| `IsClosedWorld` | boolean | Closed-world assumption? |
| `DistanceFromConcept` | integer | 1 = is the thing itself, 2 = describes the thing |
| `DimensionalityWhileEditing` | string | "OneDimensionalSymbolic", "MultiDimensionalNonSymbolic", "N/A" |
| `ModelObjectFacilityLayer` | string | OMG layer: "M1", "M2", "M4", "NA" |
| `SortOrder` | integer | Display ordering |

### 4. The LanguageCandidates Schema — Calculated Fields
The five fields that are derived from formulas (never edited directly):

#### 4.1 Level 1 Calculations (Depend Only on Raw Fields)
```
FamilyFuedQuestion = "Is " & {{Name}} & " a language?"
```
- Simple string concatenation
- Note: The typo "Fued" is preserved intentionally (source of truth!)

```
HasGrammar = {{HasSyntax}} = TRUE()
```
- Alias/derived boolean

```
IsOpenClosedWorldConflicted = AND({{IsOpenWorld}}, {{IsClosedWorld}})
```
- Logical flag for impossible states

```
IsDescriptionOf = {{DistanceFromConcept}} > 1
```
- Derived from distance field

```
RelationshipToConcept = IF({{DistanceFromConcept}} = 1, "IsMirrorOf", "IsDescriptionOf")
```
- Human-readable version of distance

#### 4.2 Level 2 Calculations (Depend on Level 1)
```
TopFamilyFeudAnswer = AND(
  {{HasSyntax}},
  {{RequiresParsing}},
  {{IsDescriptionOf}},           ← Level 1 dependency
  {{HasLinearDecodingPressure}},
  {{ResolvesToAnAST}},
  {{IsStableOntologyReference}},
  NOT({{CanBeHeld}}),
  NOT({{HasIdentity}})
)
```
- **The core classification formula**: 8 conditions must all be true
- This is the formula that gets compiled to 12 different languages

#### 4.3 Level 3 Calculations (Depend on Level 2)
```
FamilyFeudMismatch = IF(
  NOT({{TopFamilyFeudAnswer}} = {{ChosenLanguageCandidate}}),
  {{Name}} & " " & IF({{TopFamilyFeudAnswer}}, "Is", "Isn't") &
  " a Family Feud Language, but " &
  IF({{ChosenLanguageCandidate}}, "Is", "Is Not") &
  " marked as a 'Language Candidate.'"
) & IF({{IsOpenClosedWorldConflicted}}, " - Open World vs. Closed World Conflict.")
```
- Validation field: catches when computed result doesn't match human assertion
- Also flags logically impossible states (both open AND closed world)

### 5. The DAG in Disguise
- **Why Order Matters**: `TopFamilyFeudAnswer` depends on `IsDescriptionOf`
- **The Implicit Dependency Graph**:
  ```
  Level 0 (Raw)
       ↓
  Level 1: FamilyFuedQuestion, HasGrammar, IsOpenClosedWorldConflicted,
           IsDescriptionOf, RelationshipToConcept
       ↓
  Level 2: TopFamilyFeudAnswer
       ↓
  Level 3: FamilyFeudMismatch
  ```
- **How ERB Extracts This**: Formula parser identifies `{{field}}` references
- **Why This Matters**: Substrates must compute fields in dependency order

### 6. A Tour of the Data — Representative Candidates

#### 6.1 Clear Languages (TopFamilyFeudAnswer = true)
| Name | Category | Why It's a Language |
|------|----------|---------------------|
| English | Natural Language | Has syntax, requires parsing, describes concepts, not physical |
| Python | Formal Language | Programming language with grammar and AST |
| A CSV File | Formal Language | Has syntax (commas, rows), must be parsed |

#### 6.2 Clear Non-Languages (TopFamilyFeudAnswer = false)
| Name | Category | Why It's Not |
|------|----------|--------------|
| A Coffee Mug | Physical Object | No syntax, can be held, has identity, distance=1 |
| A Game of Fortnite | Running Software | No syntax, has identity, distance=1 |
| The Mona Lisa | Physical Object | Can be held, has identity, distance=1 |

#### 6.3 The Falsifiers (Designed to Test the Formula)
| Name | Purpose | Mismatch |
|------|---------|----------|
| Falsifier A | Passes formula, but NOT marked as language | "Is a Family Feud Language, but Is Not marked" |
| Falsifier B | Fails formula, but IS marked as language | "Isn't a Family Feud Language, but Is marked" |
| Falsifier C | Passes formula, IS marked, but has open/closed conflict | " - Open World vs. Closed World Conflict" |

### 7. The IsEverythingALanguage Table — Meta-Level Argument
- **Purpose**: Documents the philosophical argument, not just the data
- **16 Argument Steps**: From motivation through witnesses to conclusion
- **Key Steps**:
  - NEIAL-001: Motivation for formalizing "language"
  - NEIAL-003: Operational definition with predicates
  - NEIAL-004/005: Witnesses (English, Python)
  - NEIAL-008-011: Counterexamples (Chair, Thunderstorm, Coffee Mug, Mona Lisa)
  - NEIAL-016: Final conclusion

### 8. From Airtable to JSON — The Export Process
- **The Transpiler**: `airtabletorulebook` in ssotme.json
- **What Gets Exported**:
  - Schema (field names, types, formulas)
  - Data (all 125 candidate records)
  - Metadata (conversion info, type mappings)
- **The Output**: `effortless-rulebook.json` (canonical hub)

### 9. The Schema-First Principle
- **Type Inference Priority**:
  1. Airtable metadata (checkbox → boolean, number → integer)
  2. Formula analysis (if metadata unavailable)
  3. Data analysis (fallback only)
- **Why This Matters**: Types must be consistent across all 12 substrates
- **Error Handling**: `#NUM!`, `#ERROR!`, `#N/A` → NULL

### 10. Editing the Rulebook — What Happens Next
- **The Promise**: Edit in Airtable, regenerate everywhere
- **The Process**:
  1. Change a field or formula in Airtable
  2. Run `ssotme -build airtabletorulebook`
  3. Run `ssotme -buildall` to regenerate all substrates
  4. Run orchestrator to verify all tests pass
- **Preview of Article 3**: The orchestration layer that makes this work

---

## Key Files Referenced in This Article

| File | Purpose |
|------|---------|
| [effortless-rulebook.json](../../effortless-rulebook/effortless-rulebook.json) | Exported rulebook |
| [ssotme.json](../../ssotme.json) | Transpiler configuration |
| [Airtable Base](https://airtable.com/appC8XTj95lubn6hz/shro5WGKLfkfxltQK) | Live source of truth |

---

*Article content to be written...*
