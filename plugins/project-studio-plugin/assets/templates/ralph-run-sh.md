# Ralph run.sh Template

This template provides the shell script that launches Ralph autonomous execution.

## Usage

Copy this script to your project's `.ralph/` directory as `run.sh` and make it executable:
```bash
chmod +x .ralph/run.sh
```

Then run Ralph with:
```bash
./.ralph/run.sh           # Loop mode (default)
./.ralph/run.sh --single  # Single story only
```

## Template

```bash
#!/bin/bash
# Ralph Runner Script
# Combines project CLAUDE.md with Ralph instructions and starts Claude Code
#
# Usage:
#   ./run.sh              Run loop until all stories complete (max 10 iterations)
#   ./run.sh --single     Run single story only
#   ./run.sh --max 5      Set max iterations to 5

set -e

# Configuration
RALPH_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$RALPH_DIR")"
INSTRUCTIONS_FILE="$RALPH_DIR/INSTRUCTIONS.md"
PROJECT_CLAUDE_MD="$PROJECT_ROOT/CLAUDE.md"
COMBINED_CLAUDE_MD="$RALPH_DIR/CLAUDE.md"
PROGRESS_FILE="$RALPH_DIR/progress.txt"
PRD_FILE="$RALPH_DIR/prd.json"

# Options
MAX_ITERATIONS=10
SINGLE_MODE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --single)
      SINGLE_MODE=true
      shift
      ;;
    --max)
      MAX_ITERATIONS="$2"
      shift 2
      ;;
    --max=*)
      MAX_ITERATIONS="${1#*=}"
      shift
      ;;
    *)
      shift
      ;;
  esac
done

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           🤖 Ralph Autonomous Agent                           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"

# Check for required files
if [ ! -f "$PRD_FILE" ]; then
    echo -e "${RED}Error: $PRD_FILE not found${NC}"
    echo "Run /project-studio:start-ralph first to set up the environment"
    exit 1
fi

if [ ! -f "$INSTRUCTIONS_FILE" ]; then
    echo -e "${RED}Error: $INSTRUCTIONS_FILE not found${NC}"
    echo "Run /project-studio:start-ralph first to set up the environment"
    exit 1
fi

# Combine CLAUDE.md files for Ralph
echo "Combining instructions..."
cat "$INSTRUCTIONS_FILE" > "$COMBINED_CLAUDE_MD"
echo -e "\n---\n" >> "$COMBINED_CLAUDE_MD"

if [ -f "$PROJECT_CLAUDE_MD" ]; then
    echo "# Project Instructions" >> "$COMBINED_CLAUDE_MD"
    echo "" >> "$COMBINED_CLAUDE_MD"
    cat "$PROJECT_CLAUDE_MD" >> "$COMBINED_CLAUDE_MD"
fi

echo -e "${GREEN}✓ Instructions combined${NC}"

# Create progress.txt if it doesn't exist
if [ ! -f "$PROGRESS_FILE" ]; then
    echo "# Ralph Progress Log" > "$PROGRESS_FILE"
    echo "Started: $(date)" >> "$PROGRESS_FILE"
    echo "---" >> "$PROGRESS_FILE"
fi

# Function to show status and return remaining count
show_status() {
    TOTAL=$(jq '.userStories | length' "$PRD_FILE" 2>/dev/null || echo "0")
    PASSED=$(jq '[.userStories[] | select(.passes == true)] | length' "$PRD_FILE" 2>/dev/null || echo "0")
    REMAINING=$((TOTAL - PASSED))

    echo ""
    echo -e "${CYAN}📋 PRD Status:${NC}"
    echo "   Total: $TOTAL | Completed: $PASSED | Remaining: $REMAINING"

    if [ "$REMAINING" -gt 0 ]; then
        NEXT_STORY=$(jq -r '.userStories | map(select(.passes == false)) | sort_by(.priority) | .[0] | "\(.id): \(.title)"' "$PRD_FILE" 2>/dev/null || echo "Unknown")
        echo -e "   ${BLUE}Next: $NEXT_STORY${NC}"
    fi

    echo "$REMAINING"
}

# Function to check if all stories complete
all_complete() {
    REMAINING=$(jq '[.userStories[] | select(.passes == false)] | length' "$PRD_FILE" 2>/dev/null || echo "1")
    [ "$REMAINING" -eq 0 ]
}

# Show mode
if [ "$SINGLE_MODE" = true ]; then
    echo -e "Mode: ${CYAN}Single iteration${NC}"
else
    echo -e "Mode: ${CYAN}Loop (max $MAX_ITERATIONS iterations)${NC}"
fi

# Check initial status
REMAINING=$(show_status)
if [ "$REMAINING" -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ All stories complete! Nothing to do.${NC}"
    exit 0
fi

# Function to run one iteration
run_iteration() {
    local iteration=$1

    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  Iteration $iteration ${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""

    # Run Claude Code from .ralph/ directory
    # - NO --print flag: allows tool execution with streaming output
    # - --dangerously-skip-permissions: autonomous tool execution
    cd "$RALPH_DIR"
    claude --dangerously-skip-permissions \
        "Read prd.json and progress.txt. Implement the next user story following the Ralph loop instructions in CLAUDE.md."

    return $?
}

# Main execution
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
```

## What This Script Does

1. **Validates prerequisites** - Ensures `.ralph/INSTRUCTIONS.md` and `.ralph/prd.json` exist
2. **Combines instructions** - Merges Ralph's execution rules with your project's `CLAUDE.md`
3. **Shows status** - Displays story completion progress with colors
4. **Streams output** - You see Claude's work in real-time as it happens
5. **Loops automatically** - Continues until all stories complete or max iterations reached

## Directory Structure

All Ralph files live in `.ralph/` to avoid conflicts with your project files:

```
your-project/
├── .ralph/
│   ├── run.sh            # This script
│   ├── INSTRUCTIONS.md   # Ralph execution rules (from template)
│   ├── CLAUDE.md         # Combined instructions (auto-generated)
│   ├── prd.json          # User stories in Ralph format
│   └── progress.txt      # Progress log
├── CLAUDE.md             # Your project's instructions (untouched)
└── src/                  # Your code
```

## Execution Modes

### Loop Mode (Default)
```bash
./.ralph/run.sh
```
- Runs iterations until all stories have `passes: true`
- Shows status between iterations
- 3-second pause between iterations (Ctrl+C to stop)
- Stops at max iterations (default 10)

### Single Mode
```bash
./.ralph/run.sh --single
```
- Implements ONE story and exits
- Useful for reviewing changes between stories
- Run again to continue to next story

### Custom Max Iterations
```bash
./.ralph/run.sh --max 5
```

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│  1. Combine Instructions                                         │
│     .ralph/INSTRUCTIONS.md + CLAUDE.md → .ralph/CLAUDE.md       │
├─────────────────────────────────────────────────────────────────┤
│  2. Show Status                                                  │
│     Read prd.json, display progress                             │
├─────────────────────────────────────────────────────────────────┤
│  3. Run Claude (streaming output)                                │
│     claude --dangerously-skip-permissions "..."                 │
│     ├─ Reads prd.json, progress.txt                             │
│     ├─ Implements next story                                    │
│     ├─ Runs tests                                               │
│     ├─ Commits changes                                          │
│     ├─ Updates prd.json (passes: true)                          │
│     └─ Updates progress.txt                                     │
├─────────────────────────────────────────────────────────────────┤
│  4. Check Completion                                             │
│     All stories passes: true? → Exit                            │
│     Stories remaining? → Loop back to step 2                    │
└─────────────────────────────────────────────────────────────────┘
```

## Key Changes from Previous Version

| Before | After |
|--------|-------|
| `--print` flag (no tool execution) | No `--print` (tools execute) |
| No output until done | **Streaming output in real-time** |
| Single iteration only | **Loop mode with auto-continue** |
| Check `<promise>COMPLETE</promise>` | Check `prd.json` for completion |

## Troubleshooting

### Script hangs on startup
- MCP servers may be slow to initialize
- Try: `claude --mcp-servers "" --dangerously-skip-permissions "test"`

### Claude exits without completing story
- Check `.ralph/progress.txt` for errors
- Run again - Ralph will pick up where it left off

### Want to stop between stories
- Use `--single` mode
- Or press Ctrl+C during the 3-second pause

## Benefits of .ralph/ Containment

- **No conflicts** - Your project's `CLAUDE.md` stays untouched
- **Clean separation** - Ralph workspace is isolated
- **Easy cleanup** - Just delete `.ralph/` when done (or use `/project-studio:archive-feature`)
