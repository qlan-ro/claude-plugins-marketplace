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
6. **Convert Feature PRD to prd.json**:
   - Read `.project-studio/features/{feature}/PRD.md`
   - Parse user stories, descriptions, acceptance criteria
   - Output `.ralph/prd.json` with all stories `passes: false`
7. **Initialize .ralph/progress.txt** with header and timestamp
8. **Report setup status** to user

## Directory Structure Created

```
project-root/
├── .ralph/
│   ├── INSTRUCTIONS.md    # Ralph execution rules
│   ├── CLAUDE.md          # Combined instructions (created by run.sh)
│   ├── prd.json           # User stories (converted from Feature PRD)
│   └── progress.txt       # Progress log
├── CLAUDE.md              # User's project instructions (untouched)
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

### Step 6: Convert Feature PRD to prd.json

Read the Feature PRD markdown and convert to Ralph-compatible JSON format.

**Source:** `.project-studio/features/{feature}/PRD.md`
**Destination:** `.ralph/prd.json`

#### Parsing Rules

1. **Extract project name** from the PRD title (line starting with `# PRD:`)
2. **Extract user stories** by finding sections matching `### US-XXX: {Title}`
3. **Extract description** from the line starting with `**Description:**`
4. **Extract acceptance criteria** from lines starting with `- [ ]` under `**Acceptance Criteria:**`

#### JSON Schema

```json
{
  "project": "{project-name}",
  "branchName": "ralph/{feature-name}",
  "description": "{Feature description from Introduction section}",
  "userStories": [
    {
      "id": "US-001",
      "title": "Story Title",
      "description": "As a user, I want X so that Y.",
      "acceptanceCriteria": [
        "Criterion 1",
        "Criterion 2"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

#### Parsing Algorithm

```markdown
1. Read PRD.md file content
2. Extract project name from title: /^# PRD: (.+)$/
3. Extract description from Introduction section (first paragraph after ## Introduction)
4. Find all user story sections: /^### (US-\d+): (.+)$/
5. For each user story:
   a. Extract ID and title from header
   b. Extract description from **Description:** line
   c. Extract acceptance criteria from - [ ] items
   d. Set priority = story index (1-based)
   e. Set passes = false
   f. Set notes = ""
6. Output JSON with proper formatting
```

#### Example Input (PRD.md)

```markdown
# PRD: User Dashboard

## Introduction

A dashboard for users to view their activity.

## User Stories

### US-001: Display User Stats
**Description:** As a user, I want to see my stats so that I can track progress.

**Acceptance Criteria:**
- [ ] Show total sessions
- [ ] Show average duration
- [ ] Typecheck passes
```

#### Example Output (prd.json)

```json
{
  "project": "user-dashboard",
  "branchName": "ralph/user-dashboard",
  "description": "A dashboard for users to view their activity.",
  "userStories": [
    {
      "id": "US-001",
      "title": "Display User Stats",
      "description": "As a user, I want to see my stats so that I can track progress.",
      "acceptanceCriteria": [
        "Show total sessions",
        "Show average duration",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

### Step 7: Initialize Progress Log
```bash
# Create progress.txt in .ralph/ directory
echo "# Ralph Progress Log" > .ralph/progress.txt
echo "Started: $(date)" >> .ralph/progress.txt
echo "---" >> .ralph/progress.txt
```

## Output

```markdown
## Ralph Environment Ready

**Feature:** booking-discount
**Branch:** ralph/booking-discount

### Files Created
- `.ralph/INSTRUCTIONS.md` - Ralph execution rules
- `.ralph/prd.json` - 5 user stories (all passes: false)
- `.ralph/progress.txt` - Progress log initialized
- `run.sh` - Wrapper script (executable)

### Next Steps
1. Execute `./run.sh` to start Ralph autonomous execution
2. Monitor progress in `.ralph/progress.txt`
3. When complete, run `/archive-feature` to clean up
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

If Feature PRD not found:
```
Error: Feature PRD not found

Expected location: .project-studio/features/{feature}/PRD.md

Please create the Feature PRD first using /add-feature command.
```

If PRD parsing fails:
```
Warning: Could not parse all user stories

The PRD may not follow the expected format. Please ensure:
- User stories use format: ### US-XXX: {Title}
- Description starts with: **Description:**
- Criteria start with: - [ ]

Manual review of prd.json may be needed.
```

## Integration with Other Commands

- **Before**: Use `/add-feature` to create Feature PRD at `.project-studio/features/{feature}/PRD.md`
- **After**: Use `/archive-feature` to clean up completed work

## Notes

- This command sets up the environment AND converts the PRD; it does NOT start Ralph execution
- The `run.sh` script combines `.ralph/INSTRUCTIONS.md` with project `CLAUDE.md` into `.ralph/CLAUDE.md`
- All Ralph files (`prd.json`, `progress.txt`, `CLAUDE.md`) are kept in `.ralph/` to avoid conflicts with user's project files
- Progress is tracked in `.ralph/progress.txt`
- Feature PRD must exist at `.project-studio/features/{feature}/PRD.md` before running this command
