# Work Logger Plugin v2.0

**Zero-setup Slack status generation from AI assistant session history**

Automatically generates professional Slack status messages by analyzing your AI-assisted work across Claude Code, Codex, and Junie, validated against git history.

## What's New in v2.0

🎉 **No hooks, no manual logging required!**

- Automatically parses session history from all your AI assistants
- Combines with git history for validation
- Works out of the box - zero configuration needed
- Smarter filtering of trivial tasks

## Quick Start

### Installation

```bash
# Clone or download this plugin to your Claude plugins directory
mkdir -p ~/.claude/plugins
cp -r work-logger ~/.claude/plugins/
```

### Generate Your Slack Status

```bash
# Use the slash command
claude /slack-status

# Or just ask
"Generate my Slack status for today"
```

That's it! The plugin automatically:
1. ✅ Parses your AI assistant sessions (Claude Code, Codex, Junie)
2. ✅ Checks your git commits and PRs
3. ✅ Filters out trivial tasks
4. ✅ Generates a professional status message

## How It Works

### Data Sources

The plugin intelligently combines two sources:

**1. AI Session History** (Primary Source)
- **Claude Code**: `~/.claude/projects/`
- **Codex**: `~/.codex/sessions/`
- **Junie**: `~/Library/Caches/JetBrains/IntelliJIdea*/projects/*/matterhorn/.matterhorn/`

Captures:
- What you discussed with AI assistants
- What features/fixes you implemented
- Technical decisions and architecture discussions
- Files you worked on

**2. Git History** (Validation Source)
- Commit messages and PR numbers
- Branch names
- What was actually merged

Validates:
- What work was completed
- What's still in progress
- PR references and issue IDs

### Smart Filtering

Automatically excludes:
- Configuration changes
- Trivial file operations
- IDE settings
- Read-only activities
- Personal projects

Includes:
- Pull requests (always!)
- Bug fixes
- Feature implementations
- API changes
- Sync meetings with decisions
- Code reviews

## Example Output

### Input (from your day)
- Claude Code: Implemented ML model serving endpoint
- Junie: Fixed display issues on mobile screens
- Git: `PR #10252: [15379] - OR fixes`
- Codex: Architecture discussion for converter adapter

### Output (Slack Status)
```
Status:
• Pull Request 10252: [15379] - OR fixes
• Implemented ML model serving endpoint with FastAPI
• Fixed responsive design issues on iPhone screens (393x852)
• Architectural review for blueprint-converter-connection-adapter
```

## Advanced Usage

### Manual Testing

Test the session aggregator directly:

```bash
# Get bullet-point summary of last 24 hours
python3 ~/.claude/plugins/work-logger-plugin/parsers/session_aggregator.py \
  --hours 24 \
  --format bullets

# Get detailed log format
python3 ~/.claude/plugins/work-logger-plugin/parsers/session_aggregator.py \
  --hours 24 \
  --format log
```

### Customize Time Window

```bash
# Last 48 hours
python3 ~/.claude/plugins/work-logger-plugin/parsers/session_aggregator.py \
  --hours 48 \
  --format bullets
```

### Project Filtering

Edit the parsers to customize which projects are considered "work":

```python
# In parsers/*_parser.py
def is_work_project(self, project_name: str) -> bool:
    work_indicators = ['your-company', 'work-prefix']
    # ... customize logic
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Slack Status Writer                     │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Claude     │  │    Codex     │  │    Junie     │  │
│  │   Sessions   │  │   Sessions   │  │   Sessions   │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                  │                  │          │
│         └──────────────────┼──────────────────┘          │
│                            │                             │
│                    ┌───────▼────────┐                    │
│                    │   Session      │                    │
│                    │  Aggregator    │                    │
│                    └───────┬────────┘                    │
│                            │                             │
│              ┌─────────────┴─────────────┐              │
│              │                           │              │
│       ┌──────▼──────┐            ┌──────▼──────┐       │
│       │ AI Session  │            │   Git       │       │
│       │   Data      │            │  History    │       │
│       └──────┬──────┘            └──────┬──────┘       │
│              │                           │              │
│              └──────────┬────────────────┘              │
│                         │                               │
│                  ┌──────▼──────┐                        │
│                  │   Generate  │                        │
│                  │   Status    │                        │
│                  └─────────────┘                        │
└─────────────────────────────────────────────────────────┘
```

## What Changed from v1.x

### v1.x (Hook-based)
```
User works → Claude uses tools → Hook triggers → Writes to log file
                                                        ↓
                                              Status generation reads log
```

**Issues:**
- Required hooks configuration
- Only captured Claude Code activity
- Manual logging setup
- Missed work done with other AI assistants

### v2.0 (Session-based)
```
User works with ANY AI → Sessions automatically saved
                                      ↓
                          Status generation reads sessions + git
```

**Benefits:**
- Zero configuration
- Captures ALL AI-assisted work
- Works retroactively (can analyze past sessions)
- Richer context about work

## Troubleshooting

### No sessions found

```bash
# Check if session directories exist
ls -la ~/.claude/projects/
ls -la ~/.codex/sessions/
ls -la ~/Library/Caches/JetBrains/IntelliJIdea*/projects/*/matterhorn/.matterhorn/
```

### Sessions but no output

Try extending the time window:
```bash
python3 ~/.claude/plugins/work-logger-plugin/parsers/session_aggregator.py --hours 48
```

### Want to include personal projects

Edit the `is_work_project()` function in the parsers to adjust filtering logic.

## Components

- **`parsers/`** - Session parsing logic
  - `claude_projects_parser.py` - Claude Code sessions
  - `codex_sessions_parser.py` - Codex sessions
  - `junie_sessions_parser.py` - Junie/Matterhorn sessions
  - `session_aggregator.py` - Combines all sources
- **`skills/slack-status-writer/`** - Skill for generating status messages
- **`commands/slack-status.md`** - Slash command definition

## Requirements

- Python 3.7+ (uses stdlib only, no external dependencies)
- At least one of: Claude Code, Codex, or Junie
- Optional: git (for commit validation)

## License

MIT

## Contributing

Feel free to extend the parsers to support additional AI assistants or customize the filtering logic!
