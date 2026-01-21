# Phase 5: Planning

## Objective
Generate Feature PRDs for each feature in the backlog, with AI-executable user stories sized for the Ralph loop.

## Entry Criteria
- Approved Design Spec from Phase 4
- Approved Architecture from Phase 3
- Feature backlog from Product PRD (Phase 1)

## Why This Phase Matters

The Product PRD defined **what** to build. Design defined **how it looks**. Architecture defined **how it works**. Now we break each feature into **AI-executable stories** that Ralph can implement in a single context window.

---

## Key Activities

### 1. Feature PRD Generation

For each feature in the backlog (in dependency order), generate a Feature PRD.

**CRITICAL: Project Scaffolding Must Be Feature #1**

The first feature PRD must ALWAYS be Project Scaffolding. Without it, Ralph cannot:
- Run typechecks, tests, or builds
- Verify acceptance criteria
- Execute any subsequent features

**Output structure:**
```
docs/features/
├── 01-project-scaffolding/    ← ALWAYS FIRST
│   ├── PRD.md
│   └── progress.txt
├── 02-user-authentication/
│   ├── PRD.md
│   └── progress.txt
├── 03-session-recording/
│   ├── PRD.md
│   └── progress.txt
└── ...
```

Use `assets/templates/feature-prd-template.md` for each feature.
For scaffolding specifically, use `assets/templates/scaffolding-feature-prd.md` if available.

### 2. Story Sizing (Critical Rule)

**Each story must be completable in ONE context window (~10 min of AI work).**

Ralph spawns a fresh instance per iteration with no memory of previous work. If a story is too big, the AI runs out of context before finishing and produces broken code.

#### Right-sized stories:
- Add a database column and migration
- Add a single UI component to an existing page
- Update a server action with new logic
- Add a filter dropdown to a list

#### Too big (MUST split):

| Too Big | Split Into |
|---------|-----------|
| "Build the dashboard" | Schema, queries, UI components, filters |
| "Add authentication" | Schema, middleware, login UI, session handling |
| "Add drag and drop" | Drag events, drop zones, state update, persistence |
| "Refactor the API" | One story per endpoint or pattern |

**Rule of thumb:** If you cannot describe the change in 2-3 sentences, it's too big.

### 3. Story Ordering (Dependencies First)

Stories execute in priority order. Earlier stories must NOT depend on later ones.

**Correct order:**
1. Schema/database changes (migrations)
2. Server actions / backend logic
3. UI components that use the backend
4. Dashboard/summary views that aggregate data

**Wrong order:**
```
US-001: UI component (depends on schema that doesn't exist yet!)
US-002: Schema change
```

### 4. Acceptance Criteria (Must Be Verifiable)

Each criterion must be something Ralph can CHECK, not something vague.

#### Good criteria (verifiable):
- "Add `status` column to tasks table with default 'pending'"
- "Filter dropdown has options: All, Active, Completed"
- "Clicking delete shows confirmation dialog"
- "Typecheck passes"

#### Bad criteria (vague):
- "Works correctly"
- "User can do X easily"
- "Good UX"
- "Handles edge cases"

#### Always include as final criterion:
```
- [ ] Typecheck passes
```

#### For stories that change UI, also include:
```
- [ ] Verify changes work in browser
```

### 5. Using Design & Architecture Context

When writing stories, reference the approved specs:

**From Design Spec:**
- Component names and structure
- Screen layouts and navigation
- Design tokens (colors, spacing)

**From Architecture:**
- Data model field names and types
- API endpoint patterns
- Tech stack conventions

**Example:**
```markdown
### US-002: Display priority badge on task card

**Description:** As a user, I want to see task priority at a glance.

**Acceptance Criteria:**
- [ ] TaskCard component shows PriorityBadge (from Design Spec §Components)
- [ ] Colors: red=#EF4444 (high), yellow=#F59E0B (medium), gray=#6B7280 (low)
- [ ] Priority read from task.priority field (from Architecture §Data Model)
- [ ] Typecheck passes
- [ ] Verify changes work in browser
```

---

## Feature PRD Structure

Each Feature PRD follows this format:

```markdown
# PRD: {Feature Name}

## Introduction
Brief description of the feature and the problem it solves.

## Goals
- Specific, measurable objective 1
- Specific, measurable objective 2

## User Stories

### US-001: {Title}
**Description:** As a [user], I want [feature] so that [benefit].

**Acceptance Criteria:**
- [ ] Specific verifiable criterion
- [ ] Another criterion
- [ ] Typecheck passes

### US-002: {Title}
...

## Non-Goals
- What this feature will NOT include

## Technical Considerations
- Known constraints from Architecture
- Components to reuse from Design
```

---

## Output Artifacts

For each feature:
- `docs/features/{NN}-{feature-name}/PRD.md` - Feature PRD with sized stories
- `docs/features/{NN}-{feature-name}/progress.txt` - Ralph progress tracking

Also generate:
- `docs/IMPLEMENTATION_PLAN.md` - Overview of all features and execution order

## Phase Gate Checklist

Before proceeding to Development:
- [ ] **Feature #1 is Project Scaffolding** (package.json, build, tests, lint)
- [ ] All features have Feature PRDs
- [ ] Stories use US-001 format
- [ ] Each story completable in ONE iteration (small enough)
- [ ] Stories ordered by dependency (schema → backend → frontend)
- [ ] All criteria are verifiable (not vague)
- [ ] Every story has "Typecheck passes" as criterion
- [ ] UI stories have "Verify changes work in browser"
- [ ] Non-goals section defines clear boundaries
- [ ] User has approved the Feature PRDs

---

## Example Feature PRD

```markdown
# PRD: Task Priority System

## Introduction
Add priority levels to tasks so users can focus on what matters most.

## Goals
- Allow assigning priority (high/medium/low) to any task
- Provide clear visual differentiation between priority levels
- Enable filtering by priority
- Default new tasks to medium priority

## User Stories

### US-001: Add priority field to database
**Description:** As a developer, I need to store task priority so it persists.

**Acceptance Criteria:**
- [ ] Add priority column: 'high' | 'medium' | 'low' (default 'medium')
- [ ] Generate and run migration successfully
- [ ] Typecheck passes

### US-002: Display priority indicator on task cards
**Description:** As a user, I want to see task priority at a glance.

**Acceptance Criteria:**
- [ ] Each task card shows colored priority badge
- [ ] Colors: red=high, yellow=medium, gray=low
- [ ] Priority visible without hovering or clicking
- [ ] Typecheck passes
- [ ] Verify changes work in browser

### US-003: Add priority selector to task edit
**Description:** As a user, I want to change a task's priority when editing.

**Acceptance Criteria:**
- [ ] Priority dropdown in task edit modal
- [ ] Shows current priority as selected
- [ ] Saves immediately on selection change
- [ ] Typecheck passes
- [ ] Verify changes work in browser

### US-004: Filter tasks by priority
**Description:** As a user, I want to filter to see only high-priority items.

**Acceptance Criteria:**
- [ ] Filter dropdown with options: All | High | Medium | Low
- [ ] Filter persists in URL params
- [ ] Empty state message when no tasks match filter
- [ ] Typecheck passes
- [ ] Verify changes work in browser

## Non-Goals
- No priority-based notifications or reminders
- No automatic priority assignment based on due date
- No priority inheritance for subtasks

## Technical Considerations
- Reuse Badge component from Design Spec §Components
- Filter state via URL search params (Architecture §State Management)
```
