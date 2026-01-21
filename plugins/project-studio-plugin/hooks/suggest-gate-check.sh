#!/bin/bash
# Suggest running gate-check after phase completion

# Check which artifacts exist
DOCS_DIR="docs"

if [ ! -d "$DOCS_DIR" ]; then
    exit 0  # No docs directory, nothing to suggest
fi

# Detect current phase based on artifacts
CURRENT_PHASE=""
NEXT_PHASE=""

if [ -f "$DOCS_DIR/PRODUCT_PRD.md" ] && [ ! -f ".ai-workflow.yaml" ]; then
    CURRENT_PHASE="Discovery"
    NEXT_PHASE="AI Workflow"
elif [ -f ".ai-workflow.yaml" ] && [ ! -f "$DOCS_DIR/ARCHITECTURE.md" ]; then
    CURRENT_PHASE="AI Workflow"
    NEXT_PHASE="Architecture"
elif [ -f "$DOCS_DIR/ARCHITECTURE.md" ] && [ ! -f "$DOCS_DIR/DESIGN.md" ]; then
    CURRENT_PHASE="Architecture"
    NEXT_PHASE="Design"
elif [ -f "$DOCS_DIR/DESIGN.md" ] && [ ! -d "$DOCS_DIR/features" ]; then
    CURRENT_PHASE="Design"
    NEXT_PHASE="Planning"
elif [ -d "$DOCS_DIR/features" ]; then
    # Check if all progress.txt files show completion
    INCOMPLETE=$(find "$DOCS_DIR/features" -name "progress.txt" -exec grep -l "\[ \]" {} \; | wc -l)
    if [ "$INCOMPLETE" -gt 0 ]; then
        CURRENT_PHASE="Development"
    else
        CURRENT_PHASE="Quality"
    fi
fi

# Output suggestion if we detected a phase
if [ -n "$CURRENT_PHASE" ] && [ -n "$NEXT_PHASE" ]; then
    echo ""
    echo "💡 Tip: Run /project-studio:gate-check to verify readiness for $NEXT_PHASE phase"
fi

exit 0
