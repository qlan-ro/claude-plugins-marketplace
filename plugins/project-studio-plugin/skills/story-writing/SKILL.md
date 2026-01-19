---
name: story-writing
description: |
  User story creation for AI execution. Use this skill when:
  - Breaking features into implementable stories
  - Sizing stories for single context window
  - Writing verifiable acceptance criteria
  - Creating Ralph-loop ready Feature PRDs

  This skill is domain-specific - it knows HOW to write stories, not workflow phases.
---

# Story Writing

Create AI-executable user stories sized for single context windows.

## Critical Rule: Story Sizing

**Each story must complete in ONE context window (~10 min AI work).**

### Size Guidelines

| Describable in... | Assessment |
|-------------------|------------|
| 2-3 sentences | Right size |
| A paragraph | Too big - split |
| Multiple paragraphs | Way too big |

### Too Big (Must Split)

| Too Big | Split Into |
|---------|-----------|
| "Build the dashboard" | Schema, queries, UI shell, widgets, filters |
| "Add authentication" | Schema, signup form, login form, session, logout |
| "Create the API" | Schema, individual endpoints, validation |
| "Implement search" | Index, basic search, filters, pagination, UI |

### Right Size

- "Add email field to user schema with validation"
- "Create login form component with email/password inputs"
- "Implement GET /api/users endpoint returning user list"
- "Add loading spinner to dashboard while data fetches"

## Story Format

```markdown
### US-001: {Concise Title}

**Description:** As a {user type}, I want {specific feature} so that {benefit}.

**Acceptance Criteria:**
- [ ] {Specific, verifiable criterion}
- [ ] {Another criterion}
- [ ] Typecheck passes
- [ ] {For UI: Verify changes work in browser}

**Dependencies:** US-000 or "None"

**Notes:** {Implementation hints if helpful}
```

## Story Ordering

**Always: Schema → Backend → Frontend**

```markdown
### US-001: Add user schema
### US-002: Create user API endpoints
### US-003: Build user list component
### US-004: Add user creation form
### US-005: Connect form to API
```

Why this order:
1. Schema defines the data structure
2. Backend provides the API
3. Frontend consumes the API

## Acceptance Criteria Rules

### Good (Verifiable)
- "User sees error message when email is invalid"
- "API returns 401 for unauthenticated requests"
- "Form submits successfully with valid data"
- "Loading spinner appears during API call"
- "List displays all users from database"

### Bad (Vague - Avoid)
- "Works correctly"
- "Looks good"
- "User has good experience"
- "Performs well"
- "Is secure"

### Mandatory Criteria

Every story MUST include:
- `Typecheck passes` (always)
- `Verify changes work in browser` (UI stories only)

## Output Structure

For each feature, create:

```
docs/features/{NN}-{feature-name}/
├── PRD.md          # Stories
└── progress.txt    # Tracking
```

### PRD.md Template

```markdown
# Feature: {Feature Name}

## Overview
{1-2 sentences on what this feature does and its value}

## User Stories

### US-001: {Title}
**Description:** As a {user}, I want {feature} so that {benefit}.
**Acceptance Criteria:**
- [ ] {Criterion}
- [ ] Typecheck passes
**Dependencies:** None

### US-002: {Title}
**Description:** As a {user}, I want {feature} so that {benefit}.
**Acceptance Criteria:**
- [ ] {Criterion}
- [ ] Typecheck passes
- [ ] Verify changes work in browser
**Dependencies:** US-001

### US-003: {Title}
...

## Non-Goals
- {What this feature explicitly does NOT include}

## Technical Notes
- {Implementation hints, gotchas, or constraints}
```

### progress.txt Template

```
# Feature: {Feature Name}
# Status: Not Started

## Stories
- [ ] US-001: {Title}
- [ ] US-002: {Title}
- [ ] US-003: {Title}

## Notes
{Blockers or observations during implementation}
```

## Splitting Strategies

### Feature → Stories

1. **Identify the data** - What schema changes?
2. **Identify the operations** - What CRUD endpoints?
3. **Identify the UI** - What components/pages?
4. **Order by dependency** - Schema first

### Large Story → Smaller Stories

**Too big:** "Build user profile page"

**Split:**
- US-001: Add bio and avatar fields to user schema
- US-002: Create GET /api/users/:id/profile endpoint
- US-003: Create PUT /api/users/:id/profile endpoint
- US-004: Build ProfileCard component (display only)
- US-005: Build ProfileEditForm component
- US-006: Connect ProfileEditForm to API

### Testing Rule of Thumb

If you can't describe how to verify it in one sentence, split it.

## Common Patterns

### CRUD Feature
```
US-001: Add {entity} schema
US-002: Create GET /api/{entities} (list)
US-003: Create GET /api/{entities}/:id (detail)
US-004: Create POST /api/{entities} (create)
US-005: Create PUT /api/{entities}/:id (update)
US-006: Create DELETE /api/{entities}/:id
US-007: Build {Entity}List component
US-008: Build {Entity}Card component
US-009: Build {Entity}Form component
US-010: Build {Entity}Detail page
```

### Authentication Feature
```
US-001: Add auth fields to user schema (passwordHash, etc.)
US-002: Create POST /api/auth/signup endpoint
US-003: Create POST /api/auth/login endpoint
US-004: Create POST /api/auth/logout endpoint
US-005: Add session/JWT middleware
US-006: Build SignupForm component
US-007: Build LoginForm component
US-008: Add auth state provider
US-009: Build protected route wrapper
```

### Dashboard Feature
```
US-001: Create dashboard stats query
US-002: Build StatsCard component
US-003: Build StatsGrid component
US-004: Create recent activity query
US-005: Build ActivityFeed component
US-006: Assemble Dashboard page
```

## Checklist Before Done

- [ ] Every story fits in one context window
- [ ] Stories ordered by dependency
- [ ] All criteria are verifiable
- [ ] Every story has "Typecheck passes"
- [ ] UI stories have "Verify in browser"
- [ ] progress.txt initialized
- [ ] Non-goals stated
