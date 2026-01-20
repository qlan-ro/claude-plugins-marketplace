---
name: resume
description: Resume a project workflow from where you left off. Reads orchestration state and provides context for continuation.
---

# Resume Workflow

Resume a project workflow from the previous session's state.

## Arguments

$ARGUMENTS

## Usage

- `/resume` - Show current state and recommendations for continuing
- `/resume --verbose` - Show detailed state including all session history

## How It Works

This command reads `.project-studio/state.yaml` to understand:

1. **Current workflow type** (new-project, continue-project, add-feature)
2. **Current phase** and its status
3. **Pending decisions/blockers** that need resolution
4. **Session history** for context
5. **Resume recommendations** for next steps

## Implementation

When `/resume` is invoked:

### 1. Check for State File

```bash
# Look for state file
if [ -f ".project-studio/state.yaml" ]; then
    # State exists, read and present
else
    # No state - suggest starting fresh or running /phase status
fi
```

### 2. Present Resume Context

Display a structured summary:

```markdown
## 🔄 Resuming Project: {project-name}

### Workflow
- **Type:** {new-project | continue-project | add-feature}
- **Started:** {date}
- **Current Phase:** {phase} ({status})

### Last Session Summary
{summary from last completed session}

### Pending Items
**Decisions Needed:**
- {question 1}
- {question 2}

**Blockers:**
- {blocker description}

### Recommended Next Steps
1. {next recommended action}
2. {alternative if blocked}

### Quick Commands
- `/phase {current}` - Continue current phase
- `/gate-check` - Check if ready to advance
- `/phase status` - See full artifact status
```

### 3. Load Relevant Context

Before continuing, automatically read:
- Current phase's main artifact (if exists)
- Any pending feature PRD being worked on
- Resume context notes from state file

## Example Output

### Basic Resume

```
User: /resume

🔄 Resuming Project: task-manager-app

Workflow: new-project (started Jan 15)
Current Phase: Architecture (Phase 3) - IN PROGRESS

📝 Last Session (Jan 16):
"Completed discovery and AI workflow. Started architecture
 decisions but paused on database selection."

❓ Pending Decisions:
1. Database choice: PostgreSQL vs MongoDB vs SQLite
   Context: Need relational data but also flexible user preferences

⏭️ Recommended Next Steps:
1. Resolve database decision
2. Complete ARCHITECTURE.md
3. Run /gate-check before moving to design

💡 Quick Actions:
• /phase architecture - Continue where you left off
• /gate-check - Check phase 3 requirements
```

### Verbose Resume

```
User: /resume --verbose

🔄 Resuming Project: task-manager-app
==================================

📋 Workflow Details
-------------------
Type: new-project
Started: 2024-01-15T10:30:00Z
Started by: user

📊 Phase Progress
-----------------
✅ Phase 1: Discovery - COMPLETE
✅ Phase 2: AI Workflow - COMPLETE
🔄 Phase 3: Architecture - IN PROGRESS
⏳ Phase 4: Design - NOT STARTED
⏳ Phase 5: Planning - NOT STARTED
⏳ Phase 6: Development - NOT STARTED
⏳ Phase 7: Quality - NOT STARTED

📜 Session History
------------------
Session 1 (Jan 15, 10:30 - 12:00):
- Phases: discovery
- Created: docs/PRODUCT_PRD.md
- Summary: "Completed discovery phase with 5 features in backlog"

Session 2 (Jan 15, 14:00 - 16:30):
- Phases: ai-workflow, architecture
- Created: .ai-workflow.yaml
- Summary: "Configured AI tooling. Started architecture but
            paused on database decision."

🤖 Agent History
----------------
- product-prd-builder (create) - completed
- ai-tooling-advisor (new) - completed
- architect (create) - running (incomplete)

❓ Pending Decisions
-------------------
1. [tech-stack-db] Database selection
   Question: PostgreSQL vs MongoDB?
   Context: Complex relational data + flexible preferences
   Phase: architecture
   Added: Jan 15

🚫 Blockers
-----------
(none)

🔑 Key Decisions Made
---------------------
- TypeScript + React for frontend
- REST API architecture
- GitHub Actions for CI/CD

📦 Artifacts Status
-------------------
docs/PRODUCT_PRD.md: ✅ exists (Jan 15)
.ai-workflow.yaml: ✅ exists (Jan 15)
docs/ARCHITECTURE.md: 🟡 partial (Jan 15)
docs/DESIGN.md: ❌ not created
docs/features/: ❌ empty

⏭️ Resume Recommendations
-------------------------
1. Resolve database decision (PostgreSQL recommended for relational data)
2. Complete ARCHITECTURE.md sections: Data Model, Tech Stack
3. Run /gate-check to validate before Phase 4

💡 Quick Commands
-----------------
/phase architecture  - Continue current phase
/gate-check         - Validate phase 3 complete
/phase status       - Full artifact check
```

## When No State Exists

If `.project-studio/state.yaml` doesn't exist:

```markdown
⚠️ No orchestration state found

This could mean:
1. Project hasn't started a Project Studio workflow yet
2. State file was deleted
3. Working in wrong directory

**Options:**
- `/new-project` - Start a new project workflow
- `/continue-project` - Analyze an existing codebase
- `/phase status` - Check for existing artifacts

Current directory: {pwd}
```

## State File Location

The state file is stored at:
```
{project-root}/.project-studio/state.yaml
```

This directory may also contain:
- `session-logs/` - Detailed logs per session (optional)
- `decisions.md` - Human-readable decision log (optional)

## Integration with Other Commands

The `/resume` command works with:

- **`/phase`** - Respects current phase from state
- **`/gate-check`** - Records results to state
- **`/new-project`** - Initializes state file
- **`/continue-project`** - Initializes state for continue workflow
- **`/add-feature`** - Updates state for add-feature workflow

## Updating State

State is automatically updated by hooks:
- Session start/end
- Phase transitions
- Agent completions
- Gate check results
- Decision resolutions

Manual updates via:
```bash
./hooks/update-orchestration-state.sh <action> <args>
```

## Error Handling

If state file is corrupted:
```
⚠️ State file appears corrupted

Attempting to recover from artifacts...
- Found: PRODUCT_PRD.md, .ai-workflow.yaml
- Inferred phase: Architecture (based on existing artifacts)

Options:
1. `/phase status` - Use artifact-based detection
2. Delete .project-studio/state.yaml and reinitialize
3. Manually fix state file
```
