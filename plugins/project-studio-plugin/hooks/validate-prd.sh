#!/bin/bash
# Validate Product PRD structure

FILE="$1"

if [ ! -f "$FILE" ]; then
    echo "❌ PRD file not found: $FILE"
    exit 1
fi

ERRORS=0

# Check for required sections
check_section() {
    if ! grep -q "## $1" "$FILE"; then
        echo "⚠️ Missing section: $1"
        ERRORS=$((ERRORS + 1))
    fi
}

check_section "Problem Statement"
check_section "Target Users"
check_section "Feature Backlog"
check_section "Non-Goals"
check_section "Success Criteria"

# Check for dependency-ordered backlog
if ! grep -q "### Foundation\|### Core\|### Enhanced\|### Post-MVP" "$FILE"; then
    echo "⚠️ Feature backlog should be dependency-ordered (Foundation → Core → Enhanced → Post-MVP)"
    ERRORS=$((ERRORS + 1))
fi

# Check for non-goals
if grep -q "## Non-Goals" "$FILE"; then
    NON_GOALS=$(grep -A 10 "## Non-Goals" "$FILE" | grep -c "NOT building\|NOT supporting\|NOT including\|- ")
    if [ "$NON_GOALS" -lt 1 ]; then
        echo "⚠️ Non-Goals section appears empty - explicitly state what you're NOT building"
        ERRORS=$((ERRORS + 1))
    fi
fi

if [ $ERRORS -eq 0 ]; then
    echo "✅ Product PRD structure validated"
    exit 0
else
    echo "📋 Found $ERRORS issue(s) in PRD structure"
    exit 0  # Don't fail, just warn
fi
