# Phase C5: AI Tooling Audit

Analyze existing AI configuration and identify gaps for the continue-project workflow.

## Purpose

After understanding the codebase (C1), documenting the product (C2), architecture (C3), and design (C4), this phase ensures the project has the right AI development tools configured.

## Agent

**ai-tooling-advisor** (audit mode)

## Inputs

- `docs/CODEBASE_ANALYSIS.md` - Tech stack details
- `docs/ARCHITECTURE.md` - Technical decisions
- `docs/PRODUCT_PRD.md` - Features with status markers (✅/🟡/📋)
- Existing config files (if any)

## Process

### Step 1: Detect Existing Configuration

Check for existing AI workflow configuration:

```bash
# Check for existing config files
ls -la .ai-workflow.yaml 2>/dev/null
ls -la CLAUDE.md 2>/dev/null
ls -la .claude/ 2>/dev/null
ls -la claude.json 2>/dev/null

# Check for MCP configuration
cat .claude/mcp.json 2>/dev/null

# Check for global CLAUDE.md (security gatekeeper)
ls -la ~/.claude/CLAUDE.md 2>/dev/null
```

### Step 1.5: Check LSP Status

LSP (Language Server Protocol) provides 900x faster code navigation. Check availability:

```bash
# Check Claude Code version (LSP built-in since v2.0.74)
claude --version 2>/dev/null

# For older versions, check if LSP is enabled
echo $ENABLE_LSP_TOOL
```

**LSP Support by Language:**
| Language | LSP Status |
|----------|------------|
| TypeScript/JavaScript | ✅ Built-in |
| Python | ✅ Built-in |
| Go | ✅ Built-in |
| Rust | ✅ Built-in |
| Java | ✅ Built-in |
| C/C++ | ✅ Built-in |
| C# | ✅ Built-in |
| PHP | ✅ Built-in |
| Kotlin | ✅ Built-in |
| Ruby | ✅ Built-in |

**If LSP not enabled on older versions:**
```bash
export ENABLE_LSP_TOOL=1
```

### Step 2: Extract Tech Stack

From earlier phase outputs, identify:

- **Languages:** TypeScript, Python, Scala, SQL, etc.
- **Frameworks:** React, Angular, FastAPI, Spring Boot, etc.
- **Database:** PostgreSQL, SQLite, MongoDB, SQL Server
- **Features:** Auth, real-time, data visualization, AI/ML

### Step 3: Query Registry

Reference `references/registry.md` to find matching tools:

| Language/Framework | Recommended Skills | Recommended Agents |
|--------------------|-------------------|-------------------|
| TypeScript/React | react-tanstack, ui-ux-pro-max | frontend-agent |
| Python/FastAPI | fastapi, python-dev | python-backend |
| PostgreSQL | postgresql, database-implementation | database-agent |

### Step 4: Gap Analysis

Compare what's configured vs. what's recommended:

```markdown
## AI Tooling Audit Report

### Current Status
| Type | Count | Details |
|------|-------|---------|
| Skills | 2 | react-tanstack, postgresql |
| Agents | 0 | None configured |
| MCP Servers | 1 | postgres |
| CLAUDE.md (project) | ❌ | Missing |
| CLAUDE.md (global) | ✅ | Present at ~/.claude/CLAUDE.md |
| LSP Status | ✅ | Enabled for TypeScript, Python |

### Gaps Identified
| Tool | Type | Reason |
|------|------|--------|
| context7 | MCP Server | Live docs - always recommended |
| webapp-testing | Skill | Project has React, missing E2E tests |
| code-reviewer | Agent | No automated PR reviews |
| test-generator | Agent | Would help with test coverage |
| CLAUDE.md | Config | Project-specific instructions missing |

### For New Features (📋)
| Feature | Additional Tools Needed |
|---------|------------------------|
| Dark mode toggle | (none) |
| Export to PDF | pdf skill |
| Real-time updates | (WebSocket config) |
```

### Step 5: Present Recommendations

Show user the audit results:

```markdown
## Recommended Additions

Based on your tech stack and planned features:

### Skills to Add
| Skill | Source | Why |
|-------|--------|-----|
| webapp-testing | Claude Default | E2E testing for React |

### Agents to Add
| Agent | Skills | Purpose |
|-------|--------|---------|
| code-reviewer | code-review, git-workflow | Automated PR reviews |

### Questions
1. Add recommended tools?
   A. Yes, update .ai-workflow.yaml
   B. Select specific tools only
   C. Skip, keep current config
```

### Step 6: Update Configuration

If user approves, update or create `.ai-workflow.yaml`:

- Preserve all existing settings
- Add new tools with metadata:
  ```yaml
  - name: webapp-testing
    source: claude-default
    added: "2026-01-19"
    reason: "E2E testing for React frontend"
  ```

## Output

Updated or created files:
- `.ai-workflow.yaml` - AI tooling configuration
- `CLAUDE.md` - Project-specific instructions (if missing)

Configuration includes:
- Project classification
- All configured skills (existing + new)
- All configured agents (existing + new)
- All configured MCP servers (existing + new, including context7)
- LSP status for detected languages
- Audit trail of additions

## Gate Criteria

Before advancing to Phase 5 (Planning):

- [ ] `.ai-workflow.yaml` exists
- [ ] `CLAUDE.md` exists (project-level)
- [ ] `~/.claude/CLAUDE.md` exists or user notified (global-level)
- [ ] Tech stack tools matched from registry
- [ ] Context7 MCP server recommended (live docs)
- [ ] LSP status checked for all detected languages
- [ ] Gap analysis completed
- [ ] User approved configuration
- [ ] New feature tooling identified

## Key Principles

1. **Don't remove existing tools** - Only add what's missing
2. **Document additions** - Include date and reason for each new tool
3. **Focus on gaps** - Don't reconfigure what already works
4. **Consider new features** - 📋 items may need specific tools
5. **User approval required** - Don't auto-add tools without confirmation
6. **Always recommend Context7** - Live documentation solves training cutoff issues
7. **Check LSP status** - 900x faster code navigation is critical
8. **Generate CLAUDE.md if missing** - Project-specific instructions improve Claude behavior
