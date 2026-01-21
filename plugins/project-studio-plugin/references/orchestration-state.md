# Orchestration State Reference

This document describes the `.project-studio/state.yaml` file that enables session continuity across Claude Code sessions.

## Purpose

The orchestration state file solves these problems:

1. **Lost context** - When you close Claude Code and reopen, context is lost
2. **Phase ambiguity** - File existence doesn't capture partial progress
3. **Decision tracking** - Pending decisions get forgotten between sessions
4. **Session handoff** - No clear "what to do next" guidance

## File Location

```
{project-root}/
└── .project-studio/
    └── state.yaml
```

The `.project-studio/` directory should be committed to git to preserve state across machines.

## Schema Reference

### Schema Version

```yaml
schema_version: 1
```

Used for future migrations if the schema changes.

### Workflow Identification

```yaml
workflow:
  type: "new-project"  # new-project | continue-project | add-feature
  started_at: "2024-01-15T10:30:00Z"
  started_by: "user"
```

- **type**: Which workflow was initiated
- **started_at**: ISO timestamp when workflow began
- **started_by**: Who/what started it (for audit)

### Phase Tracking

```yaml
phase:
  current: "architecture"
  current_number: 3
  status: "in_progress"  # not_started | in_progress | blocked | completed
  continue_phase: null   # C1 | C1.5 | C2 | C3 | C4 | C5 | null
  add_feature_step: null # 1-6 | null
```

- **current**: Human-readable phase name
- **current_number**: Numeric phase (1-7)
- **status**: Current phase status
- **continue_phase**: For continue-project workflow, tracks C1-C5 phases
- **add_feature_step**: For add-feature workflow, tracks steps 1-6

### Phase Completion

```yaml
phases_completed:
  discovery: false
  ai_workflow: false
  architecture: false
  design: false
  planning: false
  development: false
  quality: false
  # Continue-project specific
  codebase_analysis: false
  skill_discovery: false
  infer_prd: false
  infer_architecture: false
  infer_design: false
  ai_tooling_audit: false
```

Boolean flags for explicit completion tracking (more reliable than file existence).

### Gate Check History

```yaml
gate_checks:
  - phase: "discovery"
    checked_at: "2024-01-15T11:00:00Z"
    passed: true
    issues: []
  - phase: "architecture"
    checked_at: "2024-01-15T14:00:00Z"
    passed: false
    issues:
      - "Missing database technology decision"
      - "Security approach not defined"
```

Records every gate check attempt with results.

### Session History

```yaml
sessions:
  - session_id: "session-20240115-103000"
    started_at: "2024-01-15T10:30:00Z"
    ended_at: "2024-01-15T12:00:00Z"
    phases_worked: ["discovery"]
    artifacts_created:
      - "docs/PRODUCT_PRD.md"
    summary: "Completed discovery phase with 5 features in backlog."
```

Archived sessions provide audit trail and context.

### Current Session

```yaml
current_session:
  session_id: "session-20240116-090000"
  started_at: "2024-01-16T09:00:00Z"
  phases_worked: ["ai-workflow", "architecture"]
  artifacts_modified:
    - ".ai-workflow.yaml"
    - "docs/ARCHITECTURE.md"
  pending_work: "Completing data model section"
```

Active session being tracked.

### Agent Execution Log

```yaml
agent_runs:
  - agent: "product-prd-builder"
    mode: "create"
    phase: "discovery"
    started_at: "2024-01-15T10:35:00Z"
    completed_at: "2024-01-15T11:45:00Z"
    output_file: "docs/PRODUCT_PRD.md"
    status: "completed"  # running | completed | failed
```

Tracks which agents ran, when, and their outputs.

### Feature Tracking

```yaml
features:
  total: 5
  in_planning: 2
  in_development: 1
  completed: 2

  items:
    - id: "01-user-authentication"
      status: "completed"
      stories_total: 5
      stories_completed: 5
      branch: "feature/user-authentication"
      pr_url: "https://github.com/org/repo/pull/12"
```

Project-level feature overview (complements per-feature progress.txt).

### Pending Items

```yaml
pending:
  decisions:
    - id: "tech-stack-db"
      question: "Which database: PostgreSQL vs MongoDB?"
      context: "Complex relational data + flexible preferences"
      options:
        - "PostgreSQL with JSONB"
        - "MongoDB"
        - "PostgreSQL + Redis"
      phase: "architecture"
      created_at: "2024-01-15T14:00:00Z"

  blockers:
    - id: "missing-api-spec"
      description: "Need external API docs from payment provider"
      phase: "architecture"
      blocking_agent: "architect"
      created_at: "2024-01-15T14:30:00Z"

  questions:
    - id: "design-library"
      question: "Tailwind CSS vs shadcn/ui?"
      phase: "design"
      created_at: "2024-01-15T15:00:00Z"
```

Items that need resolution before continuing. Critical for session handoff.

### Resume Context

```yaml
resume_context:
  last_action: "Completed AI workflow config, started architecture"
  next_recommended: "Resolve database decision, complete ARCHITECTURE.md"
  key_decisions_made:
    - "TypeScript + React for frontend"
    - "REST API (not GraphQL)"
    - "GitHub Actions for CI/CD"
  open_questions:
    - "Which component library?"
    - "Real-time features needed?"
```

Human-readable context for the next session. This is what `/workflow-status` displays.

### Artifact Tracking

```yaml
artifacts:
  "docs/PRODUCT_PRD.md":
    exists: true
    last_modified: "2024-01-15T11:45:00Z"
    checksum: "sha256:abc123..."
    created_by_agent: "product-prd-builder"
    created_in_phase: "discovery"
```

Track artifacts with checksums to detect external modifications.

### User Preferences

```yaml
preferences:
  auto_commit: true
  auto_gate_check: false
  verbosity: "normal"
  skip_confirmations: false
```

User preferences captured during workflow.

## Updating State

### Via Hooks (Automatic)

Hooks automatically update state when:
- Artifacts are created (PostToolUse hooks)
- Sessions start/end
- Gate checks complete

### Via Script (Manual)

```bash
# Session management
./hooks/update-orchestration-state.sh session-start
./hooks/update-orchestration-state.sh session-end "Completed Phase 3"

# Phase management
./hooks/update-orchestration-state.sh phase-start architecture
./hooks/update-orchestration-state.sh phase-complete architecture

# Gate checks
./hooks/update-orchestration-state.sh gate-check architecture true
./hooks/update-orchestration-state.sh gate-check architecture false "Missing database decision"

# Agent tracking
./hooks/update-orchestration-state.sh agent-start architect create architecture
./hooks/update-orchestration-state.sh agent-complete architect docs/ARCHITECTURE.md

# Workflow type
./hooks/update-orchestration-state.sh workflow-type new-project

# Feature updates
./hooks/update-orchestration-state.sh feature-update 01-auth completed

# Resume context
./hooks/update-orchestration-state.sh set-resume-context "Finished X" "Next do Y"

# Decisions
./hooks/update-orchestration-state.sh add-decision db-choice "PostgreSQL or MongoDB?" architecture
./hooks/update-orchestration-state.sh resolve-decision db-choice "PostgreSQL"

# Status check
./hooks/update-orchestration-state.sh status
```

### Dependency

The script uses `yq` for YAML manipulation. Install via:
```bash
brew install yq  # macOS
```

## Commands

### `/workflow-status`

Shows current state and recommendations for continuing:

```
🔄 Resuming Project: task-manager-app

Workflow: new-project (started Jan 15)
Current Phase: Architecture (Phase 3) - IN PROGRESS

📝 Last Session:
"Completed discovery and AI workflow. Started architecture."

❓ Pending Decisions:
1. Database: PostgreSQL vs MongoDB

⏭️ Next Steps:
1. Resolve database decision
2. Complete ARCHITECTURE.md

💡 Quick Actions:
• /phase architecture - Continue
• /gate-check - Validate
```

### `/phase status`

Enhanced with state file data (shows both artifact-based and state-based status).

## Best Practices

### 1. Start Every Session Right

When opening Claude Code on a project:
```
/workflow-status
```

This loads context and shows what to do next.

### 2. End Sessions Cleanly

Before closing:
```bash
./hooks/update-orchestration-state.sh session-end "Summary of what was done"
./hooks/update-orchestration-state.sh set-resume-context "Last thing done" "Next thing to do"
```

### 3. Track Pending Items

When you encounter a decision that needs user input:
```bash
./hooks/update-orchestration-state.sh add-decision "db-choice" "PostgreSQL or MongoDB?" "architecture"
```

When resolved:
```bash
./hooks/update-orchestration-state.sh resolve-decision "db-choice" "PostgreSQL"
```

### 4. Commit State File

The `.project-studio/state.yaml` file should be committed:
```bash
git add .project-studio/
git commit -m "chore: update orchestration state"
```

This preserves state across machines and collaborators.

## Migration

If schema changes in future versions:

1. Check `schema_version` field
2. Run migration script (to be created)
3. State is preserved during migration

## Troubleshooting

### State File Corrupted

```bash
# Check YAML syntax
yq . .project-studio/state.yaml

# If corrupted, can regenerate from artifacts
rm .project-studio/state.yaml
/phase status  # Uses artifact-based detection
# Then reinitialize state manually
```

### yq Not Installed

The state update script falls back to basic operations without yq, but full functionality requires it:
```bash
brew install yq  # macOS
apt-get install yq  # Debian/Ubuntu
```

### State Out of Sync

If state doesn't match actual artifacts:
```bash
# Check actual artifacts
/phase status

# Manually update state
./hooks/update-orchestration-state.sh phase-complete <phase>
```
