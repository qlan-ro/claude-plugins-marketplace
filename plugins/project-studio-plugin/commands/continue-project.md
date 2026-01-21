---
name: continue-project
description: Continue an existing project - analyzes codebase, infers documentation, then adds new features using the standard workflow
---

# Continue Project Workflow

You are initiating a continue-project workflow for an existing codebase. This workflow performs deep analysis to understand what exists before adding new features.

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE C1: CODEBASE ANALYSIS  │  PHASE C2: INFER PRODUCT PRD                │
│  → codebase-analyzer agent    │  → product-prd-builder agent (infer mode)   │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE C3: INFER ARCHITECTURE │  PHASE C4: INFER DESIGN                     │
│  → architect agent (doc mode) │  → designer agent (extract mode)            │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE C5: AI TOOLING AUDIT   │  PHASE 5+: STANDARD WORKFLOW                │
│  → ai-tooling-advisor agent   │  → Planning → Development → Quality         │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Getting Started

$ARGUMENTS

### Initialize Orchestration State

Before beginning, initialize the orchestration state file for session continuity:

```bash
# Create .project-studio directory and state file
./hooks/update-orchestration-state.sh session-start
./hooks/update-orchestration-state.sh workflow-type continue-project
./hooks/update-orchestration-state.sh phase-start codebase-analysis
```

This enables:
- Session history tracking
- Resume capability via `/workflow-status`
- Pending decision tracking
- Artifact change logging

If the user provided context above (project path, new features), acknowledge it.
Otherwise, ask:
1. "What is the path to your existing project?"
2. "What new features would you like to add?"

## Phase 1: Codebase Analysis

Use the **codebase-analyzer** agent to perform deep inspection:

### Analysis Steps
1. **Project Structure** - Identify directories, config files
2. **Tech Stack Detection** - Framework, database, tooling
3. **Data Model Extraction** - Entities, relationships, schemas
4. **API Surface Mapping** - Endpoints, contracts
5. **Component Inventory** - UI components, pages
6. **Existing Feature Detection** - What's already built
7. **Convention Discovery** - Naming, patterns, structure

**Output:** `docs/CODEBASE_ANALYSIS.md`

## Phase 2: Infer Product PRD

Based on codebase analysis, create a Product PRD that documents:

### Existing Features (from code)
Mark with status:
- ✅ **Done** - Fully implemented, working
- 🟡 **Partial** - Exists but incomplete
- 📋 **To Build** - New feature request

### New Features (from user request)
Add user's requested features to the backlog as 📋 **To Build**

### Feature Backlog Structure
```markdown
### Foundation (Existing)
- ✅ User authentication
- ✅ Database schema

### Core MVP
- ✅ Feature A (complete)
- 🟡 Feature B (partial - needs X)
- 📋 Feature C (new - user requested)

### Enhanced
- 📋 Feature D (new - user requested)
```

**Output:** `docs/PRODUCT_PRD.md`

## Phase 3: Infer Architecture

Document existing technical decisions (don't redesign):

1. **Tech Stack** - What's already in use
2. **Data Model** - Extract from schemas/types
3. **API Patterns** - How endpoints are structured
4. **State Management** - How state is handled
5. **Security** - Existing auth approach
6. **Tech Debt** - Note any issues found

**Output:** `docs/ARCHITECTURE.md`

## Phase C4: Infer Design

Extract existing design system (don't redesign):

1. **Design Tokens** - Colors, spacing, typography from CSS/Tailwind
2. **Component Library** - Existing UI components
3. **Page Layouts** - Current page structures
4. **Navigation** - Existing nav patterns
5. **Responsive Behavior** - Current breakpoints

**Output:** `docs/DESIGN.md`

## Phase C5: AI Tooling Audit

Use the **ai-tooling-advisor** agent to:

1. **Detect existing config** - Check for .ai-workflow.yaml, .claude/, MCP configs
2. **Analyze tech stack** - From CODEBASE_ANALYSIS.md and ARCHITECTURE.md
3. **Identify gaps** - What skills/agents/MCP servers are missing?
4. **Suggest additions** - Recommend tools for new features
5. **Update or create config** - Generate/update .ai-workflow.yaml

### Audit Checklist
- Existing skills configured?
- MCP servers for detected databases?
- Agents for the tech stack?
- Tools needed for new 📋 features?

**Output:** `.ai-workflow.yaml` (created or updated)

## Phase 5+: Standard Workflow

After inference phases, continue with standard phases:

### Phase 5: Planning
Use **feature-prd-builder** agent to create Feature PRDs for:
- 🟡 Partial features (completion stories)
- 📋 New features (full implementation stories)

### Phase 6: Development
Execute Feature PRDs using Ralph loop

### Phase 7: Quality
Testing, documentation, deployment prep

## Key Differences from New Project

| Aspect | New Project | Continue Project |
|--------|-------------|------------------|
| Phase 1 | Discovery (interviews) | C1: Codebase Analysis (code inspection) |
| Phase 2 | AI Workflow Config | C2: Infer Product PRD |
| Phase 3 | Architecture (decisions) | C3: Infer Architecture (documentation) |
| Phase 4 | Design (creation) | C4: Infer Design (extraction) |
| - | - | C5: AI Tooling Audit (gap analysis) |
| Phases 5-7 | Same | Same (Planning → Dev → Quality) |

## Important Rules

1. **Document, don't redesign** - Capture existing patterns, don't change them
2. **Respect conventions** - New code should follow existing patterns
3. **Only build what's needed** - Focus on 🟡 and 📋 items
4. **Preserve working code** - Don't break existing functionality

## Phase Gate Rules

Only advance when:
- Analysis is accurate (user confirms)
- Artifacts are complete
- Run `/gate-check` to verify readiness

Begin with Phase 1 (Codebase Analysis) now.
