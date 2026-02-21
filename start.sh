#!/bin/bash
# =============================================================================
# START.SH - ERB Dev-Ops Entry Point
# =============================================================================
# Handles dev-ops tasks (PostgreSQL, SSoTME setup) and launches orchestration.
# All orchestration work (Airtable, tests, reports) is handled by orchestrate.sh
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SSOTME_JSON="$SCRIPT_DIR/ssotme.json"

# =============================================================================
# COLORS
# =============================================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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
# TOOL DETECTION
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

check_postgres() {
    if command -v psql &> /dev/null; then
        POSTGRES_AVAILABLE=true
        return 0
    else
        POSTGRES_AVAILABLE=false
        return 1
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

# =============================================================================
# DEV-OPS ACTIONS
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
    echo ""

    read -p "Proceed? [Y/n]: " confirm
    if [[ "$confirm" =~ ^[Nn]$ ]]; then
        echo "Cancelled."
        return
    fi

    echo ""
    bash "$init_script"

    echo ""
    read -p "Press Enter to continue..."
}

action_run_orchestration() {
    local orchestrate_script="$SCRIPT_DIR/orchestration/orchestrate.sh"

    if [ ! -f "$orchestrate_script" ]; then
        echo -e "${RED}Error: orchestrate.sh not found at $orchestrate_script${NC}"
        read -p "Press Enter to continue..."
        return
    fi

    # Pass SSoTME availability to orchestrate.sh via environment
    export SSOTME_AVAILABLE
    bash "$orchestrate_script"
}

# =============================================================================
# MAIN MENU
# =============================================================================

show_header() {
    clear

    local project_name=$(get_project_name)

    echo ""
    echo -e "${BOLD}${CYAN}================================================================${NC}"
    echo -e "${BOLD}${CYAN}      ${project_name} - Dev-Ops Entry Point${NC}"
    echo -e "${BOLD}${CYAN}================================================================${NC}"
    echo ""
}

show_menu() {
    echo -e "${BOLD}${WHITE}Select an option:${NC}"
    echo ""

    # Primary action - orchestration
    echo -e "  [${GREEN}O${NC}] Orchestration Menu ${DIM}(default - press Enter)${NC}"
    echo -e "      ${DIM}Run tests, pull from Airtable, view results, etc.${NC}"
    echo ""

    # Separator
    echo -e "  ${DIM}────────────────────────────────────────${NC}"
    echo -e "  ${BOLD}Dev-Ops:${NC}"
    echo ""

    # PostgreSQL
    if $POSTGRES_AVAILABLE; then
        echo -e "  [${CYAN}I${NC}] Initialize PostgreSQL Database"
    else
        echo -e "  ${DIM}[I] Initialize PostgreSQL (not installed)${NC}"
    fi

    # SSoTME setup
    if $SSOTME_AVAILABLE; then
        echo -e "  ${DIM}[S] SSoTME Setup (already installed)${NC}"
    else
        echo -e "  [${CYAN}S${NC}] SSoTME Setup Instructions"
    fi

    echo ""
    echo -e "  [${RED}Q${NC}] Quit"
    echo ""

    # Tool Status
    echo -e "  ${DIM}────────────────────────────────────────${NC}"
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
}

main() {
    # Check tool availability
    check_ssotme
    check_postgres

    # CI mode: run orchestration and exit
    if $CI_MODE; then
        echo -e "${BOLD}Running in CI mode...${NC}"
        export SSOTME_AVAILABLE
        bash "$SCRIPT_DIR/orchestration/orchestrate.sh" --ci
        exit $?
    fi

    # Interactive menu loop
    while true; do
        show_header
        show_menu

        read -p "Enter choice [O/I/S/Q] (default: O): " choice

        # Default to O if user just presses Enter
        if [ -z "$choice" ]; then
            choice="O"
        fi

        case $choice in
            [Oo])
                action_run_orchestration
                ;;
            [Ii])
                if $POSTGRES_AVAILABLE; then
                    action_init_postgres
                else
                    echo ""
                    echo -e "${RED}PostgreSQL is not installed.${NC}"
                    read -p "Press Enter to continue..."
                fi
                ;;
            [Ss])
                action_setup_ssotme
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
