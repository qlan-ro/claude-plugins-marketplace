---
name: pr
description: |
  Create a pull request for the current feature branch.
  Usage: /pr [--draft]
  Requires all stories to be committed.
---

# /pr Command

Create a pull request for the current feature via the git-workflow agent.

## Usage

```bash
# Create PR
/pr

# Create draft PR
/pr --draft
```

## Prerequisites

Before running:
- All stories in progress.txt must be committed
- Feature branch must exist
- No uncommitted changes

## Process

1. **Verify completion** - Check all stories are `COMMITTED` in progress.txt
2. **Verify clean** - Ensure no uncommitted changes
3. **Spawn git-workflow agent** in feature-pr mode
4. **Push branch** to remote
5. **Create PR** via GitHub CLI
6. **Update progress.txt** with PR URL

## PR Content

Generated from Feature PRD and progress.txt:

```markdown
## Summary
{Feature description from PRD}

## Changes
{List of major changes from commits}

## User Stories Completed
- [x] US-001: {title}
- [x] US-002: {title}
- [x] US-003: {title}

## Testing
- [ ] All unit tests pass
- [ ] Manual testing completed
- [ ] Code review requested

## Screenshots
{If UI changes detected}

---
🤖 Generated with [Claude Code](https://claude.ai/code) via Project Studio
```

## Examples

```bash
# After completing all stories
/pr
# Output: PR #123 created: https://github.com/org/repo/pull/123

# For work-in-progress
/pr --draft
# Output: Draft PR #124 created: https://github.com/org/repo/pull/124
```

## Output

```markdown
## Pull Request Created

**PR:** #123
**URL:** https://github.com/org/repo/pull/123
**Branch:** `feature/booking-discounts` → `main`

### Summary
Added discount support for bookings with validation and calculation.

### Stories Included
- [x] US-001: Add discount field (abc1234)
- [x] US-002: Discount validation (def5678)
- [x] US-003: Apply to total (ghi9012)

### Next Steps
1. Request code review
2. Address feedback
3. Merge when approved

View PR: `gh pr view 123`
Merge PR: `gh pr merge 123`
```

## Error Handling

If stories not committed:
```
❌ Cannot create PR - uncommitted stories

Pending:
[ ] US-003: Apply discount to total - IN_PROGRESS
[ ] US-004: Discount reports - PENDING

Run /commit for each story first.
```

If uncommitted changes:
```
❌ Cannot create PR - uncommitted changes

Modified files:
- src/services/BookingService.ts

Run /commit first.
```

If not on feature branch:
```
❌ Cannot create PR - not on a feature branch

Current branch: main

Switch to a feature branch first.
```

## GitHub CLI Requirement

This command requires the GitHub CLI (`gh`) to be installed and authenticated:

```bash
# Install
brew install gh  # macOS
# or: https://cli.github.com/

# Authenticate
gh auth login
```
