#!/bin/bash
# =============================================================================
# START.SH - ERB WikiData Universal Entry Point
# =============================================================================
# All operations accessible from this single script.
# Phases implemented:
#   - Phase 1: Unified CLI entry point
#   - Phase 2: SSoTME detection with graceful fallback
#   - Phase 3: Airtable base swapping
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SSOTME_JSON="$SCRIPT_DIR/ssotme.json"
RULEBOOK_JSON="$SCRIPT_DIR/effortless-rulebook/effortless-rulebook.json"

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

# =============================================================================
# STATE TRACKING
# =============================================================================
SSOTME_AVAILABLE=false
POSTGRES_AVAILABLE=false
CI_MODE=false

# =============================================================================
# PARSE ARGUMENTS
# =============================================================================
while [[ $# -gt 0 ]]; do
    case $1 in
        --ci)
            CI_MODE=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# =============================================================================
# PHASE 2: SSoTME DETECTION
# =============================================================================
check_ssotme() {
    if command -v ssotme &> /dev/null; then
        SSOTME_AVAILABLE=true
        return 0
    else
        SSOTME_AVAILABLE=false
        return 1
    fi
}

# =============================================================================
# POSTGRESQL DETECTION
# =============================================================================
check_postgres() {
    if command -v psql &> /dev/null; then
        POSTGRES_AVAILABLE=true
        return 0
    else
        POSTGRES_AVAILABLE=false
        return 1
    fi
}

# =============================================================================
# PHASE 3: BASE ID MANAGEMENT
# =============================================================================
get_current_base_id() {
    if [ -f "$SSOTME_JSON" ]; then
        python3 -c "
import json
with open('$SSOTME_JSON', 'r') as f:
    config = json.load(f)
for setting in config.get('ProjectSettings', []):
    if setting.get('Name') == 'baseId':
        print(setting.get('Value', ''))
        break
"
    else
        echo ""
    fi
}

get_project_name() {
    if [ -f "$SSOTME_JSON" ]; then
        python3 -c "
import json
with open('$SSOTME_JSON', 'r') as f:
    config = json.load(f)
print(config.get('Name', 'Unknown'))
"
    else
        echo "Unknown"
    fi
}

set_base_id() {
    local new_base_id="$1"
    if [ -f "$SSOTME_JSON" ]; then
        python3 -c "
import json

with open('$SSOTME_JSON', 'r') as f:
    config = json.load(f)

# Update baseId in ProjectSettings
for setting in config.get('ProjectSettings', []):
    if setting.get('Name') == 'baseId':
        setting['Value'] = '$new_base_id'
        break

with open('$SSOTME_JSON', 'w') as f:
    json.dump(config, f, indent=2)

print('Base ID updated to: $new_base_id')
"
    else
        echo -e "${RED}Error: ssotme.json not found${NC}"
        return 1
    fi
}

# =============================================================================
# MENU ACTIONS
# =============================================================================

action_setup_ssotme() {
    echo ""
    echo -e "${BOLD}${CYAN}SSoTME Installation Instructions${NC}"
    echo ""
    echo -e "SSoTME (Single Source of Truth Made Easy) is required for:"
    echo -e "  ${DIM}-${NC} Pulling data from Airtable"
    echo -e "  ${DIM}-${NC} Regenerating code from rulebook changes"
    echo ""
    echo -e "${YELLOW}To install SSoTME:${NC}"
    echo ""
    echo -e "  1. Visit: ${CYAN}https://www.ssotme.com${NC}"
    echo -e "  2. Follow the installation instructions for your platform"
    echo -e "  3. Run ${WHITE}ssotme --version${NC} to verify installation"
    echo ""
    echo -e "${DIM}Note: You can still run substrate tests without SSoTME using existing files.${NC}"
    echo ""
    read -p "Press Enter to continue..."
}

action_pull_from_airtable() {
    if ! $SSOTME_AVAILABLE; then
        echo ""
        echo -e "${RED}SSoTME is not installed.${NC}"
        echo -e "Run option [1] to see installation instructions."
        echo ""
        read -p "Press Enter to continue..."
        return
    fi

    local current_base=$(get_current_base_id)
    echo ""
    echo -e "${BOLD}${CYAN}Pull/Update from Airtable${NC}"
    echo ""
    echo -e "Current Base ID: ${WHITE}$current_base${NC}"
    echo ""

    echo ""
    echo -e "${YELLOW}Running ssotme -buildall...${NC}"
    echo ""

    cd "$SCRIPT_DIR"
    ssotme -buildall

    echo ""
    echo -e "${GREEN}Pull complete!${NC}"
    echo ""
    if ! $CI_MODE; then
        read -p "Press Enter to continue..."
    fi
}

action_change_base_id() {
    if ! $SSOTME_AVAILABLE; then
        echo ""
        echo -e "${RED}SSoTME is not installed.${NC}"
        echo -e "Base swapping requires SSoTME to regenerate code after changing the base."
        echo -e "Run option [1] to see installation instructions."
        echo ""
        read -p "Press Enter to continue..."
        return
    fi

    local current_base=$(get_current_base_id)
    echo ""
    echo -e "${BOLD}${CYAN}Change Airtable Base ID${NC}"
    echo ""
    echo -e "Current Base ID: ${WHITE}$current_base${NC}"
    echo ""
    echo -e "${YELLOW}Enter new Airtable Base ID (or press Enter to cancel):${NC}"
    read -p "> " new_base_id

    if [ -z "$new_base_id" ]; then
        echo "Cancelled."
        return
    fi

    # Validate format (Airtable base IDs start with 'app')
    if [[ ! "$new_base_id" =~ ^app[A-Za-z0-9]+ ]]; then
        echo ""
        echo -e "${RED}Invalid Base ID format.${NC}"
        echo -e "Airtable Base IDs typically start with 'app' followed by alphanumeric characters."
        echo -e "Example: appC8XTj95lubn6hz"
        echo ""
        read -p "Press Enter to continue..."
        return
    fi

    echo ""
    echo -e "${YELLOW}Updating base ID to: ${WHITE}$new_base_id${NC}"
    set_base_id "$new_base_id"

    echo ""
    echo -e "${YELLOW}Regenerating from new base...${NC}"
    echo ""

    cd "$SCRIPT_DIR"
    ssotme -buildall

    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}Base swap complete!${NC}"
        echo -e "New Base ID: ${WHITE}$new_base_id${NC}"
    else
        echo ""
        echo -e "${RED}Regeneration failed.${NC}"
        echo -e "You may need to restore the previous base ID: ${WHITE}$current_base${NC}"
    fi

    echo ""
    read -p "Press Enter to continue..."
}

action_init_postgres() {
    if ! $POSTGRES_AVAILABLE; then
        echo ""
        echo -e "${RED}PostgreSQL (psql) is not installed or not in PATH.${NC}"
        echo ""
        echo -e "${YELLOW}To install PostgreSQL:${NC}"
        echo -e "  macOS:  ${WHITE}brew install postgresql${NC}"
        echo -e "  Ubuntu: ${WHITE}sudo apt install postgresql${NC}"
        echo ""
        read -p "Press Enter to continue..."
        return
    fi

    echo ""
    echo -e "${BOLD}${CYAN}Initialize PostgreSQL Database${NC}"
    echo ""

    local init_script="$SCRIPT_DIR/postgres/init-db.sh"

    if [ ! -f "$init_script" ]; then
        echo -e "${RED}Error: init-db.sh not found at $init_script${NC}"
        read -p "Press Enter to continue..."
        return
    fi

    echo -e "${YELLOW}This will:${NC}"
    echo -e "  1. Drop existing tables (if any)"
    echo -e "  2. Create tables, functions, and views"
    echo -e "  3. Insert seed data"
    echo -e "  4. Run substrate tests"
    echo ""

    if ! $CI_MODE; then
        read -p "Proceed? [Y/n]: " confirm
        if [[ "$confirm" =~ ^[Nn]$ ]]; then
            echo "Cancelled."
            return
        fi
    fi

    echo ""
    bash "$init_script"

    echo ""
    if ! $CI_MODE; then
        read -p "Press Enter to continue..."
    fi
}

action_run_tests() {
    echo ""
    echo -e "${BOLD}${CYAN}Run Substrate Tests${NC}"
    echo ""

    local orchestrate_script="$SCRIPT_DIR/orchestration/orchestrate.sh"

    if [ ! -f "$orchestrate_script" ]; then
        echo -e "${RED}Error: orchestrate.sh not found at $orchestrate_script${NC}"
        read -p "Press Enter to continue..."
        return
    fi

    bash "$orchestrate_script"

    echo ""
    if ! $CI_MODE; then
        read -p "Press Enter to continue..."
    fi
}

action_view_results() {
    echo ""
    echo -e "${BOLD}${CYAN}View Results${NC}"
    echo ""

    local summary_file="$SCRIPT_DIR/orchestration/all-tests-results.md"

    if [ -f "$summary_file" ]; then
        echo -e "${GREEN}Summary Report:${NC} $summary_file"
        echo ""
        echo -e "${DIM}--- First 50 lines ---${NC}"
        head -50 "$summary_file"
        echo ""
        echo -e "${DIM}(Use your editor to view the full report)${NC}"
    else
        echo -e "${YELLOW}No summary report found.${NC}"
        echo -e "Run substrate tests first to generate results."
    fi

    echo ""
    echo -e "${GREEN}Per-substrate reports:${NC}"
    for report in "$SCRIPT_DIR"/execution-substratrates/*/test-results.md; do
        if [ -f "$report" ]; then
            echo -e "  ${DIM}-${NC} $report"
        fi
    done

    echo ""
    read -p "Press Enter to continue..."
}

action_clean() {
    echo ""
    echo -e "${BOLD}${CYAN}Clean Generated Files${NC}"
    echo ""
    echo -e "${YELLOW}This will clean all generated files from substrates.${NC}"
    echo ""

    if ! $CI_MODE; then
        read -p "Proceed? [Y/n]: " confirm
        if [[ "$confirm" =~ ^[Nn]$ ]]; then
            echo "Cancelled."
            return
        fi
    fi

    echo ""

    # Delegate to orchestrate.sh clean mode
    cd "$SCRIPT_DIR/orchestration"
    echo "C" | bash orchestrate.sh

    echo ""
    if ! $CI_MODE; then
        read -p "Press Enter to continue..."
    fi
}

# =============================================================================
# MAIN MENU
# =============================================================================

show_header() {
    clear
    echo ""
    echo -e "${BOLD}${CYAN}================================================================${NC}"
    echo -e "${BOLD}${CYAN}      ERB WikiData - Universal Entry Point${NC}"
    echo -e "${BOLD}${CYAN}================================================================${NC}"
    echo ""

    # Show current state
    local project_name=$(get_project_name)
    local current_base=$(get_current_base_id)

    echo -e "  Project:    ${WHITE}$project_name${NC}"
    echo -e "  Base ID:    ${WHITE}$current_base${NC}"
    echo ""

    # Show tool availability
    echo -e "  ${BOLD}Tool Status:${NC}"
    if $SSOTME_AVAILABLE; then
        echo -e "    SSoTME:     ${GREEN}Available${NC}"
    else
        echo -e "    SSoTME:     ${YELLOW}Not installed${NC} ${DIM}(Airtable sync disabled)${NC}"
    fi

    if $POSTGRES_AVAILABLE; then
        echo -e "    PostgreSQL: ${GREEN}Available${NC}"
    else
        echo -e "    PostgreSQL: ${YELLOW}Not installed${NC} ${DIM}(DB init disabled)${NC}"
    fi

    echo ""
    echo -e "${BOLD}${CYAN}----------------------------------------------------------------${NC}"
}

show_menu() {
    echo ""
    echo -e "${BOLD}${WHITE}Select an option:${NC}"
    echo ""

    # Primary options (always available)
    echo -e "  ${GREEN}[1]${NC} Run Substrate Tests ${DIM}(default - press Enter)${NC}"
    echo -e "  ${CYAN}[2]${NC} View Results"
    echo ""

    # Separator
    echo -e "  ${DIM}────────────────────────────────────────${NC}"
    echo ""

    # SSoTME options
    if $SSOTME_AVAILABLE; then
        echo -e "  ${CYAN}[3]${NC} Pull/Update from Airtable"
        echo -e "  ${CYAN}[4]${NC} Change Airtable Base ID"
    else
        echo -e "  ${DIM}[3] Pull/Update from Airtable (requires SSoTME)${NC}"
        echo -e "  ${DIM}[4] Change Airtable Base ID (requires SSoTME)${NC}"
    fi

    echo -e "  ${CYAN}[5]${NC} Clean Generated Files"
    echo ""
    echo -e "  ${RED}[Q]${NC} Quit"
    echo ""
}

main() {
    # Check tool availability
    check_ssotme
    check_postgres

    # CI mode: run tests and exit
    if $CI_MODE; then
        echo -e "${BOLD}Running in CI mode...${NC}"
        action_run_tests
        exit $?
    fi

    # Interactive menu loop
    while true; do
        show_header
        show_menu

        read -p "Enter choice [1-5, Q] (default: 1): " choice

        # Default to 1 if user just presses Enter
        if [ -z "$choice" ]; then
            choice="1"
        fi

        case $choice in
            1)
                action_run_tests
                ;;
            2)
                action_view_results
                ;;
            3)
                if $SSOTME_AVAILABLE; then
                    action_pull_from_airtable
                else
                    action_setup_ssotme
                fi
                ;;
            4)
                if $SSOTME_AVAILABLE; then
                    action_change_base_id
                else
                    echo ""
                    echo -e "${RED}SSoTME is required for this option.${NC}"
                    read -p "Press Enter to continue..."
                fi
                ;;
            5)
                action_clean
                ;;
            [Qq])
                echo ""
                echo -e "${GREEN}Goodbye!${NC}"
                echo ""
                exit 0
                ;;
            *)
                echo ""
                echo -e "${RED}Invalid option: $choice${NC}"
                sleep 1
                ;;
        esac
    done
}

# Run main
main
