#!/usr/bin/env python3
# =============================================================================
# TEST ORCHESTRATOR
# =============================================================================
# Generic test framework for evaluating execution substrates.
# Compares field-by-field - no domain-specific logic in the evaluation.
# =============================================================================

import json
import os
import subprocess
import sys
from datetime import datetime

import psycopg2
from psycopg2.extras import RealDictCursor

# =============================================================================
# CONFIGURATION
# =============================================================================

# Database connection
DB_CONNECTION = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres@localhost:5432/wikidata-language-candidates"
)

# View to query for answer key
VIEW_NAME = "vw_language_candidates"

# Primary key field (used for matching records between answer key and test answers)
PRIMARY_KEY = "language_candidate_id"

# Computed columns to strip for blank test
# (These are the fields that substrates must compute)
COMPUTED_COLUMNS = [
    "family_feud_mismatch",
    "family_fued_question",
    "top_family_feud_answer",
    "has_grammar",
    "relationship_to_concept",
]

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
TESTING_DIR = os.path.join(PROJECT_ROOT, "testing")
SUBSTRATES_DIR = os.path.join(PROJECT_ROOT, "execution-substratrates")

ANSWER_KEY_PATH = os.path.join(TESTING_DIR, "answer-key.json")
BLANK_TEST_PATH = os.path.join(TESTING_DIR, "blank-test.json")
SUMMARY_PATH = os.path.join(SCRIPT_DIR, "all-tests-results.md")


# =============================================================================
# STEP 1: Generate Answer Key from Postgres
# =============================================================================

def generate_answer_key():
    """Query the view and export all data (including computed columns) to answer-key.json"""
    print(f"Step 1: Generating answer key from {VIEW_NAME}...")

    try:
        conn = psycopg2.connect(DB_CONNECTION)
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(f"SELECT * FROM {VIEW_NAME} ORDER BY {PRIMARY_KEY}")
        rows = cur.fetchall()

        # Convert to list of dicts (RealDictCursor returns dict-like rows)
        answer_key = [dict(row) for row in rows]

        # Write to file
        with open(ANSWER_KEY_PATH, 'w') as f:
            json.dump(answer_key, f, indent=2, default=str)

        print(f"  -> Exported {len(answer_key)} records to {ANSWER_KEY_PATH}")

        cur.close()
        conn.close()

        return answer_key

    except Exception as e:
        print(f"  ERROR: Failed to connect to database: {e}")
        sys.exit(1)


# =============================================================================
# STEP 2: Generate Blank Test (null placeholders for computed columns)
# =============================================================================

def generate_blank_test(answer_key):
    """Set computed columns to null in blank test (keeps structure, clears values)"""
    print(f"Step 2: Generating blank test (nulling {len(COMPUTED_COLUMNS)} computed columns)...")

    blank_test = []
    for record in answer_key:
        blank_record = dict(record)
        # Set computed columns to null (placeholder for substrate to fill in)
        for col in COMPUTED_COLUMNS:
            blank_record[col] = None
        blank_test.append(blank_record)

    with open(BLANK_TEST_PATH, 'w') as f:
        json.dump(blank_test, f, indent=2, default=str)

    print(f"  -> Exported {len(blank_test)} records to {BLANK_TEST_PATH}")
    print(f"  -> Nulled columns: {', '.join(COMPUTED_COLUMNS)}")

    return blank_test


# =============================================================================
# STEP 3: Run Each Substrate's Test
# =============================================================================

def get_substrates():
    """Get list of substrate directories"""
    substrates = []
    if os.path.isdir(SUBSTRATES_DIR):
        for name in sorted(os.listdir(SUBSTRATES_DIR)):
            path = os.path.join(SUBSTRATES_DIR, name)
            if os.path.isdir(path) and not name.startswith('.'):
                substrates.append(name)
    return substrates


def run_substrate_test(substrate_name):
    """Run a substrate's take-test.sh and return path to test-answers.json"""
    substrate_dir = os.path.join(SUBSTRATES_DIR, substrate_name)
    script_path = os.path.join(substrate_dir, "take-test.sh")
    answers_path = os.path.join(substrate_dir, "test-answers.json")

    if not os.path.exists(script_path):
        return None, f"No take-test.sh found"

    try:
        result = subprocess.run(
            ["bash", script_path],
            cwd=substrate_dir,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            return None, f"Script failed: {result.stderr}"

        if not os.path.exists(answers_path):
            return None, f"No test-answers.json generated"

        return answers_path, None

    except subprocess.TimeoutExpired:
        return None, "Script timed out"
    except Exception as e:
        return None, str(e)


def run_all_substrate_tests():
    """Run take-test.sh for each substrate"""
    print(f"Step 3: Running tests for each substrate...")

    substrates = get_substrates()
    print(f"  -> Found {len(substrates)} substrates: {', '.join(substrates)}")

    results = {}
    for substrate in substrates:
        answers_path, error = run_substrate_test(substrate)
        results[substrate] = {
            "answers_path": answers_path,
            "error": error
        }
        status = "OK" if answers_path else f"ERROR: {error}"
        print(f"  -> {substrate}: {status}")

    return results


# =============================================================================
# STEP 4: Grade Each Substrate (Generic Field-by-Field Comparison)
# =============================================================================

def load_json(path):
    """Load JSON file, return empty list if error"""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return []


def compare_values(expected, actual):
    """Compare two values, handling type differences"""
    # Convert both to strings for comparison (handles int vs str, etc.)
    return str(expected) == str(actual)


def grade_substrate(substrate_name, answer_key, answers_path):
    """
    Compare substrate's answers against answer key.
    Returns dict with detailed results.

    THIS IS GENERIC - no domain-specific logic.
    Just compares field-by-field whatever is in the JSON.
    """
    results = {
        "substrate": substrate_name,
        "total_records": len(answer_key),
        "total_fields_tested": 0,
        "fields_passed": 0,
        "fields_failed": 0,
        "failures": [],
        "error": None
    }

    if not answers_path:
        results["error"] = "No answers file"
        return results

    test_answers = load_json(answers_path)

    if not test_answers:
        results["error"] = "Could not load answers or empty file"
        return results

    # Index test answers by primary key for lookup
    answers_by_pk = {}
    for record in test_answers:
        pk = record.get(PRIMARY_KEY)
        if pk is not None:
            answers_by_pk[str(pk)] = record

    # Compare each record, field by field
    for expected_record in answer_key:
        pk = str(expected_record.get(PRIMARY_KEY))
        actual_record = answers_by_pk.get(pk, {})

        # Only check computed columns (those are what substrates must produce)
        for field in COMPUTED_COLUMNS:
            results["total_fields_tested"] += 1

            expected_val = expected_record.get(field)
            actual_val = actual_record.get(field)

            if compare_values(expected_val, actual_val):
                results["fields_passed"] += 1
            else:
                results["fields_failed"] += 1
                results["failures"].append({
                    PRIMARY_KEY: pk,
                    "field": field,
                    "expected": expected_val,
                    "actual": actual_val
                })

    return results


def generate_substrate_report(substrate_name, results):
    """Generate test-results.md for a substrate"""
    substrate_dir = os.path.join(SUBSTRATES_DIR, substrate_name)
    report_path = os.path.join(substrate_dir, "test-results.md")

    total = results["total_fields_tested"]
    passed = results["fields_passed"]
    failed = results["fields_failed"]
    score = (passed / total * 100) if total > 0 else 0

    lines = [
        f"# Test Results: {substrate_name}",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total Fields Tested | {total} |",
        f"| Passed | {passed} |",
        f"| Failed | {failed} |",
        f"| Score | {score:.1f}% |",
        "",
    ]

    if results.get("error"):
        lines.extend([
            "## Error",
            "",
            f"```",
            results["error"],
            f"```",
            "",
        ])

    if results["failures"]:
        lines.extend([
            "## Failures",
            "",
            f"| {PRIMARY_KEY} | Field | Expected | Actual |",
            f"|---------------|-------|----------|--------|",
        ])

        # Show first 50 failures to keep report manageable
        for failure in results["failures"][:50]:
            pk = failure[PRIMARY_KEY]
            field = failure["field"]
            expected = str(failure["expected"])[:40]
            actual = str(failure["actual"])[:40]
            lines.append(f"| {pk} | {field} | {expected} | {actual} |")

        if len(results["failures"]) > 50:
            lines.append(f"| ... | ... | ({len(results['failures']) - 50} more failures) | ... |")

        lines.append("")

    with open(report_path, 'w') as f:
        f.write('\n'.join(lines))

    return report_path


def grade_all_substrates(answer_key, substrate_results):
    """Grade all substrates and generate reports"""
    print(f"Step 4: Grading substrate answers...")

    all_grades = {}

    for substrate_name, run_result in substrate_results.items():
        answers_path = run_result.get("answers_path")

        grades = grade_substrate(substrate_name, answer_key, answers_path)

        if run_result.get("error"):
            grades["error"] = run_result["error"]

        all_grades[substrate_name] = grades

        report_path = generate_substrate_report(substrate_name, grades)

        total = grades["total_fields_tested"]
        passed = grades["fields_passed"]
        score = (passed / total * 100) if total > 0 else 0

        print(f"  -> {substrate_name}: {passed}/{total} ({score:.1f}%) -> {report_path}")

    return all_grades


# =============================================================================
# STEP 5: Generate Summary Report
# =============================================================================

def generate_summary_report(all_grades):
    """Generate all-tests-results.md with summary of all substrates"""
    print(f"Step 5: Generating summary report...")

    lines = [
        "# Test Orchestrator Results",
        "",
        "## Configuration",
        "",
        f"- **View:** `{VIEW_NAME}`",
        f"- **Primary Key:** `{PRIMARY_KEY}`",
        f"- **Computed Columns:** {len(COMPUTED_COLUMNS)}",
        "",
        "## Summary by Substrate",
        "",
        "| Substrate | Passed | Failed | Total | Score | Status |",
        "|-----------|--------|--------|-------|-------|--------|",
    ]

    total_passed = 0
    total_failed = 0
    total_tests = 0

    for substrate_name in sorted(all_grades.keys()):
        grades = all_grades[substrate_name]

        passed = grades["fields_passed"]
        failed = grades["fields_failed"]
        total = grades["total_fields_tested"]
        score = (passed / total * 100) if total > 0 else 0

        total_passed += passed
        total_failed += failed
        total_tests += total

        if grades.get("error"):
            status = f"ERROR: {grades['error'][:30]}"
        elif failed == 0:
            status = "PASS"
        else:
            status = "FAIL"

        lines.append(f"| {substrate_name} | {passed} | {failed} | {total} | {score:.1f}% | {status} |")

    overall_score = (total_passed / total_tests * 100) if total_tests > 0 else 0

    lines.extend([
        "",
        "## Overall Statistics",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total Substrates | {len(all_grades)} |",
        f"| Total Fields Tested | {total_tests} |",
        f"| Total Passed | {total_passed} |",
        f"| Total Failed | {total_failed} |",
        f"| Overall Score | {overall_score:.1f}% |",
        "",
        "## Computed Columns Being Tested",
        "",
    ])

    for col in COMPUTED_COLUMNS:
        lines.append(f"- `{col}`")

    lines.extend([
        "",
        "---",
        "",
        "*Generated by test-orchestrator.py*",
    ])

    with open(SUMMARY_PATH, 'w') as f:
        f.write('\n'.join(lines))

    print(f"  -> Summary written to {SUMMARY_PATH}")
    print(f"  -> Overall: {total_passed}/{total_tests} ({overall_score:.1f}%)")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 60)
    print("TEST ORCHESTRATOR")
    print("=" * 60)
    print()

    # Step 1: Generate answer key from Postgres
    answer_key = generate_answer_key()
    print()

    # Step 2: Generate blank test
    blank_test = generate_blank_test(answer_key)
    print()

    # Step 3: Run each substrate's test
    substrate_results = run_all_substrate_tests()
    print()

    # Step 4: Grade each substrate
    all_grades = grade_all_substrates(answer_key, substrate_results)
    print()

    # Step 5: Generate summary report
    generate_summary_report(all_grades)
    print()

    print("=" * 60)
    print("DONE")
    print("=" * 60)


if __name__ == "__main__":
    main()
