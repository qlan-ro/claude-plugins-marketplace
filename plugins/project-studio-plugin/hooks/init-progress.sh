#!/bin/bash
# Initialize progress.txt alongside Feature PRD

PRD_FILE="$1"
DIR=$(dirname "$PRD_FILE")
PROGRESS_FILE="$DIR/progress.txt"

# Only create if doesn't exist
if [ -f "$PROGRESS_FILE" ]; then
    echo "📋 progress.txt already exists"
    exit 0
fi

# Extract feature name from directory
FEATURE_NAME=$(basename "$DIR")

# Extract story titles from PRD
STORIES=$(grep "### US-[0-9]" "$PRD_FILE" | sed 's/### /- [ ] /')

if [ -z "$STORIES" ]; then
    echo "⚠️ No stories found in PRD to add to progress.txt"
    exit 0
fi

# Create progress.txt
cat > "$PROGRESS_FILE" << EOF
# Feature: $FEATURE_NAME
# Status: Not Started

## Stories
$STORIES

## Notes
EOF

echo "✅ Created progress.txt with $(echo "$STORIES" | wc -l | tr -d ' ') stories"
