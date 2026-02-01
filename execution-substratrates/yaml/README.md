# YAML - Schema Definition Substrate

YAML schema implementation where ALL calculation logic is expressed as structured field definitions and formula strings, with an LLM acting as the schema interpreter.

## Overview

This substrate encodes the ERB rulebook as a YAML schema. Every calculated field — including formula definitions, type constraints, and DAG dependencies — is expressed in YAML's human-readable structure. Python handles only file I/O (loading and saving JSON); all business logic inference is performed by an LLM reading the schema definition.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  inject-into-yaml.py                                        │
│  (Generic rulebook-to-schema generator)                     │
│                                                             │
│  Reads:  effortless-rulebook.json                           │
│  Writes: schema.yaml (generated schema with formulas)       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  take-test.py                                               │
│  (Domain-agnostic test coordinator)                         │
│                                                             │
│  1. Load blank-test.json (contains nulls for computed)      │
│  2. Load schema.yaml (the schema "program")                 │
│  3. For each record, for each null calculated field:        │
│     → Send schema + record to LLM                           │
│     → LLM interprets the formula from the schema            │
│     → Receive computed value from LLM                       │
│  4. Update the JSON with inferred values                    │
│  5. Save test-answers.json                                  │
└─────────────────────────────────────────────────────────────┘
```

## Role in Three-Phase Contract

### Phase 1: Inject

`inject-into-yaml.py` reads the rulebook and generates:

1. **schema.yaml** — Complete schema definition with:
   - Entity definitions (LanguageCandidate, ArgumentStep)
   - Field names, types, and descriptions
   - Formula strings for each computed field
   - DAG level annotations for execution order

### Phase 2: Execute

`take-test.py` runs the test:

```bash
./take-test.sh
```

Which executes:
1. Copy `blank-test.json` → `test-answers.json`
2. Run `take-test.py`:
   - Load `test-answers.json`
   - Load `schema.yaml` as the inference context
   - For each null field, query the LLM with schema + record
   - LLM reads the formula definition and computes the value
   - Update with inferred result
   - Save `test-answers.json`

### Phase 3: Emit

`test-answers.json` contains all computed values, produced by LLM inference from schema.

### Grade

Compare `test-answers.json` against `answer-key.json` — LLM inference must produce identical results to all other substrates.

## The Python Proxy Pattern

Python acts as a **domain-agnostic coordinator** — a "Chinese Room" that:
- Knows nothing about languages, predicates, or the thesis
- Simply orchestrates the flow: JSON in → LLM inference → JSON out
- Could be swapped for any other orchestration language

The LLM acts as a **schema interpreter** — reading the YAML schema and applying its formula definitions just as a code generator would parse and execute them.

```
┌──────────────┐      ┌────────────────────┐      ┌──────────────┐
│              │      │                    │      │              │
│  blank-test  │─────▶│   take-test.py     │─────▶│ test-answers │
│    .json     │      │   (coordinator)    │      │    .json     │
│              │      │                    │      │              │
└──────────────┘      └─────────┬──────────┘      └──────────────┘
                                │
                                │ For each null field:
                                │ "Given this schema,
                                │  what should field X be?"
                                ▼
                      ┌────────────────────┐
                      │                    │
                      │   LLM Provider     │
                      │ (OpenAI/Anthropic/ │
                      │     Ollama)        │
                      │                    │
                      └─────────┬──────────┘
                                │
                                │ Reads schema.yaml
                                │ Interprets formula
                                ▼
                      ┌────────────────────┐
                      │    schema.yaml     │
                      │  (the "program")   │
                      └────────────────────┘
```

## Computed Fields via Schema

Each calc function from the rulebook becomes a YAML formula definition:

| Calculated Field | Schema Formula |
|------------------|----------------|
| `category_contains_language` | `formula: "CONTAINS(LOWER(category), 'language')"` |
| `has_grammar` | `formula: "IF(has_syntax, 'True', 'False')"` |
| `relationship_to_concept` | `formula: "IF(distance_from_concept = 1, 'IsMirrorOf', 'IsDescriptionOf')"` |
| `family_fued_question` | `formula: "CONCAT('Is ', name, ' a language?')"` |
| `top_family_feud_answer` | `formula: "AND(category_contains_language, has_syntax, ...)"` |
| `family_feud_mismatch` | `formula: "IF(top_family_feud_answer != chosen_language_candidate, ...)"` |

## Schema Example

```yaml
entities:
  LanguageCandidate:
    primary_key: language_candidate_id
    fields:
      # Raw fields
      language_candidate_id:
        type: string
        description: "Primary key identifier"
      name:
        type: string
        description: "Display name of the candidate"
      category:
        type: string
        description: "Classification category"
      has_syntax:
        type: boolean
        description: "Does it have explicit grammar rules?"

      # Computed fields (Level 1)
      category_contains_language:
        type: boolean
        computed: true
        dag_level: 1
        formula: "CONTAINS(LOWER(category), 'language')"
        description: "Does category string contain 'language'?"

      has_grammar:
        type: string
        computed: true
        dag_level: 1
        formula: "IF(has_syntax, 'True', 'False')"
        description: "String representation of has_syntax"

      # Computed fields (Level 2)
      top_family_feud_answer:
        type: boolean
        computed: true
        dag_level: 2
        depends_on: [category_contains_language]
        formula: >
          AND(category_contains_language, has_syntax, NOT(can_be_held),
              meaning_is_serialized, requires_parsing, is_ontology_descriptor,
              NOT(has_identity), distance_from_concept = 2)
```

## Files

| File | Description |
|------|-------------|
| `inject-into-yaml.py` | Generates schema from rulebook |
| `schema.yaml` | Generated schema definition (all formulas as YAML) |
| `take-test.py` | Test runner (JSON I/O + LLM inference) |
| `inject-substrate.sh` | Runs injection |
| `take-test.sh` | Runs the test |
| `test-answers.json` | Computed results for grading |

## LLM Provider Configuration

The test runner supports multiple LLM providers:

```bash
# OpenAI (default)
python take-test.py --provider openai

# Anthropic
python take-test.py --provider anthropic

# Local Ollama
python take-test.py --provider ollama
```

## DAG Execution Order

```
Level 0: Raw fields (from JSON)
Level 1: category_contains_language, has_grammar, relationship_to_concept, family_fued_question
Level 2: top_family_feud_answer (depends on category_contains_language)
Level 3: family_feud_mismatch (depends on top_family_feud_answer)
```

The LLM respects this order — Level 2+ field queries include Level 1 results in context.

## Why YAML?

This substrate proves the ERB contract holds in a structured-but-not-executable format. YAML is:
- **Human-readable**: Easier to scan than JSON, supports comments
- **LLM-friendly**: The compact schema format is ideal for code generation prompts
- **Universal**: Used in CI/CD, Kubernetes, configuration management everywhere

The `inject-into-yaml.py` generator is domain-agnostic: it reads any ERB rulebook and produces YAML schema. The pattern is identical to other substrates — only the target representation changes.

## Interpretation

| Outcome | Meaning |
|---------|---------|
| High score | Schema formulas are unambiguous and LLM-interpretable |
| Low score | Schema may have unclear formula syntax or missing context |

A high score indicates the YAML schema is **sufficiently precise** that an LLM can correctly parse and apply the formulas — proving the schema is as rigorous as executable code.

## Status

Planned implementation.

## Source

Generated from: `effortless-rulebook/effortless-rulebook.json`
