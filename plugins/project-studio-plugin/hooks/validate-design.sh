#!/bin/bash
# Validate Design document structure

FILE="$1"

if [ ! -f "$FILE" ]; then
    echo "❌ Design file not found: $FILE"
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

check_section "User Flow"
check_section "Screen"
check_section "Design Token\|Color\|Typography"
check_section "Component"

# Check for responsive considerations
if ! grep -qi "responsive\|breakpoint\|mobile\|tablet\|desktop" "$FILE"; then
    echo "⚠️ Consider documenting responsive behavior"
    WARNINGS=$((WARNINGS + 1))
fi

# Check for navigation
if ! grep -qi "navigation\|sidebar\|menu\|nav" "$FILE"; then
    echo "⚠️ Consider documenting navigation structure"
    WARNINGS=$((WARNINGS + 1))
fi

if [ $WARNINGS -eq 0 ]; then
    echo "✅ Design document validated"
else
    echo "📋 Design document has $WARNINGS suggestion(s)"
fi

exit 0
