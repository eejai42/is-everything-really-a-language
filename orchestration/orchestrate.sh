#!/bin/bash
# =============================================================================
# ORCHESTRATE.SH
# =============================================================================
# Runs inject-substrate.sh (which also runs tests) for all execution substrates
# and then grades the results.
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SUBSTRATES_DIR="$PROJECT_ROOT/execution-substratrates"

# =============================================================================
# COLORS
# =============================================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m' # No Color

# Substrate colors (cycle through for visual distinction)
SUBSTRATE_COLORS=(
    '\033[38;5;214m'  # Orange
    '\033[38;5;118m'  # Bright green
    '\033[38;5;147m'  # Light purple
    '\033[38;5;81m'   # Sky blue
    '\033[38;5;219m'  # Pink
    '\033[38;5;228m'  # Light yellow
    '\033[38;5;123m'  # Aqua
    '\033[38;5;183m'  # Lavender
    '\033[38;5;203m'  # Coral
    '\033[38;5;157m'  # Mint
    '\033[38;5;208m'  # Dark orange
    '\033[38;5;120m'  # Light green
)

echo ""
echo -e "${BOLD}${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${CYAN}║${NC}          ${BOLD}${WHITE}EXECUTION SUBSTRATE ORCHESTRATOR${NC}                  ${BOLD}${CYAN}║${NC}"
echo -e "${BOLD}${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# -----------------------------------------------------------------------------
# Step 1: Generate answer key and blank test from database
# -----------------------------------------------------------------------------
echo -e "${BOLD}${BLUE}┌──────────────────────────────────────────────────────────────┐${NC}"
echo -e "${BOLD}${BLUE}│${NC} ${BOLD}${WHITE}STEP 1:${NC} ${YELLOW}Generating answer key and blank test...${NC}              ${BOLD}${BLUE}│${NC}"
echo -e "${BOLD}${BLUE}└──────────────────────────────────────────────────────────────┘${NC}"
python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader

# Load test-orchestrator module
spec = spec_from_loader('test_orchestrator', SourceFileLoader('test_orchestrator', '$SCRIPT_DIR/test-orchestrator.py'))
test_orch = module_from_spec(spec)
spec.loader.exec_module(test_orch)

# Run steps 1 and 2
answer_key = test_orch.generate_answer_key()
test_orch.generate_blank_test(answer_key)
"
echo ""

# -----------------------------------------------------------------------------
# Step 2: Run inject-substrate.sh for each substrate
# -----------------------------------------------------------------------------
echo -e "${BOLD}${BLUE}┌──────────────────────────────────────────────────────────────┐${NC}"
echo -e "${BOLD}${BLUE}│${NC} ${BOLD}${WHITE}STEP 2:${NC} ${YELLOW}Running inject + test for each substrate...${NC}         ${BOLD}${BLUE}│${NC}"
echo -e "${BOLD}${BLUE}└──────────────────────────────────────────────────────────────┘${NC}"
echo ""

# Get list of substrates
SUBSTRATES=$(ls -d "$SUBSTRATES_DIR"/*/ 2>/dev/null | xargs -n1 basename)

INJECT_RESULTS=""
COLOR_INDEX=0
TOTAL_SUBSTRATES=$(echo "$SUBSTRATES" | wc -w | tr -d ' ')
CURRENT=0

for substrate in $SUBSTRATES; do
    substrate_dir="$SUBSTRATES_DIR/$substrate"
    inject_script="$substrate_dir/inject-substrate.sh"
    CURRENT=$((CURRENT + 1))

    # Get color for this substrate
    COLOR="${SUBSTRATE_COLORS[$COLOR_INDEX]}"
    COLOR_INDEX=$(( (COLOR_INDEX + 1) % ${#SUBSTRATE_COLORS[@]} ))

    if [ -f "$inject_script" ]; then
        substrate_upper=$(echo "$substrate" | tr '[:lower:]' '[:upper:]')
        echo -e "${COLOR}╔══════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${COLOR}║${NC} ${BOLD}[$CURRENT/$TOTAL_SUBSTRATES]${NC} ${COLOR}▶ ${BOLD}${substrate_upper}${NC}"
        echo -e "${COLOR}╚══════════════════════════════════════════════════════════════╝${NC}"

        if bash "$inject_script"; then
            INJECT_RESULTS="$INJECT_RESULTS$substrate:OK\n"
            echo -e "  ${GREEN}✓${NC} ${substrate}: ${GREEN}${BOLD}OK${NC}"
        else
            INJECT_RESULTS="$INJECT_RESULTS$substrate:FAILED\n"
            echo -e "  ${RED}✗${NC} ${substrate}: ${RED}${BOLD}FAILED${NC}"
        fi
        echo ""
    else
        echo -e "  ${YELLOW}○${NC} ${substrate}: ${DIM}SKIPPED (no inject-substrate.sh)${NC}"
        INJECT_RESULTS="$INJECT_RESULTS$substrate:SKIPPED\n"
    fi
done

# -----------------------------------------------------------------------------
# Step 3: Grade results and generate reports
# -----------------------------------------------------------------------------
echo -e "${BOLD}${BLUE}┌──────────────────────────────────────────────────────────────┐${NC}"
echo -e "${BOLD}${BLUE}│${NC} ${BOLD}${WHITE}STEP 3:${NC} ${YELLOW}Grading results and generating reports...${NC}           ${BOLD}${BLUE}│${NC}"
echo -e "${BOLD}${BLUE}└──────────────────────────────────────────────────────────────┘${NC}"
python3 -c "
import sys
import json
sys.path.insert(0, '$SCRIPT_DIR')
from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader

# Load test-orchestrator module
spec = spec_from_loader('test_orchestrator', SourceFileLoader('test_orchestrator', '$SCRIPT_DIR/test-orchestrator.py'))
test_orch = module_from_spec(spec)
spec.loader.exec_module(test_orch)

# Load answer key
with open(test_orch.ANSWER_KEY_PATH, 'r') as f:
    answer_key = json.load(f)

# Get substrates that have test-answers.json
import os
substrates = test_orch.get_substrates()
substrate_results = {}
for substrate in substrates:
    answers_path = os.path.join(test_orch.SUBSTRATES_DIR, substrate, 'test-answers.json')
    if os.path.exists(answers_path):
        substrate_results[substrate] = {'answers_path': answers_path, 'error': None}
    else:
        substrate_results[substrate] = {'answers_path': None, 'error': 'No test-answers.json'}

# Grade all substrates
all_grades = test_orch.grade_all_substrates(answer_key, substrate_results)

# Generate summary report
test_orch.generate_summary_report(all_grades)
"
echo ""

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
echo -e "${BOLD}${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${GREEN}║${NC}              ${BOLD}${WHITE}ORCHESTRATION COMPLETE${NC}                       ${BOLD}${GREEN}║${NC}"
echo -e "${BOLD}${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}Results written to:${NC}"
echo -e "  ${DIM}•${NC} Per-substrate: ${WHITE}execution-substratrates/*/test-results.md${NC}"
echo -e "  ${DIM}•${NC} Summary:       ${WHITE}orchestration/all-tests-results.md${NC}"
echo ""
