# Article 20: Past, Present, and Future Languages

The WikiData "Is It a Natural Language?" example isn't arbitrary—it's a meditation on time and classification. Some candidates (Latin, Sanskrit) were once living languages but are now "dead." Others (English, Mandarin) are vibrant today. Still others (constructed languages, emerging creoles) represent possible futures. This article explores how ERB handles temporal predicates: can a classification change over time? How do we model historical truth vs. current truth vs. projected truth? We examine how the rulebook's formula system can encode time-aware logic, and what this means for business rules that must reason about past states, present conditions, and future possibilities.

---

## Detailed Table of Contents

### 1. The Temporal Dimension of Classification

| Time Frame | Example | Language Status |
|------------|---------|-----------------|
| **Past** | Latin | Was living, now "dead" |
| **Present** | English | Currently living |
| **Future** | Esperanto 2.0 | Might become dominant |

The same entity can have different classifications at different times.

### 2. Current Candidates and Their Temporal Status

| Candidate | Category | Temporal Notes |
|-----------|----------|----------------|
| English | Natural Language | Living, evolving |
| French | Natural Language | Living, evolving |
| Sign Language | Natural Language | Multiple variants, all living |
| Python | Formal Language | Active development |
| Binary Code | Formal Language | Unchanging specification |
| A Coffee Mug | Physical Object | Timeless classification |

### 3. The Absent Temporal Predicates

The current rulebook lacks explicit temporal fields:

```json
// Not currently in the rulebook:
{
  "name": "WasLivingLanguage",
  "datatype": "boolean",
  "type": "raw"
},
{
  "name": "IsCurrentlyLiving",
  "datatype": "boolean",
  "type": "raw"
},
{
  "name": "YearOfDeath",
  "datatype": "integer",
  "type": "raw"
}
```

**Implication**: The current classification is **atemporal** — it represents a snapshot, not a timeline.

### 4. How Temporal Logic Could Be Added

#### 4.1 Simple Boolean Predicates
```json
{
  "name": "IsHistoricallyAttestedLanguage",
  "datatype": "boolean",
  "formula": "=OR({{WasLivingLanguage}}, {{IsCurrentlyLiving}})"
}
```

#### 4.2 Time-Point Evaluation
```json
{
  "name": "WasLanguageAtYear",
  "datatype": "boolean",
  "formula": "=IF({{YearOfDeath}} IS NULL, TRUE, {{EvaluationYear}} < {{YearOfDeath}})"
}
```

#### 4.3 Temporal Interval Membership
```json
{
  "name": "LanguageDuringPeriod",
  "datatype": "boolean",
  "formula": "=AND({{EvaluationYear}} >= {{YearOfBirth}}, OR({{YearOfDeath}} IS NULL, {{EvaluationYear}} < {{YearOfDeath}}))"
}
```

### 5. The "Dead Language" Paradox

**Is Latin a language?**

| Interpretation | Answer | Reasoning |
|----------------|--------|-----------|
| **Synchronic** (now) | Maybe not | No native speakers |
| **Diachronic** (historically) | Yes | Once had millions of speakers |
| **Functional** (current use) | Yes | Used in Vatican, academia, legal |

The current formula doesn't distinguish these:
```
TopFamilyFeudAnswer = AND(HasSyntax, RequiresParsing, ...)
```

**Latin has syntax and requires parsing** → Formula says "yes"

### 6. Candidates That Would Require Temporal Modeling

| Candidate | Challenge |
|-----------|-----------|
| **Latin** | Was living, now "dead," still used formally |
| **Sanskrit** | Ancient, revived in some contexts |
| **Old English** | Evolved into Modern English — same language? |
| **Esperanto** | Never "native," but has community |
| **Klingon** | Constructed, has learners, no native speakers |

### 7. The Bitemporal Model

For full temporal reasoning, you need two time dimensions:

| Dimension | Question |
|-----------|----------|
| **Valid Time** | When was this true in reality? |
| **Transaction Time** | When did we record this in the system? |

```json
{
  "LanguageCandidateId": "latin",
  "Name": "Latin",
  "ValidFrom": "-500",
  "ValidTo": "600",        // Became "dead"
  "RecordedAt": "2024-01-15"
}
```

### 8. Formula Modifications for Temporal Queries

#### 8.1 "At Time T" Evaluation
```
TopFamilyFeudAnswerAtTime(T) = AND(
  HasSyntax,
  RequiresParsing,
  IsDescriptionOf,
  ...
  WasLivingAtTime(T)  // New temporal predicate
)
```

#### 8.2 "Ever Was" Evaluation
```
EverWasLanguage = OR(
  TopFamilyFeudAnswerAtTime(-1000),
  TopFamilyFeudAnswerAtTime(0),
  TopFamilyFeudAnswerAtTime(1000),
  TopFamilyFeudAnswerAtTime(2024)
)
```

### 9. Substrate Implications

Temporal logic manifests differently across substrates:

| Substrate | Temporal Support |
|-----------|------------------|
| **PostgreSQL** | `BETWEEN` clauses, temporal tables |
| **OWL** | OWL-Time ontology |
| **RDF** | Named graphs with time metadata |
| **Python** | `datetime` comparisons |
| **Excel** | Date functions |

### 10. Future Languages — Speculative Classification

What if we want to classify things that **don't yet exist**?

| Candidate | Status | Classification Challenge |
|-----------|--------|-------------------------|
| **Universal Translator** | Future technology | Would it BE a language or REPLACE languages? |
| **Neural Interface Protocol** | Speculative | Direct thought transfer — syntax-free? |
| **AI-Generated Languages** | Emerging | GPT outputs — language or simulation? |

### 11. The Philosophical Questions

1. **Identity Over Time**: If English changes every century, is it "the same" language?
2. **Necessary vs. Contingent Properties**: Is "having speakers" necessary for being a language?
3. **Counterfactuals**: Would Latin still be a language if the Roman Empire never fell?

### 12. Extending the Rulebook

To add temporal support:

1. **Add temporal fields**:
   ```json
   { "name": "ValidFrom", "datatype": "integer", "type": "raw" },
   { "name": "ValidTo", "datatype": "integer", "type": "raw" }
   ```

2. **Add temporal formulas**:
   ```json
   {
     "name": "IsLivingAt",
     "formula": "=AND({{EvalYear}} >= {{ValidFrom}}, OR({{ValidTo}} IS NULL, {{EvalYear}} < {{ValidTo}}))"
   }
   ```

3. **Modify classification to be time-aware**:
   ```json
   {
     "name": "TopFamilyFeudAnswerAtEvalYear",
     "formula": "=AND({{TopFamilyFeudAnswerCore}}, {{IsLivingAt}})"
   }
   ```

### 13. The Meta-Lesson

The "Is It a Language?" question reveals:
- **Classification is perspective-dependent**
- **Time is an implicit dimension** we often ignore
- **Business rules about time** are surprisingly complex
- **ERB's formula system** can handle temporal logic — if we encode it

---

## Key Files Referenced in This Article

| File | Purpose |
|------|---------|
| [effortless-rulebook.json](../../effortless-rulebook/effortless-rulebook.json) | Current (atemporal) schema |

---

*Article content to be written...*
