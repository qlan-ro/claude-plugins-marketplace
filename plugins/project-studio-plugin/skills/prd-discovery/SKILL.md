---
name: prd-discovery
description: |
  Product requirement discovery and PRD creation. Use this skill when:
  - Transforming ideas into structured PRDs
  - Conducting discovery interviews
  - Creating dependency-ordered feature backlogs
  - Defining scope boundaries (non-goals)

  This skill is domain-specific - it knows HOW to create PRDs, not workflow phases.
---

# PRD Discovery

Transform vague ideas into well-structured Product Requirement Documents.

## Interaction Style: Lettered Options

Always use lettered options for fast, unambiguous responses:

```
1. Who is the primary user?
   A. Consumers (B2C)
   B. Businesses (B2B)
   C. Internal team/employees
   D. Other: [specify]

2. What's the primary platform?
   A. Web application
   B. Mobile app (iOS/Android)
   C. Desktop application
   D. API/Backend service
```

User responds: "1A, 2A" - Fast and clear.

## Discovery Process

### Step 1: Core Understanding

Ask about:
- **Problem:** What problem are we solving?
- **Users:** Who experiences this problem?
- **Current state:** How do they solve it today?
- **Gap:** What's missing from current solutions?
- **Success:** How will we know it's working?

### Step 2: Scope Definition

Clarify:
- **Must-have (MVP):** What's essential for launch?
- **Nice-to-have:** What can wait for v2?
- **Non-goals:** What are we explicitly NOT building?
- **Constraints:** Technical, budget, timeline limitations?

### Step 3: Feature Backlog Creation

Organize features as **vertical slices** (end-to-end user capabilities), not architectural layers.

**CRITICAL: Each feature = complete user capability (schema + backend + frontend)**

```markdown
### Foundation (Build First)
- [ ] User authentication (signup, login, logout - full stack)
- [ ] Core data model & API foundation

### Core MVP (Depends on Foundation)
- [ ] Dashboard (API + UI)
- [ ] User settings (API + UI)
- [ ] Primary workflow (API + UI)

### Enhanced MVP (Depends on Core)
- [ ] Advanced feature A (full stack)
- [ ] Integration with external service

### Post-MVP (Future)
- [ ] Nice-to-have features
- [ ] Optimization
```

**Key rules:**
1. **Vertical slices, not horizontal layers** - Each feature delivers a complete user-facing capability
2. **NO backend-only features** unless purely infrastructure (e.g., "database migrations")
3. **Features must be ordered so dependencies come first**

### Anti-Pattern: Horizontal Layering (AVOID)

```markdown
# WRONG - splits by technical layer
### Foundation
- [ ] Database schema        ← No user value alone
- [ ] Authentication API     ← No user value alone
- [ ] Core API structure     ← No user value alone

### Core MVP
- [ ] Dashboard UI           ← Disconnected from backend
- [ ] Settings UI            ← Disconnected from backend
```

### Correct Pattern: Vertical Slices

```markdown
# RIGHT - each feature is end-to-end
### Foundation
- [ ] Authentication (schema + API + login/register UI)
- [ ] Project setup (schema + API + creation wizard UI)

### Core MVP
- [ ] Dashboard (queries + API + dashboard page)
- [ ] Settings (schema + API + settings page)
```

## Output Template

Create `docs/PRODUCT_PRD.md`:

```markdown
# {Product Name} - Product PRD

## Problem Statement
{Clear 2-3 sentence articulation of the problem}

## Target Users

### Primary User
- **Who:** {persona description}
- **Goal:** {what they want to achieve}
- **Pain point:** {current frustration}

### Secondary Users (if applicable)
- {Other user types}

## Success Criteria
- [ ] {Measurable criterion 1}
- [ ] {Measurable criterion 2}
- [ ] {Measurable criterion 3}

## Feature Backlog (Dependency Ordered)

<!-- IMPORTANT: Each feature is a VERTICAL SLICE (schema + API + UI) -->
<!-- NOT horizontal layers (all schemas, then all APIs, then all UIs) -->

### Foundation (Build First)
1. **{Feature}** - {Brief description} (full stack: schema + API + UI)
2. **{Feature}** - {Brief description} (full stack)

### Core MVP
3. **{Feature}** - {Brief description} (full stack)
4. **{Feature}** - {Brief description} (full stack)

### Enhanced MVP
5. **{Feature}** - {Brief description} (full stack)

### Post-MVP
6. **{Feature}** - {Brief description}

## Non-Goals (Explicit Boundaries)
- NOT building: {explicit exclusion 1}
- NOT building: {explicit exclusion 2}
- NOT building: {explicit exclusion 3}

## Technical Constraints
- {Constraint 1}
- {Constraint 2}

## Open Questions
- {Question needing future resolution}
```

## Continue-Project Mode (Inference)

When documenting an EXISTING codebase, add status markers:

```markdown
## Feature Backlog

### Foundation
1. **User authentication** ✅ Done (schema + API + login/register pages)
2. **Project management** ✅ Done (schema + CRUD API + project list/detail UI)

### Core MVP
3. **Dashboard** 🟡 Partial - API done, UI missing charts
4. **User settings** 📋 To Build (schema + API + settings page)

### New Features (Requested)
5. **Dark mode** 📋 To Build (theme provider + toggle UI)
6. **Export to PDF** 📋 To Build (export API + download button)
```

Note: Each feature shows its full-stack components (schema/API/UI) to make scope clear.

Status markers:
- ✅ **Done** - Fully implemented
- 🟡 **Partial** - Exists but incomplete
- 📋 **To Build** - New feature request

## Critical Rules

1. **Dependency ordering matters** - Foundation before features that need it
2. **Non-goals are critical** - Explicitly state what you're NOT building
3. **Verifiable criteria** - Every success criterion must be checkable
4. **Concise PRD** - Keep it scannable, not a novel
5. **WHAT not HOW** - This is scope, not implementation

## Add-Feature Mode (Append)

When adding features to an EXISTING PRD via `/add-feature`:

### Rules for Append Mode

1. **DO NOT rewrite** the entire document
2. **READ** existing PRD first
3. **PRESERVE** all existing sections and statuses
4. **ADD** new features to the appropriate backlog section
5. **UPDATE** dependencies if new feature affects existing

### Process

```markdown
## Existing Feature Backlog

### Foundation
1. **User authentication** ✅ Done
2. **Database schema** ✅ Done

### Core MVP
3. **Dashboard** ✅ Done
4. **User settings** ✅ Done

### Enhanced MVP
5. **Notifications** ✅ Done

### New Features (Added {date})    ← ADD NEW SECTION
6. **Dark mode toggle** 📋 To Build
   - As a user, I want to toggle dark mode
   - Depends on: User settings (4)
   - Priority: High
```

### Capture for Each New Feature

- User story (As a... I want... So that...)
- Acceptance criteria (verifiable)
- Dependencies on existing features
- Priority level (High/Medium/Low)

### Output

Updated `docs/PRODUCT_PRD.md` with:
- New features added to backlog as 📋
- Dependencies documented
- Existing content UNCHANGED

## Common Discovery Questions

### Problem Space
- "What triggered the need for this?"
- "What happens if we don't solve this?"
- "Who feels this pain most acutely?"

### Users
- "Walk me through a typical day for your user"
- "What's the first thing they'd want to do?"
- "What would make them abandon this product?"

### Scope
- "If you could only ship ONE feature, which?"
- "What's explicitly out of scope?"
- "What's a v2 feature vs MVP?"

### Success
- "How will you measure success?"
- "What number would make this a win?"
- "What's the minimum viable outcome?"
