# Changelog - Work Logger Plugin

## [2.0.0] - 2025-12-16

### Breaking Changes

**Removed hook-based logging system** - The plugin no longer uses hooks to log work activities. Instead, it relies entirely on parsing AI assistant session history.

### Why This Change?

The AI session parsers provide **comprehensive, automatic tracking** of all work without requiring any hooks or manual logging:
- Every AI-assisted task is automatically captured
- Rich context about discussions, implementations, and decisions
- No setup required - works out of the box
- Covers all three major AI assistants (Claude Code, Codex, Junie)

### Migration Guide

If you were using v1.x with hooks:
1. **No action needed** - The parsers work automatically
2. **Old hook files** - Can be archived or deleted (moved to `hooks.deprecated/`)
3. **Old work logs** - Still readable but no longer generated

The new approach is simpler and more powerful:
- Before (v1.x): Hooks → Work logs → Status generation
- Now (v2.0): AI sessions + Git → Status generation

## [1.1.0] - 2025-12-15

### Added

#### AI Session Parsers
New Python-based parsers that analyze AI assistant session logs to generate comprehensive work summaries:

- **Claude Code Session Parser** (`parsers/claude_projects_parser.py`)
  - Parses conversation history from `~/.claude/projects/`
  - Extracts user requests, tool uses, and file modifications
  - Filters out trivial activities and non-work projects

- **Codex Session Parser** (`parsers/codex_sessions_parser.py`)
  - Parses Codex session logs from `~/.codex/sessions/`
  - Organizes activities by date and project
  - Extracts function calls and file operations

- **Junie Session Parser** (`parsers/junie_sessions_parser.py`)
  - Parses Junie (Matterhorn) session logs from JetBrains IntelliJ caches
  - Searches across all IntelliJ versions and projects
  - Extracts conversation chains, tasks, and tool uses
  - Parses assistant plans and user requests
  - Includes file context from editor

- **Unified Session Aggregator** (`parsers/session_aggregator.py`)
  - Combines data from Claude Code, Codex, and Junie sessions
  - Provides multiple output formats (bullets, log)
  - Identifies substantial work vs trivial tasks
  - Command-line interface for easy testing

#### Updated Slack Status Writer Skill
Enhanced the `slack-status-writer` skill to use AI session data:

- Primary data source: AI assistant session parsers
- Secondary validation: Git history
- Fallback: Traditional work log files
- Improved filtering of trivial tasks
- Better project categorization

#### Documentation
- Comprehensive README for parsers (`parsers/README.md`)
- Usage examples and troubleshooting guide
- Architecture documentation
- Integration instructions

### Features

#### Smart Activity Filtering
Both parsers automatically filter out:
- Configuration and IDE changes
- Utility scripts and helper tools
- Read-only operations (browsing, searching)
- Trivial shell commands (ls, cd, pwd)
- Minor file operations

They focus on substantial work:
- Pull requests and merges
- Bug fixes and feature implementations
- API development
- Sync meetings and code reviews
- Deployments and migrations

#### Flexible Time Windows
- Configurable lookback period (default: 24 hours)
- Timezone-aware timestamp handling
- Multi-day session analysis

#### Multiple Output Formats

**Bullets Format** - Concise activity list:
```
• project-name: Key activity description
• another-project: Another important task
```

**Log Format** - Detailed timestamped entries:
```
[HH:MM] [SOURCE]
Request: What the user asked for
Tools: Tools used
Files: Files modified
---
```

### Usage

#### Command Line
```bash
# Get bullet-point summary
python3 ~/.claude/plugins/work-logger-plugin/parsers/session_aggregator.py --hours 24 --format bullets

# Get detailed log
python3 ~/.claude/plugins/work-logger-plugin/parsers/session_aggregator.py --hours 24 --format log
```

#### With Slack Status Writer Skill
```bash
# Use the slash command
claude /slack-status

# Or invoke the skill directly
# In Claude Code: "Generate my Slack status"
```

### Technical Details

#### Session File Locations
- Claude Code: `~/.claude/projects/[project-dir]/*.jsonl`
- Codex: `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`

#### Data Extraction
- Parses JSONL (JSON Lines) format
- Extracts conversation context, tool uses, file modifications
- Associates activities with projects and timestamps
- Handles both offset-aware and offset-naive datetimes

#### Project Classification
Work projects are identified by keywords:
- `blueprint`, `smile-app`, `workbench`, `optimizer`, `converter`, `playbook`

Personal/config projects are excluded:
- `claude`, `mcp`, `config`, `plugin`, `dotfiles`

### Breaking Changes
None - fully backward compatible with existing work-logger functionality.

### Migration Guide
No migration needed. The parsers work alongside existing features:
1. Traditional work log files still supported
2. Git history integration unchanged
3. Skill interface remains the same

### Dependencies
- Python 3.7+
- No external Python packages required (uses stdlib only)

### Known Issues
- None currently identified

### Future Enhancements
- [ ] Support for additional AI assistant session formats
- [ ] Machine learning-based activity classification
- [ ] Integration with calendar/meeting data
- [ ] Weekly/monthly summary generation
- [ ] Export to multiple formats (JSON, Markdown, HTML)

---

## [1.0.0] - Previous Release

Initial release with:
- Basic work logging via hooks
- Slack status writer skill
- Git history integration
- Traditional log file format
