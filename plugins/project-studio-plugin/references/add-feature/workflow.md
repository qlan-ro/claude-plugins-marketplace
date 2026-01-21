# Add Feature Workflow

Streamlined process for adding new features to an established project.

## When to Use

Use `/project-studio:add-feature` when:
- Project has completed initial workflow (new-project or continue-project)
- Foundation docs exist (PRD, Architecture, Design)
- You want to add one or more new features
- You don't need to re-analyze the entire codebase

Use `/project-studio:continue-project` instead when:
- Foundation docs are missing
- You need to re-analyze architecture or design
- Significant time has passed and codebase has changed substantially

## Prerequisites

| Document | Required | Purpose |
|----------|----------|---------|
| docs/PRODUCT_PRD.md | Yes | Feature backlog to update |
| docs/ARCHITECTURE.md | Yes | Check if changes needed |
| docs/DESIGN.md | Yes | Check if changes needed |
| .ai-workflow.yaml | Recommended | Check if new tools needed |

## Workflow Steps

### Step 1: Validate Foundation

Check for required artifacts:

```bash
# Check foundation docs exist
ls docs/PRODUCT_PRD.md
ls docs/ARCHITECTURE.md
ls docs/DESIGN.md
ls .ai-workflow.yaml
```

**If missing:** Redirect to `/project-studio:continue-project`

**If present:** Continue to Step 2

### Step 2: Update PRD

**Agent:** product-prd-builder (append mode)

**Process:**
1. Read existing PRODUCT_PRD.md
2. Display current feature backlog with statuses
3. Add new feature(s) to backlog as 📋 (To Build)
4. Capture for each new feature:
   - User story format
   - Acceptance criteria
   - Dependencies on existing features
   - Priority in backlog

**Output:** Updated `docs/PRODUCT_PRD.md`

**Append Mode Rules:**
- DO NOT rewrite entire document
- ADD new features to existing backlog section
- PRESERVE all existing feature statuses (✅, 🟡, 📋)
- UPDATE dependencies section if new feature affects existing

### Step 3: Impact Analysis

Analyze each new feature for required changes:

#### 3a. Architecture Impact

Questions to answer:
- New data models needed?
- New API endpoints?
- New external service integrations?
- Database schema changes?
- Infrastructure changes?

**If Yes to any:** Route to architect agent (amendment mode)

**Amendment Mode Rules:**
- DO NOT redesign existing architecture
- ADD new sections for new capabilities
- UPDATE affected sections minimally
- DOCUMENT any breaking changes

#### 3b. Design Impact

Questions to answer:
- New screens or pages?
- New UI components?
- New user flows?
- Changes to design tokens (colors, typography)?
- New responsive breakpoints?

**If Yes to any:** Route to designer agent (amendment mode)

**Amendment Mode Rules:**
- DO NOT recreate design system
- ADD new components/screens as sections
- EXTEND existing patterns (don't replace)
- UPDATE token list only if theme changes

#### 3c. AI Tooling Impact

Questions to answer:
- Does feature require specific skill? (e.g., PDF export → pdf skill)
- Does feature require MCP server? (e.g., new database type)
- Would new agent help? (e.g., specialized testing)

**If Yes to any:** Route to ai-tooling-advisor agent (feature mode)

**Feature Mode Rules:**
- CHECK if new feature needs specific tools from registry
- RECOMMEND additions only (not removals)
- PRESERVE all existing configuration
- ADD with metadata: date, reason, feature name

### Step 4: Planning

**Agent:** feature-prd-builder

**Process:**
1. Read updated PRODUCT_PRD.md
2. Identify NEW features only (📋 items just added)
3. Create Feature PRD for each new feature
4. Generate US-XXX stories sized for one context window
5. Create progress.txt for tracking

**Output:** `docs/features/{NN}-{feature-name}/PRD.md`

**Important:** Only create Feature PRDs for newly added features, not existing ones.

### Step 5: Development

Execute Feature PRDs using standard Ralph loop:

1. Read Feature PRD
2. Execute stories in dependency order
3. Update progress.txt after each story
4. Commit after each completed story
5. Run type checks and tests

### Step 6: Quality

Test new features with regression:

1. Run existing test suite (ensure no regression)
2. Add unit tests for new functionality
3. Add integration tests for new flows
4. Manual verification
5. Update documentation

## Impact Analysis Decision Tree

```
New Feature: "{feature name}"
    │
    ├─ Needs new data model?
    │   ├─ Yes → architect agent (amendment)
    │   └─ No
    │
    ├─ Needs new API endpoints?
    │   ├─ Yes → architect agent (amendment)
    │   └─ No
    │
    ├─ Needs new UI screens?
    │   ├─ Yes → designer agent (amendment)
    │   └─ No
    │
    ├─ Needs new components?
    │   ├─ Yes → designer agent (amendment)
    │   └─ No
    │
    ├─ Needs specific skill?
    │   ├─ Yes → ai-tooling-advisor (feature)
    │   └─ No
    │
    └─ Continue to Planning
```

## Example: Adding Dark Mode

```
/project-studio:add-feature "Dark mode toggle with system preference detection"
```

**Step 1: Foundation Check**
```
✅ docs/PRODUCT_PRD.md
✅ docs/ARCHITECTURE.md
✅ docs/DESIGN.md
✅ .ai-workflow.yaml
```

**Step 2: Update PRD**
```markdown
## Feature Backlog (Updated)
- ✅ User authentication
- ✅ Dashboard
- 📋 Dark mode toggle (NEW)
  - As a user, I want to toggle dark mode so that I can reduce eye strain
  - Acceptance: Toggle in settings, persists across sessions, detects system preference
```

**Step 3: Impact Analysis**
```
Architecture Impact:
- New data models: No (user preference in localStorage or existing user settings)
- New API endpoints: No
Result: No architecture changes needed ✓

Design Impact:
- New screens: No
- New components: Yes (ThemeToggle, ThemeProvider)
- Design tokens: Yes (dark color palette)
Result: Design updates needed → designer agent

AI Tooling Impact:
- New skills: No
- New MCP: No
Result: No tooling changes needed ✓
```

**Designer Amendment:**
```markdown
## Dark Theme (Added 2026-01-19)

### Color Tokens - Dark
| Token | Light | Dark |
|-------|-------|------|
| --bg-primary | #FFFFFF | #1A1A2E |
| --text-primary | #1A1A2E | #EAEAEA |
...

### New Components
- ThemeToggle: Switch component with sun/moon icons
- ThemeProvider: Context wrapper for theme state
```

**Step 4: Planning**
```
Feature PRD: 05-dark-mode
Stories:
- US-041: Add dark theme color tokens to design system
- US-042: Create ThemeProvider context
- US-043: Build ThemeToggle component
- US-044: Apply theme classes to existing components
- US-045: Persist theme preference in localStorage
- US-046: Add system preference detection
```

**Steps 5-6:** Development and Quality as normal

## Common Features and Their Impacts

| Feature | Architecture | Design | AI Tools |
|---------|--------------|--------|----------|
| Dark mode | No | Yes | No |
| PDF export | No | Maybe | Yes (pdf skill) |
| Real-time notifications | Yes (WebSocket) | Yes | No |
| Payment processing | Yes (Stripe) | Yes | Maybe |
| Search functionality | Yes (API) | Yes | No |
| AI chat assistant | Yes (API) | Yes | Maybe (AI skill) |
| Multi-language (i18n) | No | Yes | No |
| File uploads | Yes (storage) | Yes | No |
| Analytics dashboard | Yes (data) | Yes | Maybe (data-viz) |

## Completion Checklist

- [ ] PRD updated with new feature(s)
- [ ] Impact analysis completed
- [ ] Architecture amended (if needed)
- [ ] Design amended (if needed)
- [ ] AI tooling updated (if needed)
- [ ] Feature PRD created
- [ ] Stories sized for one context window
- [ ] Development complete
- [ ] Tests passing (new + regression)
- [ ] Documentation updated
