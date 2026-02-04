# Article 1: The Single Source of Truth Problem

Most software projects suffer from the same disease: business logic scattered across databases, APIs, frontends, documentation, and spreadsheets. When rules change, teams play whack-a-mole updating dozens of files—and inevitably miss some. This article introduces the ERB philosophy: what if you could define your business rules exactly once, in a format humans can read and edit, and have every other representation generated automatically? We examine why this matters, what makes it hard, and preview how ERB solves it through a working example: determining whether something qualifies as a "natural language."

---

## Detailed Table of Contents

### 1. The Familiar Pain
- **The Scenario Everyone Knows**: You rename a field from `isActive` to `is_enabled`
- **The Whack-a-Mole Game**: Database schema, API endpoints, frontend forms, documentation, tests—which did you miss?
- **The Real Cost**: Not the initial change, but the silent drift when one file wasn't updated
- **A Specific Example from This Repo**: The `TopFamilyFeudAnswer` formula exists in 12 places simultaneously

### 2. What "Single Source of Truth" Usually Means (And Why It Fails)
- **The Conventional Wisdom**: "The database is the source of truth"
- **Why That's Insufficient**: The database holds data, not logic—business rules still scatter
- **The Documentation Lie**: README files that say one thing while code does another
- **The ORM Trap**: When your "single model" is actually 3 different representations

### 3. A Thought Experiment: The Ideal System
- **The Impossible Ask**: Define a business rule once, have it execute everywhere
- **The Real Constraint**: Different environments need different syntaxes (SQL vs Python vs Assembly)
- **The Key Insight**: The rule is invariant; the syntax is a projection
- **What Would Have to Be True**: A semantic model that compiles to multiple targets

### 4. Enter the ERB WikiData Example
- **The Question We're Asking**: "Is X a natural language?"
- **Why This Question?**: It requires precise classification logic—perfect for demonstrating the problem
- **The 125 Test Candidates**: From "English" to "A Coffee Mug" to "A Game of Fortnite"
- **The Core Formula** (Preview):
  ```
  TopFamilyFeudAnswer = AND(
    HasSyntax, RequiresParsing, IsDescriptionOf,
    HasLinearDecodingPressure, ResolvesToAnAST,
    IsStableOntologyReference,
    NOT(CanBeHeld), NOT(HasIdentity)
  )
  ```

### 5. The Architecture Overview
- **One Rulebook, Twelve Projections**: What it means in practice
- **The Airtable Origin**: Why spreadsheets as source of truth
- **The JSON Hub**: `effortless-rulebook.json` as canonical intermediate form
- **The Substrate Map**:
  | Substrate | Language | Purpose |
  |-----------|----------|---------|
  | PostgreSQL | SQL | Canonical computation engine |
  | Python | Python | Readable SDK |
  | Go | Golang | Compiled performance |
  | Excel | XLSX | Business user interface |
  | RDF/OWL | Turtle | Semantic web reasoning |
  | GraphQL | SDL+JS | API schema + resolvers |
  | Binary | x86-64 ASM | Native machine code |
  | English | Markdown | Human documentation |
  | ... | ... | ... |

### 6. The Two Empirical Invariants (Preview)
- **Invariant 1: The Rename Test**
  - Rename `HasSyntax` to `HasGrammar` in Airtable
  - Watch it propagate to all 12 substrates automatically
  - No search-and-replace, no manual coordination
- **Invariant 2: Interpreter-Free Semantic Completeness**
  - The rulebook contains complete semantics before any projection
  - OWL, RDF, GraphQL are derived outputs, not authoritative sources
  - Contrast with traditional ontologies that require human interpretation

### 7. What Makes This Hard (The Real Engineering Challenges)
- **Formula Parsing**: Excel-dialect → AST → 12 different target languages
- **Type System Mapping**: Booleans in SQL vs Python vs Go vs Assembly
- **NULL Handling**: Different semantics across environments
- **Testing at Scale**: 125 candidates × 5 computed fields × 12 substrates = 7,500+ assertions

### 8. The Test Results Dashboard (A Preview of What's Possible)
- **Current State**: 96.4% overall pass rate
- **Perfect Substrates**: Python, Go, Excel, GraphQL, OWL, RDF, UML, YAML, CSV (100%)
- **Known Challenges**: Binary (69.6%), English/LLM (90.4%)
- **What the Failures Tell Us**: Where the abstraction leaks

### 9. The Road Ahead
- **Articles 2-4**: The source (Airtable), the orchestration, the formula compiler
- **Articles 5-13**: Deep dives into each execution substrate
- **Articles 14-16**: The English/LLM substrate and testing philosophy
- **Articles 17-20**: Theoretical foundations and implications

### 10. Why This Matters Beyond This Demo
- **The Promise**: Business rules that survive technology changes
- **The Implication**: Non-programmers can edit business logic
- **The Question**: What if your entire system was generated from a spreadsheet?

---

## Key Files Referenced in This Article

| File | Purpose |
|------|---------|
| [effortless-rulebook.json](../../effortless-rulebook/effortless-rulebook.json) | The single source of truth |
| [README.md](../../README.md) | Project overview with invariant definitions |
| [all-tests-results.md](../../orchestration/all-tests-results.md) | Test dashboard showing substrate accuracy |

---

*Article content to be written...*
