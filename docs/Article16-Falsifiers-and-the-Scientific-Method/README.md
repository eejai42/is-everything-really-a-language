# Article 16: Falsifiers and the Scientific Method

Good specifications aren't just true for valid cases—they correctly reject invalid ones. This article examines the "Falsifier A/B/C" test candidates designed to fail specific conditions. We explore how falsifiability strengthens the classification predicate, why edge cases reveal specification gaps, and how ERB's test harness catches both false positives and false negatives. The conclusion: business rules should be as rigorously testable as scientific hypotheses.

---

## Detailed Table of Contents

### 1. The Falsifiability Principle
- **Popper's Insight**: A theory is scientific only if it can be proven false
- **Applied to Software**: A specification is meaningful only if something can violate it
- **The ERB Approach**: Include test cases designed to fail specific conditions
- **Why This Matters**: Prevents vacuous "everything passes" specifications

### 2. The Three Falsifiers

The rulebook includes three special test candidates:

| Candidate | Purpose | Expected Behavior |
|-----------|---------|-------------------|
| **Falsifier A** | Passes formula, NOT marked as language | Mismatch: "Is a Language, but Is Not marked" |
| **Falsifier B** | Fails formula, IS marked as language | Mismatch: "Isn't a Language, but Is marked" |
| **Falsifier C** | Both open AND closed world (conflict) | Mismatch with conflict warning |

### 3. Falsifier A: The False Negative Detector

```json
{
  "LanguageCandidateId": "falsifier-a",
  "Name": "Falsifier A",
  "Category": "MISSING: Have you seen this Language?",
  "HasSyntax": true,
  "RequiresParsing": true,
  "IsStableOntologyReference": true,
  "HasLinearDecodingPressure": true,
  "ResolvesToAnAST": true,
  "CanBeHeld": false,
  "HasIdentity": false,
  "DistanceFromConcept": 2,
  "ChosenLanguageCandidate": false  // ← Intentionally marked as NOT a language
}
```

**What It Tests**:
- Formula computes `TopFamilyFeudAnswer = true`
- Human marked `ChosenLanguageCandidate = false`
- Mismatch detector catches this: **"Falsifier A Is a Family Feud Language, but Is Not marked as a 'Language Candidate.'"**

**Why This Matters**:
- Catches cases where the formula says "yes" but humans said "no"
- Either the formula is wrong, or the human annotation is wrong
- Forces explicit resolution of the discrepancy

### 4. Falsifier B: The False Positive Detector

```json
{
  "LanguageCandidateId": "falsifier-b",
  "Name": "Falsifier B",
  "Category": "MISSING: Have you seen this Language?",
  "HasSyntax": false,           // ← Fails formula
  "RequiresParsing": true,
  "IsStableOntologyReference": true,
  "CanBeHeld": true,            // ← Fails formula
  "HasIdentity": true,          // ← Fails formula
  "DistanceFromConcept": 1,     // ← Fails formula
  "HasLinearDecodingPressure": false,
  "ChosenLanguageCandidate": true  // ← Intentionally marked as a language
}
```

**What It Tests**:
- Formula computes `TopFamilyFeudAnswer = false`
- Human marked `ChosenLanguageCandidate = true`
- Mismatch detector catches this: **"Falsifier B Isn't a Family Feud Language, but Is marked as a 'Language Candidate.'"**

**Why This Matters**:
- Catches cases where humans said "yes" but the formula says "no"
- Either the formula is too strict, or the human annotation is wrong
- Reveals gaps in the predicate definition

### 5. Falsifier C: The Logical Conflict Detector

```json
{
  "LanguageCandidateId": "falsifier-c",
  "Name": "Falsifier C",
  "Category": "MISSING: Have you seen this Language?",
  "HasSyntax": true,
  "RequiresParsing": true,
  // ... passes the formula
  "IsOpenWorld": true,          // ← Can't be both!
  "IsClosedWorld": true,        // ← Logical conflict
  "ChosenLanguageCandidate": true
}
```

**What It Tests**:
- Formula computes `TopFamilyFeudAnswer = true` (passes)
- Formula computes `IsOpenClosedWorldConflicted = true`
- Mismatch message includes: **" - Open World vs. Closed World Conflict."**

**Why This Matters**:
- Catches logically impossible states
- Something can't be both open-world AND closed-world
- Flags data quality issues

### 6. The Mismatch Formula

```
FamilyFeudMismatch =
    IF(TopFamilyFeudAnswer ≠ ChosenLanguageCandidate,
        Name & " " &
        IF(TopFamilyFeudAnswer, "Is", "Isn't") &
        " a Family Feud Language, but " &
        IF(ChosenLanguageCandidate, "Is", "Is Not") &
        " marked as a 'Language Candidate.'"
    ) &
    IF(IsOpenClosedWorldConflicted,
        " - Open World vs. Closed World Conflict."
    )
```

This formula produces four possible states:
1. `null` — No mismatch, no conflict
2. String without conflict — Mismatch only
3. String with conflict — Mismatch plus conflict
4. Conflict only — " - Open World vs. Closed World Conflict."

### 7. The Scientific Method Parallel

| Scientific Method | ERB Testing |
|-------------------|-------------|
| **Hypothesis** | `TopFamilyFeudAnswer` formula |
| **Prediction** | True for languages, false for non-languages |
| **Falsifiable** | Falsifier A/B/C can disprove it |
| **Observation** | Test results across 12 substrates |
| **Refinement** | Adjust formula or annotations |

### 8. Test Coverage Analysis

The 125 test candidates include:

| Category | Count | Purpose |
|----------|-------|---------|
| Clear languages (English, Python, etc.) | ~30 | Positive examples |
| Clear non-languages (Coffee Mug, etc.) | ~30 | Negative examples |
| Boundary cases (Running App, etc.) | ~30 | Edge cases |
| Running software | ~20 | Special category |
| Falsifiers | 3 | Deliberate failures |
| Misc. | ~12 | Additional coverage |

### 9. False Positives vs. False Negatives

| Error Type | Description | Falsifier |
|------------|-------------|-----------|
| **False Positive** | Formula says "yes", should be "no" | Falsifier B catches |
| **False Negative** | Formula says "no", should be "yes" | Falsifier A catches |
| **Logical Error** | Data is self-contradictory | Falsifier C catches |

### 10. When Falsifiers Fail

If a falsifier stops producing a mismatch:
1. **Someone "fixed" the annotation**: Investigate why
2. **Formula changed**: May have weakened/strengthened predicate
3. **Bug introduced**: Mismatch formula broken

The presence of expected failures is a feature, not a bug.

### 11. Extending the Falsifier Set

To add a new falsifier:
1. Identify a specific condition to test
2. Create a candidate that meets all OTHER conditions
3. Fail exactly one predicate
4. Mark it opposite of what formula computes
5. Verify mismatch message appears

### 12. The Broader Lesson

Business rules should be tested like scientific theories:
- **Positive tests**: Confirm expected behavior
- **Negative tests**: Confirm rejection of invalid cases
- **Falsifiers**: Deliberate failures that verify edge detection
- **Automated verification**: Run tests across all substrates

If your specification can't be falsified, it's probably useless.

---

## Key Files Referenced in This Article

| File | Purpose |
|------|---------|
| [effortless-rulebook.json](../../effortless-rulebook/effortless-rulebook.json) | Falsifier definitions |
| [testing/answer-key.json](../../testing/answer-key.json) | Expected mismatch values |

---

*Article content to be written...*
