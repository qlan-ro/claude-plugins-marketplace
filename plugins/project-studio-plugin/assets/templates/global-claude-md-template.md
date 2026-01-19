# Global CLAUDE.md Template
# Location: ~/.claude/CLAUDE.md
# Purpose: Security gatekeeper + standards for ALL projects

## Identity & Authentication

### GitHub Account
**ALWAYS** use **{{GITHUB_USERNAME}}** for all projects:
- SSH: `git@github.com:{{GITHUB_USERNAME}}/<repo>.git`
- HTTPS: `https://github.com/{{GITHUB_USERNAME}}/<repo>.git`

### Docker Hub
Already authenticated. Username in `~/.env` as `DOCKER_HUB_USER`

---

## NEVER EVER DO

These rules are **ABSOLUTE** and apply to every project:

### NEVER Publish Sensitive Data
- NEVER publish passwords, API keys, tokens to git/npm/docker
- Before ANY commit: verify no secrets included
- NEVER echo or log credentials, even for debugging

### NEVER Commit .env Files
- NEVER commit `.env` to git
- ALWAYS verify `.env` is in `.gitignore`
- NEVER include real values in `.env.example`

### NEVER Run Dangerous Commands
- NEVER run `rm -rf /` or similar destructive commands
- NEVER run `git push --force` to main/master without explicit confirmation
- NEVER run `git reset --hard` without explicit confirmation
- NEVER drop databases in production

### NEVER Bypass Security
- NEVER skip pre-commit hooks (--no-verify)
- NEVER disable SSL verification
- NEVER hardcode credentials in source files

---

## New Project Standards

When creating ANY new project, always include:

### Required Files
- `.env` — Environment variables (NEVER commit)
- `.env.example` — Template with placeholder values only
- `.gitignore` — Must include: .env, node_modules/, dist/, .DS_Store
- `CLAUDE.md` — Project-specific instructions
- `README.md` — Project documentation

### Required .gitignore Entries
```
# Environment
.env
.env.local
.env.*.local

# Dependencies
node_modules/
vendor/
venv/
__pycache__/

# Build
dist/
build/
*.egg-info/

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db

# Secrets
*.pem
*.key
credentials.json
secrets.json
```

### Node.js Projects
Add to entry point for proper error handling:
```javascript
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection:', reason);
  process.exit(1);
});
```

---

## Chat Hygiene

### One Task, One Chat
Research shows **39% performance degradation** when mixing topics in a single chat.

- Start a new chat for each distinct task
- Use `/clear` between unrelated tasks
- After 20+ turns, consider starting fresh

### When to Use /clear
- Switching between features
- After completing a phase
- When context feels polluted
- Before starting implementation after research

---

## Commit Standards

### Format: Conventional Commits
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code change, no feature/fix
- `test`: Adding tests
- `chore`: Maintenance tasks

### Before Every Commit
1. Run `git diff --staged` to review changes
2. Verify no secrets in diff
3. Run tests if available
4. Use meaningful commit message

---

## MCP Servers (Global)

These MCP servers are useful across all projects:

```bash
# Live documentation (highly recommended)
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest

# GitHub integration
claude mcp add github -- npx -y @modelcontextprotocol/server-github

# File operations
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem
```

---

## Quality Gates

Before marking any task complete:
- [ ] Code compiles/runs without errors
- [ ] Tests pass (if applicable)
- [ ] No secrets in committed code
- [ ] Documentation updated (if applicable)
- [ ] Linting passes (if configured)
