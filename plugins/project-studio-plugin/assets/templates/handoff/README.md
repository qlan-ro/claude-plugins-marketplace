# Handoff File Templates

This directory contains templates for agent handoff files. These files enable structured communication between agents working on the same project.

## How Handoff Works

```
                      ┌─────────────────────┐
                      │   Main Orchestrator │
                      │    (Claude Agent)   │
                      └──────────┬──────────┘
                                 │
           ┌─────────────────────┼─────────────────────┐
           │                     │                     │
           ▼                     ▼                     ▼
   ┌───────────────┐    ┌───────────────┐    ┌───────────────┐
   │Database Agent │    │Backend Agent  │    │Frontend Agent │
   └───────┬───────┘    └───────┬───────┘    └───────┬───────┘
           │                     │                     │
           ▼                     ▼                     ▼
   ┌───────────────┐    ┌───────────────┐    ┌───────────────┐
   │ database-     │    │ backend-      │    │ frontend-     │
   │ agent-        │───▶│ agent-        │───▶│ agent-        │
   │ output.md     │    │ output.md     │    │ output.md     │
   └───────────────┘    └───────────────┘    └───────────────┘
           │                     │                     │
           └─────────────────────┴─────────────────────┘
                                 │
                                 ▼
                      ┌─────────────────────┐
                      │  .claude/handoff/   │
                      │  (Project Directory)│
                      └─────────────────────┘
```

## Handoff File Location

All handoff files are stored in the project's `.claude/handoff/` directory:

```
project/
└── .claude/
    └── handoff/
        ├── database-agent-output.md
        ├── scala-backend-agent-output.md
        ├── python-backend-agent-output.md
        ├── frontend-agent-output.md
        ├── databricks-agent-output.md
        ├── code-reviewer-output.md
        ├── test-generator-output.md
        └── doc-writer-output.md
```

## When to Use Handoff Files

### Write a Handoff File When:
1. You've completed work that another agent will build upon
2. You've created artifacts (files, schema, APIs) that others need
3. You're passing the task to the next phase

### Read Handoff Files When:
1. You're starting work that depends on another agent
2. You need context about what was already built
3. You're unsure about implementation details

## Template Files

| Template | Used By | Provides |
|----------|---------|----------|
| `database-agent-output.md` | Database Agent | Schema, migrations, column details |
| `backend-agent-output.md` | Backend Agents | API contracts, endpoints, auth |
| `frontend-agent-output.md` | Frontend Agent | Components, routes, state |
| `databricks-agent-output.md` | Databricks Agent | Notebooks, tables, jobs |
| `code-review-output.md` | Code Reviewer | Review verdict, issues, suggestions |
| `test-report-output.md` | Test Generator | Tests created, coverage |
| `doc-report-output.md` | Doc Writer | Docs created/updated |

## Handoff Protocol

### For Producing Agents

```markdown
# {{Agent Name}} Handoff
**Task:** {{What you completed}}
**Timestamp:** {{ISO timestamp}}

## Created Files
- List all files created/modified

## For Next Agent
- Key information they need
- Decisions made
- Constraints to follow

## Integration Points
- How to use what you built
- API contracts, schemas, etc.
```

### For Consuming Agents

1. **Always check** for upstream handoff files before starting
2. **Read completely** - don't skim
3. **Reference specifics** - use exact names, types from handoff
4. **Ask if missing** - don't assume, query the orchestrator

## Handoff Flow by Scenario

### Full-Stack Feature
```
Database Agent
    │
    ├── Writes: database-agent-output.md
    │           (schema, columns, relationships)
    │
    ▼
Backend Agent
    │
    ├── Reads:  database-agent-output.md
    ├── Writes: backend-agent-output.md
    │           (API contract, endpoints, auth)
    │
    ▼
Frontend Agent
    │
    ├── Reads:  backend-agent-output.md
    └── Writes: frontend-agent-output.md
                (components, routes)
```

### Data Pipeline
```
SQL Converter Agent
    │
    ├── Writes: sql-converter-output.md
    │           (converted SQL, compatibility notes)
    │
    ▼
Databricks Agent
    │
    ├── Reads:  sql-converter-output.md
    └── Writes: databricks-agent-output.md
                (notebooks, tables, jobs)
```

### Code Review Flow
```
Implementation Agents
    │
    ├── Write: *-agent-output.md files
    │
    ▼
Code Reviewer Agent
    │
    ├── Reads:  All relevant handoff files
    └── Writes: code-review-output.md
                (verdict, issues, suggestions)
```
