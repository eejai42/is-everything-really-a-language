# PostgreSQL - Source of Truth

PostgreSQL serves as the **canonical computation engine** for the ERB system. All other substrates are graded against its output.

## Role in Three-Phase Contract

PostgreSQL is unique: it **defines** the answer key rather than being tested against it.

### Phase 1: Inject

Generate SQL DDL + calc functions + views + seed data from the rulebook:

| Artifact | Purpose |
|----------|---------|
| `01-drop-and-create-tables.sql` | Base tables with raw fields |
| `02-create-functions.sql` | `calc_*` functions implementing the formula DAG |
| `03-create-views.sql` | `vw_*` views with all computed fields |
| `04-create-policies.sql` | Row Level Security policies |
| `05-insert-data.sql` | Seed data from rulebook |
| `init-db.sh` | Database initialization script |

### Phase 2: Execute

Compute all derived fields via the canonical view (the "all computed fields included" view):

```bash
./init-db.sh  # Initialize database and compute via views
```

### Phase 3: Emit (Generate Test Artifacts)

Export the computed results as the test baseline:

| Output | Purpose |
|--------|---------|
| `answer-key.json` | Complete view output — the ground truth |
| `blank-test.json` | Same rows but computed fields nulled — test input |

These files go into `testing/` and are used by all other substrates.

### Grade

PostgreSQL is the baseline — other substrates compare their results to it.

## Technology

**PostgreSQL** is an advanced open-source relational database with powerful SQL features. Its function system allows complex calculations to be expressed declaratively.

Key characteristics:
- **SQL functions**: `CREATE FUNCTION calc_*` implements each derived field
- **Views**: Pre-computed joins that materialize the full entity with all calculated fields
- **Referential integrity**: Foreign keys ensure data consistency
- **Row Level Security**: Fine-grained access control

## Files

| File | Description |
|------|-------------|
| `01-drop-and-create-tables.sql` | Drop and recreate tables with raw fields |
| `02-create-functions.sql` | Create calculation functions |
| `03-create-views.sql` | Create views with calculated fields |
| `04-create-policies.sql` | Create RLS policies |
| `05-insert-data.sql` | Insert data from rulebook |
| `init-db.sh` | Database initialization script |

## Usage

```bash
# Initialize the database
./init-db.sh

# Query the computed view
psql -d demo -c "SELECT name, is_a_family_feud_top_answer FROM vw_language_candidates"
```

## DAG Execution Order

```
Level 0: Raw fields (from tables)
Level 1: category_contains_language, has_grammar, relationship_to_concept, family_fued_question
Level 2: is_a_family_feud_top_answer (depends on category_contains_language)
Level 3: family_feud_mismatch (depends on is_a_family_feud_top_answer)
```

## Generation Report

**Schema:** `public`
**Database:** `demo`

Found **1** tables in rulebook:
- **LanguageCandidates** (17 fields, 24 records)

Generated:
- **1** table definitions with **12** raw fields
- **5** calculation functions
- **1** views
- RLS enabled on **1** tables
- Insert statements for **24** records

## Source

Generated from: `effortless-rulebook/effortless-rulebook.json`
