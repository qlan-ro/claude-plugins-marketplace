# Work Logger Plugin

## Overview

Automated Slack status message generation from AI assistant session history. Parses Claude Code, Codex, and Junie sessions to create professional daily status updates. Zero configuration required - just run the command and get your status.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.7+ |
| Format | JSONL (JSON Lines) |
| Dependencies | stdlib only (no pip install) |
| Data Sources | Claude Code, Codex, Junie |
| CLI | argparse |

## Getting Started

```bash
# Install the plugin
claude plugins:install ./plugins/work-logger-plugin

# Generate your Slack status
claude /slack-status

# Or test parsers directly
python3 parsers/session_aggregator.py --hours 24 --format bullets
```

## Commands

| Command | Description |
|---------|-------------|
| `/slack-status` | Generate Slack status from today's work |

## Environment Variables

> No environment variables required. Plugin reads from standard AI assistant session locations.

| Path | Description | Used By |
|------|-------------|---------|
| `~/.claude/projects/` | Claude Code sessions | claude_projects_parser |
| `~/.codex/sessions/` | Codex sessions | codex_sessions_parser |
| `~/Library/Caches/JetBrains/` | Junie/Matterhorn sessions | junie_sessions_parser |

## Architecture

```
work-logger-plugin/
├── commands/
│   └── slack-status.md           # Slash command definition
├── skills/
│   └── slack-status-writer/      # Core skill with 290+ line SKILL.md
├── parsers/                      # Python session parsers
│   ├── session_aggregator.py     # Main entry (206 lines)
│   ├── claude_projects_parser.py # Claude Code (259 lines)
│   ├── codex_sessions_parser.py  # Codex (327 lines)
│   ├── junie_sessions_parser.py  # Junie/Matterhorn (323 lines)
│   └── README.md                 # Parser documentation
└── hooks.deprecated/             # v1.x hook system (unused)
```

## Key Patterns

### Data Flow
1. AI assistants store sessions automatically
2. Parsers extract activities from all three sources
3. Aggregator merges and deduplicates
4. Trivial activities filtered automatically
5. Git history validates work items
6. Professional bullet-point status generated

### Activity Filtering
**Excluded (trivial):**
- Config/IDE changes (.vscode, .run.xml, settings.json)
- Read-only operations (viewing, searching)
- Minor changes (typos, console.log, formatting)
- Shell commands (ls, cd, pwd)

**Included (substantial):**
- Pull requests and merges
- Bug fixes and features
- API development
- Deployments and migrations
- Code reviews

### Project Classification
**Work projects:** blueprint, smile-app, workbench, optimizer, converter, playbook
**Personal (excluded):** claude, mcp, config, plugin, dotfiles, test, demo

## Testing

```bash
# Get bullet summary (default)
python3 parsers/session_aggregator.py --hours 24 --format bullets

# Get detailed log format
python3 parsers/session_aggregator.py --hours 24 --format log

# Custom time window
python3 parsers/session_aggregator.py --hours 48 --format bullets
```

### Python API

```python
from session_aggregator import SessionAggregator

aggregator = SessionAggregator()
summary = aggregator.get_work_summary(since_hours=24)
bullets = aggregator.get_activity_summary_bullets(summary)
```

## Deployment

1. Update version in `.claude-plugin/plugin.json`
2. Push to GitHub: `git push origin main`
3. Users install via marketplace

## Notes for Claude

### Do
- Use session_aggregator.py as the main entry point
- Validate activities against git history
- Filter trivial activities automatically
- Support all three AI assistants equally
- **Update versions after edits:**
  - Plugin changes → update `.claude-plugin/plugin.json` version
  - Also update `../../.claude-plugin/marketplace.json` version

### Don't
- Add external Python dependencies
- Modify session files (read-only)
- Include personal/config projects in status
- Skip trivial activity filtering

## References

- [PLUGINS-REFERENCE.md](./PLUGINS-REFERENCE.md) - Official Claude Code plugins documentation (local copy)

---

*Last updated: 2025-01-21*
