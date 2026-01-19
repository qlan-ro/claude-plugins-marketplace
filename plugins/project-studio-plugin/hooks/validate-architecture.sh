#!/bin/bash
# Validate Architecture document structure

FILE="$1"

if [ ! -f "$FILE" ]; then
    echo "❌ Architecture file not found: $FILE"
    exit 1
fi

WARNINGS=0

# Check for required sections
check_section() {
    if ! grep -qi "## $1\|# $1" "$FILE"; then
        echo "⚠️ Consider adding section: $1"
        WARNINGS=$((WARNINGS + 1))
    fi
}

check_section "Technology Stack"
check_section "Data Model"
check_section "API"
check_section "Security"

# Check for tech stack details
if ! grep -qi "Frontend\|Backend\|Database" "$FILE"; then
    echo "⚠️ Architecture should specify Frontend, Backend, and Database choices"
    WARNINGS=$((WARNINGS + 1))
fi

# Check for rationale (why decisions were made)
if ! grep -qi "because\|rationale\|reason\|chose\|selected" "$FILE"; then
    echo "⚠️ Consider documenting rationale for technology choices"
    WARNINGS=$((WARNINGS + 1))
fi

if [ $WARNINGS -eq 0 ]; then
    echo "✅ Architecture document validated"
else
    echo "📋 Architecture document has $WARNINGS suggestion(s)"
fi

exit 0
