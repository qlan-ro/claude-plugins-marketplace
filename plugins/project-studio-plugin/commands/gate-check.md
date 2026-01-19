---
name: gate-check
description: Run phase gate checklist to verify readiness before advancing to the next phase
---

# Phase Gate Check

Verify readiness to advance to the next phase by checking required artifacts and criteria.

## Arguments

$ARGUMENTS

If a phase is specified (e.g., `/gate-check discovery`), check that specific gate.
If no argument, detect current phase and check the appropriate gate.

## Gate Checklists

### Gate 1: Discovery → AI Workflow

**Artifacts:**
- [ ] `docs/PRODUCT_PRD.md` exists
- [ ] Target user clearly defined in PRD
- [ ] Problem statement articulated

**Scope:**
- [ ] Feature backlog created with dependency order
- [ ] Non-goals explicitly stated
- [ ] Success criteria defined

**Approval:**
- [ ] User has reviewed Product PRD

---

### Gate 2: AI Workflow → Architecture

**Artifacts:**
- [ ] `.ai-workflow.yaml` exists
- [ ] Project type classified

**Configuration:**
- [ ] Required skills identified
- [ ] MCP servers configured (if needed)

**Approval:**
- [ ] User has reviewed AI workflow setup

---

### Gate 3: Architecture → Design

**Artifacts:**
- [ ] `docs/ARCHITECTURE.md` exists

**Decisions:**
- [ ] Frontend framework selected
- [ ] Backend approach decided
- [ ] Database chosen
- [ ] Authentication method defined

**Technical Foundation:**
- [ ] Data model defined
- [ ] API approach decided
- [ ] Security considerations addressed

**Approval:**
- [ ] User agrees with technology choices

---

### Gate 4: Design → Planning

**Artifacts:**
- [ ] `docs/DESIGN.md` exists
- [ ] User flows documented

**UX Coverage:**
- [ ] Major user journeys mapped
- [ ] Screen inventory complete
- [ ] Component library defined

**Design System:**
- [ ] Design tokens specified
- [ ] Navigation structure defined
- [ ] Responsive strategy documented

**Approval:**
- [ ] User approves UX direction

---

### Gate 5: Planning → Development

**Artifacts:**
- [ ] Feature PRDs created for all backlog items
- [ ] Each feature has `docs/features/{NN}-{name}/PRD.md`
- [ ] Each feature has `docs/features/{NN}-{name}/progress.txt`

**Story Quality (Ralph-Ready):**
- [ ] Stories use US-XXX format
- [ ] Each story fits in ONE context window
- [ ] Stories ordered by dependency
- [ ] All criteria are verifiable
- [ ] Every story has "Typecheck passes"
- [ ] UI stories have "Verify in browser"

**Approval:**
- [ ] User has reviewed Feature PRDs
- [ ] User approves execution order

---

### Gate 6: Development → Quality

**Code Complete:**
- [ ] All Feature PRD stories implemented
- [ ] All `progress.txt` files show completion
- [ ] Core tests passing
- [ ] No critical bugs

**Quality Baseline:**
- [ ] Code lints without errors
- [ ] Type checking passes
- [ ] Basic error handling in place

---

### Gate 7: Quality → Production

**Testing:**
- [ ] Unit test coverage meets target
- [ ] Integration tests pass
- [ ] E2E tests pass for happy paths

**Quality:**
- [ ] Performance audit passed
- [ ] Security review completed
- [ ] Accessibility audit passed

**Production Ready:**
- [ ] Documentation complete
- [ ] Deployment config ready
- [ ] Environment variables documented

---

## Continue Project Gates

### Gate C1: Codebase Analysis → Infer PRD

**Artifacts:**
- [ ] `docs/CODEBASE_ANALYSIS.md` exists

**Discovery:**
- [ ] Tech stack fully identified
- [ ] Data models extracted
- [ ] API surface mapped
- [ ] Existing features catalogued
- [ ] Conventions documented

**Approval:**
- [ ] User confirms analysis accuracy

---

### Gate C2: Infer PRD → Infer Architecture

**Artifacts:**
- [ ] `docs/PRODUCT_PRD.md` exists
- [ ] Features marked with status (✅/🟡/📋)

**Scope:**
- [ ] New features added to backlog
- [ ] Partial features identified
- [ ] Non-goals stated

**Approval:**
- [ ] User approved feature priorities

---

### Gate C3: Infer Architecture → Infer Design

**Artifacts:**
- [ ] `docs/ARCHITECTURE.md` exists

**Documentation:**
- [ ] Existing tech stack documented
- [ ] Data models documented
- [ ] API patterns captured
- [ ] Tech debt noted

**Approval:**
- [ ] User confirms accuracy

---

### Gate C4: Infer Design → AI Tooling Audit

**Artifacts:**
- [ ] `docs/DESIGN.md` exists

**Extraction:**
- [ ] Design tokens extracted
- [ ] Components documented
- [ ] Layouts captured

**Approval:**
- [ ] User confirms accuracy

---

### Gate C5: AI Tooling Audit → Planning

**Artifacts:**
- [ ] `.ai-workflow.yaml` exists (created or updated)

**Audit Complete:**
- [ ] Existing config detected and analyzed
- [ ] Tech stack tools matched from registry
- [ ] Gap analysis completed
- [ ] New feature tooling identified

**Configuration:**
- [ ] Required skills configured
- [ ] MCP servers configured (if database detected)
- [ ] Agents configured for tech stack

**Approval:**
- [ ] User has reviewed tooling recommendations
- [ ] User approved configuration changes
- [ ] Ready for Feature PRDs

---

## Output Format

```markdown
## Gate Check: {Phase} → {Next Phase}

### Status: {PASS / FAIL / PARTIAL}

### Checklist Results

**Artifacts:** {X/Y passed}
- ✅ docs/PRODUCT_PRD.md exists
- ❌ Non-goals not explicitly stated

**Quality:** {X/Y passed}
- ✅ Feature backlog dependency-ordered
- ⚠️ 2 success criteria are vague

### Issues Found
1. {Issue description} - {Recommendation}
2. {Issue description} - {Recommendation}

### Recommendation
{PASS: Ready to advance to {next phase}}
{FAIL: Complete the following before advancing: ...}
```

Run the appropriate gate check based on detected or specified phase.
