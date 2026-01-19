#!/bin/bash

# This script logs work activities to local files after each tool use in Claude Code
# PostToolUse hook provides: tool_name, tool_input, tool_output via stdin as JSON
# Environment variables: $CLAUDE_PROJECT_DIR, $CLAUDE_TOOL_NAME, $CLAUDE_FILE_PATHS

# Get current date for the log file
DATE=$(date +"%Y-%m-%d")
TIMESTAMP=$(date +"%H:%M")

# Create worklog directory if it doesn't exist
PLUGIN_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
WORKLOG_DIR="$PLUGIN_ROOT/worklog"
mkdir -p "$WORKLOG_DIR"

# Log file path
LOG_FILE="$WORKLOG_DIR/$DATE.log"

# Extract project name from CLAUDE_PROJECT_DIR
PROJECT_NAME=$(basename "$CLAUDE_PROJECT_DIR" 2>/dev/null || echo "unknown")

# Simple heuristic: Skip personal projects
case "$PROJECT_NAME" in
  *personal*|*blog*|*hobby*|*side-project*|*playground*|*test*|*tmp*)
    exit 0
    ;;
esac

# Read JSON input from stdin
INPUT_JSON=$(cat)

# Extract tool details using jq (if available) or basic parsing
if command -v jq &> /dev/null; then
    TOOL_NAME=$(echo "$INPUT_JSON" | jq -r '.tool_name // empty')
    TOOL_INPUT=$(echo "$INPUT_JSON" | jq -r '.tool_input | tostring' 2>/dev/null | head -c 200)
else
    # Fallback: use environment variable
    TOOL_NAME="$CLAUDE_TOOL_NAME"
    TOOL_INPUT="(details in Claude Code session)"
fi

# Only log meaningful work actions (skip reads/searches)
case "$TOOL_NAME" in
  bash_tool|str_replace|create_file|jetbrains:*)
    # These are actual work actions
    ;;
  view|Notion:notion-fetch|Notion:notion-search)
    # Skip read-only operations
    exit 0
    ;;
  *)
    # For unknown tools, log them
    ;;
esac

# Get affected files from environment variable
FILES="${CLAUDE_FILE_PATHS:-no files}"

# Create log entry
LOG_ENTRY="[$TIMESTAMP] $PROJECT_NAME
Tool: $TOOL_NAME
Files: $FILES
Details: $TOOL_INPUT
---"

# Create log file with header if it doesn't exist
if [ ! -f "$LOG_FILE" ]; then
    echo "Work Activity Log for $DATE" > "$LOG_FILE"
    echo "" >> "$LOG_FILE"
fi

# Append the log entry to the file
echo "$LOG_ENTRY" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Exit successfully (don't interrupt Claude Code)
exit 0
