---
name: project-studio-orchestration
description: |
  Workflow orchestration for full-stack product development. Use this skill when:
  - Coordinating multi-phase development workflows
  - Routing to specialized agents (architect, designer, etc.)
  - Managing phase transitions and gate checks
  - Running /new-project, /continue-project, or /add-feature workflows

  This skill is for ORCHESTRATION ONLY - it knows WHAT agents to use, not HOW they do their work.

  TRIGGERS: "/new-project", "/continue-project", "/add-feature", "/phase", "/gate-check", "project studio", "workflow status"
---

# Project Studio Orchestration

Coordinate multi-phase development workflows by routing to specialized agents.

## Core Principle

**This skill orchestrates. Agents execute.**

- Orchestrator knows: phases, transitions, which agent handles what, gate criteria
- Orchestrator does NOT know: how to write PRDs, how to design UX, how to analyze code
- Each agent has its own skill with domain expertise

## Three Workflows

| Command | Use Case | Starting Phase |
|---------|----------|----------------|
| `/new-project` | Greenfield development | Phase 1: Discovery |
| `/continue-project` | Existing codebase | Phase C1: Codebase Analysis |
| `/add-feature` | Add to established project | Step 1: Validate Foundation |

## New Project Phases

```
Phase 1: DISCOVERY        → product-prd-builder agent
Phase 2: AI WORKFLOW      → ai-tooling-advisor agent
Phase 3: ARCHITECTURE     → architect agent
Phase 4: DESIGN           → designer agent
Phase 5: PLANNING         → feature-prd-builder agent
Phase 6: DEVELOPMENT      → Traditional or Ralph execution
Phase 6R: RALPH EXECUTION → Autonomous story implementation
Phase 7: QUALITY          → testing & deployment
```

## Continue Project Phases

```
Phase C1:   CODEBASE ANALYSIS   → codebase-analyzer agent
Phase C1.5: SKILL DISCOVERY     → Suggest specialized skills based on detected tech stack
Phase C2:   INFER PRD           → product-prd-builder agent (inference mode)
Phase C3:   INFER ARCHITECTURE  → architect agent (documentation mode)
Phase C4:   INFER DESIGN        → designer agent (extraction mode)
Phase C5:   AI TOOLING AUDIT    → ai-tooling-advisor agent (audit mode)
Phase 5+:   STANDARD WORKFLOW   → same as new-project
```

### Phase C1.5: Skill Discovery

After codebase analysis, before proceeding with inference phases:

1. **Read** `CODEBASE_ANALYSIS.md` to extract tech stack
2. **Query** `references/registry.md` for matching skills
3. **Suggest** specialized skills that would help subsequent agents:
   - Scala project → suggest `scala-spring-patterns` skill
   - Python backend → suggest `python-dev`, `fastapi` skills
   - React frontend → suggest `react-tanstack` skill
4. **User installs** recommended skills (or skips)
5. **Continue** to C2 with enhanced agent capabilities

**Why this step exists:**
- Inference phases (C2-C4) benefit from specialized skills
- A Scala backend is better documented by an agent with `scala-spring-patterns`
- Skills must be loaded BEFORE the agent runs

**Output:** List of recommended skills to install before continuing

## Add Feature Steps

```
Step 1: VALIDATE FOUNDATION  → Check PRD, Architecture, Design exist
Step 2: UPDATE PRD           → product-prd-builder agent (append mode)
Step 3: IMPACT ANALYSIS      → Conditional routing based on feature needs
        ├─ Architecture?     → architect agent (amendment mode)
        ├─ Design?           → designer agent (amendment mode)
        └─ AI Tools?         → ai-tooling-advisor agent (feature mode)
Step 4: PLANNING             → feature-prd-builder agent (new features only)
Step 5: DEVELOPMENT          → Ralph loop execution
Step 6: QUALITY              → testing + regression
```

## Agent Routing Table

| Phase/Step | Agent | Skill Loaded | Mode | Output |
|------------|-------|--------------|------|--------|
| 1 | product-prd-builder | prd-discovery | create | PRODUCT_PRD.md |
| 2 | ai-tooling-advisor | ai-tooling | new | .ai-workflow.yaml |
| 3 | architect | arch-decisions | create | ARCHITECTURE.md |
| 4 | designer | ux-design | create | DESIGN.md |
| 5 | feature-prd-builder | story-writing | create | features/*/PRD.md |
| C1 | codebase-analyzer | codebase-analysis | analyze | CODEBASE_ANALYSIS.md |
| C1.5 | (orchestrator) | - | suggest | Skill recommendations |
| C2 | product-prd-builder | prd-discovery + specialized | inference | PRODUCT_PRD.md |
| C3 | architect | arch-decisions + specialized | documentation | ARCHITECTURE.md |
| C4 | designer | ux-design + specialized | extraction | DESIGN.md |
| C5 | ai-tooling-advisor | ai-tooling | audit | .ai-workflow.yaml |
| Add-2 | product-prd-builder | prd-discovery | append | PRODUCT_PRD.md (updated) |
| Add-3 | architect | arch-decisions | amendment | ARCHITECTURE.md (if needed) |
| Add-3 | designer | ux-design | amendment | DESIGN.md (if needed) |
| Add-3 | ai-tooling-advisor | ai-tooling | feature | .ai-workflow.yaml (if needed) |
| Add-4 | feature-prd-builder | story-writing | create | features/*/PRD.md (new only) |

**Notes:**
- Phase 2 (new) creates config from scratch
- Phase C5 (continue) audits existing config and fills gaps
- Add-3 agents only run if impact analysis determines changes needed

## Phase Transitions

### Key Principle: Agents Complete Without Blocking

**Agents complete their work and return output. They do NOT ask questions mid-execution.**

```
Agent runs → Generates output → Returns to orchestrator
                                        ↓
Orchestrator presents summary → User can review/modify artifacts
                                        ↓
User runs /gate-check → /phase {next} to continue
```

**Why:**
- Agents don't block waiting for answers
- User can review artifacts at their own pace
- Clear checkpoints via gate-checks
- User controls when to advance

### Advancing Phases

1. Agent completes and returns output to orchestrator
2. Orchestrator summarizes what was created
3. User reviews generated artifacts (optional but recommended for key phases)
4. User runs `/gate-check` to verify readiness
5. User runs `/phase {next}` to continue

### Gate Checks (Summary)

| Gate | Key Criteria |
|------|--------------|
| 1→2 | PRODUCT_PRD.md exists, feature backlog ordered, non-goals stated |
| 2→3 | .ai-workflow.yaml exists |
| 3→4 | ARCHITECTURE.md exists, tech stack decided, data model defined |
| 4→5 | DESIGN.md exists, user flows mapped, components specified |
| 5→6 | Feature PRDs created, stories sized for one context window |
| 5→6R | Same as 5→6, but user chooses Ralph execution |
| 6→7 | All stories complete, core tests pass |
| 6R→7 | All stories have passes:true, /archive-feature run |
| 7→Done | Tests pass, docs complete, deployment ready |

### Continue Project Gates

| Gate | Key Criteria |
|------|--------------|
| C1→C1.5 | CODEBASE_ANALYSIS.md exists, tech stack identified |
| C1.5→C2 | Specialized skills installed (or skipped), ready for inference |
| C2→C3 | PRODUCT_PRD.md with status markers (✅/🟡/📋) |
| C3→C4 | ARCHITECTURE.md documents existing patterns |
| C4→C5 | DESIGN.md extracts existing tokens/components |
| C5→5 | .ai-workflow.yaml created/updated, tooling gaps addressed |

## Artifact Structure

```
{project}/
├── .project-studio/           # Orchestration state (NEW)
│   └── state.yaml             # Session continuity, phase tracking
├── .ai-workflow.yaml          # Phase 2
├── docs/
│   ├── CODEBASE_ANALYSIS.md   # Continue-project only
│   ├── PRODUCT_PRD.md         # Phase 1
│   ├── ARCHITECTURE.md        # Phase 3
│   ├── DESIGN.md              # Phase 4
│   └── features/              # Phase 5
│       ├── 01-{name}/
│       │   ├── PRD.md
│       │   └── progress.txt
│       └── ...
├── src/                       # Phase 6
└── tests/                     # Phase 7
```

## State Management

### Session Continuity

The `.project-studio/state.yaml` file enables session continuity:

```yaml
# Key sections:
workflow:
  type: "new-project"    # Workflow identification
  started_at: "..."

phase:
  current: "architecture"
  status: "in_progress"

sessions:              # Session history
  - session_id: "..."
    summary: "..."

pending:               # Handoff context
  decisions: [...]
  blockers: [...]

resume_context:        # Next session guidance
  last_action: "..."
  next_recommended: "..."
```

### Resuming Work

When starting a new Claude Code session:

1. Run `/workflow-status` to see current state and recommendations
2. State file shows:
   - Current phase and status
   - Pending decisions/blockers
   - Session history summary
   - Recommended next steps
3. Continue from where you left off

### State Updates

State is automatically updated by hooks when:
- Phase artifacts are created (PRODUCT_PRD.md, ARCHITECTURE.md, etc.)
- Artifacts are modified
- Gate checks are run

Manual updates via:
```bash
./hooks/update-orchestration-state.sh <action> <args>
```

### Benefits

1. **Session continuity** - Context preserved across Claude Code sessions
2. **Explicit tracking** - No ambiguity about current phase status
3. **Decision tracking** - Pending decisions don't get lost
4. **Audit trail** - Full history of what was done and when
5. **Resume guidance** - Clear recommendations for continuing

## Ralph Execution Tracking

### Ralph Session State

When a Ralph session is active, additional tracking is added to `state.yaml`:

```yaml
# Ralph-specific tracking
ralph:
  active_session: true
  feature: "booking-discount"
  branch: "ralph/booking-discount"
  started_at: "2024-01-15T10:00:00Z"

  stories:
    total: 5
    completed: 2
    current: "US-003"

  last_iteration:
    story_id: "US-002"
    commit_sha: "abc1234"
    completed_at: "2024-01-15T11:30:00Z"

  interrupted: false
  resume_context: null
```

### State Transitions

| Event | State Change |
|-------|--------------|
| `/start-ralph` | `ralph.active_session = true`, initialize tracking |
| Story complete | `ralph.stories.completed += 1`, update `last_iteration` |
| Interruption | `ralph.interrupted = true`, set `resume_context` |
| `/archive-feature` | `ralph.active_session = false`, clear tracking |

### Resuming Ralph Sessions

The `/workflow-status` command checks for active Ralph sessions:

1. **Detection**: `ralph.active_session == true` OR `prd.json` exists with incomplete stories
2. **Context**: Shows completed vs remaining stories, last commit
3. **Action**: Instructs user to run `./run.sh` to continue

Example resume output:
```
## Ralph Session Resume

**Feature:** booking-discount
**Progress:** 2/5 stories (40%)

### Completed Stories
✅ US-001: Add discount field
✅ US-002: Discount validation

### Remaining
⬜ US-003: Apply discount to total
⬜ US-004: Discount reports
⬜ US-005: Admin discount management

### Next Steps
1. Run `./run.sh` to continue
2. Ralph resumes from US-003 automatically
```

### Ralph Commands

| Command | Description |
|---------|-------------|
| `/start-ralph [feature]` | Initialize Ralph environment |
| `/archive-feature [feature]` | Archive completed session |
| `/phase ralph` | Show Ralph execution status |
| `/workflow-status` | Resume interrupted session |

See `commands/start-ralph.md` and `commands/archive-feature.md` for details.

## Slash Commands

### `/new-project [idea]`
1. If idea provided, acknowledge and begin Phase 1
2. If no idea, ask "What would you like to build?"
3. Spawn product-prd-builder agent

### `/continue-project [path]`
1. If path provided, begin analysis
2. If no path, ask for project location
3. Spawn codebase-analyzer agent

### `/add-feature [description]`
1. Validate foundation docs exist (PRD, Architecture, Design)
2. If missing → suggest `/continue-project` instead
3. If foundation exists:
   - Update PRD with new feature(s) → product-prd-builder (append mode)
   - Run impact analysis (architecture, design, AI tools)
   - Conditionally update impacted docs
   - Create Feature PRD for new items only
   - Continue to development

### `/phase [name|status]`
- `status` → Report artifact presence and current phase
- `discovery` → Phase 1 with product-prd-builder
- `architecture` → Phase 3 with architect
- `design` → Phase 4 with designer
- `planning` → Phase 5 with feature-prd-builder
- `ralph` → Phase 6R Ralph execution status (stories completed, remaining)

### `/gate-check [phase]`
1. Detect current phase from artifacts (or use specified phase)
2. Run checklist for that gate
3. Report PASS/FAIL with specific issues
4. Recommend next steps

## Orchestration Flow Example

```
User: /new-project "task management app"

Orchestrator:
  1. "Starting Phase 1: Discovery"
  2. Spawn product-prd-builder agent
  3. Agent completes → returns summary
  4. "Phase 1 Complete. Created docs/PRODUCT_PRD.md"
  5. "Run /gate-check then /phase ai-workflow to continue"

User: /gate-check

Orchestrator:
  6. Checks gate criteria
  7. "Gate 1 PASSED. Ready for Phase 2."

User: /phase ai-workflow

Orchestrator:
  8. "Starting Phase 2: AI Workflow"
  9. Spawn ai-tooling-advisor agent
  10. Agent completes → returns summary
  11. "Phase 2 Complete. Created .ai-workflow.yaml"

User: /gate-check
User: /phase architecture
... continues with user controlling transitions
```

## Key Rules

1. **Never duplicate agent knowledge** - Orchestrator routes, agents execute
2. **Agents complete without blocking** - Never ask questions mid-execution
3. **User controls advancement** - User explicitly runs `/phase {next}`
4. **Always check gates** - Don't skip phases without user consent
5. **Track artifacts** - Use file existence to determine current state
6. **Spawn correct agent** - Each phase has ONE designated agent

## Reference Materials

For detailed phase instructions and templates, see:

- `references/phases/` - Detailed instructions for each phase
  - `01-discovery.md` - PRD discovery process
  - `02-ai-workflow.md` - AI tooling configuration (Phase 2)
  - `03-architecture.md` - Architecture decisions
  - `04-design.md` - UX design process
  - `05-planning.md` - Feature PRD creation
  - `06-development.md` - Traditional development approach
  - `06-ralph-execution.md` - Ralph autonomous execution
  - `07-quality.md` - Testing & deployment

- `references/continue-project/` - Continue workflow specifics
  - `01-codebase-analysis.md`
  - `01.5-skill-discovery.md` - Skill recommendations based on tech stack
  - `02-infer-product-prd.md`
  - `03-infer-architecture.md`
  - `04-infer-design.md`
  - `05-ai-tooling-audit.md`

- `references/add-feature/` - Add feature workflow
  - `workflow.md` - Complete add-feature process

- `references/checklists/phase-gates.md` - Detailed gate criteria
- `references/registry.md` - Skills, agents, and MCP server catalog

- `assets/templates/` - Document templates
  - `product-prd-template.md`
  - `feature-prd-template.md`
  - `architecture-template.md`
  - `design-spec-template.md`
  - `ai-workflow-template.yaml`
  - `implementation-plan-template.md`

## Phase 2: AI Workflow Configuration

Phase 2 uses the **ai-tooling-advisor** agent to:

1. **Classify project** by platform, languages, frameworks, features
2. **Query registry** (`references/registry.md`) for matching tools
3. **Present recommendations** to user (skills, agents, MCP servers)
4. **Generate `.ai-workflow.yaml`** from template

See `references/phases/02-ai-workflow.md` for detailed instructions.

---

## Git Workflow Integration

The **git-workflow** agent handles all version control operations during development.

### When Git Workflow Runs

| Trigger | Mode | What Happens |
|---------|------|--------------|
| Starting Feature PRD | `branch` | Create feature branch |
| User story complete | `story-commit` | Commit changes with conventional message |
| All stories complete | `feature-pr` | Create PR and push |

### Development Flow with Git

```
Phase 5: PLANNING
    │
    └─► git-workflow (branch mode)
        └─► Creates: feature/{feature-name}

Phase 6: DEVELOPMENT (Ralph Loop)
    │
    ├─► Story US-001 complete
    │   └─► git-workflow (story-commit mode)
    │       └─► Commit: "feat(scope): description"
    │
    ├─► Story US-002 complete
    │   └─► git-workflow (story-commit mode)
    │       └─► Commit: "feat(scope): description"
    │
    └─► All stories complete
        └─► git-workflow (feature-pr mode)
            └─► Creates PR, returns URL

Phase 7: QUALITY
    └─► Review PR, merge when approved
```

### Orchestrator Integration

After each user story is marked complete in `progress.txt`:

```
1. Orchestrator detects story completion
2. Spawns git-workflow agent (story-commit mode)
3. Agent verifies (tests, lint)
4. Agent commits with conventional message
5. Agent updates progress.txt with commit SHA
6. Orchestrator continues to next story
```

After all stories in Feature PRD are complete:

```
1. Orchestrator detects feature completion
2. Runs /gate-check for Phase 6→7
3. Spawns git-workflow agent (feature-pr mode)
4. Agent pushes branch
5. Agent creates PR via GitHub CLI
6. Agent returns PR URL
7. Orchestrator reports PR to user
```

### Progress File Format

```
# Feature: Booking Discounts
# Branch: feature/booking-discounts

[x] US-001: Add discount field - COMMITTED (abc1234)
[x] US-002: Discount validation - COMMITTED (def5678)
[x] US-003: Apply discount to total - COMMITTED (ghi9012)
[ ] US-004: Discount reports - IN_PROGRESS
[ ] US-005: Admin discount management - PENDING

# Status: 3/5 stories committed
# PR: Not yet created
```

After feature completion:
```
# Status: 5/5 stories committed
# PR: #123 (https://github.com/org/repo/pull/123)
```

### Updated Agent Routing Table (Phase 6)

| Step | Agent | Mode | Output |
|------|-------|------|--------|
| Start feature | git-workflow | branch | Feature branch |
| Story complete | git-workflow | story-commit | Commit SHA |
| Feature complete | git-workflow | feature-pr | PR URL |

### Slash Command Updates

#### `/commit` (New)
Manually trigger a commit for current work:
```
/commit "feat(bookings): add discount field"
```
Spawns git-workflow in story-commit mode.

#### `/pr` (New)
Manually create a PR for current feature:
```
/pr
```
Spawns git-workflow in feature-pr mode.

### Safety Rules

The git-workflow agent enforces:

- **No force push** to main/master
- **No commits** without passing tests
- **No secrets** in committed code
- **Conventional commits** format required
- **Story reference** in commit messages

### Configuration

Git workflow behavior can be customized in `.ai-workflow.yaml`:

```yaml
git:
  auto_commit: true          # Commit after each story
  auto_pr: true              # Create PR when feature complete
  branch_prefix: "feature/"  # Branch naming
  require_tests: true        # Must pass tests before commit
  conventional_commits: true # Enforce conventional format
```
