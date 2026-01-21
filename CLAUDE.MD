# Claude Plugins Marketplace

## Overview

Personal Claude Code plugin marketplace by QLAN Software Solutions. A collection of Markdown-based plugins that enhance Claude Code workflows through specialized commands, agents, and skills for full-stack development orchestration and productivity.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Format | Markdown + JSON |
| Runtime | Claude Code CLI |
| Scripting | Python 3.7+ (stdlib only) |
| Orchestration | Bash/Shell |
| Configuration | JSON (plugin.json, marketplace.json) |

## Getting Started

```bash
# Clone the marketplace
git clone git@github.com:qlan-ro/claude-plugins-marketplace.git

# Install in Claude Code
claude plugins:install ./claude-plugins-marketplace

# Or install individual plugins
claude plugins:install ./claude-plugins-marketplace/plugins/project-studio-plugin
```

## Commands

| Command | Description |
|---------|-------------|
| `/new-project` | Start a new project with 7-phase workflow |
| `/add-feature` | Add new features to established projects |
| `/continue-project` | Analyze codebase and continue development |
| `/phase` | Jump to or check status of specific phases |
| `/gate-check` | Verify readiness before advancing phases |
| `/start-ralph` | Set up Ralph autonomous execution environment |
| `/archive-feature` | Archive completed features |
| `/commit` | Commit with conventional message |
| `/pr` | Create pull requests for feature branches |
| `/slack-status` | Generate Slack status from work history |

## Environment Variables

> This is a Markdown-based plugin system with no environment variables required. Session parsers use standard system paths.

| Path | Description | Used By |
|------|-------------|---------|
| `~/.claude/projects/` | Claude Code session history | work-logger |
| `~/.codex/sessions/` | Codex session history | work-logger |

## Architecture

```
plugins/
├── project-studio-plugin/    # Full-stack development orchestration
│   ├── agents/               # AI agents (architect, designer, etc.)
│   ├── commands/             # Slash commands
│   ├── skills/               # Specialized skills
│   ├── references/           # Phase guides & checklists
│   ├── assets/templates/     # Scaffolding templates
│   └── hooks/                # Event-triggered automation
├── work-logger-plugin/       # Slack status generator
│   ├── commands/             # /slack-status command
│   ├── skills/               # Status writer skill
│   └── parsers/              # Python session parsers
└── templates/basic-plugin/   # Template for new plugins
```

## Key Patterns

### Plugin Structure
- Each plugin has `.claude-plugin/plugin.json` metadata
- Commands, agents, and skills are Markdown files
- References provide documentation and checklists

### Agent Pattern
- Markdown files define AI agent behavior and tools
- Agents are specialized for specific domains (architect, designer, etc.)
- Each agent has clear tool access and responsibilities

### Skill Pattern
- Skills bundle prompts with tool access
- Used for domain-specific tasks (PRD discovery, UX design, etc.)
- Can be invoked via orchestration or directly

### Phase Workflow
- 7-phase orchestration: Discovery → AI Workflow → Architecture → Design → Planning → Development → Quality
- Gate checks validate phase completion before advancement
- State persistence enables session continuity

## Testing

```bash
# Validate plugin structure
ls plugins/*/.claude-plugin/plugin.json

# Test slash commands in Claude Code
claude
> /new-project
```

## Deployment

1. Push to GitHub: `git push origin main`
2. Users install via: `claude plugins:install <repo-url>`

## Notes for Claude

### Do
- Follow existing Markdown formatting conventions
- Keep agent/skill files focused and single-purpose
- Test commands in Claude Code before committing
- **Update versions after edits:**
  - Plugin changes → update `plugins/{plugin}/.claude-plugin/plugin.json` version
  - Marketplace changes → update `.claude-plugin/marketplace.json` version

### Don't
- Add external Python dependencies (stdlib only)
- Create circular references between skills
- Skip phase gate validations
- Hardcode user-specific paths

## References

- [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference) - Complete technical reference for skills, agents, hooks, MCP/LSP servers, and plugin.json
- [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) - Marketplace structure, plugin sources, and distribution
- [Distribution and Versioning](https://code.claude.com/docs/en/plugins-reference#distribution-and-versioning-reference) - Semantic versioning guidelines

---

*Last updated: 2025-01-21*
