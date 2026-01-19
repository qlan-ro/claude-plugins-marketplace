---
name: slack-status-writer
description: Generate concise, professional Slack status updates summarizing daily work accomplishments. Use when the user asks to write or generate their daily status message, end-of-day summary, or Slack status based on work completed during the day. Automatically parses AI assistant session history and git commits.
---

# Slack Status Writer

Generate professional, concise Slack status messages that summarize the user's daily work accomplishments by combining:
1. **AI assistant session history** (Claude Code, Codex, Junie) - captures all work discussions and implementations
2. **Git history** - validates completed work and captures commit messages/PRs

## Workflow

When the user requests a Slack status message:

1. **Parse AI assistant sessions** (PRIMARY SOURCE):
   - Run the session aggregator to get comprehensive activity data from all AI assistants
   - Automatically filters out trivial tasks
   - Activities are already categorized by project
   - Provides rich context about what was discussed and implemented

2. **Check git history** (VALIDATION & COMMIT DETAILS):
   - Determine the time window:
     - If current time is before 12:00 PM (noon): look at commits since yesterday 00:00
     - If current time is after 12:00 PM: look at commits since today 00:00
   - Run the appropriate git log command:
     - Before noon: `git log --since="yesterday 00:00" --oneline --author="$(git config user.name)"`
     - After noon: `git log --since="today 00:00" --oneline --author="$(git config user.name)"`
   - Run `git status` to check current branch and any uncommitted work
   - Extract PR references, commit messages, branch names
   - Git commits are the source of truth for completed/merged work

3. **Combine AI sessions with git history**:
   - Use AI session data to understand the full context of work
   - Use git commits to identify what was actually completed/merged
   - Cross-reference to avoid duplication
   - Prioritize items that appear in both sources (high confidence)

4. **Filter for work-related items only**:
   - Look for project names that indicate work projects
   - Exclude any personal projects or activities
   - Focus on deliverables and concrete accomplishments
   - **IMPORTANT: Trivial tasks are already filtered by the session aggregator**

5. **Generate the status message** following the format guidelines below

## Data Sources

### AI Session History (Primary Source)

The work-logger parses session history from three AI assistants:
- **Claude Code sessions**: `~/.claude/projects/`
- **Codex sessions**: `~/.codex/sessions/`
- **Junie sessions**: `~/Library/Caches/JetBrains/IntelliJIdea*/projects/*/matterhorn/.matterhorn/`

Use the session aggregator to get comprehensive work data:

```bash
python3 ~/.claude/plugins/work-logger-plugin/parsers/session_aggregator.py --hours 24 --format bullets
```

This will output key activities from all three AI assistants in the last 24 hours.

### Git History (Validation Source)

Git commits provide the source of truth for what was actually completed and merged. Check git history for:
- Commit messages with PR numbers and issue IDs
- Branch names that indicate work focus
- Uncommitted changes showing ongoing work

## Filtering Rules for Trivial Tasks

**ALWAYS exclude these types of small/trivial tasks from the status message:**

1. **Configuration/IDE changes**:
   - Updated run configurations
   - Modified IDE settings
   - Changed editor preferences
   - Formatting or linting config changes

2. **Utility scripts**:
   - Creating helper scripts for personal use (like finding unused classes)
   - Small automation scripts that don't impact the product
   - One-off debugging scripts

3. **Minor file operations**:
   - Renaming files without logic changes
   - Moving files around
   - Deleting unused files
   - Adding .gitignore entries

4. **Trivial code changes**:
   - Fixing typos in comments
   - Adding console.log for debugging
   - Minor formatting changes
   - Updating variable names without refactoring

5. **Read-only activities**:
   - Viewing files
   - Searching code
   - Reading documentation
   - Exploring codebase

**DO include these types of substantial tasks:**
- Pull requests (always)
- Bug fixes
- Feature implementations
- API changes
- Database migrations
- Deployment activities
- Performance optimizations
- Refactoring with business impact
- Sync meetings with decisions/action items
- Code reviews with significant feedback

## Git History Integration

When checking git history, look for:

1. **Commit messages**: Extract PR numbers, issue IDs, and work descriptions
   ```bash
   # Example output:
   21f17de Fix bug with libraries conflict when using CUR
   bdb7547 Fix bug with libraries conflict when using CUR
   19de0d1 Merged PR 10252: [15379] - OR fixes
   ```

2. **Branch names**: Often indicate the work focus
   ```bash
   # Example: Branch "dchiulan/libraries-update-cur-bug"
   # Indicates: Working on CUR bug related to libraries update
   ```

3. **Uncommitted changes**: Shows ongoing work
   ```bash
   # Example git status output:
   M  .run/mvn [clean,install][NO TESTS][NO UI].run.xml
   ?? scripts/find-unused-classes.sh
   # Filter: The .run file is trivial config, the script is a utility (both excluded)
   ```

The git history provides the most reliable source of what was actually accomplished, while the work log adds context for activities beyond code commits.

## Status Message Format

**Format:**
- Start with "Status:" or "Status [Month Day]:" (with date if appropriate)
- Use bullet points for individual work items
- Keep each bullet concise (1-2 lines maximum)
- Include relevant PR numbers, user stories, bug numbers, or technical details
- Use past tense for completed work
- Group related items together when possible

**Tone and Style:**
- Professional and matter-of-fact
- Technical and specific (include API names, technologies, system components)
- Action-oriented (what was accomplished, not what was attempted)
- Avoid flowery language or excessive detail
- Include "(edited)" tag if the status was updated later

**Content Priorities:**
1. **Pull Requests**: Always mention PR numbers in format "Pull Request #####" or link format
2. **User Stories**: Reference as "User Story #####"
3. **Bug Fixes**: Reference as "Bug #####" or describe the technical issue
4. **Syncs/Meetings**: Summarize key decisions or next steps, mention who was involved
5. **Technical Work**: Specify what was implemented, updated, or investigated
6. **Code Reviews**: Mention if significant reviews were completed
7. **Infrastructure/DevOps**: Deployments, library updates, configuration changes

## Examples

**Example 1 - Multiple PRs and tasks:**
```
Status:
• Pull Request 10239: [15352] - [OptimizationReview] data usage values from Average KPI Changes per Run are 0
• Pull Request 10240: [15358] - [API] Feature request for Markel: display Modern vs Legacy on the c...
For the 2nd PR I let it in draft as I still need to do some tests and add some migration files (edited)
```

**Example 2 - Implementation work:**
```
Status:
• Finished OR SQL Warehouse summary implementation, including some new KPIs from Figma that I didn't expose in the initial implementation
(edited)
```

**Example 3 - Syncs and planning:**
```
Status:
• Synced with Mada for AI and DBX platform on Optimization Review
• Synced with OR team about integrating existing APIs in the UI
```

**Example 4 - Multiple work streams:**
```
Status:
• Sync with OR team, planned tasks and assignments for the next few days. Each of the backend developers own one of the workload type APIs
• User Story 15271: [ui] update supporting stats grouping on summary KPIs for Jobs in
• Resumed work on the Optimization Review -> SQL Warehouse support
(edited)
```

**Example 5 - Bug fixes and investigation:**
```
Status:
• Fixed multiple places where there were logged stacktraces for known exceptions
• Investigated some issue with serializing an internal Azure SDK object, it broke after bumping Azure libraries. Costi provided the fix
```

**Example 6 - Infrastructure work:**
```
Status:
• Tested deployments with the new dependency updates.
• Fixed one found issue for DAJ job
• Some work remaining for external spark support
```

## Instructions for Generating Status

When writing a status message:

1. **Parse AI assistant sessions** (PRIMARY SOURCE):
   - Use the Bash tool to run the session aggregator:
     ```bash
     python3 ~/.claude/plugins/work-logger-plugin/parsers/session_aggregator.py --hours 24 --format bullets
     ```
   - This provides a comprehensive list of work activities from Claude Code, Codex, and Junie
   - The aggregator automatically filters out trivial tasks
   - Activities are already categorized by project
   - Includes rich context about what was discussed and implemented

2. **Check git history** (VALIDATION & COMMIT DETAILS):
   - Determine the appropriate time window based on current time
   - Use the Bash tool to run the appropriate command:
     - If before 12:00 PM: `git log --since="yesterday 00:00" --oneline --author="$(git config user.name)"`
     - If after 12:00 PM: `git log --since="today 00:00" --oneline --author="$(git config user.name)"`
   - Use the Bash tool to run: `git status` to see current branch and uncommitted changes
   - Parse commit messages for PR numbers, bug fixes, feature descriptions
   - Note the current branch name (e.g., `dchiulan/libraries-update-cur-bug` tells you about the work)

3. **Cross-reference and combine**:
   - Match AI session activities with git commits
   - Items that appear in both sources have high confidence
   - Use session data for context, git for confirmation of completion
   - Prioritize completed work (in git) over in-progress work (only in sessions)

4. **Extract key work items**:
   - PR numbers or descriptions (from commits and session data)
   - User story IDs
   - Bug fixes and investigations
   - Feature implementations
   - Meetings and syncs with outcomes
   - Technical work (APIs, deployments, refactoring)

5. **Consolidate related items**: Group similar work together into coherent bullets

6. **Format as bullets**: Create 2-5 concise bullet points

7. **Include technical details**: Add PR numbers, technologies, system names, APIs

8. **Keep it concise**: Each bullet should be 1-2 lines max

9. **Use developer language**: The audience is other engineers

**Do not include:**
- Verbose explanations or background
- Future plans (unless directly tied to current work)
- Generic statements like "worked on project X"
- Time spent or effort estimates
- Personal projects or non-work activities
- Apologetic or hedging language
- **Trivial tasks** (already filtered by the session aggregator)

## Handling Missing or Sparse Data

If no AI session data is found:
- Check if the session directories exist and are accessible
- Try extending the time window (e.g., 48 hours instead of 24)
- Fall back to git history only
- Inform the user: "I couldn't find any AI assistant session data for today. Using git history only for the status."

If git history is empty:
- Rely on AI session data alone
- Note that no commits were made: "No git commits found for today. Status based on AI session activity only."

If both sources are sparse:
- Generate status from whatever substantial items are available
- Note to the user: "Found [N] activities in AI sessions. Here's your status based on those activities."
- Offer to create the status manually if needed: "Would you like to add any additional work to your status?"
