# Article 14: The English Substrate — LLM-Validated Documentation

What if your documentation was so precise that an AI could read it and correctly compute every derived value? The English substrate generates `specification.md`, `glossary.md`, and candidate profiles—then validates them by having an LLM read the prose and infer the answers. This article explores deterministic structure with stochastic content, pluggable LLM providers, and cost tier optimization. If the LLM gets the wrong answer, your documentation isn't clear enough.

---

## Detailed Table of Contents

### 1. The Radical Idea
- **Traditional Docs**: Written by humans, read by humans, often wrong
- **LLM-Testable Docs**: If an AI can't compute the right answer from your docs, they're unclear
- **The Achievement**: 90.4% accuracy (stochastic variation accounts for the rest)
- **Test Time**: 2.15s + LLM latency

### 2. The Generated Files

```
execution-substrates/english/
├── specification.md          # Full English specification
├── glossary.md               # Term definitions
├── candidate-profiles.md     # Individual candidate descriptions
├── inject-into-english.py    # Code generator
├── take-test.py              # Test runner (calls LLM)
├── test-answers.json         # Output for grading
└── README.md
```

### 3. Deterministic Structure + Stochastic Content

The English substrate has two layers:

| Layer | Type | Example |
|-------|------|---------|
| **Skeleton** | Deterministic | Section headers, formula references |
| **Content** | Stochastic | LLM-generated prose explaining concepts |

```markdown
## Classification Formula: TopFamilyFeudAnswer        ← Deterministic header

The TopFamilyFeudAnswer field determines whether     ← LLM-generated prose
a candidate qualifies as a language according to
our formal definition...

### Formula                                           ← Deterministic header
```
TopFamilyFeudAnswer = AND(HasSyntax, RequiresParsing, ...)
```                                                  ← Deterministic formula
```

### 4. The Specification — `specification.md`

```markdown
# Language Classification Specification

## Overview

This document defines the formal criteria for classifying
entities as "languages" using a set of explicit predicates.

## The Core Classification Formula

A candidate X is classified as a **Language** if and only if:

```
TopFamilyFeudAnswer(X) = AND(
    HasSyntax(X),
    RequiresParsing(X),
    IsDescriptionOf(X),
    HasLinearDecodingPressure(X),
    ResolvesToAnAST(X),
    IsStableOntologyReference(X),
    NOT(CanBeHeld(X)),
    NOT(HasIdentity(X))
)
```

### Predicate Definitions

**HasSyntax**: Does the candidate have explicit grammar rules?
A candidate has syntax if it follows a formal or informal
grammar that governs valid constructions...

**RequiresParsing**: Must the candidate be parsed to extract meaning?
Parsing implies that the candidate must be processed sequentially
to understand its content...

[... more predicates ...]

## Derived Fields

### IsDescriptionOf

**Formula**: `distance_from_concept > 1`

A candidate is a "description of" something (rather than
being the thing itself) when its distance from the concept
is greater than 1...
```

### 5. The Glossary — `glossary.md`

```markdown
# Glossary of Terms

## Predicates (Raw Fields)

| Term | Definition |
|------|------------|
| **HasSyntax** | Whether the candidate possesses formal grammar rules |
| **RequiresParsing** | Whether meaning extraction requires sequential processing |
| **CanBeHeld** | Whether the candidate is a physical, tangible object |
| **HasIdentity** | Whether the candidate has persistent individual identity |
| **DistanceFromConcept** | 1 = is the thing itself, 2 = describes the thing |

## Derived Fields

| Term | Formula | Definition |
|------|---------|------------|
| **IsDescriptionOf** | `distance > 1` | True if candidate describes rather than embodies |
| **TopFamilyFeudAnswer** | 8-way AND | Classification as language |
```

### 6. The LLM Evaluation Process

```
┌─────────────────────────────────────────────────────────────┐
│                    LLM FUZZY GRADING                         │
└─────────────────────────────────────────────────────────────┘

Input:
├── specification.md (the generated English docs)
├── blank-test.json (candidate with raw fields, nulled computed)
└── Prompt: "Based on the specification, what is TopFamilyFeudAnswer for this candidate?"

Processing:
1. Feed specification to LLM context
2. For each candidate:
   └── Ask LLM to compute each derived field
   └── Parse LLM response (true/false/string)
3. Compare to answer-key.json

Output:
└── test-answers.json (LLM-inferred values)
```

### 7. The Test Runner — `take-test.py`

```python
def take_test():
    # 1. Load specification
    with open('specification.md') as f:
        spec = f.read()

    # 2. Load test data
    with open('../../testing/blank-test.json') as f:
        test_data = json.load(f)

    # 3. For each candidate, ask LLM to compute
    results = []
    for record in test_data:
        prompt = f"""
        Based on the specification below, determine the computed fields
        for this candidate:

        Name: {record['name']}
        HasSyntax: {record['has_syntax']}
        RequiresParsing: {record['requires_parsing']}
        CanBeHeld: {record['can_be_held']}
        HasIdentity: {record['has_identity']}
        DistanceFromConcept: {record['distance_from_concept']}
        [... more fields ...]

        What is TopFamilyFeudAnswer? (true or false)
        What is FamilyFeudMismatch? (string or null)

        Specification:
        {spec}
        """

        response = llm_call(prompt)
        parsed = parse_llm_response(response)

        record['top_family_feud_answer'] = parsed['top_family_feud_answer']
        record['family_feud_mismatch'] = parsed['family_feud_mismatch']
        results.append(record)

    # 4. Write results
    with open('test-answers.json', 'w') as f:
        json.dump(results, f)
```

### 8. The LLM Fuzzy Grader — `llm-fuzzy-grader.py`

```python
# Supported providers
PROVIDERS = {
    'openai': {
        'smart': 'gpt-4o',
        'medium': 'gpt-4o-mini',
        'cheap': 'gpt-3.5-turbo'
    },
    'anthropic': {
        'smart': 'claude-3-sonnet',
        'medium': 'claude-3-haiku',
        'cheap': 'claude-3-haiku'
    },
    'ollama': {
        'local': 'llama3.2'
    }
}

# Usage
python llm-fuzzy-grader.py english --provider openai --tier smart --write-answers
```

### 9. Cost Tier Optimization

| Tier | Model | Speed | Accuracy | Cost |
|------|-------|-------|----------|------|
| **Smart** | GPT-4o / Claude Sonnet | Slow | Highest | $$$ |
| **Medium** | GPT-4o-mini / Haiku | Medium | Good | $$ |
| **Cheap** | GPT-3.5 | Fast | Lower | $ |
| **Local** | Llama 3.2 (Ollama) | Variable | Good | Free |

### 10. Test Results

- **Pass Rate**: 90.4% (12 failures out of 125)
- **Execution Time**: 2.15s + LLM latency
- **Why Not 100%?**: LLM inference is stochastic; edge cases in string formatting

### 11. The Failures Tell a Story

When an LLM gets the wrong answer:
1. **Ambiguous wording**: The spec wasn't clear enough
2. **Edge case**: The formula has subtle behavior
3. **Context limit**: Too much text for the model

Each failure is an opportunity to improve documentation clarity.

### 12. The Philosophical Insight

If your documentation is clear enough for an AI to compute correct answers:
- **It's unambiguous**: No room for misinterpretation
- **It's complete**: All necessary information is present
- **It's testable**: You can verify correctness programmatically

### 13. Comparison: Deterministic vs. English Substrates

| Aspect | Deterministic (Python, Go) | English (LLM) |
|--------|---------------------------|---------------|
| **Execution** | Microseconds | Seconds |
| **Accuracy** | 100% | ~90% |
| **Cost** | Free | API costs |
| **Human Readable** | Requires code literacy | Natural language |
| **Debugging** | Stack traces | "Unclear wording" |

---

## Key Files Referenced in This Article

| File | Purpose |
|------|---------|
| [specification.md](../../execution-substrates/english/specification.md) | Full English spec |
| [glossary.md](../../execution-substrates/english/glossary.md) | Term definitions |
| [inject-into-english.py](../../execution-substrates/english/inject-into-english.py) | Generator |
| [llm-fuzzy-grader.py](../../orchestration/llm-fuzzy-grader.py) | LLM evaluation tool |

---

*Article content to be written...*
