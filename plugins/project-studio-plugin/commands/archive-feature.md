---
name: archive-feature
description: |
  Archive a completed feature after Ralph execution finishes.
  Usage: /archive-feature [feature-name]
  Moves prd.json and progress.txt to archive, cleans up .ralph/ directory.
---

# /archive-feature Command

Archive a completed feature and clean up Ralph execution artifacts.

## Usage

```bash
# Archive a specific feature
/archive-feature booking-discount

# Auto-detect feature from .project-studio state or prd.json
/archive-feature
```

## Process

1. **Detect or use feature name** from argument, `prd.json`, or `.project-studio/state.yaml`
2. **Verify all stories are complete** by checking `prd.json` (all must have `passes: true`)
3. **Create archive directory** at `.project-studio/archive/{date}-{feature}/`
4. **Move artifacts** to archive:
   - `prd.json` → `.project-studio/archive/{date}-{feature}/prd.json`
   - `progress.txt` → `.project-studio/archive/{date}-{feature}/progress.txt`
5. **Clean up .ralph/ directory** (remove CLAUDE.md, keep INSTRUCTIONS.md template)
6. **Update state.yaml** to mark feature as complete
7. **Print summary** of completed stories

## Prerequisites

Before running `/archive-feature`:
- All user stories in `prd.json` must have `passes: true`
- The feature should be fully implemented and committed

## Implementation Steps

When the user runs `/archive-feature [feature-name]`:

### Step 1: Determine Feature Name

```markdown
IF argument provided:
  feature_name = argument
ELSE IF prd.json exists:
  feature_name = prd.json.project (slug from project name)
ELSE IF .project-studio/state.yaml exists:
  feature_name = state.yaml current feature
ELSE:
  ASK user for feature name
```

### Step 2: Verify Story Completion

Read `prd.json` and verify all stories are complete:

```markdown
1. Read prd.json from project root
2. Check each story in userStories array
3. If ANY story has passes: false:
   - STOP and show error with incomplete stories list
   - Suggest: "Complete remaining stories before archiving"
4. If ALL stories have passes: true:
   - Continue with archiving
```

**Error if incomplete:**
```
Error: Feature has incomplete user stories

The following stories are not yet complete:
- US-003: Add User Profile (passes: false)
- US-005: Implement Settings (passes: false)

Complete all stories before archiving. You can:
1. Continue Ralph execution to complete remaining stories
2. Manually mark stories as complete if they were done outside Ralph
```

### Step 3: Create Archive Directory

```bash
# Generate timestamp for unique archive directory
date_stamp=$(date +%Y-%m-%d)

# Create archive directory structure
mkdir -p .project-studio/archive/${date_stamp}-${feature_name}
```

Example: `.project-studio/archive/2026-01-21-booking-discount/`

### Step 4: Move Artifacts to Archive

```bash
# Move prd.json to archive
mv prd.json .project-studio/archive/${date_stamp}-${feature_name}/prd.json

# Move progress.txt to archive
mv progress.txt .project-studio/archive/${date_stamp}-${feature_name}/progress.txt
```

If `run.sh` exists at project root:
```bash
# Move run.sh to archive (optional, for reference)
mv run.sh .project-studio/archive/${date_stamp}-${feature_name}/run.sh
```

### Step 5: Clean Up .ralph/ Directory

The `.ralph/` directory contains:
- `INSTRUCTIONS.md` - Ralph instructions template (KEEP for reuse)
- `CLAUDE.md` - Combined instructions from run.sh (DELETE - regenerated each run)

```bash
# Remove generated combined CLAUDE.md
rm -f .ralph/CLAUDE.md

# Keep INSTRUCTIONS.md for future Ralph executions
# (do NOT delete .ralph/INSTRUCTIONS.md)
```

**Why keep INSTRUCTIONS.md?**
- The INSTRUCTIONS.md template is copied from the plugin once
- Future `/start-ralph` runs can skip the copy if it already exists
- Modifications to instructions are preserved between features

### Step 6: Update state.yaml

If `.project-studio/state.yaml` exists, update the feature status:

```yaml
# Find the feature in features.items and update:
features:
  items:
    - id: "{feature_name}"
      status: "completed"  # Changed from "in_development"
      stories_completed: {total_stories}  # Set to match stories_total
      pr_url: "{pr_url_if_available}"  # Optional
```

Also update counters:
```yaml
features:
  in_development: {decrement by 1}
  completed: {increment by 1}
```

**YAML Update Pseudocode:**
```markdown
1. Read .project-studio/state.yaml
2. Find feature by id in features.items
3. Set status = "completed"
4. Set stories_completed = stories_total
5. Update counters: in_development--, completed++
6. Write updated state.yaml
```

### Step 7: Print Summary

Generate a summary of the completed feature:

```markdown
## Feature Archived: {feature_name}

**Completed:** {date}
**Branch:** ralph/{feature_name}

### Stories Completed ({count} total)

| Story | Title | Status |
|-------|-------|--------|
| US-001 | Create Login Form | ✓ Passed |
| US-002 | Add Validation | ✓ Passed |
| US-003 | Implement OAuth | ✓ Passed |

### Artifacts Archived

- `.project-studio/archive/{date}-{feature}/prd.json`
- `.project-studio/archive/{date}-{feature}/progress.txt`

### Next Steps

1. Create pull request: `git push -u origin ralph/{feature_name}`
2. Merge to main branch
3. Start next feature with `/add-feature`
```

## Output Example

```markdown
## Feature Archived: booking-discount

**Completed:** 2026-01-21
**Branch:** ralph/booking-discount

### Stories Completed (5 total)

| Story | Title | Status |
|-------|-------|--------|
| US-001 | Add Discount Model | ✓ Passed |
| US-002 | Create Discount Service | ✓ Passed |
| US-003 | Add API Endpoints | ✓ Passed |
| US-004 | Build Discount UI | ✓ Passed |
| US-005 | Add Validation Rules | ✓ Passed |

### Artifacts Archived

- `.project-studio/archive/2026-01-21-booking-discount/prd.json`
- `.project-studio/archive/2026-01-21-booking-discount/progress.txt`
- `.project-studio/archive/2026-01-21-booking-discount/run.sh`

### Next Steps

1. Create pull request: `git push -u origin ralph/booking-discount`
2. Merge to main branch
3. Start next feature with `/add-feature`
```

## Error Handling

### Feature Name Not Found

```
Error: Could not determine feature name

No feature name provided and could not auto-detect from:
- prd.json (file not found)
- .project-studio/state.yaml (file not found or no current feature)

Usage: /archive-feature <feature-name>
```

### prd.json Not Found

```
Error: No prd.json found

Expected file at project root: ./prd.json

This command archives Ralph execution artifacts. Please ensure:
1. Ralph execution has been set up with /start-ralph
2. The prd.json file exists at project root
```

### Incomplete Stories

```
Error: Feature has incomplete user stories

The following stories are not yet complete:
- US-003: Add User Profile (passes: false)
- US-005: Implement Settings (passes: false)

Complete all stories before archiving. You can:
1. Continue Ralph execution to complete remaining stories
2. Manually mark stories as complete if they were done outside Ralph
```

### Archive Directory Already Exists

```
Warning: Archive directory already exists

Directory: .project-studio/archive/2026-01-21-booking-discount/

Options:
1. Use a unique suffix: .project-studio/archive/2026-01-21-booking-discount-2/
2. Overwrite existing archive (not recommended)

Proceeding with unique suffix...
```

## Integration with Other Commands

- **Before**: Use `/start-ralph` to set up Ralph environment and begin execution
- **After**: Use `/add-feature` to start the next feature
- **Related**: Use `/pr` to create a pull request for the completed feature branch

## Notes

- This command does NOT create a pull request (use `/pr` for that)
- This command does NOT merge branches
- The archived files are kept for historical reference
- The `.ralph/INSTRUCTIONS.md` template is preserved for future features
- If state.yaml doesn't exist, only archive operations are performed
