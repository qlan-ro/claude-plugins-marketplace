# Work Logger Plugin for Claude Code

Automatically logs your work activities throughout the day and generates professional Slack status messages.

## What It Does

1. **Auto-logging**: After every tool use in Claude Code, automatically logs what you worked on to local files
2. **Daily work log**: Creates a file called `YYYY-MM-DD.log` in the `worklog` folder with timestamped entries
3. **Git history integration**: Checks git commits, branch names, and current work to accurately reflect completed tasks
4. **Slack status generation**: At end of day, combines git history and work log to generate a concise Slack status message in your style, filtering out trivial tasks
5. **Quick command**: Use `/slack-status` to instantly generate your status message

## Installation

### Option 1: Local Plugin (Recommended for Testing)

```bash
# 1. Copy the plugin to Claude Code's plugins directory
mkdir -p ~/.claude/plugins
cp -r work-logger-plugin ~/.claude/plugins/work-logger

# 2. Restart Claude Code
```

### Option 2: Project Plugin (Share with Team)

```bash
# 1. Copy to your project
cp -r work-logger-plugin /path/to/your/project/.claude/plugins/work-logger

# 2. Commit to git
cd /path/to/your/project
git add .claude/plugins/work-logger
git commit -m "Add work logger plugin"
git push
```

## How It Works

### Automatic Logging

Every time Claude Code uses a tool (writes a file, runs a command, etc.), the plugin automatically:

1. Captures which tool was used (e.g., bash_tool, str_replace, create_file)
2. Captures which files were affected
3. Logs it to a local file in `~/.claude/plugins/cache/local/work-logger/1.0.0/worklog/` with timestamp and project name
4. Skips read-only operations (like viewing files or searching)
5. Filters out personal projects based on project name

**Example log entry:**
```
[14:23] optimization-review-api
Tool: str_replace
Files: src/api/kpi-calculator.ts
Details: {"old_str":"return null","new_str":"return 0"}
---

[14:25] optimization-review-api
Tool: bash_tool
Files: no files
Details: {"command":"npm test"}
---

[15:45] optimization-review-api
Tool: create_file
Files: /path/to/pr_description.md
Details: {"path":"pr_description.md","file_text":"PR #10239: Fix KPI calculation..."}
---
```

### Generating Slack Status

At the end of your workday, use the quick command:

```
/slack-status
```

Or simply ask:

```
Hey Claude, generate my Slack status for today
```

Claude will:
1. **Check git history** (if in a git repo) with smart time windows:
   - Before 12 PM: looks at commits since yesterday (you're likely still working on "yesterday's" tasks)
   - After 12 PM: looks at commits since today
2. Read work log files (yesterday's + today's if before noon, or just today's if after noon)
3. Parse the tool usage entries to understand what you worked on
4. Filter for work-related projects only (excludes personal projects)
5. **Filter out trivial tasks** like config changes, utility scripts, and minor operations
6. Combine git commits with work log to extract key accomplishments
7. Generate a concise, professional status message

**Example - What the log might look like:**
```
Work Activity Log for 2024-12-06

[09:15] optimization-review-api
Tool: str_replace
Files: src/kpi/calculator.ts
Details: Fixed null handling in Average KPI calculation
---

[10:30] optimization-review-api
Tool: create_file  
Files: pull_request_10239.md
Details: Created PR description for KPI fix
---

[14:20] optimization-review-api
Tool: bash_tool
Files: no files
Details: Deployed updated libraries, fixed DAJ job issue
---

[16:00] optimization-review-api
Tool: str_replace
Files: src/api/routes.ts
Details: Integrated OR team APIs into UI endpoints
---
```

**Example - Generated Slack status:**
```
Status:
• Pull Request #10239: Fixed data usage values returning 0 in Average KPI Changes per Run
• Deployed updated dependency libraries and resolved DAJ job issue
• Integrated OR team APIs into UI for optimization review workflows
```

## Filtering Work vs Personal Projects

The plugin automatically tries to identify work projects based on project names. To improve filtering:

- Name work projects with clear indicators (e.g., `company-api`, `work-dashboard`)
- Keep personal projects in separate directories with obvious names (e.g., `personal-blog`, `side-project`)

You can also manually specify in your request:
```
Generate my Slack status for today, focusing only on the optimization-review-api and data-platform projects
```

## Customization

### Adjust Logging Detail

Edit `hooks/scripts/log_work.sh` to change what gets logged:

- Line 20-21: Adjust character limits for truncation
- Add filters to exclude certain project patterns
- Change the log format

### Change Log Location

By default, logs go to the `worklog` folder inside the plugin directory. To change:

Edit the `WORKLOG_DIR` variable in `hooks/scripts/log_work.sh`:
```bash
WORKLOG_DIR="/path/to/your/preferred/location"
```

### Modify Status Format

Edit `skills/slack-status-writer/SKILL.md` to adjust:
- Bullet point style
- Technical detail level
- Tone and formatting

## Troubleshooting

### Logs not appearing

1. Check that the worklog directory exists: `ls ~/.claude/plugins/cache/local/work-logger/1.0.0/worklog/`
2. Verify the hook script is executable: `chmod +x ~/.claude/plugins/cache/local/work-logger/1.0.0/hooks/scripts/log_work.sh`
3. Check today's log file: `cat ~/.claude/plugins/cache/local/work-logger/1.0.0/worklog/$(date +%Y-%m-%d).log`
4. Check Claude Code logs for errors

### Status message missing work items

1. Verify today's work log exists: `ls ~/.claude/plugins/cache/local/work-logger/1.0.0/worklog/$(date +%Y-%m-%d).log`
2. Check if the log has entries (view the file)
3. Remember: Trivial tasks like config changes and utility scripts are automatically filtered out
4. Try being more specific: "Generate Slack status from all substantial entries in today's work log"

### Only personal projects being logged

The hook logs ALL projects. The filtering happens when generating the status. Make sure work projects have distinguishable names.

## Privacy Note

- All logs are stored locally in `~/.claude/plugins/cache/local/work-logger/1.0.0/worklog/` on your Mac
- Nothing is sent to external servers
- The plugin only logs what you've worked on with Claude Code
- You can view, edit, or delete work logs anytime from the worklog directory

## Manual Override

If you want to skip auto-logging for a session, you can temporarily disable the plugin:

```bash
# In Claude Code
/plugin disable work-logger
```

Re-enable:
```bash
/plugin enable work-logger
```

## License

MIT
