# Phase 2: AI Workflow Configuration

## Objective
Configure the optimal AI development environment by querying the tooling registry and selecting the best skills, agents, and MCP servers for this specific project. Also generate project CLAUDE.md and verify global CLAUDE.md exists.

## Entry Criteria
- Approved PRD from Phase 1
- Understanding of project type and tech requirements

## Why This Phase Matters
Different projects need different AI tooling. Configuring this upfront:
- Prevents context-switching and tool discovery mid-development
- Ensures agents have the right skills loaded
- Optimizes for the specific tech stack
- Reduces hallucination by narrowing agent scope
- **Creates project CLAUDE.md** for project-specific instructions
- **Verifies global CLAUDE.md** as security gatekeeper

## Key Insight: CLAUDE.md as Security Gatekeeper

From Claude Code Mastery guide:
> "Your global ~/.claude/CLAUDE.md is a security gatekeeper AND project blueprint."

Security researchers discovered Claude Code automatically reads .env files. Your global CLAUDE.md creates behavioral rules that prevent accidental exposure, even when Claude has access.

## Registry Reference
See `references/registry.md` for the complete catalog of available:
- **Skills** (Claude default, skillsmp.com, aitmpl.com, custom)
- **Agents** (global, local/shared, project-specific)
- **MCP Servers** (database, cloud, development tools)
- **MCP Tradeoffs** (when to use MCP vs CLI alternatives)

---

## Key Activities

### 1. Project Classification
Analyze the PRD and classify the project:

```yaml
classification:
  # Platform
  platform: [web, mobile, desktop, cli, api]

  # Languages (from PRD tech requirements or inferred)
  languages:
    - typescript    # Frontend
    - swift         # iOS Watch app

  # Frameworks
  frameworks:
    - react         # Web frontend
    - react-native  # Mobile (if applicable)

  # Database
  database: [postgresql, sqlite, mongodb, none]

  # Features (from PRD user stories)
  features:
    - auth
    - data-visualization
    - real-time
    - offline-first
    - third-party-apis

  # Integrations
  integrations:
    - apple-healthkit
    - cloud-sync
```

### 1.5. Check Global CLAUDE.md (Security Gatekeeper)

Before configuring project tools, verify global CLAUDE.md exists:

```bash
# Check for global CLAUDE.md
if [ -f ~/.claude/CLAUDE.md ]; then
  echo "✅ Global CLAUDE.md exists"
else
  echo "⚠️ Global CLAUDE.md missing - will suggest creation"
fi
```

**If missing**, recommend creating using template at `assets/templates/global-claude-md-template.md`.

The global CLAUDE.md should contain:
- Identity & authentication (GitHub username, Docker Hub)
- **NEVER rules** (security gatekeeper)
- New project standards
- Chat hygiene guidelines
- Commit standards

### 2. Query Registry for Matching Tools
Based on classification, query `references/registry.md` to find matching tools.

**Always include Context7 MCP server** for live documentation (solves training cutoff issues).

**Example Query (Football Tracker):**
```
Input:
  platform: [mobile, web]
  languages: [typescript, swift]
  frameworks: [react, react-native]
  database: sqlite (local-first)
  features: [data-visualization, offline-first, healthkit-integration]

Output:
  skills:
    - docx (default)
    - xlsx (data analysis)
    - react-tanstack (React patterns)
    - ui-ux-pro-max (design)
    - web-artifacts-builder (components)
  agents:
    - frontend-agent (UI development)
    - code-reviewer (quality)
    - test-generator (testing)
  mcp_servers:
    - sqlite (local database)
```

### 3. Present Recommendations to User
Show the user what tools were found and why:

```markdown
## Recommended AI Tooling for Football Tracker

Based on your PRD, I recommend:

### Skills (7 total)
| Skill | Source | Why |
|-------|--------|-----|
| docx | Claude Default | Documentation |
| xlsx | Claude Default | Data analysis for stats |
| react-tanstack | [aitmpl.com](url) | React Query for data fetching |
| ui-ux-pro-max | [skillsmp.com](url) | Enhanced design patterns |
| web-artifacts-builder | Claude Default | Component generation |
| webapp-testing | Claude Default | Playwright tests |
| git-workflow | [aitmpl.com](url) | Commit/PR best practices |

### Agents (3 total)
| Agent | Skills Loaded | Purpose |
|-------|---------------|---------|
| Frontend Agent | frontend-design, react-tanstack, ui-ux-pro-max | Build UI components |
| Code Reviewer | code-review, git-workflow | PR reviews |
| Test Generator | webapp-testing | Generate test cases |

### MCP Servers (3 total)
| Server | Purpose | Config Needed |
|--------|---------|---------------|
| context7 | Live documentation (ALWAYS recommended) | None |
| sqlite | Local database | --db-path ./data/sessions.db |
| filesystem | File operations | None (default) |

### LSP Status
| Language | Status |
|----------|--------|
| TypeScript | ✅ Built-in (900x faster navigation) |
| Swift | ✅ Built-in |

Shall I proceed with this configuration?
```

### 4. User Customization
Allow user to:
- Add/remove suggested tools
- Specify custom skills they want
- Configure MCP server settings
- Choose agent composition

Use AskUserQuestion:
```
Questions:
1. "Approve this tooling configuration?" [Yes / Modify / Start Over]
2. "Any additional skills you want?" [Search registry / Skip]
3. "MCP servers look correct?" [Yes / Configure / Skip]
```

### 5. Generate Project CLAUDE.md

Create `CLAUDE.md` at project root using `assets/templates/project-claude-md-template.md`:

```markdown
# Football Tracker

> Generated by Project Studio | 2026-01-19

## Project Overview
Smartwatch football session tracker with heatmaps and statistics.

**Type:** Mobile + Web App
**Status:** Phase 2 - AI Workflow Configuration

## Tech Stack
| Category | Technology |
|----------|------------|
| Languages | TypeScript, Swift |
| Frameworks | React, React Native |
| Database | SQLite (local-first) |
| Platform | Mobile, Web |

## NEVER Rules (Project-Specific)
- NEVER modify database schema without migration
- NEVER deploy to production without passing CI
- NEVER commit API keys (HealthKit, analytics)

## Chat Hygiene
### One Task, One Chat
Research shows **39% performance degradation** when mixing topics.
- Start new chat for each distinct feature
- Use `/clear` between phases
- After 20+ turns, consider starting fresh

## Skills Loaded
| Skill | Source | Purpose |
|-------|--------|---------|
| react-tanstack | aitmpl.com | React Query patterns |
| ui-ux-pro-max | skillsmp.com | Design system |
| webapp-testing | Claude Default | E2E testing |

## Quick Commands
```bash
npm run dev      # Start development
npm test         # Run tests
npm run build    # Production build
```
```

### 5.5. Generate Configuration File
Create `.ai-workflow.yaml` with selected tools:

```yaml
# AI Workflow Configuration
# Generated by Project Studio - Phase 2
# Project: Football Tracker
# Date: 2026-01-17

project:
  name: football-tracker
  type: mobile-web
  description: "Smartwatch football session tracker with heatmaps and statistics"

classification:
  platform: [mobile, web]
  languages: [typescript, swift]
  frameworks: [react, react-native]
  database: sqlite
  features: [data-visualization, offline-first, healthkit-integration]

# Skills from registry
skills:
  # Claude Default
  default:
    - docx
    - xlsx
    - frontend-design
    - web-artifacts-builder
    - webapp-testing

  # External (auto-installed from registry)
  external:
    - name: react-tanstack
      source: aitmpl.com
      url: https://www.aitmpl.com/component/skill/react-best-practices
    - name: ui-ux-pro-max
      source: skillsmp.com
      url: https://skillsmp.com/skills/nextlevelbuilder-ui-ux-pro-max-skill-claude-skills-ui-ux-pro-max-skill-md
    - name: git-workflow
      source: aitmpl.com
      url: https://www.aitmpl.com/plugin/git-workflow
    - name: code-review
      source: aitmpl.com
      url: https://www.aitmpl.com/component/skill/code-reviewer

  # Custom (to create if needed)
  custom: []

# Agents configuration
agents:
  # Global agents (always available)
  global:
    - id: code-reviewer
      skills: [code-review, git-workflow]
      triggers: [pr_create]

    - id: doc-writer
      skills: [docx, xlsx]
      triggers: [release, on_request]

    - id: test-generator
      skills: [code-review, webapp-testing]
      triggers: [feature_complete]

  # Project-specific agents
  local:
    - id: frontend-agent
      skills: [frontend-design, react-tanstack, ui-ux-pro-max, web-artifacts-builder]
      description: "Build React components with best practices"
      triggers: [on_request]

# MCP Servers
mcp_servers:
  - id: sqlite
    command: uvx mcp-sqlite
    args: ["--db-path", "./data/sessions.db"]
    when: "Database operations"

# Workflows
workflows:
  on_save:
    trigger: file_save
    patterns: ["src/**/*.{ts,tsx}"]
    actions: [lint, type_check, test_related]

  on_commit:
    trigger: pre_commit
    actions: [format, lint_fix]

  on_pr:
    trigger: pr_create
    actions: [generate_description, run_tests, code_review]

# Conventions
conventions:
  commit_format: conventional
  branch_naming: "feature/{description}"
  test_pattern: "**/*.test.{ts,tsx}"

# Registry sources (for future dynamic fetching)
registry:
  providers:
    - name: skillsmp
      url: https://skillsmp.com
      api: https://api.skillsmp.com/v1
    - name: aitmpl
      url: https://aitmpl.com
      api: https://api.aitmpl.com/v1
  cache_ttl: 86400  # 24 hours
```

### 6. Install/Configure Tools
Execute the configuration:

```bash
# Install external skills (future CLI support)
claude skill install aitmpl:react-tanstack
claude skill install skillsmp:ui-ux-pro-max

# Configure MCP servers
claude mcp add sqlite --db-path ./data/sessions.db

# Verify installation
claude skill list
claude mcp list
```

---

## Output Artifacts
- `CLAUDE.md` - Project-specific instructions with chat hygiene guidelines
- `.ai-workflow.yaml` - Complete workflow configuration
- Installed skills (logged)
- Configured MCP servers (including context7)
- Agent templates ready for use
- Global CLAUDE.md status reported

## Phase Gate Checklist
Before proceeding to Architecture:
- [ ] Project classified by tech stack and features
- [ ] Global `~/.claude/CLAUDE.md` checked (exists or user notified)
- [ ] Project `CLAUDE.md` created with tech stack and conventions
- [ ] Registry queried for matching tools
- [ ] Skills identified (default + external)
- [ ] Agents configured (global + local)
- [ ] Context7 MCP server included (live docs)
- [ ] MCP servers configured (if needed)
- [ ] LSP status checked for all languages
- [ ] `.ai-workflow.yaml` created
- [ ] User has approved AI workflow setup

---

## Quick Reference: Classification → Tools

### Mobile + Web App (like Football Tracker)
```yaml
skills: [react-tanstack, ui-ux-pro-max, web-artifacts-builder, xlsx]
agents: [frontend-agent, code-reviewer, test-generator]
mcp: [sqlite]
```

### Backend API (Python)
```yaml
skills: [fastapi, python-dev, database-implementation, postgresql]
agents: [python-backend, database-agent, code-reviewer]
mcp: [postgres]
```

### Backend API (Scala/Spring)
```yaml
skills: [scala-spring-patterns, senior-data-engineer, flyway-migrations]
agents: [scala-backend, database-agent, code-reviewer]
mcp: [postgres]
```

### Data Pipeline (Databricks)
```yaml
skills: [databricks-development, jupyter-notebook, python-dev, senior-data-engineer]
agents: [databricks-agent, python-backend]
mcp: [databricks]
```

### Full-Stack (React + FastAPI + Postgres)
```yaml
skills: [react-tanstack, fastapi, postgresql, database-implementation]
agents: [frontend-agent, python-backend, database-agent, code-reviewer]
mcp: [postgres]
```

---

## Registry Provider Integration

### Current: Static Registry
The `references/registry.md` file contains a curated list of tools.
Update this file when new skills/agents become available.

### Future: Dynamic API
When providers offer APIs, update the query logic:

```python
async def query_registry(classification: dict) -> list[Tool]:
    """Query skillsmp.com and aitmpl.com for matching tools."""

    results = []

    # Query skillsmp.com
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://api.skillsmp.com/v1/skills/search",
            params={
                "languages": ",".join(classification["languages"]),
                "frameworks": ",".join(classification["frameworks"]),
                "features": ",".join(classification["features"])
            }
        )
        results.extend(resp.json()["skills"])

    # Query aitmpl.com
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://api.aitmpl.com/v1/search",
            params={"q": " ".join(classification["features"])}
        )
        results.extend(resp.json()["components"])

    return dedupe_and_rank(results)
```

### MCP Registry Integration
For MCP servers, query the official registry:

```bash
# Search MCP registry
mcp search "postgres database"

# Install from registry
mcp install @anthropic/mcp-postgres
```
