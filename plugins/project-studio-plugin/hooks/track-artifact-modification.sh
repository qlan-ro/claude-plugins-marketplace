#!/bin/bash
# Track artifact modifications for session history
# Called by hook when docs/**/*.md files are written/edited

FILE_PATH="$1"

# Skip if no file path provided
if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Find project root
find_project_root() {
    local dir="$PWD"
    while [ "$dir" != "/" ]; do
        if [ -d "$dir/.project-studio" ] || [ -d "$dir/docs" ]; then
            echo "$dir"
            return 0
        fi
        dir=$(dirname "$dir")
    done
    echo "$PWD"
}

PROJECT_ROOT=$(find_project_root)
STATE_FILE="$PROJECT_ROOT/.project-studio/state.yaml"

# Only track if state file exists
if [ ! -f "$STATE_FILE" ]; then
    exit 0
fi

# Check if yq is available
if ! command -v yq &> /dev/null; then
    exit 0
fi

# Get relative path from project root
REL_PATH="${FILE_PATH#$PROJECT_ROOT/}"

# Add to current session's artifacts_modified list (avoid duplicates)
EXISTING=$(yq ".current_session.artifacts_modified | any(. == \"$REL_PATH\")" "$STATE_FILE")

if [ "$EXISTING" != "true" ]; then
    yq -i ".current_session.artifacts_modified += [\"$REL_PATH\"]" "$STATE_FILE"
fi

# Update artifact checksum
CHECKSUM=$(sha256sum "$FILE_PATH" 2>/dev/null | cut -d' ' -f1 || echo "unknown")
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

yq -i ".artifacts.\"$REL_PATH\".exists = true" "$STATE_FILE"
yq -i ".artifacts.\"$REL_PATH\".last_modified = \"$TIMESTAMP\"" "$STATE_FILE"
yq -i ".artifacts.\"$REL_PATH\".checksum = \"sha256:$CHECKSUM\"" "$STATE_FILE"

exit 0
