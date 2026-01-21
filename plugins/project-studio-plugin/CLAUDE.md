# Project Studio Plugin

## Overview

Full-stack product development orchestration from idea to production-ready code. Guides teams through a structured 7-phase workflow, transforming vague ideas into working applications with proper documentation and AI-optimized planning. Integrates with Ralph for autonomous story execution.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Format | Markdown + YAML |
| Runtime | Claude Code CLI |
| State Management | YAML (orchestration state) |
| Scripting | Bash/Shell |
| AI Execution | Ralph loop pattern |

## Getting Started

```bash
# Install the plugin
claude plugins:install ./plugins/project-studio-plugin

# Start a new project
claude /new-project "Your project idea"

# Or continue an existing project
claude /continue-project /path/to/project
```

## Commands

| Command | Description |
|---------|-------------|
| `/new-project [idea]` | Start 7-phase greenfield workflow |
| `/continue-project [path]` | Analyze codebase and infer documentation |
| `/add-feature [description]` | Add features to established project |
| `/phase [name\|status]` | Jump to phase or check status |
| `/gate-check [phase]` | Verify readiness before advancing |
| `/start-ralph [feature]` | Initialize Ralph execution environment |
| `/archive-feature [feature]` | Archive completed feature artifacts |
| `/commit [message]` | Commit with conventional message |
| `/pr [--draft]` | Create pull request for feature branch |
| `/resume [--verbose]` | Show state and pending items |

## Environment Variables

> No environment variables required. Plugin operates on project-local state files.

| Path | Description | Purpose |
|------|-------------|---------|
| `.project-studio/state.yaml` | Orchestration state | Session continuity |
| `.ai-workflow.yaml` | AI tooling config | Skills/agents/MCP servers |
| `docs/` | Generated artifacts | PRD, Architecture, Design |

## Architecture

```
project-studio-plugin/
├── agents/                     # 5 core AI agents
│   ├── product-prd-builder.md  # PRD creation (create/inference/append)
│   ├── architect.md            # Tech decisions (create/documentation/amendment)
│   ├── designer.md             # UX specs (create/extraction/amendment)
│   ├── feature-prd-builder.md  # Story breakdown (US-XXX format)
│   └── codebase-analyzer.md    # Existing codebase analysis
├── commands/                   # 10 slash commands
├── skills/                     # 7 domain-specific skills
│   ├── prd-discovery/          # Idea → PRD transformation
│   ├── orchestration/          # Phase routing and state
│   ├── story-writing/          # User story sizing
│   ├── arch-decisions/         # Tech stack options
│   ├── ux-design/              # Design specifications
│   ├── codebase-analysis/      # Code archaeology
│   └── ai-tooling/             # Tool recommendations
├── references/                 # Phase guides and checklists
│   ├── phases/                 # 8 phase reference docs
│   ├── continue-project/       # Existing codebase workflow
│   ├── checklists/             # Gate checks, story sizing
│   └── registry.md             # Skills/agents/MCP catalog
├── hooks/                      # 13 automation hooks
├── assets/templates/           # Document and config templates
└── scripts/                    # Ralph execution scripts
```

## Key Patterns

### Phase Workflow (New Project)
1. **Discovery** → product-prd-builder → `PRODUCT_PRD.md`
2. **AI Workflow** → ai-tooling-advisor → `.ai-workflow.yaml`
3. **Architecture** → architect → `ARCHITECTURE.md`
4. **Design** → designer → `DESIGN.md`
5. **Planning** → feature-prd-builder → `features/*/PRD.md`
6. **Development** → Ralph or manual → `src/*`
7. **Quality** → testing/docs → `tests/*`

### Agent Routing
Each phase routes to ONE specialized agent with a specific skill and mode.

### Session Continuity
`.project-studio/state.yaml` tracks:
- Current phase and status
- Gate check history
- Pending decisions/blockers
- Resume context for next session

### Vertical Slices
Features are complete user capabilities (schema + backend + frontend), not horizontal layers.

### Story Sizing
Each user story must fit in ONE context window (~10 min of AI work).

## Testing

```bash
# Validate plugin structure
ls agents/*.md commands/*.md skills/*/

# Test workflow in Claude Code
claude
> /new-project "Test project"
> /phase status
> /gate-check
```

## Deployment

1. Update version in `.claude-plugin/plugin.json`
2. Push to GitHub: `git push origin main`
3. Users install via marketplace

## Notes for Claude

### Do
- Route to ONE agent per phase
- Wait for gate-check before advancing phases
- Update orchestration state after each action
- Size stories for one context window
- Use vertical slices for feature breakdown
- **Update versions after edits:**
  - Plugin changes → update `.claude-plugin/plugin.json` version
  - Also update `../../.claude-plugin/marketplace.json` version

### Don't
- Skip phase gates
- Create horizontal layer stories (just DB, just API)
- Block agents mid-execution for input
- Lose state between sessions
- Mix phases without completing current

## References

- [PLUGINS-REFERENCE.md](./PLUGINS-REFERENCE.md) - Official Claude Code plugins documentation (local copy)

---

*Last updated: 2025-01-21*
