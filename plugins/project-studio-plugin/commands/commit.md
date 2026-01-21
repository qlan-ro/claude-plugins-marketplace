---
name: project-studio:commit
description: |
  Commit current work with a conventional commit message.
  Usage: /project-studio:commit [message]
  If no message provided, generates one based on changes.
---

# /project-studio:commit Command

Manually trigger a commit for current work via the git-workflow agent.

## Usage

```bash
# With explicit message
/project-studio:commit "feat(bookings): add discount field"

# Auto-generate message from changes
/project-studio:commit
```

## Process

1. **Detect current feature** from progress.txt or branch name
2. **Spawn git-workflow agent** in story-commit mode
3. **Verify** - Run tests and linting
4. **Stage** - Add relevant files
5. **Commit** - With conventional message
6. **Update progress.txt** - Mark story as committed

## Message Format

If message provided:
```
{provided-message}

Co-Authored-By: Claude <noreply@anthropic.com>
```

If auto-generated:
```
{type}({scope}): {description from diff analysis}

{body - summarized changes}

Refs: {story-id from progress.txt}
Co-Authored-By: Claude <noreply@anthropic.com>
```

## Examples

```bash
# Feature commit
/project-studio:commit "feat(auth): add OAuth2 login flow"

# Bug fix
/project-studio:commit "fix(api): resolve null pointer in user lookup"

# Refactoring
/project-studio:commit "refactor(services): extract validation logic"

# Let agent decide
/project-studio:commit
# Agent analyzes changes and creates appropriate message
```

## Validation

Before committing, git-workflow agent verifies:
- [ ] Tests pass
- [ ] Linting passes
- [ ] No secrets in staged files
- [ ] Commit message follows conventional format

## Output

```markdown
## Committed

**Commit:** `abc1234`
**Message:** feat(bookings): add discount field
**Files:** 5 files changed

### Changes
- `src/components/BookingForm.tsx`
- `src/dto/BookingDTO.ts`
- `src/services/BookingService.ts`

### Progress
Updated progress.txt:
[x] US-042: Add discount field - COMMITTED (abc1234)
```

## Error Handling

If tests fail:
```
❌ Cannot commit - tests failing

Failures:
- BookingService.test.ts: 2 failures
- BookingForm.test.tsx: 1 failure

Fix tests before committing.
```

If nothing to commit:
```
ℹ️ Nothing to commit - working tree clean
```
