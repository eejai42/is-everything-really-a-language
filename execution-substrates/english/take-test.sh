#!/bin/bash

# take-test.sh for english execution substrate
# Executes the English substrate using LLM to produce test answers
#
# This substrate uses an LLM (OpenAI) to "execute" English specifications.
#
# TIMING: This script measures the FULL time including:
#   1. Injection (if glossary.md/specification.md don't exist)
#   2. Test-taking (LLM computing answers from English prose)
#
# The English substrate reads from:
#   - glossary.md (predicate definitions in plain English)
#   - specification.md (calculation instructions in plain English)
# And writes test answers to:
#   - test-answers/

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
LOG_FILE="$SCRIPT_DIR/.last-run.log"
LAST_RUN_ANSWERS="$SCRIPT_DIR/.last-run-answers"

# If running interactively (stdin is a tty), ask user before running
if [[ -t 0 ]]; then
    echo ""
    echo "english: This substrate uses LLM (OpenAI) and may take 3+ minutes."
    read -p "english: Run English substrate? [y/N] " response

    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "english: SKIPPED by user"

        # Restore previous answers if they exist
        if [[ -d "$LAST_RUN_ANSWERS" ]]; then
            echo "english: Restoring previous test answers..."
            mkdir -p "$SCRIPT_DIR/test-answers"
            cp -r "$LAST_RUN_ANSWERS/"* "$SCRIPT_DIR/test-answers/" 2>/dev/null || true
            echo "english: Previous answers restored"
        else
            echo "english: No previous answers to restore"
            mkdir -p "$SCRIPT_DIR/test-answers"
        fi

        # Signal to orchestrator that this was skipped
        echo "SUBSTRATE_SKIPPED"
        exit 0
    fi
fi

# Ensure test-answers directory exists
mkdir -p "$SCRIPT_DIR/test-answers"

# Capture output for the substrate report
{
    echo "=== English (LLM) Substrate Test Run ==="
    echo "Started: $(date)"
    echo ""

    # Check if English documents exist - if not, run injection first
    if [[ ! -f "$SCRIPT_DIR/glossary.md" ]] || [[ ! -f "$SCRIPT_DIR/specification.md" ]]; then
        echo "english: English documents not found, running injection first..."
        echo "english: This will generate glossary.md and specification.md via LLM"
        echo ""

        # Run injection with --regenerate to force generation
        python3 "$SCRIPT_DIR/inject-into-english.py" --regenerate

        if [[ $? -ne 0 ]]; then
            echo "english: ERROR - injection failed"
            exit 1
        fi
        echo ""
        echo "english: Injection complete, now running test..."
        echo ""
    fi

    # Run English substrate test (reads English docs, computes answers via LLM)
    python3 "$SCRIPT_DIR/take-test.py"

    echo ""
    echo "Completed: $(date)"
} 2>&1 | tee "$LOG_FILE"

# Save successful answers for future skip/restore
if [[ $? -eq 0 ]]; then
    rm -rf "$LAST_RUN_ANSWERS"
    mkdir -p "$LAST_RUN_ANSWERS"
    cp -r "$SCRIPT_DIR/test-answers/"* "$LAST_RUN_ANSWERS/" 2>/dev/null || true
fi

echo "english: test completed"

# Generate substrate report
python3 "$PROJECT_ROOT/orchestration/create-substrate-report.py" english --log "$LOG_FILE"
