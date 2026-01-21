---
name: project-studio:quick-fix
description: |
  Execute small tasks directly with automatic doc impact checking.
  Usage: /project-studio:quick-fix [task description]
  For: bug fixes, logging, refactoring, small changes that don't warrant full workflow.
---

# Quick Fix Command

Execute small tasks directly without the full PRD workflow, while ensuring documentation stays in sync if changes have broader impact.

## Arguments

$ARGUMENTS

## Usage

```bash
# Bug fixes
/project-studio:quick-fix "Fix null pointer in UserService.authenticate()"

# Add logging
/project-studio:quick-fix "Add logging to payment processing flow"

# Small refactors
/project-studio:quick-fix "Extract validation logic from BookingController"

# Error handling
/project-studio:quick-fix "Handle timeout errors in API client"

# Interactive mode
/project-studio:quick-fix
# Will ask what you want to fix
```

## When to Use

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              TASK SIZING                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ✅ USE /quick-fix for:                                                 │
│  • Bug fixes                                                            │
│  • Adding logging/debugging                                             │
│  • Error handling improvements                                          │
│  • Code refactoring (same behavior)                                     │
│  • Performance optimizations                                            │
│  • Renaming/reorganizing                                                │
│  • Documentation updates                                                │
│  • Test additions for existing code                                     │
│                                                                         │
│  ❌ USE /add-feature instead for:                                       │
│  • New user-facing functionality                                        │
│  • New API endpoints                                                    │
│  • New database tables/models                                           │
│  • New screens/pages                                                    │
│  • Anything that adds NEW capability                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│  STEP 1: EXECUTE TASK                                                   │
│  Implement the fix/change directly                                      │
├─────────────────────────────────────────────────────────────────────────┤
│  STEP 2: VERIFY                                                         │
│  Run tests to ensure no regression                                      │
├─────────────────────────────────────────────────────────────────────────┤
│  STEP 3: IMPACT CHECK                                                   │
│  Did changes affect API, data model, UI behavior, or feature scope?     │
│  If YES → Update relevant doc section (surgical, minimal)               │
├─────────────────────────────────────────────────────────────────────────┤
│  STEP 4: COMMIT                                                         │
│  Conventional commit: fix:, refactor:, perf:, chore:, docs:             │
└─────────────────────────────────────────────────────────────────────────┘
```

## Process

### Step 1: Execute Task

Implement the requested change directly:

1. Locate the relevant code
2. Make the fix/change
3. Keep changes focused and minimal

### Step 2: Verify

Run verification appropriate to the change:

```bash
# Run tests
npm test
# or
pytest
# or project-specific test command

# Run linting
npm run lint
# or equivalent
```

If tests fail, fix them before proceeding.

### Step 3: Impact Check

After implementation, assess if changes affect documentation:

```markdown
## Impact Assessment

### Changes Made
- `src/services/UserService.ts` - Added null check in authenticate()
- `src/services/UserService.test.ts` - Added test for null case

### Documentation Impact

| Area | Affected? | Action |
|------|-----------|--------|
| API contract (routes, responses, errors) | No | - |
| Data model (schemas, entities) | No | - |
| UI behavior (flows, components) | No | - |
| Feature scope (capabilities) | No | - |

**Result:** No documentation updates needed.
```

### Impact Matrix

| If You Changed... | Update This Doc | Section |
|-------------------|-----------------|---------|
| API routes | `docs/ARCHITECTURE.md` | API Design |
| API response format | `docs/ARCHITECTURE.md` | API Design |
| Error codes/responses | `docs/ARCHITECTURE.md` | Error Handling |
| Database schema | `docs/ARCHITECTURE.md` | Data Model |
| Entity relationships | `docs/ARCHITECTURE.md` | Data Model |
| UI component behavior | `docs/DESIGN.md` | Components |
| User flow changes | `docs/DESIGN.md` | User Flows |
| Feature behavior | `docs/PRODUCT_PRD.md` | Feature description |
| Acceptance criteria | `docs/PRODUCT_PRD.md` | Feature AC |

### Surgical Doc Updates

When docs need updating, make **minimal, targeted changes**:

```markdown
## Example: Added new error code

### Before (ARCHITECTURE.md)
| Code | Meaning |
|------|---------|
| 401 | Unauthorized |
| 404 | Not found |

### After (ARCHITECTURE.md)
| Code | Meaning |
|------|---------|
| 401 | Unauthorized |
| 404 | Not found |
| 408 | Request timeout |  ← Added only this line
```

Do NOT rewrite entire sections. Add/modify only what changed.

### Step 4: Commit

Use conventional commit format based on change type:

| Change Type | Prefix | Example |
|-------------|--------|---------|
| Bug fix | `fix:` | `fix(auth): handle null user in authenticate` |
| Refactoring | `refactor:` | `refactor(booking): extract validation logic` |
| Performance | `perf:` | `perf(api): add caching to user lookup` |
| Logging/debug | `chore:` | `chore(payments): add logging to payment flow` |
| Documentation | `docs:` | `docs(api): add timeout error code` |
| Tests | `test:` | `test(auth): add null user test case` |

## Example Sessions

### Simple Bug Fix (No Doc Impact)

```
User: /project-studio:quick-fix "Fix null pointer in UserService.authenticate()"

Claude: ## Quick Fix: Null pointer in UserService.authenticate()

### Step 1: Executing Fix

Found issue in `src/services/UserService.ts:47`
- `authenticate()` doesn't check if user exists before accessing properties

Fix applied:
- Added null check before accessing user.passwordHash
- Return early with AuthError if user not found

### Step 2: Verification

Running tests...
✅ All 47 tests passing
✅ Linting passed

### Step 3: Impact Check

| Area | Affected? |
|------|-----------|
| API contract | No - same 401 response |
| Data model | No |
| UI behavior | No |
| Feature scope | No |

**No documentation updates needed.**

### Step 4: Commit

Created commit:
```
fix(auth): handle null user in authenticate

Added null check to prevent crash when user lookup returns undefined.
Returns 401 Unauthorized instead of 500 Internal Server Error.

Co-Authored-By: Claude <noreply@anthropic.com>
```

✅ Quick fix complete.
```

### Fix With Doc Impact

```
User: /project-studio:quick-fix "Add rate limiting error response to login endpoint"

Claude: ## Quick Fix: Rate limiting error for login

### Step 1: Executing Fix

Added rate limiting response to `src/api/auth/login.ts`:
- Return 429 Too Many Requests when rate limit exceeded
- Include Retry-After header
- Return structured error body

### Step 2: Verification

Running tests...
✅ All tests passing (added 2 new tests for rate limiting)
✅ Linting passed

### Step 3: Impact Check

| Area | Affected? | Action |
|------|-----------|--------|
| API contract | **Yes** - new error code | Update ARCHITECTURE.md |
| Data model | No | - |
| UI behavior | No | - |
| Feature scope | No | - |

**Updating documentation...**

Updated `docs/ARCHITECTURE.md` → Error Handling section:
- Added 429 rate limit response
- Documented Retry-After header
- Added error body schema

### Step 4: Commit

Created commit:
```
fix(auth): add rate limiting error response to login

Returns 429 Too Many Requests with Retry-After header when
login attempts exceed rate limit. Prevents brute force attacks.

Co-Authored-By: Claude <noreply@anthropic.com>
```

✅ Quick fix complete. Documentation updated.
```

## Skipping Steps

You can skip verification in urgent situations:

```bash
/project-studio:quick-fix --skip-verify "Emergency fix for production crash"
```

But **never skip impact check** - doc drift causes problems later.

## Escalation

If during the fix you realize:
- This is actually a new feature → Stop and use `/project-studio:add-feature`
- This requires significant architecture changes → Stop and use `/project-studio:add-feature`
- This is bigger than expected → Stop and reassess

```
⚠️ Escalation Notice

This task appears larger than a quick fix:
- Requires new database table
- Adds new API endpoint
- Changes multiple user flows

Recommend using /project-studio:add-feature instead.

Continue anyway? (y/N)
```

## Output Summary

On completion:

```markdown
## Quick Fix Complete

**Task:** Fix null pointer in UserService.authenticate()
**Commit:** `abc1234`
**Files Changed:** 2

### Changes
- `src/services/UserService.ts` - Added null check
- `src/services/UserService.test.ts` - Added test case

### Documentation
- No updates needed

### Verification
- ✅ Tests passing
- ✅ Linting passed
```

## Quick Reference

| Need | Command |
|------|---------|
| Small fix/change | `/project-studio:quick-fix "description"` |
| New capability | `/project-studio:add-feature "description"` |
| Commit only | `/project-studio:commit` |
| Check workflow status | `/project-studio:workflow-status` |
