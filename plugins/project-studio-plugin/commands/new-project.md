---
name: new-project
description: Start a new project from an idea - guides through discovery, architecture, design, and planning phases optimized for AI agent execution
---

# New Project Workflow

You are initiating a new project workflow. Guide the user through a structured 7-phase process to transform their idea into a production-ready application.

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: DISCOVERY           │  PHASE 2: AI WORKFLOW                       │
│  → product-prd-builder agent  │  → ai-tooling-advisor agent                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 3: ARCHITECTURE        │  PHASE 4: DESIGN                            │
│  → architect agent            │  → designer agent                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 5: PLANNING            │  PHASE 6: DEVELOPMENT                       │
│  → feature-prd-builder agent  │  → Execute stories (Ralph loop)             │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 7: QUALITY                                                           │
│  → Testing, documentation, deployment prep                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Getting Started

$ARGUMENTS

If the user provided an idea above, acknowledge it and begin Phase 1 (Discovery).
If no idea was provided, ask: "What would you like to build?"

## Phase 1: Discovery

Use the **product-prd-builder** agent to:
1. Ask clarifying questions using lettered options (A/B/C/D format)
2. Define the problem statement and target users
3. Create a dependency-ordered feature backlog
4. Establish explicit non-goals
5. Define success criteria

**Output:** `docs/PRODUCT_PRD.md`

## Phase 2: AI Workflow Configuration

Use the **ai-tooling-advisor** agent to:
1. Classify project by platform, languages, frameworks, features
2. Query registry for matching skills, agents, MCP servers
3. Present recommendations with rationale
4. Generate configuration file

**Output:** `.ai-workflow.yaml`

## Phase 3: Architecture

Use the **architect** agent to:
1. Present technology options with pros/cons
2. Make stack decisions (frontend, backend, database)
3. Design data models
4. Define API structure
5. Plan security approach

**Output:** `docs/ARCHITECTURE.md`

## Phase 4: Design

Use the **designer** agent to:
1. Map user flows
2. Create screen inventory with wireframes
3. Define design tokens (colors, spacing, typography)
4. Specify component library
5. Plan responsive behavior

**Output:** `docs/DESIGN.md`

## Phase 5: Planning

Use the **feature-prd-builder** agent to:
1. Break down each feature into US-XXX stories
2. Ensure each story fits in ONE context window
3. Order stories by dependency (schema → backend → frontend)
4. Write verifiable acceptance criteria
5. Set up progress.txt tracking

**Output:** `docs/features/{NN}-{name}/PRD.md` + `progress.txt`

## Phase 6: Development

Execute Feature PRDs using Ralph loop:
1. Read story from progress.txt
2. Implement the story
3. Verify acceptance criteria
4. Mark complete in progress.txt
5. Repeat

**Output:** Working codebase

## Phase 7: Quality

Prepare for production:
1. Test coverage
2. Documentation
3. Deployment configuration
4. Performance audit

**Output:** Production-ready application

## Phase Gate Rules

Only advance to the next phase when:
- All required artifacts are complete
- User has explicitly approved the output
- Run `/gate-check` to verify readiness

## Quick Reference

| Phase | Agent | Output |
|-------|-------|--------|
| 1. Discovery | product-prd-builder | PRODUCT_PRD.md |
| 2. AI Workflow | ai-tooling-advisor | .ai-workflow.yaml |
| 3. Architecture | architect | ARCHITECTURE.md |
| 4. Design | designer | DESIGN.md |
| 5. Planning | feature-prd-builder | features/*/PRD.md |
| 6. Development | (Ralph loop) | src/* |
| 7. Quality | (manual) | tests/*, docs/* |

Begin with Phase 1 now.
