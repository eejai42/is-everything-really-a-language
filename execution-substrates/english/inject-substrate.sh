#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Parse arguments
SKIP_INJECT=false
for arg in "$@"; do
    case $arg in
        --skip-inject)
            SKIP_INJECT=true
            shift
            ;;
    esac
done

# Inject data into the english substrate (unless --skip-inject)
# This generates the markdown files (specification.md, etc.) using an LLM
if [ "$SKIP_INJECT" = false ]; then
    python3 "$SCRIPT_DIR/inject-into-english.py" --regenerate || {
        INJECT_EXIT_CODE=$?
        if [ "$INJECT_EXIT_CODE" != "2" ]; then
            echo "Error during injection (exit code $INJECT_EXIT_CODE)"
            exit $INJECT_EXIT_CODE
        fi
        # Exit code 2 means markdown files already exist - continue to test
    }
fi

# Run the test for this substrate
# This uses an LLM to "execute" the English specification and compute answers
"$SCRIPT_DIR/take-test.sh"
