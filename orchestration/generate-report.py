#!/usr/bin/env python3
# =============================================================================
# GENERATE-REPORT.PY
# =============================================================================
# Generates a comprehensive, self-contained HTML report from orchestration data.
# Includes all 12 substrates (11 generated + postgres as master/answer key).
#
# Usage: python3 generate-report.py [--output path/to/report.html]
# =============================================================================

import argparse
import glob
import json
import os
import pickle
import re
from datetime import datetime
from html import escape

# =============================================================================
# PATHS
# =============================================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
TESTING_DIR = os.path.join(PROJECT_ROOT, "testing")
ANSWER_KEYS_DIR = os.path.join(TESTING_DIR, "answer-keys")
BLANK_TESTS_DIR = os.path.join(TESTING_DIR, "blank-tests")
SUBSTRATES_DIR = os.path.join(PROJECT_ROOT, "execution-substratrates")
RULEBOOK_DIR = os.path.join(PROJECT_ROOT, "effortless-rulebook")
RULEBOOK_PATH = os.path.join(RULEBOOK_DIR, "effortless-rulebook.json")
POSTGRES_DIR = os.path.join(PROJECT_ROOT, "postgres")
DEFAULT_OUTPUT = os.path.join(SCRIPT_DIR, "orchestration-report.html")


# =============================================================================
# DATA COLLECTION
# =============================================================================

def load_rulebook():
    """Load the effortless-rulebook.json file"""
    if not os.path.exists(RULEBOOK_PATH):
        return {}
    with open(RULEBOOK_PATH, 'r') as f:
        return json.load(f)


def to_snake_case(name: str) -> str:
    """Convert PascalCase to snake_case"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def discover_entities(rulebook: dict) -> list:
    """Discover all entities from the rulebook"""
    entities = []
    skip_keys = {'$schema', 'model_name', 'Description', '_meta'}
    for key, value in rulebook.items():
        if key in skip_keys:
            continue
        if isinstance(value, dict) and 'schema' in value:
            entities.append(key)
    return entities


def to_pascal_case(name: str) -> str:
    """Convert snake_case to PascalCase"""
    return ''.join(word.capitalize() for word in name.split('_'))


def get_entity_data(rulebook: dict, entity_name: str) -> dict:
    """Get full entity data including description (handles both cases)"""
    if entity_name in rulebook:
        return rulebook[entity_name]
    # Try PascalCase
    pascal = to_pascal_case(entity_name)
    if pascal in rulebook:
        return rulebook[pascal]
    return {}


def get_entity_schema(rulebook: dict, entity_name: str) -> list:
    """Get schema for an entity (handles both cases)"""
    return get_entity_data(rulebook, entity_name).get('schema', [])


def get_entity_description(rulebook: dict, entity_name: str) -> str:
    """Get description for an entity"""
    return get_entity_data(rulebook, entity_name).get('Description', '')


def get_field_description(rulebook: dict, entity_name: str, field_name: str) -> str:
    """Get description for a field within an entity"""
    schema = get_entity_schema(rulebook, entity_name)
    # field_name is snake_case, schema field names are PascalCase
    pascal_field = to_pascal_case(field_name)
    for field in schema:
        if field['name'] == field_name or field['name'] == pascal_field:
            return field.get('Description', field.get('description', ''))
    return ''


def get_field_formula(rulebook: dict, entity_name: str, field_name: str) -> str:
    """Get formula for a field within an entity"""
    schema = get_entity_schema(rulebook, entity_name)
    pascal_field = to_pascal_case(field_name)
    for field in schema:
        if field['name'] == field_name or field['name'] == pascal_field:
            return field.get('formula', '')
    return ''


def load_metadata():
    """Load testing metadata"""
    metadata_path = os.path.join(TESTING_DIR, "_metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            return json.load(f)
    return {}


def load_answer_keys():
    """Load all answer keys"""
    answer_keys = {}
    if os.path.isdir(ANSWER_KEYS_DIR):
        for file in glob.glob(os.path.join(ANSWER_KEYS_DIR, "*.json")):
            entity = os.path.basename(file).replace('.json', '')
            with open(file, 'r') as f:
                answer_keys[entity] = json.load(f)
    return answer_keys


def get_substrates():
    """Get list of all substrates (11 generated + postgres)"""
    substrates = ['postgres']  # postgres is first (master)
    if os.path.isdir(SUBSTRATES_DIR):
        for name in sorted(os.listdir(SUBSTRATES_DIR)):
            path = os.path.join(SUBSTRATES_DIR, name)
            if os.path.isdir(path) and not name.startswith('.'):
                substrates.append(name)
    return substrates


def load_substrate_grades(substrate_name: str) -> dict:
    """Load grades for a substrate from pickle or reconstruct from results"""
    # Try pickle file first (exists during orchestration)
    if substrate_name == 'postgres':
        # Postgres is the master - always 100%
        return {
            "substrate": "postgres",
            "is_master": True,
            "total_fields_tested": 0,
            "fields_passed": 0,
            "fields_failed": 0,
            "elapsed_seconds": 0.0,
            "entities": {},
            "error": None
        }

    substrate_dir = os.path.join(SUBSTRATES_DIR, substrate_name)
    grades_file = os.path.join(substrate_dir, ".grades.pkl")

    if os.path.exists(grades_file):
        with open(grades_file, 'rb') as f:
            return pickle.load(f)

    # Try to reconstruct from test-results.md
    results_file = os.path.join(substrate_dir, "test-results.md")
    if os.path.exists(results_file):
        return parse_test_results_md(results_file, substrate_name)

    return {
        "substrate": substrate_name,
        "total_fields_tested": 0,
        "fields_passed": 0,
        "fields_failed": 0,
        "elapsed_seconds": 0.0,
        "entities": {},
        "error": "No results found"
    }


def parse_test_results_md(filepath: str, substrate_name: str) -> dict:
    """Parse test-results.md to extract grades"""
    grades = {
        "substrate": substrate_name,
        "total_fields_tested": 0,
        "fields_passed": 0,
        "fields_failed": 0,
        "elapsed_seconds": 0.0,
        "entities": {},
        "error": None
    }

    with open(filepath, 'r') as f:
        content = f.read()

    # Extract summary metrics
    total_match = re.search(r'\| Total Fields Tested \| (\d+) \|', content)
    passed_match = re.search(r'\| Passed \| (\d+) \|', content)
    failed_match = re.search(r'\| Failed \| (\d+) \|', content)
    duration_match = re.search(r'\| Duration \| ([\d.]+)s \|', content)

    if total_match:
        grades["total_fields_tested"] = int(total_match.group(1))
    if passed_match:
        grades["fields_passed"] = int(passed_match.group(1))
    if failed_match:
        grades["fields_failed"] = int(failed_match.group(1))
    if duration_match:
        grades["elapsed_seconds"] = float(duration_match.group(1))

    # Extract per-entity results
    entity_sections = re.findall(r'### (\w+)\n\n- Fields: (\d+)/(\d+)', content)
    for entity, passed, total in entity_sections:
        grades["entities"][entity] = {
            "fields_tested": int(total),
            "fields_passed": int(passed),
            "fields_failed": int(total) - int(passed),
            "failures": []
        }

    return grades


def load_substrate_test_answers(substrate_name: str) -> dict:
    """Load test answers from a substrate"""
    if substrate_name == 'postgres':
        return load_answer_keys()

    answers = {}
    answers_dir = os.path.join(SUBSTRATES_DIR, substrate_name, "test-answers")
    if os.path.isdir(answers_dir):
        for file in glob.glob(os.path.join(answers_dir, "*.json")):
            entity = os.path.basename(file).replace('.json', '')
            try:
                with open(file, 'r') as f:
                    answers[entity] = json.load(f)
            except:
                pass
    return answers


def collect_all_data():
    """Collect all data needed for the report"""
    rulebook = load_rulebook()
    metadata = load_metadata()
    answer_keys = load_answer_keys()
    substrates = get_substrates()

    # Collect schema info
    entities_schema = {}
    for entity_name in discover_entities(rulebook):
        snake_name = to_snake_case(entity_name)
        schema = rulebook.get(entity_name, {}).get('schema', [])
        entities_schema[snake_name] = {
            "pascal_name": entity_name,
            "schema": schema,
            "data": rulebook.get(entity_name, {}).get('data', [])
        }

    # Collect grades for all substrates
    all_grades = {}
    for substrate in substrates:
        grades = load_substrate_grades(substrate)

        # For postgres, calculate based on answer keys
        if substrate == 'postgres':
            total_computed = 0
            for entity, meta in metadata.items():
                computed_cols = meta.get('computed_columns', [])
                record_count = meta.get('record_count', 0)
                total_computed += len(computed_cols) * record_count
                grades["entities"][entity] = {
                    "fields_tested": len(computed_cols) * record_count,
                    "fields_passed": len(computed_cols) * record_count,
                    "fields_failed": 0,
                    "failures": [],
                    "computed_columns": computed_cols
                }
            grades["total_fields_tested"] = total_computed
            grades["fields_passed"] = total_computed

        all_grades[substrate] = grades

    # Build report data structure
    # Use model_name (Airtable base ID) as the project identifier
    model_name = rulebook.get("model_name", os.path.basename(PROJECT_ROOT))
    report_data = {
        "meta": {
            "generated_at": datetime.now().isoformat(),
            "project_name": model_name,  # Now uses Airtable base ID
            "directory_name": os.path.basename(PROJECT_ROOT),
            "rulebook_path": RULEBOOK_PATH,
            "model_name": model_name,
            "rulebook_description": rulebook.get("Description", "")
        },
        "summary": {
            "total_substrates": len(substrates),
            "passing_substrates": sum(
                1 for g in all_grades.values()
                if g["fields_failed"] == 0 and g["total_fields_tested"] > 0
            ),
            "total_entities": len(metadata),
            "total_computed_columns": sum(
                len(m.get("computed_columns", []))
                for m in metadata.values()
            ),
            "total_records": sum(
                m.get("record_count", 0)
                for m in metadata.values()
            )
        },
        "entities": {},
        "substrates": all_grades,
        "answer_keys": answer_keys
    }

    # Build entity info with answer keys and descriptions
    for entity_name, meta in metadata.items():
        computed_cols = meta.get("computed_columns", [])
        # Build computed columns with formulas and descriptions
        computed_columns_info = []
        for col in computed_cols:
            computed_columns_info.append({
                "name": col,
                "formula": get_field_formula(rulebook, entity_name, col),
                "description": get_field_description(rulebook, entity_name, col)
            })

        report_data["entities"][entity_name] = {
            "primary_key": meta.get("primary_key"),
            "computed_columns": computed_cols,
            "computed_columns_info": computed_columns_info,
            "record_count": meta.get("record_count", 0),
            "schema": entities_schema.get(entity_name, {}).get("schema", []),
            "description": get_entity_description(rulebook, entity_name),
            "answer_key": answer_keys.get(entity_name, [])
        }

    # Calculate overall stats
    total_passed = sum(g["fields_passed"] for g in all_grades.values())
    total_failed = sum(g["fields_failed"] for g in all_grades.values())
    total_tested = sum(g["total_fields_tested"] for g in all_grades.values())
    total_time = sum(g.get("elapsed_seconds", 0) for g in all_grades.values())

    report_data["summary"]["overall_score"] = (
        (total_passed / total_tested * 100) if total_tested > 0 else 0
    )
    report_data["summary"]["total_runtime_seconds"] = total_time
    report_data["summary"]["total_fields_tested"] = total_tested
    report_data["summary"]["total_passed"] = total_passed
    report_data["summary"]["total_failed"] = total_failed

    return report_data


# =============================================================================
# HTML GENERATION
# =============================================================================

def generate_html(data: dict) -> str:
    """Generate self-contained HTML report"""

    # Escape data for embedding in JS
    json_data = json.dumps(data, default=str, indent=2)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Orchestration Report - {escape(data["meta"]["project_name"])}</title>
    <style>
{get_css()}
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <h1>Orchestration Report</h1>
            <div class="header-meta">
                <span class="project-name">{escape(data["meta"]["project_name"])}</span>
                <span class="timestamp">{escape(data["meta"]["generated_at"][:19].replace('T', ' '))}</span>
            </div>
        </div>
        <button id="theme-toggle" title="Toggle dark/light mode">
            <span class="sun">&#9728;</span>
            <span class="moon">&#9790;</span>
        </button>
    </header>

    <nav class="tabs">
        <button class="tab active" data-tab="overview">Overview</button>
        <button class="tab" data-tab="entities">Entities</button>
        <button class="tab" data-tab="substrates">Substrates</button>
        <button class="tab" data-tab="details">Details</button>
    </nav>

    <main>
        <section id="overview" class="tab-content active">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value" id="passing-count">
                        {data["summary"]["passing_substrates"]} / {data["summary"]["total_substrates"]}
                    </div>
                    <div class="stat-label">Substrates Passing</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value score-{get_score_class(data["summary"]["overall_score"])}">
                        {data["summary"]["overall_score"]:.1f}%
                    </div>
                    <div class="stat-label">Overall Score</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">
                        {data["summary"]["total_runtime_seconds"]:.1f}s
                    </div>
                    <div class="stat-label">Total Runtime</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">
                        {data["summary"]["total_entities"]}
                    </div>
                    <div class="stat-label">Entities</div>
                </div>
            </div>

            <h2>Substrate Health Matrix</h2>
            <div class="matrix-container">
                <table class="health-matrix" id="health-matrix">
                    <thead>
                        <tr>
                            <th>Substrate</th>
                            {generate_entity_headers(data)}
                            <th>Score</th>
                            <th>Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        {generate_matrix_rows(data)}
                    </tbody>
                </table>
            </div>
        </section>

        <section id="entities" class="tab-content">
            <div class="entity-selector">
                <label for="entity-select">Select Entity:</label>
                <select id="entity-select">
                    {generate_entity_options(data)}
                </select>
            </div>
            <div id="entity-details"></div>
        </section>

        <section id="substrates" class="tab-content">
            <div class="substrate-selector">
                <label for="substrate-select">Select Substrate:</label>
                <select id="substrate-select">
                    {generate_substrate_options(data)}
                </select>
            </div>
            <div id="substrate-details"></div>
        </section>

        <section id="details" class="tab-content">
            <h2>Failure Details</h2>
            <div id="failure-list">
                {generate_failure_details(data)}
            </div>
        </section>
    </main>

    <footer>
        <p>Generated by ERB Test Orchestrator</p>
    </footer>

    <script>
const REPORT_DATA = {json_data};

{get_javascript()}
    </script>
</body>
</html>'''

    return html


def get_score_class(score: float) -> str:
    """Get CSS class for score coloring"""
    if score >= 100:
        return "perfect"
    elif score >= 80:
        return "good"
    elif score >= 60:
        return "warning"
    else:
        return "danger"


def generate_entity_headers(data: dict) -> str:
    """Generate table headers for entities"""
    headers = []
    for entity in sorted(data["entities"].keys()):
        headers.append(f'<th class="entity-col">{escape(entity)}</th>')
    return '\n                            '.join(headers)


def generate_matrix_rows(data: dict) -> str:
    """Generate matrix rows for each substrate"""
    rows = []
    entities = sorted(data["entities"].keys())

    for substrate_name in sorted(data["substrates"].keys()):
        grades = data["substrates"][substrate_name]
        is_master = grades.get("is_master", False)

        total = grades["total_fields_tested"]
        passed = grades["fields_passed"]
        score = (passed / total * 100) if total > 0 else 0
        elapsed = grades.get("elapsed_seconds", 0)

        row_class = "master-row" if is_master else ""
        score_class = get_score_class(score)

        cells = []

        # Substrate name cell
        substrate_label = f"{substrate_name} (master)" if is_master else substrate_name
        cells.append(f'<td class="substrate-name">{escape(substrate_label)}</td>')

        # Entity cells
        for entity in entities:
            entity_grades = grades.get("entities", {}).get(entity, {})
            e_total = entity_grades.get("fields_tested", 0)
            e_passed = entity_grades.get("fields_passed", 0)
            e_failed = entity_grades.get("fields_failed", 0)

            if is_master:
                cell_class = "cell-master"
                symbol = "&#9733;"  # star
            elif e_total == 0:
                cell_class = "cell-na"
                symbol = "&mdash;"
            elif e_failed == 0:
                cell_class = "cell-pass"
                symbol = "&#10003;"  # checkmark
            else:
                cell_class = "cell-fail"
                symbol = f"{e_failed}"

            cells.append(
                f'<td class="{cell_class}" '
                f'data-substrate="{escape(substrate_name)}" '
                f'data-entity="{escape(entity)}" '
                f'title="{e_passed}/{e_total}">{symbol}</td>'
            )

        # Score cell
        if is_master:
            cells.append('<td class="score-cell score-perfect">100%</td>')
        else:
            cells.append(f'<td class="score-cell score-{score_class}">{score:.1f}%</td>')

        # Time cell
        cells.append(f'<td class="time-cell">{elapsed:.1f}s</td>')

        rows.append(f'<tr class="{row_class}">{"".join(cells)}</tr>')

    return '\n                        '.join(rows)


def generate_entity_options(data: dict) -> str:
    """Generate <option> elements for entity selector"""
    options = []
    for entity in sorted(data["entities"].keys()):
        options.append(f'<option value="{escape(entity)}">{escape(entity)}</option>')
    return '\n                    '.join(options)


def generate_substrate_options(data: dict) -> str:
    """Generate <option> elements for substrate selector"""
    options = []
    for substrate in sorted(data["substrates"].keys()):
        is_master = data["substrates"][substrate].get("is_master", False)
        label = f"{substrate} (master)" if is_master else substrate
        options.append(f'<option value="{escape(substrate)}">{escape(label)}</option>')
    return '\n                    '.join(options)


def generate_failure_details(data: dict) -> str:
    """Generate failure detail cards"""
    failures = []

    for substrate_name, grades in sorted(data["substrates"].items()):
        if grades.get("is_master"):
            continue

        for entity_name, entity_grades in grades.get("entities", {}).items():
            for failure in entity_grades.get("failures", []):
                failures.append({
                    "substrate": substrate_name,
                    "entity": entity_name,
                    "pk": failure.get("pk"),
                    "field": failure.get("field"),
                    "expected": failure.get("expected"),
                    "actual": failure.get("actual")
                })

    if not failures:
        return '<div class="no-failures">No failures to display</div>'

    html_parts = []
    for f in failures[:50]:  # Limit to 50 failures in initial render
        html_parts.append(f'''
            <div class="failure-card">
                <div class="failure-header">
                    <span class="failure-substrate">{escape(str(f["substrate"]))}</span>
                    <span class="failure-arrow">&rarr;</span>
                    <span class="failure-entity">{escape(str(f["entity"]))}</span>
                    <span class="failure-arrow">&rarr;</span>
                    <span class="failure-field">{escape(str(f["field"]))}</span>
                </div>
                <div class="failure-body">
                    <div class="failure-row">
                        <span class="failure-label">Record:</span>
                        <span class="failure-value">{escape(str(f["pk"]))}</span>
                    </div>
                    <div class="failure-row">
                        <span class="failure-label">Expected:</span>
                        <code class="expected">{escape(str(f["expected"]))}</code>
                    </div>
                    <div class="failure-row">
                        <span class="failure-label">Actual:</span>
                        <code class="actual">{escape(str(f["actual"]))}</code>
                    </div>
                </div>
            </div>
        ''')

    if len(failures) > 50:
        html_parts.append(
            f'<div class="more-failures">...and {len(failures) - 50} more failures</div>'
        )

    return '\n'.join(html_parts)


def get_css() -> str:
    """Return embedded CSS"""
    return '''
:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f8f9fa;
    --bg-tertiary: #e9ecef;
    --text-primary: #212529;
    --text-secondary: #6c757d;
    --border-color: #dee2e6;
    --accent-color: #0d6efd;
    --success-color: #198754;
    --warning-color: #ffc107;
    --danger-color: #dc3545;
    --master-color: #6f42c1;
    --shadow: 0 2px 8px rgba(0,0,0,0.1);
    --radius: 8px;
}

[data-theme="dark"] {
    --bg-primary: #1a1a2e;
    --bg-secondary: #16213e;
    --bg-tertiary: #0f3460;
    --text-primary: #eaeaea;
    --text-secondary: #b0b0b0;
    --border-color: #3a3a5c;
    --accent-color: #4dabf7;
    --success-color: #51cf66;
    --warning-color: #fcc419;
    --danger-color: #ff6b6b;
    --master-color: #b197fc;
    --shadow: 0 2px 8px rgba(0,0,0,0.3);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg-secondary);
    color: var(--text-primary);
    line-height: 1.6;
    min-height: 100vh;
}

header {
    background: var(--bg-primary);
    border-bottom: 1px solid var(--border-color);
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: var(--shadow);
}

.header-content h1 {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
}

.header-meta {
    display: flex;
    gap: 1rem;
    font-size: 0.875rem;
    color: var(--text-secondary);
}

.project-name {
    font-weight: 500;
}

#theme-toggle {
    background: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: 50%;
    width: 40px;
    height: 40px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    transition: all 0.2s;
}

#theme-toggle:hover {
    background: var(--accent-color);
    color: white;
}

#theme-toggle .moon { display: none; }
[data-theme="dark"] #theme-toggle .sun { display: none; }
[data-theme="dark"] #theme-toggle .moon { display: inline; }

.tabs {
    display: flex;
    gap: 0;
    background: var(--bg-primary);
    padding: 0 2rem;
    border-bottom: 1px solid var(--border-color);
}

.tab {
    background: none;
    border: none;
    padding: 1rem 1.5rem;
    cursor: pointer;
    font-size: 0.9375rem;
    color: var(--text-secondary);
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
}

.tab:hover {
    color: var(--text-primary);
    background: var(--bg-secondary);
}

.tab.active {
    color: var(--accent-color);
    border-bottom-color: var(--accent-color);
    font-weight: 500;
}

main {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
}

.tab-content {
    display: none;
}

.tab-content.active {
    display: block;
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.stat-card {
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    padding: 1.5rem;
    text-align: center;
    box-shadow: var(--shadow);
}

.stat-value {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.stat-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.score-perfect { color: var(--success-color); }
.score-good { color: var(--success-color); }
.score-warning { color: var(--warning-color); }
.score-danger { color: var(--danger-color); }

h2 {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: var(--text-primary);
}

.matrix-container {
    overflow-x: auto;
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
}

.health-matrix {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
}

.health-matrix th,
.health-matrix td {
    padding: 0.75rem 1rem;
    text-align: center;
    border-bottom: 1px solid var(--border-color);
}

.health-matrix th {
    background: var(--bg-tertiary);
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
    color: var(--text-secondary);
}

.health-matrix .substrate-name {
    text-align: left;
    font-weight: 500;
}

.health-matrix .entity-col {
    min-width: 100px;
}

.cell-pass {
    background: rgba(25, 135, 84, 0.15);
    color: var(--success-color);
    font-weight: 600;
}

.cell-fail {
    background: rgba(220, 53, 69, 0.15);
    color: var(--danger-color);
    font-weight: 600;
    cursor: pointer;
}

.cell-fail:hover {
    background: rgba(220, 53, 69, 0.25);
}

.cell-na {
    color: var(--text-secondary);
}

.cell-master {
    background: rgba(111, 66, 193, 0.15);
    color: var(--master-color);
    font-weight: 600;
}

.master-row {
    background: rgba(111, 66, 193, 0.05);
}

.master-row .substrate-name {
    color: var(--master-color);
}

.score-cell {
    font-weight: 600;
}

.time-cell {
    color: var(--text-secondary);
    font-family: monospace;
}

.entity-selector,
.substrate-selector {
    margin-bottom: 1.5rem;
}

.entity-selector label,
.substrate-selector label {
    font-weight: 500;
    margin-right: 0.5rem;
}

.entity-selector select,
.substrate-selector select {
    padding: 0.5rem 1rem;
    font-size: 1rem;
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    background: var(--bg-primary);
    color: var(--text-primary);
    min-width: 200px;
}

#entity-details,
#substrate-details {
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow);
}

.schema-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1.5rem;
}

.schema-table th,
.schema-table td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid var(--border-color);
}

.schema-table th {
    background: var(--bg-tertiary);
    font-weight: 600;
    font-size: 0.875rem;
}

.type-raw {
    color: var(--text-secondary);
}

.type-calculated {
    color: var(--accent-color);
    font-weight: 500;
}

.formula-cell {
    font-family: monospace;
    font-size: 0.8125rem;
    color: var(--master-color);
}

.desc-cell {
    font-size: 0.8125rem;
    color: var(--text-secondary);
    max-width: 200px;
}

.entity-header {
    margin-bottom: 1rem;
}

.entity-header h3 {
    margin-bottom: 0.25rem;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table th,
.data-table td {
    padding: 0.5rem 0.75rem;
    text-align: left;
    border: 1px solid var(--border-color);
    font-size: 0.875rem;
}

.data-table th {
    background: var(--bg-tertiary);
    font-weight: 600;
}

.data-table .computed {
    background: rgba(13, 110, 253, 0.1);
}

.failure-card {
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    border-left: 4px solid var(--danger-color);
    border-radius: var(--radius);
    padding: 1rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow);
}

.failure-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.75rem;
    font-size: 0.9375rem;
}

.failure-substrate {
    font-weight: 600;
    color: var(--accent-color);
}

.failure-arrow {
    color: var(--text-secondary);
}

.failure-entity {
    font-weight: 500;
}

.failure-field {
    font-family: monospace;
    color: var(--danger-color);
}

.failure-body {
    font-size: 0.875rem;
}

.failure-row {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 0.25rem;
}

.failure-label {
    font-weight: 500;
    min-width: 80px;
    color: var(--text-secondary);
}

.failure-value {
    font-family: monospace;
}

code.expected {
    background: rgba(25, 135, 84, 0.15);
    color: var(--success-color);
    padding: 0.125rem 0.375rem;
    border-radius: 4px;
}

code.actual {
    background: rgba(220, 53, 69, 0.15);
    color: var(--danger-color);
    padding: 0.125rem 0.375rem;
    border-radius: 4px;
}

.no-failures {
    text-align: center;
    padding: 3rem;
    color: var(--text-secondary);
    font-size: 1.125rem;
}

.more-failures {
    text-align: center;
    padding: 1rem;
    color: var(--text-secondary);
    font-style: italic;
}

.substrate-info {
    margin-bottom: 1.5rem;
}

.substrate-stats {
    display: flex;
    gap: 2rem;
    margin-top: 0.5rem;
}

.substrate-stat {
    display: flex;
    gap: 0.5rem;
    align-items: center;
}

.substrate-stat-label {
    color: var(--text-secondary);
    font-size: 0.875rem;
}

.substrate-stat-value {
    font-weight: 600;
}

details {
    margin-bottom: 1rem;
}

summary {
    cursor: pointer;
    font-weight: 500;
    padding: 0.5rem;
    background: var(--bg-tertiary);
    border-radius: var(--radius);
    user-select: none;
}

summary:hover {
    background: var(--bg-secondary);
}

details[open] summary {
    margin-bottom: 0.5rem;
}

footer {
    text-align: center;
    padding: 2rem;
    color: var(--text-secondary);
    font-size: 0.875rem;
    border-top: 1px solid var(--border-color);
    margin-top: 2rem;
}

@media (max-width: 768px) {
    header {
        padding: 1rem;
    }

    .tabs {
        padding: 0 1rem;
        overflow-x: auto;
    }

    main {
        padding: 1rem;
    }

    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .stat-value {
        font-size: 1.5rem;
    }
}

/* Graded Test Table Styles */
.entity-test-section {
    margin-bottom: 2rem;
    padding: 1rem;
    background: var(--bg-secondary);
    border-radius: var(--radius);
    border: 1px solid var(--border-color);
}

.entity-test-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}

.entity-name {
    font-size: 1.1rem;
    font-weight: 600;
}

.entity-score {
    font-size: 0.9rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
    background: var(--bg-tertiary);
}

.entity-description {
    color: var(--text-secondary);
    font-size: 0.875rem;
    margin-bottom: 1rem;
    font-style: italic;
}

.computed-cols-info {
    margin-bottom: 1rem;
    padding: 0.75rem;
    background: var(--bg-primary);
    border-radius: 4px;
    font-size: 0.875rem;
}

.computed-cols-info ul {
    margin: 0.5rem 0 0 1.5rem;
    padding: 0;
}

.computed-cols-info li {
    margin-bottom: 0.25rem;
}

.computed-cols-info .formula {
    font-family: monospace;
    color: var(--master-color);
    background: var(--bg-tertiary);
    padding: 0.125rem 0.375rem;
    border-radius: 3px;
}

.graded-test-table {
    width: 100%;
    border-collapse: collapse;
    background: var(--bg-primary);
    border-radius: var(--radius);
    overflow: hidden;
}

.graded-test-table th,
.graded-test-table td {
    padding: 0.75rem;
    text-align: left;
    border: 1px solid var(--border-color);
}

.graded-test-table th {
    background: var(--bg-tertiary);
    font-weight: 600;
    font-size: 0.875rem;
}

.graded-test-table .computed-col-header {
    background: rgba(13, 110, 253, 0.15);
    color: var(--accent-color);
}

.graded-test-table .record-pk {
    font-family: monospace;
    font-weight: 500;
    background: var(--bg-secondary);
}

.graded-test-table .cell-passed {
    background: rgba(25, 135, 84, 0.1);
}

.graded-test-table .cell-passed .check-mark {
    color: var(--success-color);
    font-weight: bold;
    margin-right: 0.5rem;
}

.graded-test-table .cell-passed code {
    font-family: monospace;
    font-size: 0.8125rem;
    color: var(--text-primary);
}

.graded-test-table .cell-failed {
    background: rgba(220, 53, 69, 0.1);
    padding: 0.5rem;
}

.graded-test-table .expected-actual {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.25rem;
}

.graded-test-table .expected-actual:last-child {
    margin-bottom: 0;
}

.graded-test-table .expected-label,
.graded-test-table .actual-label {
    font-size: 0.75rem;
    font-weight: 500;
    min-width: 60px;
    color: var(--text-secondary);
}

.no-results {
    text-align: center;
    padding: 2rem;
    color: var(--text-secondary);
}

@media print {
    header, .tabs, footer {
        display: none;
    }

    .tab-content {
        display: block !important;
        page-break-after: always;
    }

    body {
        background: white;
        color: black;
    }
}
'''


def get_javascript() -> str:
    """Return embedded JavaScript"""
    return '''
// Theme toggle
const themeToggle = document.getElementById('theme-toggle');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

if (localStorage.getItem('theme') === 'dark' || (!localStorage.getItem('theme') && prefersDark)) {
    document.documentElement.setAttribute('data-theme', 'dark');
}

themeToggle.addEventListener('click', () => {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark');
    localStorage.setItem('theme', isDark ? 'light' : 'dark');
});

// Tab navigation
const tabs = document.querySelectorAll('.tab');
const tabContents = document.querySelectorAll('.tab-content');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const targetId = tab.dataset.tab;

        tabs.forEach(t => t.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));

        tab.classList.add('active');
        document.getElementById(targetId).classList.add('active');
    });
});

// Entity selector
const entitySelect = document.getElementById('entity-select');
const entityDetails = document.getElementById('entity-details');

function renderEntityDetails(entityName) {
    const entity = REPORT_DATA.entities[entityName];
    if (!entity) {
        entityDetails.innerHTML = '<p>Entity not found</p>';
        return;
    }

    // Entity header with description
    let html = `<div class="entity-header">
        <h3>${escapeHtml(entityName)}</h3>`;
    if (entity.description) {
        html += `<p class="entity-description">${escapeHtml(entity.description)}</p>`;
    }
    html += '</div>';

    html += '<h4>Schema</h4>';
    html += '<table class="schema-table"><thead><tr>';
    html += '<th>Field</th><th>Type</th><th>Nullable</th><th>Formula</th><th>Description</th>';
    html += '</tr></thead><tbody>';

    entity.schema.forEach(field => {
        const typeClass = field.type === 'calculated' ? 'type-calculated' : 'type-raw';
        const formula = field.formula || '&mdash;';
        const desc = field.Description || field.description || '&mdash;';
        html += `<tr>
            <td>${escapeHtml(field.name)}</td>
            <td class="${typeClass}">${escapeHtml(field.type || 'raw')}</td>
            <td>${field.nullable ? 'Yes' : 'No'}</td>
            <td class="formula-cell">${escapeHtml(formula)}</td>
            <td class="desc-cell">${escapeHtml(desc)}</td>
        </tr>`;
    });
    html += '</tbody></table>';

    // Answer key data
    html += '<h3>Answer Key Data (from PostgreSQL)</h3>';
    if (entity.answer_key && entity.answer_key.length > 0) {
        const computedCols = entity.computed_columns || [];
        const cols = Object.keys(entity.answer_key[0]);

        html += '<table class="data-table"><thead><tr>';
        cols.forEach(col => {
            const isComputed = computedCols.includes(col);
            html += `<th class="${isComputed ? 'computed' : ''}">${escapeHtml(col)}</th>`;
        });
        html += '</tr></thead><tbody>';

        entity.answer_key.forEach(row => {
            html += '<tr>';
            cols.forEach(col => {
                const isComputed = computedCols.includes(col);
                const val = row[col] !== null ? String(row[col]) : 'null';
                html += `<td class="${isComputed ? 'computed' : ''}">${escapeHtml(val)}</td>`;
            });
            html += '</tr>';
        });
        html += '</tbody></table>';
    } else {
        html += '<p>No data available</p>';
    }

    // Substrate results for this entity
    html += '<h3>Substrate Results</h3>';
    html += '<div class="substrate-entity-results">';

    Object.keys(REPORT_DATA.substrates).sort().forEach(substrate => {
        const grades = REPORT_DATA.substrates[substrate];
        const entityGrades = grades.entities ? grades.entities[entityName] : null;

        if (entityGrades) {
            const passed = entityGrades.fields_passed;
            const total = entityGrades.fields_tested;
            const score = total > 0 ? (passed / total * 100).toFixed(1) : 0;
            const status = entityGrades.fields_failed === 0 ? 'PASS' : 'FAIL';
            const statusClass = entityGrades.fields_failed === 0 ? 'score-good' : 'score-danger';

            html += `<div class="substrate-stat">
                <span class="substrate-stat-label">${escapeHtml(substrate)}:</span>
                <span class="substrate-stat-value ${statusClass}">${score}% (${status})</span>
            </div>`;
        }
    });
    html += '</div>';

    entityDetails.innerHTML = html;
}

if (entitySelect && REPORT_DATA.entities) {
    const firstEntity = Object.keys(REPORT_DATA.entities).sort()[0];
    if (firstEntity) {
        renderEntityDetails(firstEntity);
    }

    entitySelect.addEventListener('change', (e) => {
        renderEntityDetails(e.target.value);
    });
}

// Substrate selector
const substrateSelect = document.getElementById('substrate-select');
const substrateDetails = document.getElementById('substrate-details');

function renderSubstrateDetails(substrateName) {
    const substrate = REPORT_DATA.substrates[substrateName];
    if (!substrate) {
        substrateDetails.innerHTML = '<p>Substrate not found</p>';
        return;
    }

    const total = substrate.total_fields_tested;
    const passed = substrate.fields_passed;
    const failed = substrate.fields_failed;
    const score = total > 0 ? (passed / total * 100).toFixed(1) : 0;
    const elapsed = substrate.elapsed_seconds || 0;
    const isMaster = substrate.is_master;

    let statusText = isMaster ? 'MASTER (Answer Key)' : (failed === 0 ? 'PASS' : 'FAIL');
    let statusClass = isMaster ? 'score-perfect' : (failed === 0 ? 'score-good' : 'score-danger');

    let html = '<div class="substrate-info">';
    html += `<h3>${escapeHtml(substrateName)}</h3>`;
    html += '<div class="substrate-stats">';
    html += `<div class="substrate-stat">
        <span class="substrate-stat-label">Status:</span>
        <span class="substrate-stat-value ${statusClass}">${statusText}</span>
    </div>`;
    html += `<div class="substrate-stat">
        <span class="substrate-stat-label">Score:</span>
        <span class="substrate-stat-value">${score}%</span>
    </div>`;
    html += `<div class="substrate-stat">
        <span class="substrate-stat-label">Runtime:</span>
        <span class="substrate-stat-value">${elapsed.toFixed(2)}s</span>
    </div>`;
    html += '</div></div>';

    if (substrate.error) {
        html += `<div class="failure-card">
            <div class="failure-header">
                <span class="failure-field">Error</span>
            </div>
            <div class="failure-body">
                <code class="actual">${escapeHtml(substrate.error)}</code>
            </div>
        </div>`;
    }

    // Detailed Graded Test Results per Entity
    html += '<h3>Graded Test Results</h3>';

    // For each entity in the report, show the graded test
    Object.keys(REPORT_DATA.entities).sort().forEach(entityName => {
        const entity = REPORT_DATA.entities[entityName];
        const entityGrades = substrate.entities ? substrate.entities[entityName] : null;
        const answerKey = entity.answer_key || [];
        const computedCols = entity.computed_columns || [];
        const computedColsInfo = entity.computed_columns_info || [];
        const pk = entity.primary_key;

        if (computedCols.length === 0 || answerKey.length === 0) return;

        // Entity header with description
        const entityDesc = entity.description || '';
        const eTotal = entityGrades ? entityGrades.fields_tested : 0;
        const ePassed = entityGrades ? entityGrades.fields_passed : 0;
        const eFailed = entityGrades ? entityGrades.fields_failed : 0;
        const eScore = eTotal > 0 ? (ePassed / eTotal * 100).toFixed(1) : 0;
        const eClass = eFailed === 0 ? 'score-good' : 'score-danger';

        html += `<div class="entity-test-section">`;
        html += `<h4 class="entity-test-header">
            <span class="entity-name">${escapeHtml(entityName)}</span>
            <span class="entity-score ${eClass}">${ePassed}/${eTotal} (${eScore}%)</span>
        </h4>`;
        if (entityDesc) {
            html += `<p class="entity-description">${escapeHtml(entityDesc)}</p>`;
        }

        // Show computed columns being tested with formulas
        html += `<div class="computed-cols-info">
            <strong>Computed Columns Being Tested:</strong>
            <ul>`;
        computedColsInfo.forEach(col => {
            const formula = col.formula || 'N/A';
            const desc = col.description || '';
            html += `<li><code>${escapeHtml(col.name)}</code>`;
            if (formula && formula !== 'N/A') {
                html += ` = <span class="formula">${escapeHtml(formula)}</span>`;
            }
            if (desc) {
                html += ` <em>(${escapeHtml(desc)})</em>`;
            }
            html += `</li>`;
        });
        html += `</ul></div>`;

        // Build failure lookup for quick access
        const failureLookup = {};
        if (entityGrades && entityGrades.failures) {
            entityGrades.failures.forEach(f => {
                const key = `${f.pk}|${f.field}`;
                failureLookup[key] = f;
            });
        }

        // Graded test table - show all records with computed fields graded
        html += `<table class="graded-test-table">
            <thead><tr>
                <th>Record (${escapeHtml(pk || 'ID')})</th>`;
        computedCols.forEach(col => {
            html += `<th class="computed-col-header">${escapeHtml(col)}</th>`;
        });
        html += `</tr></thead><tbody>`;

        answerKey.forEach(record => {
            const pkVal = record[pk];
            html += `<tr><td class="record-pk">${escapeHtml(String(pkVal))}</td>`;

            computedCols.forEach(col => {
                const expectedVal = record[col];
                const failKey = `${pkVal}|${col}`;
                const failure = failureLookup[failKey];

                if (failure) {
                    // FAILED - show expected vs actual
                    html += `<td class="cell-failed">
                        <div class="expected-actual">
                            <span class="expected-label">Expected:</span>
                            <code class="expected">${escapeHtml(String(failure.expected))}</code>
                        </div>
                        <div class="expected-actual">
                            <span class="actual-label">Actual:</span>
                            <code class="actual">${escapeHtml(String(failure.actual))}</code>
                        </div>
                    </td>`;
                } else {
                    // PASSED
                    html += `<td class="cell-passed">
                        <span class="check-mark">&#10003;</span>
                        <code>${escapeHtml(String(expectedVal))}</code>
                    </td>`;
                }
            });
            html += `</tr>`;
        });

        html += `</tbody></table></div>`;
    });

    if (!substrate.entities || Object.keys(substrate.entities).length === 0) {
        html += '<p class="no-results">No test results available for this substrate.</p>';
    }

    substrateDetails.innerHTML = html;
}

if (substrateSelect && REPORT_DATA.substrates) {
    const firstSubstrate = Object.keys(REPORT_DATA.substrates).sort()[0];
    if (firstSubstrate) {
        renderSubstrateDetails(firstSubstrate);
    }

    substrateSelect.addEventListener('change', (e) => {
        renderSubstrateDetails(e.target.value);
    });
}

// Matrix cell click handlers
document.querySelectorAll('.cell-fail').forEach(cell => {
    cell.addEventListener('click', () => {
        const substrate = cell.dataset.substrate;
        const entity = cell.dataset.entity;

        // Switch to details tab and scroll to relevant failure
        document.querySelector('.tab[data-tab="details"]').click();

        // Could add highlighting of specific failure here
    });
});

// Utility function
function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

console.log('Orchestration Report loaded. Data:', REPORT_DATA);
'''


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Generate HTML orchestration report'
    )
    parser.add_argument(
        '--output', '-o',
        default=DEFAULT_OUTPUT,
        help=f'Output path for HTML report (default: {DEFAULT_OUTPUT})'
    )
    args = parser.parse_args()

    print("=" * 60)
    print("GENERATING ORCHESTRATION REPORT")
    print("=" * 60)
    print()

    # Collect data
    print("Collecting data from all sources...")
    data = collect_all_data()

    print(f"  - Project: {data['meta']['project_name']}")
    print(f"  - Substrates: {data['summary']['total_substrates']}")
    print(f"  - Entities: {data['summary']['total_entities']}")
    print(f"  - Overall score: {data['summary']['overall_score']:.1f}%")
    print()

    # Generate HTML
    print("Generating HTML report...")
    html = generate_html(data)

    # Write output
    output_path = args.output
    with open(output_path, 'w') as f:
        f.write(html)

    print(f"  -> Report written to: {output_path}")
    print()

    # Open in browser on macOS
    abs_path = os.path.abspath(output_path)
    import platform
    import subprocess
    if platform.system() == 'Darwin':
        print("Opening report in browser...")
        subprocess.run(['open', abs_path], check=False)
    elif platform.system() == 'Windows':
        print("Opening report in browser...")
        subprocess.run(['start', abs_path], shell=True, check=False)
    elif platform.system() == 'Linux':
        print("Opening report in browser...")
        subprocess.run(['xdg-open', abs_path], check=False)
    else:
        print(f"Open report: file://{abs_path}")

    print()
    print("=" * 60)
    print("DONE")
    print("=" * 60)


if __name__ == "__main__":
    main()
