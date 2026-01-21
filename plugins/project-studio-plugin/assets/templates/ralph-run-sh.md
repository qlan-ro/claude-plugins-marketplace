# Ralph run.sh Template

This template provides the shell script that launches Ralph autonomous execution.

## Usage

Copy this script to your project root as `run.sh` and make it executable:
```bash
chmod +x run.sh
```

Then run Ralph with:
```bash
./run.sh
```

## Template

```bash
#!/bin/bash
# Ralph Runner Script
# Combines project CLAUDE.md with Ralph instructions and starts Claude Code

set -e

# Configuration - all Ralph files live in .ralph/
RALPH_DIR=".ralph"
INSTRUCTIONS_FILE="$RALPH_DIR/INSTRUCTIONS.md"
PROJECT_CLAUDE_MD="CLAUDE.md"
COMBINED_CLAUDE_MD="$RALPH_DIR/CLAUDE.md"
PROGRESS_FILE="$RALPH_DIR/progress.txt"
PRD_FILE="$RALPH_DIR/prd.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🤖 Starting Ralph Autonomous Agent${NC}"
echo "=================================="

# Check for required files in .ralph/
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

# Start with Ralph instructions
cat "$INSTRUCTIONS_FILE" > "$COMBINED_CLAUDE_MD"
echo "" >> "$COMBINED_CLAUDE_MD"
echo "---" >> "$COMBINED_CLAUDE_MD"
echo "" >> "$COMBINED_CLAUDE_MD"

# Add project CLAUDE.md if it exists
if [ -f "$PROJECT_CLAUDE_MD" ]; then
    echo "# Project Instructions" >> "$COMBINED_CLAUDE_MD"
    echo "" >> "$COMBINED_CLAUDE_MD"
    cat "$PROJECT_CLAUDE_MD" >> "$COMBINED_CLAUDE_MD"
fi

echo -e "${GREEN}✓ Instructions combined into $COMBINED_CLAUDE_MD${NC}"

# Create progress.txt if it doesn't exist
if [ ! -f "$PROGRESS_FILE" ]; then
    echo "# Ralph Progress Log" > "$PROGRESS_FILE"
    echo "Started: $(date)" >> "$PROGRESS_FILE"
    echo "---" >> "$PROGRESS_FILE"
fi

# Show current status
echo ""
echo "📋 Current PRD Status:"
echo "----------------------"

# Count stories from .ralph/prd.json
TOTAL=$(jq '.userStories | length' "$PRD_FILE")
PASSED=$(jq '[.userStories[] | select(.passes == true)] | length' "$PRD_FILE")
REMAINING=$((TOTAL - PASSED))

echo "Total stories: $TOTAL"
echo "Completed: $PASSED"
echo "Remaining: $REMAINING"

if [ "$REMAINING" -eq 0 ]; then
    echo -e "${GREEN}✓ All stories complete!${NC}"
    exit 0
fi

# Show next story
echo ""
echo "📌 Next Story:"
jq -r '.userStories | map(select(.passes == false)) | sort_by(.priority) | .[0] | "   \(.id): \(.title)"' "$PRD_FILE"

echo ""
echo "=================================="
echo -e "${GREEN}Starting Claude Code with Ralph mode...${NC}"
echo ""

# Start Claude Code from .ralph/ directory (CLAUDE.md is auto-read)
cd "$RALPH_DIR"
claude --print "Read prd.json and progress.txt. Implement the next user story following the Ralph loop."
```

## What This Script Does

1. **Validates prerequisites** - Ensures `.ralph/INSTRUCTIONS.md` and `.ralph/prd.json` exist
2. **Combines instructions** - Merges Ralph's execution rules with your project's `CLAUDE.md`
3. **Shows status** - Displays story completion progress
4. **Launches Claude** - Runs Claude from `.ralph/` directory where `CLAUDE.md` is auto-read

## Directory Structure

All Ralph files live in `.ralph/` to avoid conflicts with your project files:

```
your-project/
├── .ralph/
│   ├── INSTRUCTIONS.md    # Ralph execution rules (from template)
│   ├── CLAUDE.md          # Combined instructions (Claude reads this)
│   ├── prd.json           # User stories in Ralph format
│   └── progress.txt       # Progress log
├── CLAUDE.md              # Your project's instructions (untouched)
└── run.sh                 # This script
```

## How It Works

1. Script runs from project root
2. Combines `.ralph/INSTRUCTIONS.md` + project `CLAUDE.md` → `.ralph/CLAUDE.md`
3. Changes directory to `.ralph/`
4. Runs `claude --print "..."`
5. Claude auto-reads `.ralph/CLAUDE.md` from current directory
6. Ralph implements stories, updating `.ralph/prd.json` and `.ralph/progress.txt`

## Benefits of .ralph/ Containment

- **No conflicts** - Your project's `CLAUDE.md` stays untouched
- **Clean separation** - Ralph workspace is isolated
- **Easy cleanup** - Just delete `.ralph/` when done (or use `/project-studio:archive-feature`)

## Customization

You can customize the script for your project:

- **Add pre-flight checks** - Add quality gate checks before Ralph starts
- **Add post-run cleanup** - Archive completed work after Ralph finishes
- **Modify the prompt** - Change the initial instruction to Claude
