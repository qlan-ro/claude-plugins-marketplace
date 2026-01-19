# Phase 2: Infer Product PRD

## Objective
Generate a Product PRD from the codebase analysis, documenting existing features (done) and new features (to build).

## Entry Criteria
- Codebase Analysis complete (`docs/CODEBASE_ANALYSIS.md`)
- User has confirmed analysis accuracy

## Why This Phase Matters
Even for existing projects, we need a Product PRD to:
- Understand what's already built (avoid rebuilding)
- Define what's next (new features)
- Establish clear boundaries (non-goals)
- Track overall product scope

---

## Key Activities

### 1. Clarify New Feature Goals

Ask the user what they want to add. Use lettered options:

```
Based on the codebase analysis, I see these existing features:
✅ Authentication (complete)
✅ User Profile (complete)
🟡 Dashboard (partial - missing charts)

1. What's the main goal for this session?
   A. Complete partial features (Dashboard charts)
   B. Add new features
   C. Both complete partial + add new
   D. Refactor/improve existing

2. If adding new features, what area?
   A. [Suggest based on common patterns]
   B. [Suggest based on data model gaps]
   C. [Suggest based on TODO comments found]
   D. Other: [specify]
```

### 2. Infer Problem Statement

From codebase context, infer:

```markdown
## Problem Statement

**What this product does:**
{Infer from README, package.json description, or main components}

**Current State:**
{List existing features from analysis}

**Gaps/Opportunities:**
{Infer from partial features, TODO comments, or user input}
```

### 3. Infer Target Users

From code patterns:

| Code Evidence | Likely User |
|---------------|-------------|
| `admin/`, role checks | Admin users |
| Public pages, no auth | Anonymous visitors |
| Auth required everywhere | Registered users |
| B2B patterns (orgs, teams) | Business users |
| Consumer patterns (profiles) | Individual consumers |

```markdown
## Target Users

**Primary User:** {Inferred from code patterns}
- Evidence: {What code suggested this}

**Secondary Users:** {If applicable}
```

### 4. Build Feature Backlog

Combine existing (done) + new (to do):

```markdown
## Feature Backlog

### ✅ Complete (Existing)
These features exist and are functional.

| # | Feature | Status | Evidence |
|---|---------|--------|----------|
| 1 | User Authentication | ✅ Done | auth/, JWT, login page |
| 2 | User Profile | ✅ Done | profile page, settings API |
| 3 | Basic Dashboard | ✅ Done | dashboard page |

### 🟡 Partial (Needs Completion)
These features exist but are incomplete.

| # | Feature | Current State | Remaining Work |
|---|---------|---------------|----------------|
| 4 | Dashboard Charts | Page exists | Add chart components |
| 5 | Search | UI exists | Backend not connected |

### 📋 New (To Build)
New features from this session. Listed in dependency order.

| # | Feature | Description | Depends On |
|---|---------|-------------|------------|
| 6 | {Feature} | {Description} | {Dependencies} |
| 7 | {Feature} | {Description} | {Dependencies} |

### 🚫 Post-MVP (Future)
Features explicitly deferred.

| # | Feature | Description | When to Consider |
|---|---------|-------------|------------------|
| 8 | {Feature} | {Description} | {Trigger} |
```

### 5. Define Non-Goals

Based on scope discussion:

```markdown
## Non-Goals

What we will NOT do in this session:

- No rebuilding existing authentication
- No changing the database schema for existing features
- No UI redesign of working pages
- {User-specified non-goals}
```

### 6. Success Criteria

For the new/partial work:

```markdown
## Success Criteria

| Metric | Target |
|--------|--------|
| Partial features completed | {N} of {M} |
| New features implemented | {N} of {M} |
| All new code has tests | Yes |
| No regressions in existing features | Yes |
```

---

## Output Artifact

Create `docs/PRODUCT_PRD.md`:

```markdown
# Product PRD: {PROJECT_NAME}

**Date:** {DATE}
**Status:** Inferred from existing codebase + user input

---

## Problem Statement

**What this product does:**
{Inferred description}

**Current State:**
- {N} features complete
- {M} features partial
- {K} features planned

---

## Target Users

**Primary User:** {Type}
- Evidence: {Code patterns}

---

## Feature Backlog

### ✅ Complete (Existing)

| # | Feature | Evidence |
|---|---------|----------|
| 1 | Authentication | auth/, JWT |
| 2 | User Profile | profile page |

### 🟡 Partial (Needs Completion)

| # | Feature | Remaining Work |
|---|---------|----------------|
| 3 | Dashboard | Add charts |

### 📋 New (To Build)

| # | Feature | Description |
|---|---------|-------------|
| 4 | {Feature} | {Description} |

### 🚫 Post-MVP

| # | Feature | When |
|---|---------|------|
| 5 | {Feature} | {Trigger} |

---

## Non-Goals

- {Non-goal 1}
- {Non-goal 2}

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Features completed | {N} |
| Tests passing | Yes |
| No regressions | Yes |

---

## Constraints

- Must follow existing conventions (see CODEBASE_ANALYSIS.md)
- Must use existing tech stack
- Must not break existing features

---

## Open Questions

- {Any clarifications needed before proceeding}
```

---

## Phase Gate Checklist

Before proceeding to Infer Architecture:
- [ ] Existing features documented with status
- [ ] New features identified and ordered
- [ ] Non-goals explicitly stated
- [ ] Success criteria defined
- [ ] `docs/PRODUCT_PRD.md` created
- [ ] User has approved the Product PRD
