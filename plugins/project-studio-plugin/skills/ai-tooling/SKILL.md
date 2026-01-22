---
name: ai-tooling
description: |
  AI tooling recommendation and configuration. Use this skill when:
  - Recommending skills, agents, and MCP servers for a project
  - Classifying projects by tech stack and features
  - Querying the tooling registry
  - Generating .ai-workflow.yaml configuration
  - **Generating project CLAUDE.md** (project-specific instructions)
  - **Checking global ~/.claude/CLAUDE.md** (security gatekeeper)
  - **Checking LSP status** for detected languages
  - Auditing existing projects for missing tools (continue-project workflow)

  This skill is domain-specific - it knows HOW to recommend AI tooling, not workflow phases.
---

# AI Tooling Configuration

Recommend and configure optimal AI tools (skills, agents, MCP servers) for projects.
Also generates CLAUDE.md files and verifies LSP status.

## Key Insight: Defense in Depth

From Claude Code Mastery guide:

| Layer | Mechanism | Reliability |
|-------|-----------|-------------|
| 1 | CLAUDE.md rules | Suggestion (can be overridden under context pressure) |
| 2 | Hooks (PreToolUse) | **Deterministic** (always executes) |
| 3 | .gitignore | Git-level protection |

**CLAUDE.md is a security gatekeeper** - behavioral rules that prevent accidental secret exposure even when Claude has file access.

## Two Modes

### New Project Mode (Phase 2)
Create configuration from scratch based on PRD and planned tech stack.

### Audit Mode (Phase C5 - Continue Project)
Analyze existing project, detect what's configured, identify gaps, suggest additions.

---

## Process Overview

### New Project Flow
1. **Check** global `~/.claude/CLAUDE.md` exists (security gatekeeper)
2. **Classify** the project by tech stack and features
3. **Query** the registry for matching tools (always include Context7)
4. **Check** LSP status for detected languages
5. **Present** recommendations with rationale
6. **Customize** based on user input
7. **Generate** `CLAUDE.md` (project-specific instructions)
8. **Generate** `.ai-workflow.yaml` configuration

### Audit Flow (Existing Projects)
1. **Detect** existing configuration (.ai-workflow.yaml, CLAUDE.md, .claude/, claude.json)
2. **Check** global `~/.claude/CLAUDE.md` exists
3. **Read** CODEBASE_ANALYSIS.md and ARCHITECTURE.md for tech stack
4. **Check** LSP status for detected languages
5. **Compare** configured tools vs. recommended tools
6. **Identify** gaps (missing skills, agents, MCP servers, CLAUDE.md)
7. **Suggest** additions for new features (📋 items from PRD)
8. **Generate** CLAUDE.md if missing
9. **Update** or create `.ai-workflow.yaml`

## Step 1: Project Classification

Analyze the PRD and/or codebase to classify:

```yaml
classification:
  platform: [web, mobile, desktop, cli, api, data-pipeline]

  languages:
    - typescript
    - python
    - scala

  frameworks:
    - react
    - fastapi
    - spring-boot

  database: [postgresql, sqlite, mongodb, sqlserver, none]

  features:
    - auth
    - data-visualization
    - real-time
    - offline-first
    - third-party-apis
    - ai-ml

  integrations:
    - github
    - notion
    - stripe
```

## Step 2: Query Registry

Reference: `references/registry.md`

### Matching Rules

**By Language:**
| Language | Skills | Agents |
|----------|--------|--------|
| TypeScript/JS | react-tanstack, web-artifacts-builder, angular-modern | frontend-agent |
| Python | python-dev, fastapi, jupyter-notebook | python-backend |
| Scala | scala-spring-patterns, senior-data-engineer | scala-backend |
| SQL | postgresql, sqlserver, database-implementation | database-agent |

**By Framework:**
| Framework | Skills | Agents |
|-----------|--------|--------|
| React | react-tanstack, web-artifacts-builder, ui-ux-pro-max | frontend-agent |
| Angular | angular-modern, ui-ux-pro-max | frontend-agent |
| FastAPI | fastapi, python-dev | python-backend |
| Spring Boot | scala-spring-patterns | scala-backend |
| Databricks | databricks-development, jupyter-notebook | databricks-agent |

**By Database:**
| Database | Skills | MCP Server |
|----------|--------|------------|
| PostgreSQL | postgresql, database-implementation | postgres |
| SQLite | database-implementation | sqlite |
| SQL Server | sqlserver, database-implementation | sqlserver |

**By Feature:**
| Feature | Skills | Agents |
|---------|--------|--------|
| Auth | oauth2-jwt | - |
| Data Viz | xlsx, jupyter-notebook | databricks-agent |
| AI/ML | openai-integration, senior-prompt-engineer | categorizer |
| Testing | webapp-testing | test-generator |

### Always Include

**Claude Default Skills:**
- docx, pdf, pptx, xlsx (as needed)
- frontend-design (UI projects)
- web-artifacts-builder (React projects)
- webapp-testing (web projects)

**Global Agents:**
- code-reviewer (all projects)
- doc-writer (all projects)
- test-generator (all projects)

**Global MCP Servers:**
- context7 (ALWAYS - live documentation, solves training cutoff)
- filesystem (built-in)
- git (built-in)
- fetch (built-in)

**LSP Check (900x faster code navigation):**
| Language | Status |
|----------|--------|
| TypeScript/JS | ✅ Built-in |
| Python | ✅ Built-in |
| Go | ✅ Built-in |
| Rust | ✅ Built-in |
| Java | ✅ Built-in |
| Scala | ✅ Built-in |

For older Claude Code versions: `export ENABLE_LSP_TOOL=1`

## Step 3: Present Recommendations

Format recommendations clearly:

```markdown
## Recommended AI Tooling for {Project Name}

Based on your project classification:
- Platform: {platform}
- Languages: {languages}
- Frameworks: {frameworks}
- Database: {database}

### Skills ({count})

| Skill | Source | Why |
|-------|--------|-----|
| react-tanstack | aitmpl.com | React Query for data fetching |
| postgresql | skillsmp.com | PostgreSQL database patterns |
| webapp-testing | Claude Default | Playwright E2E tests |

### Agents ({count})

| Agent | Skills Loaded | Purpose |
|-------|---------------|---------|
| frontend-agent | react-tanstack, ui-ux-pro-max | Build UI components |
| database-agent | postgresql, database-implementation | Schema & migrations |
| code-reviewer | code-review, git-workflow | PR reviews |

### MCP Servers ({count})

| Server | Command | Config |
|--------|---------|--------|
| context7 | npx -y @upstash/context7-mcp@latest | None (ALWAYS recommended) |
| postgres | npx -y @anthropic/mcp-postgres | DATABASE_URL |
| github | npx -y @anthropic/mcp-github | GITHUB_TOKEN |

### LSP Status
| Language | Status |
|----------|--------|
| TypeScript | ✅ Built-in (900x faster navigation) |
| Python | ✅ Built-in |

### CLAUDE.md Status
- Global (~/.claude/CLAUDE.md): ✅ Exists / ⚠️ Missing (suggest creation)
- Project (./CLAUDE.md): Will be generated

### Questions

1. Approve this configuration?
   A. Yes, generate CLAUDE.md and .ai-workflow.yaml
   B. Add more tools
   C. Remove some tools
   D. Start over
```

## Step 4: User Customization

Allow modifications:
- Add skills from registry
- Remove unnecessary tools
- Configure MCP server settings
- Specify custom skills to create

## Step 5: Check and Suggest Global CLAUDE.md

```bash
# Check if global CLAUDE.md exists
if [ -f ~/.claude/CLAUDE.md ]; then
  echo "✅ Global CLAUDE.md exists"
else
  echo "⚠️ Global CLAUDE.md missing"
fi
```

**If missing**, recommend creating using `assets/templates/global-claude-md-template.md`:

```markdown
### Global CLAUDE.md Recommendation

Your global ~/.claude/CLAUDE.md is missing. This file acts as a **security gatekeeper**
for ALL your projects.

**Recommended:** Create it with these sections:
- GitHub account identity
- **NEVER rules** (never commit .env, never publish secrets)
- New project scaffolding standards
- Chat hygiene guidelines (one task, one chat)

**Template available at:** `assets/templates/global-claude-md-template.md`

Create now? [Yes / Skip]
```

## Step 6: Generate Project CLAUDE.md and AGENTS.md

Output: `CLAUDE.md` and `AGENTS.md` at project root

### AGENTS.md (Simple Pointer)

Always create `AGENTS.md` alongside `CLAUDE.md`:

```markdown
# AI Agent Instructions

For project-specific instructions, conventions, and guidelines, see:

👉 **[CLAUDE.md](./CLAUDE.md)**

This file contains:
- Project overview and tech stack
- Development commands
- Coding conventions
- Architecture decisions
- Security rules (NEVER do)
```

This file is a standard convention recognized by various AI coding assistants.

### CLAUDE.md (Full Instructions)

Use template at `assets/templates/project-claude-md-template.md` and fill:
- `{{PROJECT_NAME}}` - from PRD
- `{{PROJECT_DESCRIPTION}}` - from PRD overview
- `{{TECH_STACK}}` - from classification
- `{{NEVER_RULES}}` - project-specific restrictions
- `{{SKILLS_TABLE}}` - from selected skills
- `{{MCP_SERVERS_TABLE}}` - from selected MCP servers
- `{{QUICK_COMMANDS}}` - npm/yarn/etc commands

**Include Chat Hygiene section** (research shows 39% degradation when mixing topics):
```markdown
## Chat Hygiene

### One Task, One Chat
- Start new chat for each distinct feature
- Use `/clear` between phases
- After 20+ turns, consider starting fresh
```

## Step 7: Generate .ai-workflow.yaml

Output: `.ai-workflow.yaml`

```yaml
# AI Workflow Configuration
# Generated by Project Studio - Phase 2
# Project: {name}
# Date: {date}

project:
  name: "{project-name}"
  type: "{type}"
  description: "{description}"

classification:
  platform: [{platforms}]
  languages: [{languages}]
  frameworks: [{frameworks}]
  database: {database}
  features: [{features}]

skills:
  default:
    - docx
    - xlsx
    - frontend-design

  external:
    - name: react-tanstack
      source: aitmpl.com
      url: https://www.aitmpl.com/component/skill/react-best-practices
    - name: postgresql
      source: skillsmp.com
      url: https://skillsmp.com/skills/...

agents:
  global:
    - id: code-reviewer
      skills: [code-review, git-workflow]
      triggers: [pr_create]

  local:
    - id: frontend-agent
      skills: [frontend-design, react-tanstack]
      description: "Build React components"

mcp_servers:
  - id: postgres
    command: npx -y @anthropic/mcp-postgres
    env: [DATABASE_URL]

workflows:
  on_save:
    trigger: file_save
    patterns: ["src/**/*.{ts,tsx}"]
    actions: [lint, type_check]

  on_commit:
    trigger: pre_commit
    actions: [format, lint_fix]

conventions:
  commit_format: conventional
  branch_naming: "feature/{description}"
  test_pattern: "**/*.test.{ts,tsx}"
```

## Quick Reference: Project Type → Tools

### Web App (Full-Stack React + Postgres)
```yaml
skills: [react-tanstack, ui-ux-pro-max, postgresql, database-implementation]
agents: [frontend-agent, database-agent, code-reviewer]
mcp: [postgres]
```

### Mobile + Web App
```yaml
skills: [react-tanstack, ui-ux-pro-max, web-artifacts-builder]
agents: [frontend-agent, code-reviewer, test-generator]
mcp: [sqlite]
```

### Backend API (Python)
```yaml
skills: [fastapi, python-dev, postgresql, database-implementation]
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
skills: [databricks-development, jupyter-notebook, python-dev]
agents: [databricks-agent, python-backend]
mcp: [databricks]
```

### CLI Tool
```yaml
skills: [python-dev, git-workflow]
agents: [python-backend, code-reviewer]
mcp: []
```

## Registry Sources

| Provider | URL | Type |
|----------|-----|------|
| Claude Default | Built-in | Core skills |
| SkillsMP | skillsmp.com | Skills marketplace |
| AITemplates | aitmpl.com | Skills & agents |
| MCP Registry | mcp-registry.anthropic.com | MCP servers |

For full registry, see `references/registry.md`.

## Audit Mode: Existing Project Analysis

### Step A1: Detect Existing Configuration

```bash
# Check for existing AI config
ls -la .ai-workflow.yaml 2>/dev/null
ls -la .claude/ 2>/dev/null
ls -la claude.json 2>/dev/null

# Check for MCP config
cat .claude/mcp.json 2>/dev/null
```

### Step A2: Read Project Analysis

```bash
# From codebase analysis phase
cat docs/CODEBASE_ANALYSIS.md
cat docs/ARCHITECTURE.md
cat docs/PRODUCT_PRD.md
```

Extract:
- Tech stack (languages, frameworks, database)
- Existing features (✅ Done)
- New features (📋 To Build)

### Step A3: Gap Analysis

Compare what's configured vs. what's recommended:

```markdown
## AI Tooling Audit Report

### Currently Configured
| Type | Configured | Source |
|------|------------|--------|
| Skills | react-tanstack | .ai-workflow.yaml |
| MCP | postgres | .claude/mcp.json |
| Agents | none | - |

### Recommended (Based on Tech Stack)
| Type | Tool | Why |
|------|------|-----|
| Skills | react-tanstack | ✅ Already configured |
| Skills | webapp-testing | ❌ Missing - needed for tests |
| MCP | postgres | ✅ Already configured |
| Agents | code-reviewer | ❌ Missing - recommended for PRs |

### Gaps Identified
1. **webapp-testing** skill - Project has React, needs E2E tests
2. **code-reviewer** agent - No PR review automation

### New Features Need
For 📋 items in PRD:
- Feature X needs: {skill}
- Feature Y needs: {MCP server}
```

### Step A4: Present Audit Results

```markdown
## AI Tooling Audit Results

### Current Status
- ✅ 3 skills configured
- ✅ 1 MCP server configured
- ❌ 0 agents configured

### Recommended Additions
| Tool | Type | Reason |
|------|------|--------|
| webapp-testing | Skill | E2E testing for React |
| code-reviewer | Agent | Automated PR reviews |
| test-generator | Agent | Generate test cases |

### For New Features (📋)
| New Feature | Tools Needed |
|-------------|--------------|
| Dark mode | (none additional) |
| Export to PDF | pdf skill |

### Questions
1. Add recommended tools?
   A. Yes, update .ai-workflow.yaml
   B. Select specific tools
   C. Skip, keep current config
```

### Step A5: Update Configuration

If updating existing config, preserve existing settings and add new:

```yaml
# Existing settings preserved
skills:
  default:
    - docx
    - xlsx
  external:
    - name: react-tanstack  # existing
      source: aitmpl.com
    # NEW ADDITIONS
    - name: webapp-testing  # added by audit
      source: claude-default
      added: "2026-01-19"
      reason: "E2E testing for React frontend"
```

---

## Checklist: New Project Mode

- [ ] Global `~/.claude/CLAUDE.md` checked (exists or user notified)
- [ ] Project classified by tech stack
- [ ] Registry queried for matching tools
- [ ] Context7 MCP server included (live documentation)
- [ ] LSP status checked for all detected languages
- [ ] Recommendations presented to user
- [ ] User approved or customized
- [ ] Project `CLAUDE.md` generated (with chat hygiene guidelines)
- [ ] Project `AGENTS.md` generated (pointer to CLAUDE.md)
- [ ] `.ai-workflow.yaml` generated

## Checklist: Audit Mode

- [ ] Existing config detected and parsed
- [ ] Global `~/.claude/CLAUDE.md` checked (exists or user notified)
- [ ] Project `CLAUDE.md` checked (exists or will be generated)
- [ ] Project `AGENTS.md` checked (exists or will be generated)
- [ ] Tech stack read from analysis docs
- [ ] LSP status checked for all detected languages
- [ ] Gap analysis completed (including Context7 MCP)
- [ ] New feature needs identified
- [ ] Recommendations presented
- [ ] Project `CLAUDE.md` generated if missing
- [ ] Project `AGENTS.md` generated if missing
- [ ] Config updated or created

---

## Add-Feature Mode (Feature)

When adding features via `/project-studio:add-feature` that may need new AI tools:

### When to Trigger Feature Mode

During impact analysis, check if new feature needs specific tools:

| Feature Type | May Need |
|--------------|----------|
| PDF export | `pdf` skill |
| Excel reports | `xlsx` skill |
| Image processing | Image manipulation skill |
| AI/ML integration | `openai-integration`, `senior-prompt-engineer` |
| Real-time data | WebSocket skill |
| Email sending | Email integration |
| Payment processing | Stripe/payment skill |
| Charts/graphs | `data-visualization`, `jupyter-notebook` |

### Rules for Feature Mode

1. **DO NOT reconfigure** entire setup
2. **READ** existing `.ai-workflow.yaml` first
3. **PRESERVE** all existing configuration
4. **ADD** only tools specifically needed for new feature
5. **INCLUDE** metadata: date, reason, feature name

### Process

1. **Analyze new feature requirements:**
```markdown
## AI Tooling Check: {Feature Name}

Feature: Export to PDF
Requirements:
- Generate PDF documents from data
- Include charts and tables

Tool Needed: pdf skill (Claude Default)
```

2. **Check if already configured:**
```bash
# Check existing config
grep -i "pdf" .ai-workflow.yaml
```

3. **Present recommendation (if needed):**
```markdown
### AI Tooling for New Feature

Feature: Export to PDF

**Current Config:** No PDF skill configured

**Recommendation:**
| Tool | Type | Why |
|------|------|-----|
| pdf | Skill (Claude Default) | Generate PDF exports |

Add this tool?
A. Yes, update .ai-workflow.yaml
B. No, skip
```

4. **Update config with metadata:**
```yaml
skills:
  default:
    - docx
    - xlsx
    # FEATURE ADDITIONS
    - name: pdf
      added: "2026-01-19"
      reason: "PDF export feature"
      feature: "Export to PDF"
```

### Output

Updated `.ai-workflow.yaml` with:
- New tools for specific feature
- Clear metadata showing why added
- Existing config UNCHANGED

### Checklist: Feature Mode

- [ ] New feature analyzed for tool needs
- [ ] Existing config checked for tool presence
- [ ] Recommendation presented (if new tool needed)
- [ ] User approved addition
- [ ] Config updated with metadata
