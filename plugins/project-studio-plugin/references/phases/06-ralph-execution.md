# Phase 6: Ralph Execution

## Objective
Execute user stories autonomously using the Ralph loop pattern, where each story is completed in a single context window.

## Entry Criteria
- Feature PRD created in Phase 5 (Planning)
- Stories sized for single context window execution
- Gate check passed for Phase 5→6

## Overview

Ralph execution is an **alternative to traditional development** (see `06-development.md`). Instead of manual coding, Ralph autonomously implements stories one at a time.

```
Traditional Development (06-development.md):
  Human writes code → Human tests → Human commits

Ralph Execution (06-ralph-execution.md):
  /start-ralph → Ralph implements → Ralph commits → /archive-feature
```

## Why Ralph?

| Aspect | Traditional | Ralph |
|--------|-------------|-------|
| Iteration | Human-driven | Autonomous |
| Context | Full conversation history | Fresh context per story |
| Pace | Variable | Consistent |
| Best for | Complex decisions | Well-defined stories |

Use Ralph when:
- Stories are well-defined with clear acceptance criteria
- Stories are properly sized (single context window)
- Code patterns are established (not greenfield architecture)

Use traditional development when:
- High uncertainty requires exploration
- Stories need human judgment
- Complex architectural decisions mid-story

---

## Key Activities

### 1. Initialize Ralph Environment

```bash
/start-ralph {feature-name}
```

This command:
1. Creates `.ralph/` directory with INSTRUCTIONS.md
2. Converts Feature PRD to `prd.json` (stories start with `passes: false`)
3. Generates `run.sh` wrapper script
4. Creates git branch `ralph/{feature-name}`
5. Initializes `progress.txt` for tracking

**Output Structure:**
```
project-root/
├── .ralph/
│   ├── INSTRUCTIONS.md    # Ralph execution rules
│   └── CLAUDE.md          # Combined instructions (run.sh creates this)
├── prd.json               # User stories in Ralph format
├── progress.txt           # Progress log
└── run.sh                 # Wrapper script
```

### 2. Execute Ralph Loop

```bash
./run.sh
```

Each iteration Ralph:
1. Reads `prd.json` to find next story (`passes: false`)
2. Reads `progress.txt` for context and patterns
3. Implements ONE story
4. Runs quality checks (typecheck, lint, test)
5. Commits with format: `feat: [US-XXX] - {Title}`
6. Updates `prd.json` to set `passes: true`
7. Appends progress to `progress.txt`

**Iteration Cycle:**
```
┌─────────────────────────────────────────────────┐
│                  Ralph Iteration                │
├─────────────────────────────────────────────────┤
│                                                 │
│   1. Read prd.json → Find US-XXX (passes:false) │
│                       ↓                         │
│   2. Read progress.txt → Get patterns/context   │
│                       ↓                         │
│   3. Implement story → Follow acceptance criteria│
│                       ↓                         │
│   4. Quality checks → typecheck, lint, test     │
│                       ↓                         │
│   5. Commit → "feat: [US-XXX] - Title"          │
│                       ↓                         │
│   6. Update prd.json → passes: true             │
│                       ↓                         │
│   7. Update progress.txt → Append learnings     │
│                       ↓                         │
│   8. Check: All stories complete?               │
│      YES → <promise>COMPLETE</promise>          │
│      NO  → End turn (next iteration picks up)   │
│                                                 │
└─────────────────────────────────────────────────┘
```

### 3. Monitor Progress

Watch `progress.txt` for:
- Completed stories
- Patterns discovered (consolidated in "Codebase Patterns" section)
- Gotchas and learnings
- Current story status

### 4. Handle Interruptions

If Ralph is interrupted mid-session:
1. Check `prd.json` for current state (which stories passed)
2. Check `progress.txt` for last completed work
3. Re-run `./run.sh` to continue

Ralph resumes from the next incomplete story automatically.

### 5. Archive Completed Feature

When all stories have `passes: true`:

```bash
/archive-feature
```

This command:
1. Verifies all stories complete
2. Moves artifacts to `.project-studio/archive/{date}-{feature}/`
3. Cleans up `.ralph/` directory (preserves INSTRUCTIONS.md template)
4. Updates `state.yaml` feature status

---

## State Tracking

The orchestrator tracks Ralph sessions in `state.yaml`:

```yaml
# Ralph-specific tracking
ralph:
  active_session: true          # Is Ralph currently running?
  feature: "booking-discount"   # Current feature name
  branch: "ralph/booking-discount"
  started_at: "2024-01-15T10:00:00Z"

  # Story progress
  stories:
    total: 5
    completed: 2
    current: "US-003"

  # Session tracking for resume
  last_iteration:
    story_id: "US-002"
    commit_sha: "abc1234"
    completed_at: "2024-01-15T11:30:00Z"

  # Interruption recovery
  interrupted: false
  resume_context: null
```

### State Transitions

```
/start-ralph:
  ralph.active_session = true
  ralph.feature = {feature}
  ralph.started_at = {now}
  ralph.stories.total = {count from prd.json}
  ralph.stories.completed = 0

Per iteration (auto-updated via progress.txt):
  ralph.stories.completed += 1
  ralph.stories.current = {next story}
  ralph.last_iteration = {story_id, commit_sha, timestamp}

Interruption detected:
  ralph.interrupted = true
  ralph.resume_context = "Last completed: US-XXX"

/archive-feature:
  ralph.active_session = false
  ralph.feature = null
  features.items[feature].status = "completed"
```

---

## Resuming Interrupted Sessions

### Detection

When running `/resume` command, orchestrator checks:
1. Is `ralph.active_session == true`?
2. Does `prd.json` exist with incomplete stories?
3. Does `progress.txt` show partial completion?

### Resume Flow

```markdown
User: /resume

Orchestrator detects:
- Ralph session was active
- Feature: booking-discount
- Progress: 2/5 stories complete
- Last commit: abc1234 (US-002)

Output:
## Ralph Session Resume

**Feature:** booking-discount
**Branch:** ralph/booking-discount
**Progress:** 2/5 stories (40%)

### Completed Stories
✅ US-001: Add discount field
✅ US-002: Discount validation

### Remaining Stories
⬜ US-003: Apply discount to total
⬜ US-004: Discount reports
⬜ US-005: Admin discount management

### Next Steps
1. Run `./run.sh` to continue Ralph execution
2. Ralph will pick up from US-003 automatically
```

### Manual Resume

If `/resume` doesn't work, manual recovery:

```bash
# Check current state
cat prd.json | grep '"passes"'
tail -50 progress.txt

# Continue Ralph
./run.sh
```

---

## Integration with Orchestration

### Phase Entry (from Phase 5)

```
1. User completes Phase 5 (Planning)
2. Gate check passes (stories sized for single context window)
3. User runs /phase ralph OR /start-ralph {feature}
4. Orchestrator initializes Ralph environment
5. State updates: phase.current = "ralph-execution"
```

### During Execution

```
1. Each Ralph iteration commits changes
2. progress.txt updated (source of truth)
3. state.yaml sync (optional, via hook or manual)
4. Orchestrator can report status via /phase status
```

### Phase Exit (to Phase 7)

```
1. All stories complete (all passes: true)
2. Ralph outputs <promise>COMPLETE</promise>
3. User runs /archive-feature
4. State updates: phase.current = "quality"
5. Proceed to Quality phase gate check
```

---

## Slash Commands

### `/start-ralph [feature-name]`
Initialize Ralph environment for autonomous execution.

See `commands/start-ralph.md` for full documentation.

### `/archive-feature [feature-name]`
Archive completed Ralph session and clean up.

See `commands/archive-feature.md` for full documentation.

### `/phase ralph` or `/phase status`
Show current Ralph execution status:
- Stories completed vs remaining
- Last commit info
- Resume instructions if interrupted

---

## Progress File Format

Ralph maintains `progress.txt` with this structure:

```markdown
# Ralph Progress Log
Started: Wed Jan 15 10:00:00 UTC 2024
---

## Codebase Patterns
- Pattern 1 discovered across iterations
- Pattern 2 that future iterations should know
---

## 2024-01-15 10:30 - US-001
- What was implemented
- Files changed
- **Learnings for future iterations:**
  - Patterns discovered
  - Gotchas encountered
  - Useful context
---

## 2024-01-15 11:00 - US-002
...
---
```

The "Codebase Patterns" section is critical - Ralph consolidates reusable learnings there for future iterations.

---

## Phase Gate Checklist

Before proceeding to Quality (Phase 7):
- [ ] All user stories have `passes: true` in prd.json
- [ ] All commits follow conventional format
- [ ] progress.txt documents all implementations
- [ ] No broken tests (Ralph enforces this per-story)
- [ ] Feature archived via `/archive-feature`
- [ ] state.yaml shows Ralph session completed

---

## Troubleshooting

### Ralph stuck on a story

1. Check `progress.txt` for the last entry
2. Read the story's acceptance criteria in `prd.json`
3. Manually implement if needed
4. Update `prd.json` to set `passes: true`
5. Re-run `./run.sh` to continue

### Quality checks failing

1. Run checks manually: `npm run typecheck && npm run lint && npm test`
2. Fix failures
3. Re-run `./run.sh`

### Stories too large for context window

1. Stop Ralph execution
2. Update Feature PRD to split large stories
3. Re-run `/start-ralph` to regenerate `prd.json`
4. Continue execution

### Branch conflicts

```bash
# Save current progress
git stash

# Update from main
git fetch origin main
git rebase origin/main

# Restore progress
git stash pop

# Continue
./run.sh
```

---

## Best Practices

1. **Size stories correctly** - Use `references/checklists/story-sizing.md`
2. **Order by dependency** - Schema → Backend → Frontend
3. **Clear acceptance criteria** - Each criterion should be verifiable
4. **Monitor progress** - Check `progress.txt` periodically
5. **Don't interrupt unnecessarily** - Let Ralph complete stories
6. **Archive promptly** - Run `/archive-feature` when complete
