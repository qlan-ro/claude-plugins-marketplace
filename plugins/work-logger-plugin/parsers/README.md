# AI Session Parsers for Work Logger

This directory contains Python parsers that extract work activities from AI assistant session logs to help generate comprehensive status messages.

## Overview

The parsers analyze conversation history from three sources:
- **Claude Code** sessions (`~/.claude/projects/`)
- **Codex** sessions (`~/.codex/sessions/`)
- **Junie** (Matterhorn) sessions (`~/Library/Caches/JetBrains/IntelliJIdea*/projects/*/matterhorn/.matterhorn/`)

They extract meaningful work activities while filtering out trivial tasks like configuration changes, file browsing, and minor edits.

## Components

### 1. `claude_projects_parser.py`
Parses Claude Code project sessions stored in JSONL format.

**Features:**
- Extracts user requests and tool uses
- Identifies file modifications
- Filters out non-work projects (personal, config, etc.)
- Filters trivial activities (settings changes, helper scripts, read-only operations)
- Associates activities with projects

### 2. `codex_sessions_parser.py`
Parses Codex (OpenAI) session logs organized by date.

**Features:**
- Extracts user messages from session events
- Identifies function calls and tool uses
- Extracts file operations from commands
- Filters out trivial shell commands (ls, cd, pwd)
- Associates activities with working directory/project

### 3. `junie_sessions_parser.py`
Parses Junie (Matterhorn) session logs from JetBrains IntelliJ caches.

**Features:**
- Searches across all IntelliJ versions and projects
- Extracts conversation chains and tasks
- Parses user requests, assistant plans, and tool uses
- Extracts file context from editor
- Filters based on project type and activity importance

### 4. `session_aggregator.py`
Combines outputs from all three parsers into a unified work summary.

**Features:**
- Merges activities from multiple sources
- Sorts by timestamp
- Removes duplicates
- Provides multiple output formats (log, bullets)
- Identifies substantial work (PRs, features, bugs, syncs)

## Usage

### Command Line

Get key activities from the last 24 hours:
```bash
python3 ~/.claude/plugins/work-logger-plugin/parsers/session_aggregator.py --hours 24 --format bullets
```

Get detailed log format:
```bash
python3 ~/.claude/plugins/work-logger-plugin/parsers/session_aggregator.py --hours 24 --format log
```

### From Python

```python
from session_aggregator import SessionAggregator

aggregator = SessionAggregator()
summary = aggregator.get_work_summary(since_hours=24)

# Get bullet-point summary
bullets = aggregator.get_activity_summary_bullets(summary)
for bullet in bullets:
    print(f"• {bullet}")

# Get formatted log
log_output = aggregator.format_for_logging(summary)
print(log_output)
```

### Integration with Slack Status Writer

The parsers are integrated into the `slack-status-writer` skill. When you request a status message, the skill will:

1. Run the session aggregator to get comprehensive activity data
2. Cross-reference with git history
3. Generate a professional Slack status message

Simply use:
```bash
claude /slack-status
```

Or invoke the skill:
```python
# In Claude Code
Use the slack-status-writer skill
```

## Filtering Logic

### Work vs Personal Projects

**Included (work projects):**
- Projects containing: `blueprint`, `smile-app`, `workbench`, `optimizer`, `converter`, `playbook`

**Excluded (personal/config):**
- Projects containing: `claude`, `mcp`, `config`, `plugin`, `dotfiles`

### Trivial vs Substantial Activities

**Excluded (trivial):**
- Configuration/IDE changes (`.vscode/settings.json`, `.run.xml`)
- Utility scripts for personal use
- Minor file operations (rename, move, delete)
- Trivial code changes (typos, console.log, formatting)
- Read-only activities (viewing files, searching, reading docs)
- Basic shell commands (ls, cd, pwd, cat)

**Included (substantial):**
- Pull requests
- Bug fixes
- Feature implementations
- API changes
- Database migrations
- Deployment activities
- Performance optimizations
- Refactoring with business impact
- Sync meetings with decisions/action items
- Code reviews with significant feedback

## Output Formats

### Bullets Format
Concise list of key activities with project names:
```
• blueprint-converter: Implemented ML model serving endpoint
• smile-app: Fixed authentication bug in login flow
• workbench: Reviewed PR #10252 for OR API integration
```

### Log Format
Detailed timestamped entries with tool uses and files:
```
=== blueprint-converter ===

[14:30] [CLAUDE]
Request: Implement ML model serving endpoint with FastAPI
Tools: Write, Edit, Bash
Files: app/main.py, requirements.txt
---

[15:45] [CODEX]
Request: Fix authentication bug in user session handling
Tools: edit_file, shell_command
Files: auth/session.py
---
```

## Technical Details

### Session File Formats

**Claude Code** (`.jsonl` files):
```json
{
  "type": "user",
  "timestamp": "2025-12-15T19:42:28.267Z",
  "message": {
    "role": "user",
    "content": [{"type": "text", "text": "..."}]
  },
  "cwd": "/path/to/project"
}
```

**Codex** (`.jsonl` files):
```json
{
  "type": "event_msg",
  "timestamp": "2025-12-15T19:42:28.365Z",
  "payload": {
    "type": "user_message",
    "message": "..."
  }
}
```

### Time Window Logic

- Activities are filtered by timestamp
- Default lookback: 24 hours
- Timezone-aware comparisons (UTC)
- For Codex: checks multiple days to ensure coverage

## Troubleshooting

### No activities found

Check that session directories exist:
```bash
ls -la ~/.claude/projects/
ls -la ~/.codex/sessions/
```

### Permission errors

Ensure read permissions:
```bash
chmod -R u+r ~/.claude/projects/
chmod -R u+r ~/.codex/sessions/
```

### Import errors

Run from the parsers directory:
```bash
cd ~/.claude/plugins/work-logger-plugin/parsers
python3 session_aggregator.py --hours 24
```

## Extending the Parsers

### Adding New Project Filters

Edit the `is_work_project()` methods in both parsers to customize which projects are considered "work":

```python
def is_work_project(self, project_name: str) -> bool:
    work_indicators = ['your-org', 'work-prefix', 'company-name']
    # ... rest of logic
```

### Adding New Trivial Patterns

Edit the `is_trivial_activity()` methods to customize what's filtered:

```python
trivial_patterns = [
    'your-config-file',
    'temporary-script',
    # ... add more patterns
]
```

### Supporting Additional Session Formats

Create a new parser class following the pattern:
1. Implement `parse_jsonl_file()`
2. Implement `extract_user_messages()`
3. Implement `extract_tool_uses()`
4. Implement `get_work_summary()`
5. Add to `SessionAggregator`

## License

MIT (same as work-logger plugin)
