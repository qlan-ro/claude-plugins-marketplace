---
name: project-studio:phase
description: Jump to or check status of a specific phase (e.g., /project-studio:phase discovery, /project-studio:phase architecture, /project-studio:phase status)
---

# Phase Navigation

Navigate to a specific phase or check current status.

## Arguments

$ARGUMENTS

## Usage

- `/project-studio:phase status` - Show current phase and progress
- `/project-studio:phase discovery` - Jump to Phase 1 (Discovery / Codebase Analysis)
- `/project-studio:phase ai-workflow` - Jump to Phase 2 (AI Workflow Config) or Phase C5 (Audit)
- `/project-studio:phase architecture` - Jump to Phase 3 (Architecture)
- `/project-studio:phase design` - Jump to Phase 4 (Design)
- `/project-studio:phase ai-tooling-audit` - Jump to Phase C5 (AI Tooling Audit - continue workflow only)
- `/project-studio:phase planning` - Jump to Phase 5 (Planning / Feature PRDs)
- `/project-studio:phase development` - Jump to Phase 6 (Development)
- `/project-studio:phase quality` - Jump to Phase 7 (Quality)

## Phase Status Check

If argument is "status" or empty, check for existing artifacts and report:

```markdown
## Current Project Status

### Artifacts Found
- [ ] docs/PRODUCT_PRD.md - Phase 1
- [ ] .ai-workflow.yaml - Phase 2
- [ ] docs/ARCHITECTURE.md - Phase 3
- [ ] docs/DESIGN.md - Phase 4
- [ ] docs/features/*/PRD.md - Phase 5
- [ ] src/* - Phase 6
- [ ] tests/* - Phase 7

### Current Phase: {determined from artifacts}
### Next Step: {recommendation}
```

## Phase Descriptions

### Phase 1: Discovery (New Project) / Codebase Analysis (Continue)
- **New:** Use product-prd-builder agent to define scope
- **Continue:** Use codebase-analyzer agent to understand existing code
- **Output:** PRODUCT_PRD.md (or CODEBASE_ANALYSIS.md first)

### Phase 2: AI Workflow Configuration (New)
- **New:** Use ai-tooling-advisor agent to configure skills, MCP servers, agents
- **Output:** .ai-workflow.yaml

### Phase C2: Infer PRD (Continue)
- **Continue:** Use product-prd-builder agent (inference mode) to document existing features + add new requests
- **Output:** PRODUCT_PRD.md with status markers (✅/🟡/📋)

### Phase 3: Architecture
- **New:** Use architect agent to make tech decisions
- **Continue:** Document existing architecture (don't redesign)
- **Output:** ARCHITECTURE.md

### Phase 4: Design
- **New:** Use designer agent to create design system
- **Continue:** Extract existing design tokens and patterns (Phase C4)
- **Output:** DESIGN.md

### Phase C5: AI Tooling Audit (Continue)
- **Continue:** Use ai-tooling-advisor agent (audit mode) to analyze existing config and identify gaps
- **Output:** .ai-workflow.yaml (created or updated)

### Phase 5: Planning
- Use feature-prd-builder agent for both workflows
- Create US-XXX stories sized for one context window
- **Output:** docs/features/{NN}-{name}/PRD.md + progress.txt

### Phase 6: Development
- Execute Feature PRDs using Ralph loop
- Track progress in progress.txt
- **Output:** Working codebase

### Phase 7: Quality
- Testing, documentation, deployment prep
- **Output:** Production-ready application

## Jumping to a Phase

When jumping to a specific phase:

1. **Check prerequisites** - Are earlier phase artifacts present?
2. **Warn if skipping** - "Phase 1-2 artifacts not found. Continue anyway?"
3. **Load context** - Read relevant existing artifacts
4. **Begin phase** - Start the appropriate agent or workflow

## Example Responses

### `/project-studio:phase status`
```
📊 Project Status

✅ Phase 1: Discovery - COMPLETE (PRODUCT_PRD.md exists)
✅ Phase 2: AI Workflow - COMPLETE (.ai-workflow.yaml exists)
🔄 Phase 3: Architecture - IN PROGRESS (ARCHITECTURE.md partial)
⏳ Phase 4: Design - NOT STARTED
⏳ Phase 5: Planning - NOT STARTED
⏳ Phase 6: Development - NOT STARTED
⏳ Phase 7: Quality - NOT STARTED

Current: Phase 3 (Architecture)
Recommendation: Complete ARCHITECTURE.md, then run /project-studio:gate-check
```

### `/project-studio:phase design`
```
⚠️ Jumping to Phase 4 (Design)

Prerequisites check:
✅ PRODUCT_PRD.md found
✅ ARCHITECTURE.md found

Ready to begin Phase 4. Using designer agent...
```

Handle the argument provided and execute the appropriate action.
