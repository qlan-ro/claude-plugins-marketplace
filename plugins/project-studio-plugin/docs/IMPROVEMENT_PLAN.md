# Project Studio Plugin Improvement Plan
## Ralph-Compatible Workflow + Companion App Integration

---

## Executive Summary

**Goal:** Transform `project-studio-plugin` to be **Ralph-compatible** while adding companion app integration:

1. **Ralph-compatible execution** - Generate `prd.json` + `progress.txt` that work with vanilla `ralph.sh`
2. **Hybrid PRD format** - Keep human-readable `PRD.md` + generate machine-parseable `tasks.json`
3. **Fresh context per iteration** - Adopt Ralph's stateless loop model
4. **External Ralph dependency** - Use `snarktank/ralph` as-is, not embedded
5. **Companion app integration** - WebSocket bridge for monitoring AND control
6. **Sequential first, parallel later** - Start single-threaded, add worktree parallelism later

**Key Components:**
- **Plugin** (claude-plugins-marketplace): PRD creation, tasks.json generation, state management
- **Ralph** (snarktank/ralph): External dependency for execution loop
- **Companion App** (/Projects/project-studio): Web UI for visualization and control
- **Communication**: WebSocket bridge with HMAC-signed tokens

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Companion Web App                             │
│  (Next.js + Express + PostgreSQL + WebSocket Server)            │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Dashboard   │  │   Progress   │  │  Command Interface   │  │
│  │  (monitor)   │  │  (tracking)  │  │  (control)           │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│           │                │                    │                │
│           └────────────────┴────────────────────┘                │
│                            │                                     │
│                    WebSocket Server (:3001)                      │
└────────────────────────────┬────────────────────────────────────┘
                             │ WebSocket (HMAC tokens)
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                    Claude Code Session                           │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Project Studio Plugin                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐   │   │
│  │  │ Orchestrator│  │ WS Bridge   │  │ State Manager   │   │   │
│  │  │ (skills)    │  │ (events)    │  │ (.project-studio)│  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │         Parallel Execution (git worktrees)                │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐               │   │
│  │  │ Worker 1 │  │ Worker 2 │  │ Worker 3 │               │   │
│  │  │ (story)  │  │ (story)  │  │ (tests)  │               │   │
│  │  └──────────┘  └──────────┘  └──────────┘               │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Ralph vs Current Project-Studio

| Aspect | Ralph (snarktank/ralph) | Current Project-Studio | Target State |
|--------|------------------------|----------------------|--------------|
| **Task format** | JSON `prd.json` | Markdown PRD only | **Hybrid: PRD.md + tasks.json** |
| **Progress tracking** | Single `progress.txt` | Multiple per feature | **Single progress.txt** |
| **Iteration model** | Fresh context per loop | Continuous session | **Fresh context (Ralph loop)** |
| **Learnings storage** | `AGENTS.md` + progress.txt patterns | State file only | **`.ralph/LEARNINGS.md` + curated patterns** |
| **Story sizing** | ONE context window (enforced) | Encouraged | **Enforced with validation** |
| **Orchestration** | `ralph.sh` bash loop | Skills + orchestrator | **External ralph.sh** |
| **Working files** | Project root (gitignored) | `.project-studio/` | **Project root (Ralph-compatible)** |

---

## Ralph Integration Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Project-Studio Plugin                         │
│  (Phase 1-5: Discovery → Architecture → Design → Planning)      │
│                                                                  │
│  Outputs:                                                        │
│  ├── docs/PRODUCT_PRD.md        (human-readable)                │
│  ├── docs/ARCHITECTURE.md       (human-readable)                │
│  ├── docs/DESIGN.md             (human-readable)                │
│  └── .project-studio/features/*/  (per-feature)                 │
│       └── PRD.md                (Ralph-compatible format)       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ /project-studio:start-ralph command
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Ralph Execution Loop                          │
│  (External: snarktank/ralph)                                    │
│                                                                  │
│  ./ralph.sh --tool claude 50                                    │
│                                                                  │
│  Reads:                        Writes:                          │
│  ├── prd.json                  ├── prd.json (updates passes)    │
│  ├── progress.txt              ├── progress.txt (appends)       │
│  ├── .ralph/LEARNINGS.md       ├── .ralph/LEARNINGS.md          │
│  └── Combined context          └── Git commits                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ WebSocket events
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Companion Web App                             │
│  (Real-time monitoring + control)                               │
│                                                                  │
│  ├── Dashboard (progress visualization)                         │
│  ├── Question answering UI                                      │
│  └── Command interface                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## File Structure (Ralph-Compatible)

```
project-root/
├── prd.json                      # ACTIVE feature (Ralph reads this)
├── progress.txt                  # Single file (Ralph appends here)
├── AGENTS.md                     # Project agent notes (optional, user-maintained)
├── CLAUDE.md                     # PROJECT instructions (generated by ai-tooling phase)
├── .ralph/
│   ├── INSTRUCTIONS.md           # Ralph execution rules (from snarktank/ralph)
│   ├── LEARNINGS.md              # Ralph execution learnings (Ralph updates this)
│   └── run.sh                    # Wrapper combining all context files
│
├── .project-studio/
│   ├── state.yaml                # Plugin state (phases, current feature)
│   ├── config.yaml               # Plugin config (companion app URL, etc.)
│   ├── features/                 # Feature PRDs (Ralph-compatible format)
│   │   ├── 01-authentication/
│   │   │   └── PRD.md            # Ralph-compatible PRD (parsed by Ralph)
│   │   └── 02-dashboard/
│   │       └── PRD.md
│   └── archive/                  # Completed feature archives
│       └── 2026-01-20-auth/
│           ├── prd.json
│           └── progress.txt
│
├── docs/
│   ├── PRODUCT_PRD.md            # Overall product PRD
│   ├── ARCHITECTURE.md           # Technical architecture
│   └── DESIGN.md                 # UX/UI design
│
└── .gitignore                    # Includes: prd.json, progress.txt
```

**Key points:**
- `prd.json` and `progress.txt` at root (Ralph-compatible)
- These files are **gitignored** (working files, not committed)
- When starting a feature: `/project-studio:start-ralph` runs Ralph's parser on `.project-studio/features/*/PRD.md` → `prd.json`
- When completing a feature: `/project-studio:archive-feature` archives to `.project-studio/archive/`

---

## Handling CLAUDE.md Conflict

**Problem:** Ralph's `CLAUDE.md` (execution instructions) conflicts with the project's `CLAUDE.md` (project-specific AI instructions generated by ai-tooling phase).

**Solution:** Keep them separate and pass Ralph instructions via stdin when launching.

### File Separation

| File | Purpose | Source |
|------|---------|--------|
| `CLAUDE.md` | Project-specific AI instructions | Generated by ai-tooling phase |
| `.ralph/INSTRUCTIONS.md` | Ralph execution instructions | Copied from snarktank/ralph |

### How Ralph Receives Instructions

**Option A: Modified ralph.sh (Recommended)**

The `/project-studio:start-ralph` command generates a project-specific `ralph.sh` wrapper that:
1. Reads `.ralph/INSTRUCTIONS.md` (Ralph execution rules)
2. Reads `CLAUDE.md` (project context)
3. Combines them and passes to Claude Code

```bash
# .ralph/run.sh (generated by /project-studio:start-ralph)
#!/bin/bash

# Combine Ralph instructions + project context
COMBINED_PROMPT=$(cat << 'COMBINED_EOF'
# Ralph Execution Instructions
$(cat .ralph/INSTRUCTIONS.md)

# Project Context
$(cat CLAUDE.md)
COMBINED_EOF
)

# Run Claude with combined context
echo "$COMBINED_PROMPT" | claude --dangerously-skip-permissions --print
```

**Option B: Use Claude's --append-system-prompt flag (if available)**

```bash
claude --append-system-prompt "$(cat .ralph/INSTRUCTIONS.md)" --print < /dev/null
```

**Option C: Symlink during Ralph execution**

```bash
# Before Ralph run
mv CLAUDE.md CLAUDE.project.md
cp .ralph/INSTRUCTIONS.md CLAUDE.md

# After Ralph run (in cleanup)
mv CLAUDE.project.md CLAUDE.md
```

### /project-studio:start-ralph Command Updates

The command should:
1. Copy Ralph's `INSTRUCTIONS.md` to `.ralph/INSTRUCTIONS.md` (if not exists)
2. Generate `.ralph/run.sh` wrapper script
3. Ensure both files are read during execution

```bash
# Generated .ralph/run.sh
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Read Ralph instructions and project CLAUDE.md
RALPH_INSTRUCTIONS=$(cat "$SCRIPT_DIR/INSTRUCTIONS.md")
PROJECT_CLAUDE=$(cat "$PROJECT_DIR/CLAUDE.md" 2>/dev/null || echo "")

# Combine for Claude context
FULL_CONTEXT="$RALPH_INSTRUCTIONS

---
# Project-Specific Instructions
$PROJECT_CLAUDE"

# Run Claude with full context
cd "$PROJECT_DIR"
echo "$FULL_CONTEXT" | claude --dangerously-skip-permissions --print
```

---

## Handling AGENTS.md Conflict

**Problem:** Ralph's `AGENTS.md` (execution learnings) conflicts with the project's `AGENTS.md` (project-specific AI agent notes/documentation the user may maintain independently).

**Solution:** Same pattern as CLAUDE.md - keep them separate, combine when running Ralph.

### File Separation

| File | Purpose | Source |
|------|---------|--------|
| `AGENTS.md` | Project-specific agent notes (optional, user-maintained) | User or ai-tooling phase |
| `.ralph/LEARNINGS.md` | Ralph execution learnings | Ralph updates during execution |

### How Ralph Uses Learnings

**Option A: Combined Context (Recommended)**

The `.ralph/run.sh` wrapper combines both files when running Ralph:

```bash
# In .ralph/run.sh (updated)

# Read both learnings files
RALPH_LEARNINGS=$(cat "$SCRIPT_DIR/LEARNINGS.md" 2>/dev/null || echo "")
PROJECT_AGENTS=$(cat "$PROJECT_DIR/AGENTS.md" 2>/dev/null || echo "")

# Combine for Claude context
FULL_CONTEXT="$RALPH_INSTRUCTIONS

---
# Project-Specific Instructions
$PROJECT_CLAUDE

---
# Ralph Execution Learnings (patterns discovered during Ralph loop)
$RALPH_LEARNINGS

---
# Project Agent Notes (user-maintained)
$PROJECT_AGENTS"
```

**Option B: Ralph writes to .ralph/LEARNINGS.md only**

Modify Ralph's prompt to write learnings to `.ralph/LEARNINGS.md` instead of root `AGENTS.md`:
- Pros: No conflict with user's AGENTS.md
- Cons: Requires modifying Ralph instructions

**Option C: Namespaced sections in AGENTS.md**

If user doesn't have their own AGENTS.md, Ralph can use root `AGENTS.md` with clear section markers:

```markdown
# AGENTS.md

## Ralph Execution Learnings
<!-- DO NOT EDIT BELOW - Ralph auto-updates this section -->
- Pattern: Use `sql<number>` for aggregations
- Pattern: Always IF NOT EXISTS in migrations
<!-- END RALPH SECTION -->

## Project-Specific Notes
<!-- User-maintained section -->
- Custom notes here...
```

### Updated File Structure

```
project-root/
├── prd.json                      # ACTIVE feature (Ralph reads this)
├── progress.txt                  # Single file (Ralph appends here)
├── AGENTS.md                     # Project agent notes (optional, user-maintained)
├── CLAUDE.md                     # Project instructions (ai-tooling phase)
├── .ralph/
│   ├── INSTRUCTIONS.md           # Ralph execution rules (from snarktank/ralph)
│   ├── LEARNINGS.md              # Ralph learnings (Ralph updates this)
│   └── run.sh                    # Wrapper combining all context files
│
├── .project-studio/
│   └── ...
```

### /project-studio:start-ralph Command Updates (Extended)

The command should now:
1. Copy Ralph's `INSTRUCTIONS.md` to `.ralph/INSTRUCTIONS.md`
2. Create empty `.ralph/LEARNINGS.md` if it doesn't exist
3. Generate `.ralph/run.sh` wrapper that combines:
   - `.ralph/INSTRUCTIONS.md` (Ralph execution rules)
   - `CLAUDE.md` (project AI instructions)
   - `.ralph/LEARNINGS.md` (Ralph execution learnings)
   - `AGENTS.md` (project agent notes, if exists)
4. Update Ralph's prompt template to write learnings to `.ralph/LEARNINGS.md`

### Updated .ralph/run.sh Template

```bash
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Read all context files
RALPH_INSTRUCTIONS=$(cat "$SCRIPT_DIR/INSTRUCTIONS.md")
PROJECT_CLAUDE=$(cat "$PROJECT_DIR/CLAUDE.md" 2>/dev/null || echo "")
RALPH_LEARNINGS=$(cat "$SCRIPT_DIR/LEARNINGS.md" 2>/dev/null || echo "")
PROJECT_AGENTS=$(cat "$PROJECT_DIR/AGENTS.md" 2>/dev/null || echo "")

# Combine for Claude context
FULL_CONTEXT="# Ralph Execution Instructions
$RALPH_INSTRUCTIONS

---
# Project-Specific Instructions
$PROJECT_CLAUDE

---
# Ralph Execution Learnings
$RALPH_LEARNINGS

---
# Project Agent Notes
$PROJECT_AGENTS

---
# IMPORTANT: Write any new learnings to .ralph/LEARNINGS.md, NOT to AGENTS.md
"

# Run Claude with full context
cd "$PROJECT_DIR"
echo "$FULL_CONTEXT" | claude --dangerously-skip-permissions --print
```

---

## Plugin Changes Required

### 1. Ralph-Compatible PRD Format (story-writing skill update)

**Approach:** Use Ralph's built-in `skill-prd-parser` instead of creating our own converter.

**Changes to `story-writing` skill:**
- Output PRD.md in a format Ralph's parser can read
- Follow Ralph's expected markdown structure for stories
- Include metadata Ralph expects (feature ID, branch name, etc.)

**PRD.md format (Ralph-compatible):**
```markdown
# Feature: Authentication

**Feature ID:** 01-authentication
**Branch:** ralph/authentication
**Description:** User authentication system

## User Stories

### US-001: Add user schema
**Priority:** 1

As a developer, I need user table for authentication.

**Acceptance Criteria:**
- [ ] Create users table with id, email, password_hash
- [ ] Add migration file
- [ ] Typecheck passes

### US-002: Implement signup API
**Priority:** 2
...
```

**Why not create our own converter:**
- Ralph already has `skill-prd-parser.js` that converts PRDs to task lists
- Duplicating this functionality adds maintenance burden
- `/project-studio:start-ralph` command can invoke Ralph's parser to generate `prd.json`

### 2. Ralph Activation Command (NEW)

**Command:** `/project-studio:start-ralph [feature-id]`

**What it does:**
1. Validates feature PRD.md exists and is Ralph-compatible format
2. Invokes Ralph's `skill-prd-parser` to generate `prd.json` from PRD.md
3. Creates/resets `progress.txt` with header
4. Creates git branch from feature's `branchName`
5. Generates `.ralph/run.sh` wrapper (combines context files)
6. Prints instructions to run Ralph loop

**Example output:**
```
✅ Feature 01-authentication activated for Ralph execution

Files created:
  - prd.json (6 stories, 0 completed)
  - progress.txt (initialized)
  - Branch: ralph/authentication

To start Ralph loop:
  cd /path/to/project
  ./path/to/ralph/ralph.sh --tool claude 50

Or run manually with Claude Code (one story at a time).
```

### 3. WebSocket Bridge Skill (NEW)

Connects to companion app for real-time monitoring.

**Location:** `skills/websocket-bridge/SKILL.md`

**Events emitted:**
```yaml
# Plugin → Companion App
- type: "ralph:started"
  payload: { projectId, featureId, totalStories }

- type: "story:completed"
  payload: { projectId, storyId, commitSha }

- type: "ralph:completed"
  payload: { projectId, featureId, duration }

- type: "question:asked"
  payload: { projectId, questionId, question, options }
```

**Commands received:**
```yaml
# Companion App → Plugin
- type: "answer:received"
  payload: { questionId, answer: "A" }
```

### 4. Enhanced State Manager

Extend `.project-studio/state.yaml` with:

```yaml
# Current session
session:
  id: "uuid"
  started_at: "ISO-8601"
  websocket_connected: true
  companion_app_url: "ws://localhost:3001"

# Execution tracking (Ralphysh patterns)
execution:
  max_iterations: 5
  current_iteration: 0
  iteration_history: []

# Parallel workers
workers:
  - id: "worker-1"
    story_id: "US-001"
    worktree: ".worktrees/us-001"
    status: "executing"
  - id: "worker-2"
    story_id: "US-002"
    worktree: ".worktrees/us-002"
    status: "completed"

# Decision log (Ralphysh pattern)
decisions:
  - timestamp: "ISO-8601"
    agent: "architect"
    decision: "Selected PostgreSQL"
    reasoning: "JSONB support, team familiarity"
    alternatives: ["MySQL", "MongoDB"]

# Learned guardrails (Ralphysh pattern)
guardrails:
  never_touch:
    - "*.lock"
    - "migrations/*.sql"
  learned:
    - date: "2026-01-20"
      rule: "Always run tests before commit"
      source: "failed-story-US-003"
```

### 5. AGENTS.md Integration

Ralph uses `AGENTS.md` for learnings. We'll integrate this with project-studio:

**Location:** Project root `AGENTS.md` (created by plugin if not exists)

**Content structure:**
```markdown
# Project Learnings

## Codebase Patterns
- Use `sql<number>` template for aggregations
- Always use `IF NOT EXISTS` for migrations
- Components follow `src/components/{feature}/{Component}.tsx` pattern

## Directory-Specific Notes

### src/api/
- All endpoints return `{ data, error }` shape
- Use `withAuth` middleware for protected routes

### src/db/
- Migrations must be idempotent
- Use transactions for multi-table operations
```

**Plugin responsibility:**
- Create initial AGENTS.md during architecture phase
- Ralph updates it during execution with new learnings
- Plugin reads it for context in future phases

### 6. Standalone Mode Preservation

The plugin MUST work without the companion app or Ralph:

```yaml
# .project-studio/config.yaml
ralph:
  enabled: true               # Generate tasks.json for Ralph
  auto_archive: true          # Archive completed features

companion_app:
  enabled: false              # Default: works standalone
  url: "ws://localhost:3001"
  fallback: "file"            # If WS fails, write to events.jsonl
```

**Modes:**
1. **Plugin-only:** Use plugin for planning (Phases 1-5), manual implementation
2. **Plugin + Ralph:** Use plugin for planning, Ralph for execution
3. **Plugin + Ralph + Companion:** Full stack with web UI monitoring

---

## Companion App Changes Required

Your companion app documentation is already well-designed. Key alignments needed:

### 1. WebSocket Protocol Alignment

Update `apps/api/src/websocket/` to handle plugin events:

```typescript
// Handle plugin events
ws.on('message', (data) => {
  const event = JSON.parse(data);

  switch(event.type) {
    case 'phase:started':
      // Update project phase in database
      // Broadcast to all subscribed clients
      break;
    case 'story:completed':
      // Update story status
      // Trigger progress recalculation
      break;
    case 'question:asked':
      // Show modal in web UI
      // Wait for user answer
      // Send answer back to plugin
      break;
  }
});
```

### 2. Command Interface

The web UI needs a "Command Interface" to trigger plugin commands:

```typescript
// POST /api/projects/:id/commands
{
  command: "/project-studio:new-project",
  args: "Task management app",
  options: { interview: true }
}

// This sends WebSocket message to Claude Code session
ws.send(JSON.stringify({
  type: 'command:execute',
  payload: { projectId, command, args, options }
}));
```

### 3. Progress Visualization

Real-time progress from plugin events:

```
┌─────────────────────────────────────────────────┐
│  Feature: Authentication (4/14 stories)         │
│  ████████░░░░░░░░░░░░░░  28%                   │
│                                                 │
│  ✅ US-001 Create user schema                   │
│  ✅ US-002 Implement signup API                 │
│  ✅ US-003 Create login endpoint                │
│  🔄 US-004 Add JWT middleware (in progress)     │
│  ⏳ US-005 Build signup form                    │
│  ⏳ US-006 Create login page                    │
│  ...                                            │
└─────────────────────────────────────────────────┘
```

---

## Implementation Phases

### Phase A: Ralph Compatibility (Core)

**Week 1-2: Make plugin generate Ralph-compatible files**

| # | Change | Files | Effort |
|---|--------|-------|--------|
| A1 | Update `story-writing` skill for Ralph-compatible PRD format | `skills/story-writing/SKILL.md` | Medium |
| A2 | Create `/project-studio:start-ralph` command (uses Ralph's parser) | `commands/start-ralph.md` | Medium |
| A3 | Create `/project-studio:archive-feature` command | `commands/archive-feature.md` | Low |
| A4 | Add `.ralph/LEARNINGS.md` generation to architecture phase | `agents/architect.md` | Low |
| A5 | Update .gitignore template | `assets/templates/gitignore-additions.txt` | Low |

### Phase B: Ralph Patterns in Plugin

**Week 3-4: Adopt Ralph patterns for reliability**

| # | Change | Files | Effort |
|---|--------|-------|--------|
| B1 | Enforce one-context-window story sizing | `skills/story-writing/SKILL.md` | Medium |
| B2 | Add "Codebase Patterns" to progress.txt | `references/progress-format.md` | Low |
| B3 | Curated learnings in AGENTS.md | `skills/orchestration/SKILL.md` | Medium |
| B4 | Fresh context awareness in agents | All agent files | Medium |

### Phase C: WebSocket Bridge (Companion Integration)

**Week 5-6: Connect plugin to companion app**

| # | Change | Files | Effort |
|---|--------|-------|--------|
| C1 | Create `websocket-bridge` skill | `skills/websocket-bridge/SKILL.md` | Medium |
| C2 | Event emission hooks | `hooks/emit-event.sh` | Medium |
| C3 | `/project-studio:connect` and `/project-studio:disconnect` commands | `commands/connect.md` | Low |
| C4 | Graceful degradation (offline mode) | Config + bridge skill | Low |

### Phase D: Future Enhancements (Post-MVP)

**Week 7+: Advanced features**

| # | Change | Files | Effort |
|---|--------|-------|--------|
| D1 | Git worktree parallelism | `skills/parallel-execution/SKILL.md` | High |
| D2 | Multi-feature orchestration | Orchestrator updates | High |
| D3 | Cost tracking per iteration | New hooks | Medium |
| D4 | Interview mode (pre-execution questions) | All agents | Medium |

---

## New Plugin Files to Create

```
plugins/project-studio-plugin/
├── skills/
│   └── websocket-bridge/          # NEW: Companion app integration
│       ├── SKILL.md               # WebSocket communication
│       └── protocol.md            # Event types documentation
│
├── hooks/
│   ├── emit-event.sh              # NEW: Send events to WebSocket
│   └── archive-feature.sh         # NEW: Archive completed features
│
├── commands/
│   ├── start-ralph.md             # NEW: Activate feature for Ralph
│   ├── archive-feature.md         # NEW: Archive completed feature
│   ├── connect.md                 # NEW: Connect to companion app
│   └── disconnect.md              # NEW: Disconnect from companion
│
├── references/
│   ├── ralph-integration.md       # NEW: How plugin works with Ralph
│   ├── ralph-prd-format.md        # NEW: Ralph-compatible PRD.md format spec
│   └── progress-format.md         # NEW: progress.txt format spec
│
└── assets/templates/
    ├── progress-txt-template.md   # NEW: Initial progress.txt content
    ├── learnings-md-template.md   # NEW: Initial .ralph/LEARNINGS.md content
    ├── gitignore-additions.txt    # NEW: Lines to add to .gitignore
    ├── ralph-instructions.md      # NEW: Ralph execution instructions (from snarktank/ralph)
    └── ralph-run-sh-template.sh   # NEW: Wrapper script template
```

---

## Files to Modify

| File | Changes |
|------|---------|
| `skills/story-writing/SKILL.md` | Output Ralph-compatible PRD.md format |
| `agents/feature-prd-builder.md` | Use Ralph-compatible story format |
| `agents/architect.md` | Generate initial `.ralph/LEARNINGS.md` |
| `skills/orchestration/SKILL.md` | Add Ralph workflow awareness |
| `references/phases/05-planning.md` | Document Ralph-compatible PRD format |
| `references/phases/06-development.md` | Document Ralph execution option |

---

## Companion App Alignment

Your companion app (in `/Projects/project-studio`) needs these additions:

### 1. Plugin Connection Handler

```typescript
// apps/api/src/websocket/plugin-handler.ts
export class PluginConnectionHandler {
  // Handle Claude Code session connecting
  handlePluginConnect(ws: WebSocket, projectId: string) {
    // Register plugin as event source for this project
    // Start receiving phase/story/question events
  }

  // Send command to plugin
  sendCommand(projectId: string, command: string, args: any) {
    const ws = this.getPluginConnection(projectId);
    ws.send(JSON.stringify({
      type: 'command:execute',
      payload: { command, args }
    }));
  }
}
```

### 2. Question Answering UI

When plugin sends `question:asked`, show modal:

```
┌─────────────────────────────────────────────────┐
│  🤖 Agent Question                              │
│                                                 │
│  Which database should we use?                  │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ A) PostgreSQL (Recommended)             │   │
│  │    Relational, JSONB support, mature    │   │
│  └─────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────┐   │
│  │ B) MongoDB                              │   │
│  │    Document-based, flexible schema      │   │
│  └─────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────┐   │
│  │ C) SQLite                               │   │
│  │    Simple, file-based, no server needed │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  [Skip] [Answer A]                              │
└─────────────────────────────────────────────────┘
```

### 3. Parallel Worker Visualization

```
┌─────────────────────────────────────────────────┐
│  Parallel Workers (3/4 active)                  │
│                                                 │
│  Worker 1 ████████████░░░░  75%  US-001        │
│  Worker 2 ██████░░░░░░░░░░  40%  US-002        │
│  Worker 3 ████████████████ 100%  US-003 ✅     │
│  Worker 4 ░░░░░░░░░░░░░░░░  --   (idle)        │
│                                                 │
│  [Pause All] [Cancel] [Add Worker]              │
└─────────────────────────────────────────────────┘
```

---

## Critical Files to Modify (Plugin)

| File | Changes |
|------|---------|
| `skills/orchestration/SKILL.md` | Add WebSocket event emission, iteration tracking, parallel coordination |
| `hooks/hooks.toml` | Add new hooks: emit-event, track-iteration, guard-files, summarize-session |
| `references/orchestration-state.md` | Expand state schema with workers, decisions, guardrails |
| `agents/*.md` (all 7) | Add decision logging, interview mode, iteration awareness |
| `commands/new-project.md` | Add `--interview`, `--dry-run`, `--parallel` flags |
| `commands/add-feature.md` | Same flags as new-project |

---

## Verification Plan

### Phase A Verification (Ralph Compatibility)
1. **tasks.json generation:** Create Feature PRD → verify `tasks.json` generated with correct schema
2. **Ralph compatibility:** Copy tasks.json to prd.json → run `ralph.sh` → verify it works
3. **Start command:** Run `/project-studio:start-ralph 01-auth` → verify prd.json created at root
4. **Archive command:** Run `/project-studio:archive-feature` → verify files moved to `.project-studio/archive/`
5. **AGENTS.md:** Complete architecture phase → verify AGENTS.md created with initial patterns

### Phase B Verification (Ralph Patterns)
1. **Story sizing:** Create story > 3 sentences → verify warning/split suggestion
2. **Progress format:** Complete story → verify progress.txt has "Codebase Patterns" section
3. **Learnings curation:** Discover pattern → verify added to AGENTS.md
4. **Fresh context:** Verify each Ralph iteration starts with empty context + file reads

### Phase C Verification (WebSocket Bridge)
1. **Connection:** Run `/project-studio:connect` → verify WebSocket connects to companion app
2. **Event emission:** Ralph completes story → verify event appears in companion dashboard
3. **Offline mode:** Disconnect companion → verify Ralph continues working standalone

### Phase D Verification (Future Enhancements)
1. **Parallelism:** Start 2 features → verify each gets own worktree
2. **Cost tracking:** Complete feature → verify token usage logged

---

## Success Criteria

| Metric | Target | How to Verify |
|--------|--------|---------------|
| Ralph compatibility | 100% | Vanilla ralph.sh runs on generated prd.json |
| tasks.json schema | Valid | JSON validates against schema |
| Story sizing | ≤3 sentences | Validator warns on oversized stories |
| AGENTS.md integration | Present | Created during architecture phase |
| Companion app events | Real-time | Events appear within 100ms |
| Standalone mode | 100% | Plugin + Ralph work without companion |

---

## User Workflow Example

### Starting a New Project with Ralph

```bash
# 1. Run project-studio plugin for planning
claude
> /project-studio:new-project "Task management app"
  # Completes phases 1-5: Discovery → Architecture → Design → Planning
  # Outputs:
  #   docs/PRODUCT_PRD.md
  #   docs/ARCHITECTURE.md
  #   docs/DESIGN.md
  #   .project-studio/features/01-authentication/PRD.md  # Ralph-compatible format
  #   CLAUDE.md              # Project-specific AI instructions

# 2. Activate feature for Ralph execution
> /project-studio:start-ralph 01-authentication
  # Ralph's parser reads .project-studio/features/01-authentication/PRD.md
  # Creates:
  #   prd.json (generated by Ralph's prd-parser)
  #   progress.txt (initialized)
  #   .ralph/INSTRUCTIONS.md (Ralph execution rules)
  #   .ralph/LEARNINGS.md (empty, Ralph will populate)
  #   .ralph/run.sh (wrapper that combines all context files)
  #   Branch: ralph/authentication

# 3. Exit Claude Code, run Ralph loop
exit

# 4. Run Ralph with wrapper (preserves project CLAUDE.md)
./.ralph/run.sh 50
  # Wrapper combines:
  #   - .ralph/INSTRUCTIONS.md (how to execute Ralph loop)
  #   - CLAUDE.md (project-specific context)
  #   - .ralph/LEARNINGS.md (Ralph execution learnings)
  #   - AGENTS.md (project agent notes, if exists)
  # Each iteration: fresh Claude instance with combined context
  # Updates prd.json (passes: true), appends to progress.txt
  # Writes learnings to .ralph/LEARNINGS.md (NOT root AGENTS.md)

# 5. When complete, archive and continue
claude
> /project-studio:archive-feature
  # Moves prd.json, progress.txt to archive
  # Ready for next feature: /project-studio:start-ralph 02-dashboard
```

### With Companion App (Optional)

```bash
# Same as above, but first:
> /project-studio:connect
  # Connects to ws://localhost:3001
  # Events emitted during Ralph execution appear in web UI
  # Can answer questions from browser
```
