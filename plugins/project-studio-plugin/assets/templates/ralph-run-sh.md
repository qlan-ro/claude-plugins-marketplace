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
# Ralph Wrapper Script
# Combines Ralph execution instructions with project-specific CLAUDE.md

set -e

# Configuration
RALPH_DIR=".ralph"
INSTRUCTIONS_FILE="$RALPH_DIR/INSTRUCTIONS.md"
PROJECT_CLAUDE_MD="CLAUDE.md"
COMBINED_CLAUDE_MD="$RALPH_DIR/CLAUDE.md"
PROGRESS_FILE="progress.txt"
PRD_FILE="prd.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Ralph Wrapper ===${NC}"

# Create .ralph directory if it doesn't exist
if [ ! -d "$RALPH_DIR" ]; then
    echo -e "${YELLOW}Creating $RALPH_DIR directory...${NC}"
    mkdir -p "$RALPH_DIR"
fi

# Check for INSTRUCTIONS.md
if [ ! -f "$INSTRUCTIONS_FILE" ]; then
    echo -e "${RED}Error: $INSTRUCTIONS_FILE not found${NC}"
    echo "Run /start-ralph first to set up the Ralph environment"
    exit 1
fi

# Check for prd.json
if [ ! -f "$PRD_FILE" ]; then
    echo -e "${RED}Error: $PRD_FILE not found${NC}"
    echo "Run /start-ralph first to generate prd.json from your PRD"
    exit 1
fi

# Create progress.txt if it doesn't exist
if [ ! -f "$PROGRESS_FILE" ]; then
    echo -e "${YELLOW}Creating empty $PROGRESS_FILE...${NC}"
    echo "# Ralph Progress Log" > "$PROGRESS_FILE"
    echo "Started: $(date)" >> "$PROGRESS_FILE"
    echo "---" >> "$PROGRESS_FILE"
fi

# Combine INSTRUCTIONS.md with project CLAUDE.md
echo -e "${YELLOW}Combining Ralph instructions with project CLAUDE.md...${NC}"

# Start with Ralph instructions
cat "$INSTRUCTIONS_FILE" > "$COMBINED_CLAUDE_MD"

# Add separator
echo "" >> "$COMBINED_CLAUDE_MD"
echo "---" >> "$COMBINED_CLAUDE_MD"
echo "" >> "$COMBINED_CLAUDE_MD"
echo "# Project-Specific Instructions" >> "$COMBINED_CLAUDE_MD"
echo "" >> "$COMBINED_CLAUDE_MD"

# Append project CLAUDE.md if it exists
if [ -f "$PROJECT_CLAUDE_MD" ]; then
    cat "$PROJECT_CLAUDE_MD" >> "$COMBINED_CLAUDE_MD"
    echo -e "${GREEN}Combined with $PROJECT_CLAUDE_MD${NC}"
else
    echo "No project CLAUDE.md found - using Ralph instructions only" >> "$COMBINED_CLAUDE_MD"
    echo -e "${YELLOW}No $PROJECT_CLAUDE_MD found - using Ralph instructions only${NC}"
fi

echo ""
echo -e "${GREEN}Ralph environment ready!${NC}"
echo ""
echo "Files prepared:"
echo "  - $COMBINED_CLAUDE_MD (combined instructions)"
echo "  - $PRD_FILE (user stories)"
echo "  - $PROGRESS_FILE (progress log)"
echo ""
echo "To run Ralph, use:"
echo "  claude --print \"$(cat $COMBINED_CLAUDE_MD)\""
echo ""
echo "Or manually start Claude with the combined CLAUDE.md as context."
```

## What This Script Does

1. **Creates `.ralph/` directory** - Sets up the Ralph working directory
2. **Validates prerequisites** - Ensures `INSTRUCTIONS.md` and `prd.json` exist
3. **Creates `progress.txt`** - Initializes the progress log if missing
4. **Combines instructions** - Merges Ralph's execution rules with your project's `CLAUDE.md`

## Directory Structure After Running

```
your-project/
├── .ralph/
│   ├── INSTRUCTIONS.md    # Ralph execution rules (from template)
│   └── CLAUDE.md          # Combined instructions for Claude
├── prd.json               # User stories in Ralph format
├── progress.txt           # Progress log
├── CLAUDE.md              # Your project's instructions
└── run.sh                 # This script
```

## Customization

You can customize the script for your project:

- **Change file locations** - Modify the configuration variables at the top
- **Add pre-flight checks** - Add quality gate checks before Ralph starts
- **Add post-run cleanup** - Archive completed work after Ralph finishes
