---
name: add-feature
description: Add new features to an established project with foundation docs already in place
---

# Add Feature Command

Streamlined workflow for adding new features to a project that has already completed the initial workflow (new-project or continue-project).

## Arguments

$ARGUMENTS

## Usage

```bash
/add-feature "Dark mode toggle"
/add-feature "PDF export and email notifications"
/add-feature   # Interactive mode - will ask what to add
```

## Prerequisites

This command requires existing foundation documents:
- `docs/PRODUCT_PRD.md` - Product requirements
- `docs/ARCHITECTURE.md` - Technical architecture
- `docs/DESIGN.md` - Design system
- `.ai-workflow.yaml` - AI tooling config (optional but recommended)

If these don't exist, use `/continue-project` instead.

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: VALIDATE FOUNDATION                                     │
│  Check that PRD, Architecture, Design docs exist                 │
├─────────────────────────────────────────────────────────────────┤
│  STEP 2: UPDATE PRD                                              │
│  → product-prd-builder agent (append mode)                       │
│  Add new features to backlog as 📋                               │
├─────────────────────────────────────────────────────────────────┤
│  STEP 3: IMPACT ANALYSIS                                         │
│  Analyze if new feature requires changes to:                     │
│  - Architecture? → architect agent (amendment mode)              │
│  - Design? → designer agent (amendment mode)                     │
│  - AI Tools? → ai-tooling-advisor agent (feature mode)           │
├─────────────────────────────────────────────────────────────────┤
│  STEP 4: PLANNING                                                │
│  → feature-prd-builder agent                                     │
│  Create Feature PRDs for new items only                          │
├─────────────────────────────────────────────────────────────────┤
│  STEP 5: DEVELOPMENT                                             │
│  Execute new Feature PRDs (Ralph loop)                           │
├─────────────────────────────────────────────────────────────────┤
│  STEP 6: QUALITY                                                 │
│  Test new features + regression on existing                      │
└─────────────────────────────────────────────────────────────────┘
```

## Step-by-Step Process

### Step 1: Validate Foundation

Check for required artifacts:

```markdown
## Foundation Check

Checking for required documents...

| Document | Status | Path |
|----------|--------|------|
| Product PRD | ✅ Found | docs/PRODUCT_PRD.md |
| Architecture | ✅ Found | docs/ARCHITECTURE.md |
| Design | ✅ Found | docs/DESIGN.md |
| AI Workflow | ✅ Found | .ai-workflow.yaml |

✅ Foundation complete. Ready to add features.
```

If missing critical docs:
```
❌ Missing foundation documents:
- docs/PRODUCT_PRD.md - NOT FOUND
- docs/ARCHITECTURE.md - NOT FOUND

Use /continue-project to establish foundation first.
```

### Step 2: Update PRD

Use **product-prd-builder** agent in **append mode**:

1. Read existing PRODUCT_PRD.md
2. Present current feature backlog with statuses
3. Add new feature(s) to backlog as 📋
4. Capture requirements for new feature:
   - User story
   - Acceptance criteria
   - Dependencies on existing features
   - Priority/order in backlog

Output: Updated `docs/PRODUCT_PRD.md` with new features added

### Step 3: Impact Analysis

Analyze each new feature for impacts:

```markdown
## Impact Analysis: {Feature Name}

### Architecture Impact
- [ ] New data models needed?
- [ ] New API endpoints?
- [ ] New external integrations?
- [ ] Infrastructure changes?

**Result:** {No changes / Minor updates / Significant changes}

### Design Impact
- [ ] New screens/pages?
- [ ] New components?
- [ ] New user flows?
- [ ] Design token changes?

**Result:** {No changes / Minor updates / Significant changes}

### AI Tooling Impact
- [ ] New skills needed?
- [ ] New MCP servers?
- [ ] New agents helpful?

**Result:** {No changes / Add tools}
```

**Based on analysis:**

| Impact | Action |
|--------|--------|
| Architecture: No changes | Skip |
| Architecture: Changes needed | → architect agent (amendment mode) |
| Design: No changes | Skip |
| Design: Changes needed | → designer agent (amendment mode) |
| AI Tools: No changes | Skip |
| AI Tools: Additions needed | → ai-tooling-advisor agent (feature mode) |

### Step 4: Planning

Use **feature-prd-builder** agent:

1. Read updated PRODUCT_PRD.md
2. Create Feature PRD ONLY for new 📋 items
3. Generate US-XXX stories sized for one context window
4. Create progress.txt for tracking

Output: `docs/features/{NN}-{feature-name}/PRD.md`

### Step 5: Development

Execute Feature PRDs using standard development workflow:

1. Read Feature PRD
2. Execute stories in order (Ralph loop)
3. Update progress.txt after each story
4. Commit after each completed story

### Step 6: Quality

Test new features:

1. Run existing test suite (regression)
2. Add tests for new features
3. Manual verification of new functionality
4. Update documentation if needed

## Agent Modes for Add-Feature

### product-prd-builder (append mode)
- DO NOT rewrite entire PRD
- ADD new features to existing backlog
- PRESERVE all existing feature statuses
- UPDATE dependencies if new feature affects existing

### architect (amendment mode)
- DO NOT redesign architecture
- ADD new sections for new capabilities
- UPDATE existing sections only if impacted
- DOCUMENT breaking changes if any

### designer (amendment mode)
- DO NOT recreate design system
- ADD new components/screens as needed
- UPDATE design tokens only if theme changes
- EXTEND existing patterns

### ai-tooling-advisor (feature mode)
- CHECK if new feature needs specific tools
- RECOMMEND additions only
- PRESERVE existing configuration
- ADD with metadata (date, reason, feature)

## Example Session

```
User: /add-feature "Dark mode toggle"

Claude: 📋 Add Feature: Dark mode toggle

## Step 1: Foundation Check
✅ docs/PRODUCT_PRD.md - Found
✅ docs/ARCHITECTURE.md - Found
✅ docs/DESIGN.md - Found
✅ .ai-workflow.yaml - Found

## Step 2: Updating PRD

Adding to feature backlog:
- 📋 Dark mode toggle (NEW)

Quick questions:
1. Should dark mode persist across sessions? (Y/n)
2. System preference detection? (Y/n)
3. Priority: A) Next up  B) After current features  C) Backlog

User: Y, Y, A

Claude: Updated PRODUCT_PRD.md with dark mode feature.

## Step 3: Impact Analysis

### Architecture Impact
- New data models: No (user preference only)
- New API endpoints: No (localStorage or existing user settings)
- External integrations: No
**Result: No architecture changes needed** ✓

### Design Impact
- New screens: No
- New components: Yes (ThemeToggle component)
- New user flows: No
- Design tokens: Yes (dark color palette)
**Result: Design updates needed** → Running designer agent...

### AI Tooling Impact
- New skills: No
- New MCP servers: No
**Result: No tooling changes needed** ✓

[Designer agent adds dark theme tokens to DESIGN.md]

## Step 4: Planning

Creating Feature PRD for dark mode...

Feature: 05-dark-mode
Stories:
- US-041: Add dark theme color tokens
- US-042: Create ThemeProvider context
- US-043: Build ThemeToggle component
- US-044: Apply theme to existing components
- US-045: Persist theme preference

Created: docs/features/05-dark-mode/PRD.md

## Ready for Development

Run `/phase development` to start implementing, or continue adding features.
```

## Completion

When add-feature workflow completes:
1. PRD updated with new feature(s)
2. Foundation docs amended (if needed)
3. Feature PRD created with stories
4. Ready for development phase

## Quick Reference

| Need | Command |
|------|---------|
| Add feature to established project | `/add-feature "feature name"` |
| Start brand new project | `/new-project` |
| Onboard existing codebase | `/continue-project` |
| Check current phase | `/phase status` |
| Verify gate criteria | `/gate-check` |
