#!/bin/bash
# Ralph Wiggum - Long-running AI agent loop
# Usage: ./ralph.sh [--tool claude] [--max-iterations N] [--single]
#
# Options:
#   --tool claude     Use Claude Code (default)
#   --max-iterations  Maximum iterations before stopping (default: 10)
#   --single          Run single iteration only (no loop)

set -e

# Configuration
TOOL="claude"
MAX_ITERATIONS=10
SINGLE_MODE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --tool)
      TOOL="$2"
      shift 2
      ;;
    --tool=*)
      TOOL="${1#*=}"
      shift
      ;;
    --max-iterations)
      MAX_ITERATIONS="$2"
      shift 2
      ;;
    --max-iterations=*)
      MAX_ITERATIONS="${1#*=}"
      shift
      ;;
    --single)
      SINGLE_MODE=true
      shift
      ;;
    *)
      # Assume it's max_iterations if it's a number (backwards compat)
      if [[ "$1" =~ ^[0-9]+$ ]]; then
        MAX_ITERATIONS="$1"
      fi
      shift
      ;;
  esac
done

# Validate tool choice
if [[ "$TOOL" != "claude" ]]; then
  echo "Error: Invalid tool '$TOOL'. Currently only 'claude' is supported."
  exit 1
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRD_FILE="$SCRIPT_DIR/prd.json"
PROGRESS_FILE="$SCRIPT_DIR/progress.txt"
ARCHIVE_DIR="$SCRIPT_DIR/archive"
LAST_BRANCH_FILE="$SCRIPT_DIR/.last-branch"

# Check required files
if [ ! -f "$PRD_FILE" ]; then
  echo -e "${RED}Error: $PRD_FILE not found${NC}"
  echo "Run /project-studio:start-ralph first to set up the environment"
  exit 1
fi

# Archive previous run if branch changed
if [ -f "$PRD_FILE" ] && [ -f "$LAST_BRANCH_FILE" ]; then
  CURRENT_BRANCH=$(jq -r '.branchName // empty' "$PRD_FILE" 2>/dev/null || echo "")
  LAST_BRANCH=$(cat "$LAST_BRANCH_FILE" 2>/dev/null || echo "")

  if [ -n "$CURRENT_BRANCH" ] && [ -n "$LAST_BRANCH" ] && [ "$CURRENT_BRANCH" != "$LAST_BRANCH" ]; then
    DATE=$(date +%Y-%m-%d)
    FOLDER_NAME=$(echo "$LAST_BRANCH" | sed 's|^ralph/||')
    ARCHIVE_FOLDER="$ARCHIVE_DIR/$DATE-$FOLDER_NAME"

    echo -e "${YELLOW}Archiving previous run: $LAST_BRANCH${NC}"
    mkdir -p "$ARCHIVE_FOLDER"
    [ -f "$PRD_FILE" ] && cp "$PRD_FILE" "$ARCHIVE_FOLDER/"
    [ -f "$PROGRESS_FILE" ] && cp "$PROGRESS_FILE" "$ARCHIVE_FOLDER/"
    echo "   Archived to: $ARCHIVE_FOLDER"

    echo "# Ralph Progress Log" > "$PROGRESS_FILE"
    echo "Started: $(date)" >> "$PROGRESS_FILE"
    echo "---" >> "$PROGRESS_FILE"
  fi
fi

# Track current branch
if [ -f "$PRD_FILE" ]; then
  CURRENT_BRANCH=$(jq -r '.branchName // empty' "$PRD_FILE" 2>/dev/null || echo "")
  if [ -n "$CURRENT_BRANCH" ]; then
    echo "$CURRENT_BRANCH" > "$LAST_BRANCH_FILE"
  fi
fi

# Initialize progress file if needed
if [ ! -f "$PROGRESS_FILE" ]; then
  echo "# Ralph Progress Log" > "$PROGRESS_FILE"
  echo "Started: $(date)" >> "$PROGRESS_FILE"
  echo "---" >> "$PROGRESS_FILE"
fi

# Function to show status and return remaining count
# Display goes to stderr, only the count goes to stdout (for capture)
show_status() {
  TOTAL=$(jq '.userStories | length' "$PRD_FILE" 2>/dev/null || echo "0")
  PASSED=$(jq '[.userStories[] | select(.passes == true)] | length' "$PRD_FILE" 2>/dev/null || echo "0")
  REMAINING=$((TOTAL - PASSED))

  echo "" >&2
  echo -e "${CYAN}📋 PRD Status:${NC}" >&2
  echo "   Total: $TOTAL | Completed: $PASSED | Remaining: $REMAINING" >&2

  if [ "$REMAINING" -gt 0 ]; then
    NEXT_STORY=$(jq -r '.userStories | map(select(.passes == false)) | sort_by(.priority) | .[0] | "\(.id): \(.title)"' "$PRD_FILE" 2>/dev/null || echo "Unknown")
    echo -e "   ${BLUE}Next: $NEXT_STORY${NC}" >&2
  fi

  echo "$REMAINING"
}

# Function to check if all stories complete
all_complete() {
  REMAINING=$(jq '[.userStories[] | select(.passes == false)] | length' "$PRD_FILE" 2>/dev/null || echo "1")
  [ "$REMAINING" -eq 0 ]
}

# Header
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           🤖 Ralph Autonomous Agent                           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"

if [ "$SINGLE_MODE" = true ]; then
  echo -e "Mode: ${CYAN}Single iteration${NC}"
else
  echo -e "Mode: ${CYAN}Loop (max $MAX_ITERATIONS iterations)${NC}"
fi

# Check if already complete
REMAINING=$(show_status)
if [ "$REMAINING" -eq 0 ]; then
  echo ""
  echo -e "${GREEN}✅ All stories complete! Nothing to do.${NC}"
  exit 0
fi

# Main loop
run_iteration() {
  local iteration=$1

  echo ""
  echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
  echo -e "${GREEN}  Iteration $iteration ${NC}"
  echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
  echo ""

  # Run Claude Code non-interactively
  # -p (print mode): exits after task completes instead of entering interactive REPL
  # --dangerously-skip-permissions: allows autonomous tool execution without prompts
  cd "$SCRIPT_DIR"
  claude -p --dangerously-skip-permissions "Read prd.json and progress.txt. Implement the next user story following the Ralph loop instructions in CLAUDE.md."

  return $?
}

if [ "$SINGLE_MODE" = true ]; then
  # Single iteration mode
  run_iteration 1

  echo ""
  REMAINING=$(show_status)
  if [ "$REMAINING" -eq 0 ]; then
    echo -e "${GREEN}✅ All stories complete!${NC}"
  else
    echo -e "${YELLOW}Story complete. Run again for next story.${NC}"
  fi
else
  # Loop mode
  for i in $(seq 1 $MAX_ITERATIONS); do
    run_iteration $i

    # Check completion after each iteration
    if all_complete; then
      echo ""
      echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
      echo -e "${GREEN}║  ✅ All stories complete! Ralph finished at iteration $i      ║${NC}"
      echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
      exit 0
    fi

    REMAINING=$(show_status)
    echo ""
    echo -e "${CYAN}Iteration $i complete. $REMAINING stories remaining.${NC}"
    echo "Continuing in 3 seconds... (Ctrl+C to stop)"
    sleep 3
  done

  echo ""
  echo -e "${YELLOW}⚠️  Reached max iterations ($MAX_ITERATIONS) without completing all stories.${NC}"
  echo "   Check $PROGRESS_FILE for status."
  echo "   Run again to continue."
  exit 1
fi
