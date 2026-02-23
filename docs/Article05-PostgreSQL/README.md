# Article 5: PostgreSQL — The Most Reliable Mirror

PostgreSQL is the default substrate for generating the answer key—not because it's privileged, but because it's well-tested and deterministic. This article shows how ERB generates DDL tables, `calc_*` functions, materialized views, and Row Level Security policies from the rulebook. We examine how the function composition enforces DAG execution order. Any substrate achieving 100% conformance could serve this role; Postgres is simply the practical default.

---

## Detailed Table of Contents

### 1. Why PostgreSQL Is the Default Answer-Key Substrate
- **Practical Choice, Not Privilege**: PostgreSQL generates the `answer-key.json` by default
- **The Reference for Conformance**: Other substrates are graded against what Postgres computes, but any 100%-conformant substrate could serve this role
- **The ERB Pattern**: Views read, tables write, functions calculate
- **Database**: `wikidata-language-candidates` on localhost:5432

### 2. The Generated SQL Files

ERB generates a complete, ordered set of SQL files:

| File | Purpose | Contents |
|------|---------|----------|
| `000-drop-all.sql` | Clean slate | DROP statements |
| `01-drop-and-create-tables.sql` | Base table DDL | 2 tables |
| `02-create-functions.sql` | `calc_*()` functions | 7 functions |
| `02b-custom-functions.sql` | Manual overrides | Custom logic |
| `03-create-views.sql` | `vw_*` views | 2 views |
| `04-create-policies.sql` | Row Level Security | RLS policies |
| `05-insert-data.sql` | Test data | 125 records |

### 3. The Tables — Normalized Base Facts

#### 3.1 `language_candidates` Table Structure
- **19 columns**: All raw/input fields
- **Primary Key**: `language_candidate_id` (TEXT)
- **Boolean fields**: `has_syntax`, `has_identity`, `can_be_held`, etc.
- **No computed columns**: Those live in the view
- **WRITE target**: INSERT/UPDATE/DELETE go here

#### 3.2 `is_everything_a_language` Table
- **11 columns**: Argument documentation
- **Purpose**: Meta-level philosophical argument storage

### 4. The Functions — One Per Calculated Field

#### 4.1 Function Naming Convention
```
calc_{table_name}_{field_name}(p_{primary_key} TEXT) RETURNS {type}
```

#### 4.2 The Seven Generated Functions
| Function | Level | Returns | Dependencies |
|----------|-------|---------|--------------|
| `calc_language_candidates_family_fued_question` | 1 | TEXT | name |
| `calc_language_candidates_has_grammar` | 1 | BOOLEAN | has_syntax |
| `calc_language_candidates_is_description_of` | 1 | BOOLEAN | distance_from_concept |
| `calc_language_candidates_is_open_closed_world_conflicted` | 1 | BOOLEAN | is_open_world, is_closed_world |
| `calc_language_candidates_relationship_to_concept` | 1 | TEXT | distance_from_concept |
| `calc_language_candidates_top_family_feud_answer` | 2 | BOOLEAN | 8 fields + is_description_of |
| `calc_language_candidates_family_feud_mismatch` | 3 | TEXT | top_family_feud_answer + more |

#### 4.3 DAG Enforcement Through Function Calls
Level 2 functions call Level 1 functions:
```sql
-- Inside calc_language_candidates_top_family_feud_answer:
AND (calc_language_candidates_is_description_of(p_language_candidate_id) = 'true')
```

### 5. The View — Denormalized Read Interface

```sql
CREATE OR REPLACE VIEW vw_language_candidates AS
SELECT
    -- Raw columns (direct from table)
    t.language_candidate_id,
    t.name,
    t.category,
    t.has_syntax,
    -- ... 15 more raw columns

    -- Calculated columns (via function calls)
    calc_language_candidates_family_fued_question(t.language_candidate_id)
        AS family_fued_question,
    calc_language_candidates_top_family_feud_answer(t.language_candidate_id)
        AS top_family_feud_answer,
    -- ... 4 more calculated columns

FROM language_candidates t;
```

### 6. The ERB Pattern Visualized

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION CODE                          │
└─────────────────────────────────────────────────────────────┘
         │                              │
         │ READ                         │ WRITE
         ▼                              ▼
┌─────────────────────┐       ┌─────────────────────┐
│  vw_language_       │       │  language_          │
│  candidates         │       │  candidates         │
│  (19 raw + 6 calc)  │       │  (19 raw only)      │
└─────────────────────┘       └─────────────────────┘
         │
         │ SELECT invokes
         ▼
┌─────────────────────┐
│  calc_*() functions │
│  (7 functions)      │
└─────────────────────┘
```

### 7. Function Properties Deep Dive

```sql
CREATE OR REPLACE FUNCTION calc_...(p_id TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    ...
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;
```

| Property | Meaning | Why |
|----------|---------|-----|
| `plpgsql` | PL/pgSQL language | Supports procedural logic |
| `STABLE` | No DB modification | Optimizer can cache within transaction |
| `SECURITY DEFINER` | Runs as function owner | Required for RLS |

### 8. The NULL Handling Strategy

```sql
-- Pattern: COALESCE to FALSE for NULL booleans
COALESCE(
    (SELECT has_syntax FROM language_candidates
     WHERE language_candidate_id = p_id),
    FALSE
)
```
- **NULL AND TRUE** would return NULL (bad)
- **COALESCE(NULL, FALSE) AND TRUE** returns FALSE (predictable)

### 9. Row Level Security Policies

`04-create-policies.sql` enables multi-tenant scenarios:
```sql
ALTER TABLE language_candidates ENABLE ROW LEVEL SECURITY;

CREATE POLICY language_candidates_select_policy
    ON language_candidates FOR SELECT
    USING (true);  -- All rows visible in this demo
```

### 10. Querying the View — Common Patterns

#### 10.1 Get All Candidates
```sql
SELECT name, category, top_family_feud_answer
FROM vw_language_candidates
ORDER BY sort_order;
```

#### 10.2 Find Mismatches
```sql
SELECT name, family_feud_mismatch
FROM vw_language_candidates
WHERE family_feud_mismatch IS NOT NULL
  AND family_feud_mismatch <> '';
```

#### 10.3 Count Languages vs Non-Languages
```sql
SELECT top_family_feud_answer, COUNT(*)
FROM vw_language_candidates
GROUP BY top_family_feud_answer;
```

### 11. Custom Function Overrides

`02b-custom-functions.sql` allows manual overrides for complex cases:
```sql
-- Override when generated formula translation fails
CREATE OR REPLACE FUNCTION calc_language_candidates_family_feud_mismatch(
    p_language_candidate_id TEXT
) RETURNS TEXT AS $$
DECLARE
    v_name TEXT;
    v_computed BOOLEAN;
    v_chosen BOOLEAN;
BEGIN
    -- Manual implementation of string concatenation logic
    ...
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;
```

### 12. The Answer Key Generation Process

```python
# In test-orchestrator.py:
def generate_answer_key():
    conn = psycopg2.connect(DB_CONNECTION)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM vw_language_candidates ORDER BY language_candidate_id")
    answer_key = [dict(row) for row in cur.fetchall()]
    # Write to testing/answer-key.json
```

### 13. Initialization Sequence

```bash
# init-db.sh
psql -d wikidata-language-candidates -f 000-drop-all.sql
psql -d wikidata-language-candidates -f 01-drop-and-create-tables.sql
psql -d wikidata-language-candidates -f 02-create-functions.sql
psql -d wikidata-language-candidates -f 02b-custom-functions.sql  # Overrides
psql -d wikidata-language-candidates -f 03-create-views.sql
psql -d wikidata-language-candidates -f 04-create-policies.sql
psql -d wikidata-language-candidates -f 05-insert-data.sql
```

---

## Key Files Referenced in This Article

| File | Purpose |
|------|---------|
| [01-drop-and-create-tables.sql](../../postgres/01-drop-and-create-tables.sql) | Table DDL |
| [02-create-functions.sql](../../postgres/02-create-functions.sql) | Generated calc functions |
| [02b-custom-functions.sql](../../postgres/02b-custom-functions.sql) | Manual overrides |
| [03-create-views.sql](../../postgres/03-create-views.sql) | View definitions |
| [04-create-policies.sql](../../postgres/04-create-policies.sql) | RLS policies |
| [05-insert-data.sql](../../postgres/05-insert-data.sql) | Test data |

---

*Article content to be written...*
