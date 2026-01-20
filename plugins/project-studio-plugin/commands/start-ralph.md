---
name: start-ralph
description: |
  Set up the Ralph autonomous execution environment.
  Usage: /start-ralph [feature-name]
  Creates .ralph/ directory, copies templates, and creates feature branch.
---

# /start-ralph Command

Initialize the Ralph autonomous agent environment for a feature.

## Usage

```bash
# Start Ralph for a specific feature
/start-ralph booking-discount

# Auto-detect feature from .project-studio state
/start-ralph
```

## Process

1. **Detect or use feature name** from argument or `.project-studio/state.yaml`
2. **Create `.ralph/` directory** if it doesn't exist
3. **Copy templates**:
   - Copy `assets/templates/ralph-instructions.md` to `.ralph/INSTRUCTIONS.md`
   - Generate `run.sh` from `assets/templates/ralph-run-sh.md`
4. **Make run.sh executable** with `chmod +x run.sh`
5. **Create git branch** `ralph/{feature-name}` from current branch
6. **Report setup status** to user

## Directory Structure Created

```
project-root/
├── .ralph/
│   ├── INSTRUCTIONS.md    # Ralph execution rules
│   └── CLAUDE.md          # Combined instructions (created by run.sh)
├── prd.json               # User stories (created by /start-ralph in US-004)
├── progress.txt           # Progress log (created by run.sh)
└── run.sh                 # Wrapper script
```

## Prerequisites

Before running `/start-ralph`:
- Feature PRD should exist at `.project-studio/features/{feature}/PRD.md`
- Project should have a `CLAUDE.md` file at root (optional but recommended)

## Implementation Steps

When the user runs `/start-ralph [feature-name]`:

### Step 1: Determine Feature Name
```markdown
IF argument provided:
  feature_name = argument
ELSE IF .project-studio/state.yaml exists:
  feature_name = state.yaml.currentFeature
ELSE:
  ASK user for feature name
```

### Step 2: Create .ralph/ Directory
```bash
mkdir -p .ralph
```

### Step 3: Copy INSTRUCTIONS.md Template
Copy the Ralph instructions template to `.ralph/INSTRUCTIONS.md`:
```bash
# Source: assets/templates/ralph-instructions.md (from plugin)
# Destination: .ralph/INSTRUCTIONS.md (in user's project)
```

The template contains Ralph's execution rules:
- Read prd.json and progress.txt
- Pick highest priority story with passes: false
- Implement one story per iteration
- Commit with conventional format
- Update PRD and progress log
- Signal completion with `<promise>COMPLETE</promise>`

### Step 4: Generate run.sh
Extract the shell script from `assets/templates/ralph-run-sh.md` and save to `run.sh`:
```bash
# Extract content between ```bash and ``` markers
# Save to run.sh at project root
chmod +x run.sh
```

### Step 5: Create Git Branch
```bash
git checkout -b ralph/{feature-name}
```

If branch already exists:
```bash
git checkout ralph/{feature-name}
```

### Step 6: Initialize Progress Log
```bash
# Create progress.txt if it doesn't exist
echo "# Ralph Progress Log" > progress.txt
echo "Started: $(date)" >> progress.txt
echo "---" >> progress.txt
```

## Output

```markdown
## Ralph Environment Ready

**Feature:** booking-discount
**Branch:** ralph/booking-discount

### Files Created
- `.ralph/INSTRUCTIONS.md` - Ralph execution rules
- `run.sh` - Wrapper script (executable)
- `progress.txt` - Progress log initialized

### Next Steps
1. Run `/start-ralph` with PRD conversion (US-004) to generate `prd.json`
2. Execute `./run.sh` to start Ralph autonomous execution
3. Monitor progress in `progress.txt`
4. When complete, run `/archive-feature` to clean up
```

## Error Handling

If templates not found:
```
Error: Ralph templates not found

The following templates are required:
- assets/templates/ralph-instructions.md
- assets/templates/ralph-run-sh.md

Ensure the project-studio-plugin is properly installed.
```

If git branch creation fails:
```
Warning: Could not create git branch

Branch 'ralph/{feature-name}' may already exist or git is not initialized.
Continuing with setup...
```

## Integration with Other Commands

- **Before**: Use `/add-feature` to create Feature PRD
- **Next**: US-004 will add PRD-to-JSON conversion to this command
- **After**: Use `/archive-feature` to clean up completed work

## Notes

- This command sets up the environment only; it does NOT start Ralph execution
- PRD conversion to `prd.json` is handled in US-004
- The `run.sh` script combines `.ralph/INSTRUCTIONS.md` with project `CLAUDE.md`
- Progress is tracked in `progress.txt` at project root
