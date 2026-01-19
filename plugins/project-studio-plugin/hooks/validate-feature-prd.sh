#!/bin/bash
# Validate Feature PRD story sizing and structure

FILE="$1"

if [ ! -f "$FILE" ]; then
    echo "❌ Feature PRD file not found: $FILE"
    exit 1
fi

ERRORS=0
WARNINGS=0

# Check for US-XXX format stories
STORY_COUNT=$(grep -c "### US-[0-9]" "$FILE" || echo "0")
if [ "$STORY_COUNT" -eq 0 ]; then
    echo "❌ No US-XXX format stories found"
    ERRORS=$((ERRORS + 1))
else
    echo "📋 Found $STORY_COUNT user stories"
fi

# Check each story has acceptance criteria
CRITERIA_COUNT=$(grep -c "Acceptance Criteria" "$FILE" || echo "0")
if [ "$CRITERIA_COUNT" -lt "$STORY_COUNT" ]; then
    echo "⚠️ Some stories missing Acceptance Criteria"
    WARNINGS=$((WARNINGS + 1))
fi

# Check for "Typecheck passes" in criteria
TYPECHECK_COUNT=$(grep -c "Typecheck passes" "$FILE" || echo "0")
if [ "$TYPECHECK_COUNT" -lt "$STORY_COUNT" ]; then
    echo "⚠️ Some stories missing 'Typecheck passes' criterion"
    WARNINGS=$((WARNINGS + 1))
fi

# Check for vague criteria (common patterns)
if grep -qi "works correctly\|looks good\|user has good experience\|performs well" "$FILE"; then
    echo "⚠️ Found vague acceptance criteria - make them specific and verifiable"
    WARNINGS=$((WARNINGS + 1))
fi

# Check for Non-Goals section
if ! grep -q "## Non-Goals" "$FILE"; then
    echo "⚠️ Missing Non-Goals section"
    WARNINGS=$((WARNINGS + 1))
fi

# Check story descriptions aren't too long (proxy for story size)
while IFS= read -r line; do
    DESC_LENGTH=${#line}
    if [ "$DESC_LENGTH" -gt 500 ]; then
        echo "⚠️ Story description may be too long - consider splitting"
        WARNINGS=$((WARNINGS + 1))
        break
    fi
done < <(grep -A 1 "### US-" "$FILE" | grep "Description:")

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "✅ Feature PRD validated - stories appear properly sized"
elif [ $ERRORS -eq 0 ]; then
    echo "📋 Feature PRD has $WARNINGS warning(s) to review"
else
    echo "❌ Feature PRD has $ERRORS error(s) and $WARNINGS warning(s)"
fi

exit 0  # Don't fail build, just report
