# Article 15: The Invariant System — Empirically Testable Claims

ERB makes two bold operational claims: (1) rename an entity once in Airtable, and the change propagates deterministically to all 12 substrates; (2) the rulebook is semantically complete before any projection—no human interpretation needed. This article demonstrates both invariants with concrete examples, explains why they matter for system reliability, and shows how to verify them yourself.

---

## Detailed Table of Contents

### 1. What Is an Invariant?
- **Definition**: A property that remains true regardless of system state
- **Software Invariants**: Properties that hold across all operations
- **ERB's Claim**: Two fundamental invariants define the architecture
- **Why It Matters**: Invariants enable confident refactoring

### 2. Invariant 1: Ontology Mutation (The Rename Test)

> A system has a **single source of ontological truth** if and only if an entity can be renamed **once** and that rename propagates deterministically across **all substrates** without search, heuristics, or manual coordination.

#### 2.1 The Test
1. Open Airtable, rename `HasSyntax` to `HasGrammarRules`
2. Run `ssotme -buildall`
3. Verify all substrates updated correctly

#### 2.2 What Gets Changed (Automatically)

| Substrate | Before | After |
|-----------|--------|-------|
| **PostgreSQL** | `has_syntax BOOLEAN` | `has_grammar_rules BOOLEAN` |
| **PostgreSQL** | `calc_*_has_syntax()` | `calc_*_has_grammar_rules()` |
| **Python** | `self.has_syntax` | `self.has_grammar_rules` |
| **Go** | `HasSyntax *bool` | `HasGrammarRules *bool` |
| **Excel** | Column header "has_syntax" | Column header "has_grammar_rules" |
| **GraphQL** | `has_syntax: Boolean` | `has_grammar_rules: Boolean` |
| **OWL** | `erb:hasSyntax` | `erb:hasGrammarRules` |
| **RDF** | `erb:hasSyntax` | `erb:hasGrammarRules` |
| **SPARQL** | `?s erb:hasSyntax ?val` | `?s erb:hasGrammarRules ?val` |
| **Assembly** | `OFFSET_HAS_SYNTAX` | `OFFSET_HAS_GRAMMAR_RULES` |
| **English** | "HasSyntax predicate" | "HasGrammarRules predicate" |
| **UML/OCL** | `self.has_syntax` | `self.has_grammar_rules` |

#### 2.3 What This Proves
- **No Search-and-Replace**: The build system knows the ontology
- **No Manual Coordination**: One edit, twelve consistent outputs
- **Deterministic**: Same input always produces same output

#### 2.4 The Negative Test
In traditional systems:
1. Rename field in database → application breaks
2. Search-replace in codebase → miss some files
3. Documentation → forgotten, now inconsistent
4. Tests → hardcoded old name

### 3. Invariant 2: Interpreter-Free Semantic Completeness

> The rulebook is **semantically complete prior to projection**. No human or algorithmic interpreter is required to "reconnect" the model to its reasoning.

#### 3.1 Traditional Ontology Workflow
```
OWL Ontology
    ↓
+ Natural language annotations
    ↓
+ Human interpretation
    ↓
= Executable constraints
```

The semantics are **reconstructed downstream**.

#### 3.2 ERB Workflow
```
Rulebook (formulas + data + schema)
    ↓
Projection to OWL/RDF/SQL/Python/Go/...
```

The semantics are **complete before projection**.

#### 3.3 Concrete Example

Traditional OWL:
```turtle
erb:TopFamilyFeudAnswer a owl:DatatypeProperty ;
    rdfs:comment "Determines if candidate is a language. See NEIAL-003 for definition." .
```
**Problem**: The comment is not executable. A human must read it.

ERB-generated OWL:
```turtle
erb:TopFamilyFeudAnswer a owl:DatatypeProperty ;
    rdfs:comment "Computed via SHACL rule" .

# The actual computation is in rules.shacl.ttl:
erb:TopFamilyFeudAnswerRule a sh:SPARQLRule ;
    sh:construct """
        CONSTRUCT { $this erb:topFamilyFeudAnswer ?result }
        WHERE { ... full formula ... }
    """ .
```
**Solution**: The rule is executable. No interpretation needed.

### 4. Why These Invariants Matter

| Problem | How Invariants Help |
|---------|---------------------|
| **Inconsistent renaming** | Invariant 1: Single-point rename |
| **Documentation drift** | Invariant 1: Docs generated from source |
| **Semantic ambiguity** | Invariant 2: Formulas are executable |
| **Reconstruction errors** | Invariant 2: No reconstruction needed |
| **Multi-team coordination** | Both: One source of truth |

### 5. Verifying Invariant 1 Yourself

```bash
# 1. Make a change in Airtable (or edit effortless-rulebook.json directly)
# Example: Rename "HasSyntax" to "HasGrammarRules"

# 2. Regenerate all substrates
ssotme -buildall

# 3. Verify the change propagated
grep -r "has_syntax" postgres/          # Should find nothing
grep -r "has_grammar_rules" postgres/   # Should find the new name

grep -r "HasSyntax" execution-substrates/golang/  # Nothing
grep -r "HasGrammarRules" execution-substrates/golang/  # Found

# 4. Run tests to verify semantic equivalence
cd orchestration
./orchestrate.sh
# All tests should still pass (assuming formula logic unchanged)
```

### 6. Verifying Invariant 2 Yourself

```bash
# 1. Look at a generated OWL file
cat execution-substrates/owl/rules.shacl.ttl | grep "CONSTRUCT"
# Should see full formula, not a comment reference

# 2. Check that Python has the actual logic
cat execution-substrates/python/erb_calc.py | grep "def calc_"
# Should see complete function implementations

# 3. Verify no external interpretation needed
# Try running a substrate without reading any documentation:
cd execution-substrates/python
python take-test.py
# It should just work - no human in the loop
```

### 7. The Architectural Consequences

#### 7.1 Renaming Is Safe
Because Invariant 1 holds, refactoring is low-risk:
- Rename any field, table, or formula
- Regenerate, run tests, deploy
- No hidden breakage

#### 7.2 Semantics Are Preserved
Because Invariant 2 holds, substrate choice is free:
- OWL has the same semantics as Python
- GraphQL has the same semantics as Go
- Choose based on deployment needs, not semantic fidelity

### 8. Counter-Examples: Systems Without These Invariants

#### 8.1 Without Invariant 1 (No Single Ontology)
- Rename in database → App crashes
- Search-replace in code → Miss ORM mappings
- API docs → Now show wrong field name
- Client SDKs → Need manual update

#### 8.2 Without Invariant 2 (Incomplete Semantics)
- OWL says "see implementation guide"
- Implementation guide references "original requirements doc"
- Requirements doc references "stakeholder meeting notes"
- Actual behavior: whatever the developer guessed

### 9. The Formal Statement

**Invariant 1** (Ontology Mutation):
```
∀ rename R in source S:
    apply(R, S) → ∀ substrate T: apply(project(S, T), R) = project(apply(R, S), T)
```
Renaming commutes with projection.

**Invariant 2** (Semantic Completeness):
```
∀ substrate T, ∀ input I:
    execute(project(S, T), I) = evaluate(S, I)
```
Every projection computes the same answer as the source.

### 10. Testing Infrastructure

The test orchestrator implicitly verifies both invariants:
- **125 candidates × 5 computed fields × 12 substrates**
- **If any substrate diverges, we know immediately**
- **Current score: 96.4% overall (deterministic substrates: 100%)**

---

## Key Files Referenced in This Article

| File | Purpose |
|------|---------|
| [README.md](../../README.md) | Invariant definitions |
| [effortless-rulebook.json](../../effortless-rulebook/effortless-rulebook.json) | Source of truth |
| [all-tests-results.md](../../orchestration/all-tests-results.md) | Test verification |

---

*Article content to be written...*
