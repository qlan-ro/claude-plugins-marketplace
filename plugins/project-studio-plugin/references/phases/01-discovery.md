# Phase 1: Discovery

## Objective
Transform a vague idea into a clear Product PRD with scoped features and dependency-ordered backlog.

## Entry Criteria
- User has described an idea (even if vague)

## Key Activities

### 1. Clarifying Questions (Lettered Options)

Ask 3-5 essential questions with lettered options for fast responses.

**Format questions like this:**

```
1. Who is the primary user?
   A. Consumers (B2C)
   B. Businesses (B2B)
   C. Internal team/employees
   D. Other: [specify]

2. What's the primary platform?
   A. Mobile-first (iOS/Android)
   B. Web-first
   C. Both equally important
   D. Desktop app

3. What's your MVP timeline?
   A. 2-4 weeks (bare minimum)
   B. 1-2 months (solid MVP)
   C. 3+ months (full-featured)
   D. No specific deadline

4. What's the core problem being solved?
   A. [Option based on idea]
   B. [Option based on idea]
   C. [Option based on idea]
   D. Other: [specify]
```

**User responds:** "1A, 2C, 3B, 4A" → Fast, unambiguous.

**Question categories to cover:**
- **Problem/Goal:** What problem does this solve?
- **Users:** Who is the target user?
- **Platform:** Where does this run?
- **Scope:** What's MVP vs later?
- **Constraints:** Timeline, integrations, technical limits?

### 2. Feature Backlog (Dependency Ordered)

After clarification, generate a **dependency-ordered** feature list:

```markdown
## Feature Backlog

### Foundation (Build First)
These must exist before anything else can work.
1. **Project Scaffolding** ← ALWAYS FIRST
2. User authentication (if needed)
3. Core data models/schema
4. Basic API structure

### Core MVP (Depends on Foundation)
The minimum features that deliver value.
5. [Primary feature]
6. [Primary feature]
7. [Primary feature]

### Enhanced MVP (Depends on Core)
Features that complete the MVP experience.
8. [Enhancement]
9. [Enhancement]

### Post-MVP (Future)
Features explicitly deferred.
10. [Future feature]
11. [Future feature]
```

**CRITICAL: Project Scaffolding must ALWAYS be Feature #1**

The Project Scaffolding feature sets up:
- Package manager config (package.json, pyproject.toml, etc.)
- Build tooling (TypeScript, Vite, etc.)
- Testing framework (Jest, Vitest, pytest)
- Linting/formatting (ESLint, Prettier, Ruff)
- Project structure (src/, tests/, etc.)
- CI configuration (optional)

Without this, Ralph cannot run typechecks, tests, or builds. This feature MUST complete before any other feature starts.

**Why ordering matters:** This sets up Phase 5 (Planning) to generate Feature PRDs in the correct execution order.

### 3. Non-Goals (Explicit Boundaries)

Define what the product will NOT do. Critical for preventing scope creep.

```markdown
## Non-Goals

- No [feature that sounds related but isn't MVP]
- No [integration that can wait]
- No [platform not being targeted]
- No [user type not being served]
```

Be specific. "No social features" is better than "Keep it simple."

### 4. Success Criteria

Define how we know the product succeeded:

```markdown
## Success Criteria

| Metric | Target | Timeframe |
|--------|--------|-----------|
| [Key metric] | [Target] | 3 months |
| [Key metric] | [Target] | 3 months |
```

### 5. Product PRD Creation

Use `assets/templates/product-prd-template.md` to create the document.

**Key sections:**
- Problem Statement
- Target Users
- Feature Backlog (ordered)
- Non-Goals
- Success Criteria
- Constraints & Assumptions

**NOT included** (these come later):
- Detailed user stories (Phase 5: Feature PRDs)
- Technical architecture (Phase 3)
- UI/UX specs (Phase 4)

## Output Artifacts
- `docs/PRODUCT_PRD.md` - Product scope and feature backlog

## Phase Gate Checklist
Before proceeding to AI Workflow:
- [ ] Target user clearly defined
- [ ] Problem statement articulated
- [ ] Feature backlog created with dependency order
- [ ] **Project Scaffolding is Feature #1 in Foundation**
- [ ] Non-goals explicitly stated
- [ ] Success criteria defined
- [ ] User has approved the Product PRD

## Example

**User says:** "I want to build a football tracker app"

**Ask:**
```
1. Who is the primary user?
   A. Casual weekend players
   B. Amateur/club players
   C. Coaches managing teams
   D. Professional athletes

2. What's the primary platform?
   A. Mobile app (iOS/Android)
   B. Web app
   C. Both mobile + web
   D. Smartwatch only

3. What data source?
   A. Apple Watch only
   B. Android Wear only
   C. Phone GPS
   D. Multiple sources

4. What's the MVP timeline?
   A. 2-4 weeks
   B. 1-2 months
   C. 3+ months
   D. No deadline
```

**User responds:** "1A, 2C, 3A, 4B"

**Generate backlog:**
```
### Foundation
1. Project Scaffolding (Swift/SwiftUI, Xcode project, tests)
2. User authentication (Apple Sign-In)
3. Session data model

### Core MVP
4. Watch app: session recording
5. Mobile app: session list
6. Heatmap visualization

### Enhanced MVP
7. Statistics dashboard
8. Progress trends

### Post-MVP
9. Social sharing
10. Team features
```
