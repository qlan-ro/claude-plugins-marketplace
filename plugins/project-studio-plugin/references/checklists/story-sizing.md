# Story Sizing Checklist

Validate user stories for single-context-window execution by Ralph agents.

## Core Principle

**Each story must complete in ONE context window (~10 minutes of AI work).**

Stories that are too large will fail during Ralph execution because:
- The agent loses context mid-implementation
- Changes become too interconnected to commit atomically
- Quality checks become harder to pass in one iteration

---

## Automatic Validation Rules

When validating stories, apply these rules and generate warnings:

### Rule 1: Description Length

| Condition | Assessment | Action |
|-----------|------------|--------|
| Description ≤ 3 sentences | PASS | Story is appropriately sized |
| Description > 3 sentences | WARNING | Suggest splitting |

**Why:** If you need more than 3 sentences to describe what a story does, it's doing too much.

### Rule 2: Acceptance Criteria Count

| Condition | Assessment | Action |
|-----------|------------|--------|
| Criteria ≤ 5 items | PASS | Story is appropriately sized |
| Criteria > 5 items | WARNING | Suggest splitting |

**Why:** More than 5 acceptance criteria indicates multiple concerns bundled together.

### Rule 3: Files to Modify

| Condition | Assessment | Action |
|-----------|------------|--------|
| Files ≤ 5 | PASS | Story is appropriately sized |
| Files > 5 | WARNING | Suggest splitting |

**Why:** Touching more than 5 files usually means the change is too spread out for atomic implementation.

---

## Warning Message Templates

### Description Too Long

```
WARNING: Story {story_id} description exceeds 3 sentences.
Current: {sentence_count} sentences

Stories should be describable in 2-3 sentences. Consider splitting into:
- {suggested_split_1}
- {suggested_split_2}

Reference: references/checklists/story-sizing.md
```

### Too Many Acceptance Criteria

```
WARNING: Story {story_id} has {criteria_count} acceptance criteria (limit: 5).

Stories with >5 criteria often combine multiple concerns. Consider:
- Grouping related criteria into separate stories
- Moving edge cases to follow-up stories
- Splitting by layer (schema, backend, frontend)

Reference: references/checklists/story-sizing.md
```

### Too Many Files

```
WARNING: Story {story_id} estimates {file_count} files to modify (limit: 5).

Multi-file changes are harder to implement atomically. Consider:
- One story per component/module
- Separate schema changes from API changes
- Separate API changes from UI changes

Reference: references/checklists/story-sizing.md
```

---

## Splitting Strategies

When a story fails validation, suggest these splitting patterns:

### By Layer (Most Common)

**Before:** "Add user authentication"

**After:**
- US-001: Add auth fields to user schema
- US-002: Create signup endpoint
- US-003: Create login endpoint
- US-004: Build signup form component
- US-005: Build login form component
- US-006: Add auth state provider

### By Operation

**Before:** "Build CRUD for products"

**After:**
- US-001: Create product schema
- US-002: Implement GET /products endpoint
- US-003: Implement POST /products endpoint
- US-004: Implement PUT /products/:id endpoint
- US-005: Implement DELETE /products/:id endpoint

### By Component

**Before:** "Build dashboard with stats, charts, and activity feed"

**After:**
- US-001: Build StatsCard component
- US-002: Build ChartsPanel component
- US-003: Build ActivityFeed component
- US-004: Assemble Dashboard page

### By Data Flow

**Before:** "Implement real-time notifications"

**After:**
- US-001: Add notification schema
- US-002: Create notification API endpoints
- US-003: Implement WebSocket connection
- US-004: Build notification UI component
- US-005: Wire notifications to WebSocket

---

## Size Reference Table

| Story Type | Typical Size | Example |
|------------|-------------|---------|
| Schema addition | 1-2 files | "Add email field to user table" |
| Single endpoint | 2-3 files | "Create GET /users endpoint" |
| Simple component | 1-2 files | "Build LoadingSpinner component" |
| Form component | 2-4 files | "Build LoginForm with validation" |
| Integration | 3-5 files | "Connect form to API endpoint" |
| Page assembly | 3-5 files | "Assemble dashboard from components" |

---

## Quick Self-Check

Before finalizing a story, ask:

1. **Can I describe this in 2-3 sentences?** If no, split it.
2. **Are there ≤5 acceptance criteria?** If no, split it.
3. **Will this touch ≤5 files?** If no, split it.
4. **Can I verify completion in one sentence?** If no, split it.
5. **Does this have one clear purpose?** If no, split it.

---

## Integration with /start-ralph

The `/start-ralph` command should validate stories before creating `prd.json`:

1. Parse each story from Feature PRD
2. Apply validation rules above
3. Display warnings for oversized stories
4. Allow user to proceed with warnings or fix first
5. Include warning status in prd.json notes field

Example output:
```
Validating stories...
  US-001: Add user schema              PASS
  US-002: Build user form              PASS
  US-003: Implement full auth flow     WARNING: Description > 3 sentences
                                       WARNING: 8 acceptance criteria

2 of 3 stories passed validation.
Proceed anyway? Stories with warnings may fail during Ralph execution.
```

---

## Related References

- [Story Writing Skill](../../skills/story-writing/SKILL.md) - Full story writing guidance
- [Phase Gates Checklist](./phase-gates.md) - Phase completion validation
