# Project Studio Plugin - Ralph Integration

## Overview

Transform the project-studio-plugin to be **Ralph-compatible** by generating proper `prd.json` + `progress.txt` files and integrating with the snarktank/ralph execution loop.

## Goals

1. Generate Ralph-compatible output files from Feature PRDs
2. Handle CLAUDE.md conflict (project instructions vs Ralph execution rules)
3. Create `/start-ralph` and `/archive-feature` commands
4. Enable standalone operation (no companion app required)

---

## User Stories

### US-001: Create Ralph Run Wrapper Script Generator

**As a** developer using project-studio-plugin
**I want** a `/start-ralph` command that generates `.ralph/run.sh`
**So that** I can run Ralph with combined context (execution rules + project instructions)

**Acceptance Criteria:**
- Creates `.ralph/` directory if not exists
- Copies Ralph INSTRUCTIONS.md template to `.ralph/INSTRUCTIONS.md`
- Generates `.ralph/run.sh` that combines:
  - `.ralph/INSTRUCTIONS.md` (Ralph execution rules)
  - `CLAUDE.md` (project-specific context)
- Makes `run.sh` executable
- Creates empty `progress.txt` at project root
- Creates git branch `ralph/{feature-name}`

**Files to modify:**
- `commands/start-ralph.md` (new)
- `assets/templates/ralph-instructions.md` (new)
- `assets/templates/ralph-run-sh.md` (new)

---

### US-002: Create Ralph Instructions Template

**As a** developer
**I want** a proper INSTRUCTIONS.md template based on snarktank/ralph
**So that** Ralph knows how to execute the loop correctly

**Acceptance Criteria:**
- Template includes: read prd.json, track progress.txt, one story per iteration
- Template includes: commit frequently, keep CI green
- Template includes: signal completion with `<promise>COMPLETE</promise>`
- Template includes: append learnings to progress.txt
- Template does NOT override project CLAUDE.md content

**Files to modify:**
- `assets/templates/ralph-instructions.md` (new)

---

### US-003: Create Feature PRD to prd.json Converter

**As a** developer
**I want** `/start-ralph` to convert `.project-studio/features/*/PRD.md` to `prd.json`
**So that** vanilla ralph.sh can execute my features

**Acceptance Criteria:**
- Reads PRD.md from `.project-studio/features/{feature}/PRD.md`
- Parses user stories into JSON format with: id, title, description, acceptance_criteria, passes
- Outputs `prd.json` at project root
- All stories start with `passes: false`
- JSON validates against Ralph's expected schema

**Files to modify:**
- `commands/start-ralph.md` (update)
- `skills/prd-conversion/SKILL.md` (new)

---

### US-004: Create Archive Feature Command

**As a** developer
**I want** `/archive-feature` command
**So that** completed features are archived and I can start the next one

**Acceptance Criteria:**
- Moves `prd.json` to `.project-studio/archive/{date}-{feature}/prd.json`
- Moves `progress.txt` to `.project-studio/archive/{date}-{feature}/progress.txt`
- Cleans up `.ralph/` directory (keeps INSTRUCTIONS.md template)
- Updates `.project-studio/state.yaml` to mark feature complete
- Prints summary of completed stories

**Files to modify:**
- `commands/archive-feature.md` (new)

---

### US-005: Add Story Sizing Validation

**As a** developer
**I want** stories validated for single-context-window size
**So that** Ralph can complete each story in one iteration

**Acceptance Criteria:**
- Warning if story description > 3 sentences
- Warning if acceptance criteria > 5 items
- Warning if files to modify > 5 files
- Suggests splitting oversized stories
- Can be bypassed with `--force` flag

**Files to modify:**
- `skills/story-writing/SKILL.md` (update)
- `references/checklists/story-sizing.md` (new)

---

### US-006: Update Orchestration Skill for Ralph Workflow

**As a** developer
**I want** the orchestration skill to support Ralph workflow
**So that** the plugin guides me through Ralph-compatible development

**Acceptance Criteria:**
- New phase: "Ralph Execution" after Planning phase
- Phase includes: `/start-ralph`, monitor progress, `/archive-feature`
- State tracking for active Ralph session
- Can resume interrupted Ralph sessions

**Files to modify:**
- `skills/orchestration/SKILL.md` (update)
- `references/phases/06-ralph-execution.md` (new)

---

## Technical Notes

### prd.json Schema (Ralph-compatible)

```json
{
  "project": "feature-name",
  "stories": [
    {
      "id": "US-001",
      "title": "Story title",
      "description": "As a... I want... So that...",
      "acceptance_criteria": ["criterion 1", "criterion 2"],
      "files_to_modify": ["path/to/file.ts"],
      "passes": false
    }
  ]
}
```

### Directory Structure After /start-ralph

```
project-root/
├── prd.json              # Ralph reads this (gitignored)
├── progress.txt          # Ralph appends here (gitignored)
├── CLAUDE.md             # Project instructions (unchanged)
├── .ralph/
│   ├── INSTRUCTIONS.md   # Ralph execution rules
│   ├── LEARNINGS.md      # Ralph updates this
│   └── run.sh            # Wrapper script
└── .project-studio/
    └── features/
        └── {feature}/
            └── PRD.md    # Source PRD (committed)
```

---

## Out of Scope

- Companion app WebSocket integration (future phase)
- Parallel worker execution (future phase)
- Cost tracking (future phase)
- Interview mode during Ralph execution (future phase)

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Ralph compatibility | Vanilla ralph.sh runs on generated prd.json |
| Story sizing | All stories fit single context window |
| Wrapper script | Combines execution rules + project context |
| Archive command | Clean transition between features |
