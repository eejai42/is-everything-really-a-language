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
    echo "english: This substrate uses LLM (OpenAI) to execute tests."
    echo "english: Running the test requires an LLM API call (2-5 minutes)."
    read -p "english: Run English substrate (LLM)? [y/N] " response

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

# Check if English documents exist - if not, ask before running injection
# (Must be OUTSIDE the tee block to allow interactive prompts)
if [[ ! -f "$SCRIPT_DIR/specification.md" ]]; then
    echo "english: specification.md not found."
    echo "english: Generation requires an LLM call and may take 1-2 minutes."

    # Ask before making LLM call
    if [[ -t 0 ]]; then
        read -p "english: Generate specification.md via LLM? [y/N] " gen_response
        if [[ ! "$gen_response" =~ ^[Yy]$ ]]; then
            echo "english: Generation SKIPPED by user"
            echo "english: Cannot run test without specification.md"
            echo "SUBSTRATE_SKIPPED"
            exit 0
        fi
    fi

    echo ""
    INJECT_START=$(date +%s)
    echo "english: Generating specification via LLM..."
    python3 "$SCRIPT_DIR/inject-into-english.py" --regenerate
    INJECT_STATUS=$?
    INJECT_END=$(date +%s)
    INJECT_DURATION=$((INJECT_END - INJECT_START))

    if [[ $INJECT_STATUS -ne 0 ]]; then
        echo "english: ERROR - injection failed"
        exit 1
    fi
    echo ""
    echo "english: Injection complete (${INJECT_DURATION}s), now running test..."
fi

# Capture output for the substrate report
{
    echo "=== English (LLM) Substrate Test Run ==="
    echo ""

    # Run English substrate test (reads English docs, computes answers via LLM)
    python3 "$SCRIPT_DIR/take-test.py"

    echo ""
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
