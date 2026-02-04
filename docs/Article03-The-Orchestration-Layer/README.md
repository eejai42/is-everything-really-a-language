# Article 3: The Orchestration Layer — Conducting the Symphony

Between the Airtable source and the 12 execution substrates sits the orchestration layer. This article explains how `ssotme.json` defines the transpilation pipeline, how the test orchestrator validates every substrate against a unified answer key, and how the three-phase contract (Inject → Execute → Grade) ensures consistency. We'll trace a single change from Airtable through the entire build process, watching it propagate to Postgres, Python, Go, Excel, RDF, and even x86 assembly.

---

## Detailed Table of Contents

### 1. The Conductor's Podium
- **The Problem**: 12 substrates, each with different syntax, toolchains, and runtimes
- **The Solution**: A unified orchestration layer that treats substrates as interchangeable computation engines
- **The Key Insight**: Substrates don't define truth—they project it
- **The Metaphor**: A symphony orchestra where every instrument plays the same score

### 2. The ssotme.json Configuration
The `ssotme.json` file is the build manifest:

```json
{
  "Name": "ERB-root-seed",
  "ProjectSettings": [
    { "Name": "baseId", "Value": "appC8XTj95lubn6hz" }
  ],
  "ProjectTranspilers": [...]
}
```

#### 2.1 The Transpiler Registry
| Transpiler | Direction | Command | Purpose |
|------------|-----------|---------|---------|
| `airtabletorulebook` | Airtable → JSON | `airtable-to-rulebook -o effortless-rulebook.json` | Pull source of truth |
| `rulebooktopostgres` | JSON → SQL | `rulebook-to-postgres -i ../effortless-rulebook.json` | Generate DDL |
| `init-db` | SQL → Postgres | `./init-db.sh` | Execute DDL |
| `JsonHbarsTransform` | JSON → Markdown | `json-hbars-transform ...` | Generate documentation |

#### 2.2 The Disabled Transpilers (And Why They Exist)
- `rulebooktoairtable` (disabled): Push local changes back to Airtable
- `airtabletoodxml` (disabled): Export to ODXML format
- `OdxmlToCSharpPOCOs` (disabled): Generate C# from ODXML

### 3. The Build Pipeline Sequence
```
Airtable (browser)
    │
    ▼ [airtabletorulebook]
effortless-rulebook.json
    │
    ├──▶ [rulebooktopostgres] ──▶ postgres/*.sql
    │                               │
    │                               ▼ [init-db]
    │                           PostgreSQL database
    │
    ├──▶ [substrate injectors] ──▶ execution-substratrates/*/
    │
    └──▶ [JsonHbarsTransform] ──▶ README.SCHEMA.md
```

### 4. The Test Orchestrator — `test-orchestrator.py`
The 31KB Python script that validates everything:

#### 4.1 Configuration Constants
```python
DB_CONNECTION = "postgresql://postgres@localhost:5432/wikidata-language-candidates"
VIEW_NAME = "vw_language_candidates"
PRIMARY_KEY = "language_candidate_id"

COMPUTED_COLUMNS = [
    "family_feud_mismatch",
    "family_fued_question",
    "top_family_feud_answer",
    "relationship_to_concept",
    "is_open_closed_world_conflicted",
]
```

#### 4.2 Directory Structure
```
orchestration/
├── test-orchestrator.py    # Main orchestration script
├── formula_parser.py       # Excel→AST→Target compiler
├── shared.py               # Utilities
├── llm-fuzzy-grader.py     # LLM evaluation for non-executable substrates
├── orchestrate.sh          # Shell wrapper
└── all-tests-results.md    # Output dashboard
```

### 5. The Three-Phase Contract

#### Phase 1: Generate Answer Key (PostgreSQL as Ground Truth)
```python
def generate_answer_key():
    # Query vw_language_candidates
    # Export ALL fields (including computed) to answer-key.json
```
- **Why Postgres?**: SQL functions are the "reference implementation"
- **Output**: `testing/answer-key.json` with 125 records, all fields populated

#### Phase 2: Generate Blank Test (Computed Fields → NULL)
```python
def generate_blank_test(answer_key):
    for col in COMPUTED_COLUMNS:
        blank_record[col] = None  # Substrate must compute this
```
- **What's Blanked**: The 5 calculated fields
- **What's Preserved**: All raw fields (inputs to the formulas)
- **Output**: `testing/blank-test.json`

#### Phase 3: Run Each Substrate's Test
```
For each substrate in execution-substratrates/:
    1. Run take-test.sh
    2. Load test-answers.json
    3. Compare field-by-field against answer-key.json
    4. Report pass/fail + score
```

### 6. The Substrate Contract — What Every Substrate Must Provide

Every substrate directory must contain:

| File | Purpose |
|------|---------|
| `inject-into-<substrate>.py` | Generate substrate code from rulebook |
| `take-test.py` (or `.sh`) | Run the test, produce `test-answers.json` |
| `test-answers.json` | Computed results for grading |
| `README.md` | Documentation |

#### 6.1 The Injector Contract
The injector MUST be domain-agnostic:
- ❌ No mention of "language", "syntax", "grammar"
- ✅ Only translates generic schema structures → target language constructs

#### 6.2 The Test Runner Contract
The test runner:
1. Loads `blank-test.json`
2. Populates substrate data structures
3. Calls generated `calc_*()` functions
4. Writes `test-answers.json`

### 7. The Grading Algorithm

```python
def grade_substrate(answer_key, test_answers):
    mismatches = []
    for record in answer_key:
        pk = record[PRIMARY_KEY]
        for col in COMPUTED_COLUMNS:
            expected = answer_key[pk][col]
            actual = test_answers[pk][col]
            if normalize(expected) != normalize(actual):
                mismatches.append((pk, col, expected, actual))

    score = 100 * (total_fields - len(mismatches)) / total_fields
    return score, mismatches
```

#### 7.1 Normalization Rules
- Strings: lowercase, strip whitespace
- Booleans: `True`/`"true"`/`1` → `true`
- NULLs: `None`/`null`/`""` → `null`

### 8. The Color-Coded Dashboard

The orchestrator produces `all-tests-results.md`:

```
╔════════════════════════════════════════════════════════════════╗
║                     TEST RESULTS DASHBOARD                      ║
╚════════════════════════════════════════════════════════════════╝

Substrate         Score     Failures   Time
─────────────────────────────────────────────────
python           100.0%         0      115ms    ✓
golang           100.0%         0      201ms    ✓
xlsx             100.0%         0      336ms    ✓
...
binary            69.6%        38      434ms    ✗
english           90.4%        12     2150ms    ✗
```

#### 8.1 The Score Gradient
- 100%: Bright green
- 90-99%: Light green
- 70-89%: Yellow-green
- 50-69%: Yellow/Orange
- <50%: Red

### 9. Tracing a Change Through the System

**Scenario**: Rename `HasSyntax` to `HasGrammarRules` in Airtable

```
1. Edit in Airtable (browser)
   └── HasSyntax → HasGrammarRules

2. Run: ssotme -build airtabletorulebook
   └── effortless-rulebook.json updated

3. Run: ssotme -buildall
   └── postgres/02-create-functions.sql: calc_*_has_grammar_rules()
   └── execution-substratrates/python/erb_calc.py: has_grammar_rules
   └── execution-substratrates/golang/erb_sdk.go: HasGrammarRules
   └── execution-substratrates/xlsx/rulebook.xlsx: Column renamed
   └── execution-substratrates/owl/ontology.owl: :hasGrammarRules
   └── ... (12 total substrates)

4. Run: ./orchestrate.sh
   └── All tests pass (assuming formula logic unchanged)
```

### 10. The Failure Modes (And What They Tell Us)

| Failure Type | Cause | Example |
|--------------|-------|---------|
| **Type mismatch** | Boolean vs string representation | `true` vs `"True"` |
| **Precision error** | Floating point differences | `0.3333` vs `0.33333333` |
| **NULL handling** | Different semantics | `null` vs `""` vs `false` |
| **String concat** | Edge cases in assembly | Binary substrate at 69.6% |
| **LLM variance** | Stochastic generation | English substrate at 90.4% |

### 11. The LLM Fuzzy Grader — `llm-fuzzy-grader.py`

For non-executable substrates (English, DOCX, UML):

```bash
python llm-fuzzy-grader.py english --provider openai --write-answers
```

#### 11.1 How It Works
1. Feed substrate output (prose/diagrams) to LLM
2. Ask: "Based on this specification, what should field X be for candidate Y?"
3. Compare LLM's inference to `answer-key.json`

#### 11.2 Supported Providers
- OpenAI: GPT-4o, GPT-4o-mini
- Anthropic: Claude Sonnet, Claude Haiku
- Ollama: Local models (Llama 3.2)

### 12. Running the Full Orchestration

```bash
# Pull latest from Airtable
ssotme -build airtabletorulebook

# Regenerate all substrates
ssotme -buildall

# Run full test suite
cd orchestration
./orchestrate.sh

# View results
cat all-tests-results.md
```

### 13. Why This Architecture Works

1. **Separation of Concerns**: Source (Airtable) → Hub (JSON) → Targets (substrates)
2. **No Privileged Substrate**: PostgreSQL is canonical only for grading, not for definition
3. **Domain Agnosticism**: The orchestrator knows nothing about "languages"—it just compares JSON
4. **Falsifiability**: Failures point to specific (record, field) pairs

---

## Key Files Referenced in This Article

| File | Purpose |
|------|---------|
| [ssotme.json](../../ssotme.json) | Build manifest |
| [test-orchestrator.py](../../orchestration/test-orchestrator.py) | Main orchestration script |
| [llm-fuzzy-grader.py](../../orchestration/llm-fuzzy-grader.py) | LLM evaluation |
| [all-tests-results.md](../../orchestration/all-tests-results.md) | Test dashboard |
| [answer-key.json](../../testing/answer-key.json) | Ground truth |
| [blank-test.json](../../testing/blank-test.json) | Test input template |

---

*Article content to be written...*
