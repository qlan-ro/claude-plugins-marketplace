# Phase Gate Checklists

Use these checklists to verify readiness before advancing to the next phase.

---

# New Project Workflow Gates

## Gate 1: Discovery → AI Workflow

**Artifacts Complete:**
- [ ] Product PRD document created (`docs/PRODUCT_PRD.md`)
- [ ] Target user clearly defined
- [ ] Problem statement articulated

**Scope Defined:**
- [ ] Feature backlog created with dependency order
- [ ] Non-goals explicitly stated
- [ ] Success criteria defined

**Approval:**
- [ ] User has reviewed Product PRD
- [ ] User has explicitly approved to proceed

---

## Gate 2: AI Workflow → Architecture

**Artifacts Complete:**
- [ ] `.ai-workflow.yaml` created
- [ ] Project type classified

**Tooling Configured:**
- [ ] Required skills identified and installed
- [ ] MCP servers configured (if needed)
- [ ] Agent templates selected
- [ ] Automation workflows defined

**Approval:**
- [ ] User has reviewed AI workflow setup
- [ ] User approves tooling configuration

---

## Gate 3: Architecture → Design

**Artifacts Complete:**
- [ ] Architecture document created (`docs/ARCHITECTURE.md`)
- [ ] Technology stack documented

**Decisions Made:**
- [ ] Frontend framework selected
- [ ] Backend approach decided
- [ ] Database chosen
- [ ] Authentication method defined

**Technical Foundation:**
- [ ] Data model defined
- [ ] API approach decided
- [ ] Security considerations addressed

**Approval:**
- [ ] User has reviewed architecture
- [ ] User agrees with technology choices

---

## Gate 4: Design → Planning

**Artifacts Complete:**
- [ ] Design specification created (`docs/DESIGN.md`)
- [ ] User flows documented

**UX Coverage:**
- [ ] All major user journeys mapped
- [ ] Screen inventory complete
- [ ] Wireframes for key screens

**Design System:**
- [ ] Component library decision made
- [ ] Navigation structure defined
- [ ] Responsive strategy documented

**Approval:**
- [ ] User has reviewed design spec
- [ ] User approves UX direction

---

## Gate 5: Planning → Development

**Artifacts Complete:**
- [ ] Feature PRDs created for all features in backlog
- [ ] Each feature has `docs/features/{NN}-{name}/PRD.md`
- [ ] Each feature has `docs/features/{NN}-{name}/progress.txt`

**Story Quality (Ralph-Ready):**
- [ ] Stories use US-001 format
- [ ] Each story completable in ONE context window
- [ ] Stories ordered by dependency (schema → backend → frontend)
- [ ] All criteria are verifiable (not vague)
- [ ] Every story has "Typecheck passes" as criterion
- [ ] UI stories have "Verify changes work in browser"
- [ ] Non-goals section defines clear boundaries

**Approval:**
- [ ] User has reviewed Feature PRDs
- [ ] User approves execution order

---

## Gate 6: Development → Quality

**Code Complete:**
- [ ] All Feature PRD stories implemented
- [ ] All `progress.txt` files show completion
- [ ] Core tests passing
- [ ] No critical bugs

**Quality Baseline:**
- [ ] Code lints without errors
- [ ] Type checking passes
- [ ] Basic error handling in place

**Approval:**
- [ ] All acceptance criteria met
- [ ] Ready for quality phase

---

## Gate 7: Quality → Production

**Testing Complete:**
- [ ] Unit test coverage meets target (>80%)
- [ ] Integration tests pass
- [ ] E2E tests pass for happy paths

**Quality Verified:**
- [ ] Performance audit passed
- [ ] Security review completed
- [ ] Accessibility audit passed

**Production Ready:**
- [ ] Documentation complete
- [ ] Deployment config ready
- [ ] Environment variables documented
- [ ] Monitoring configured

**Final Approval:**
- [ ] All Product PRD success criteria verified
- [ ] User has approved final delivery
- [ ] Ready to deploy

---

## Handling Gate Failures

If a gate check fails:

1. **Identify gaps** - Which items are incomplete?
2. **Estimate effort** - How much work to complete?
3. **Communicate** - Inform user of status
4. **Iterate** - Complete missing items
5. **Re-check** - Run gate checklist again

Never skip gates to "save time" - this creates technical and product debt that compounds later.

---

# Continue Project Workflow Gates

## Gate C1: Codebase Analysis → Skill Discovery

**Artifacts Complete:**
- [ ] Codebase analysis document created (`docs/CODEBASE_ANALYSIS.md`)
- [ ] Project structure documented

**Discovery Complete:**
- [ ] Tech stack fully identified
- [ ] Data models extracted
- [ ] API surface mapped
- [ ] Existing features catalogued
- [ ] Conventions documented

**Approval:**
- [ ] User has reviewed codebase analysis
- [ ] User confirms analysis accuracy

---

## Gate C1.5: Skill Discovery → Infer Product PRD

**Analysis Complete:**
- [ ] Tech stack extracted from CODEBASE_ANALYSIS.md
- [ ] Matching skills identified from registry

**Recommendations Presented:**
- [ ] Specialized skills suggested for detected stack
- [ ] Installation instructions provided

**User Decision:**
- [ ] User installed recommended skills, OR
- [ ] User explicitly skipped skill installation

**Ready to Proceed:**
- [ ] User ready to continue with inference phases

---

## Gate C2: Infer Product PRD → Infer Architecture

**Artifacts Complete:**
- [ ] Product PRD document created (`docs/PRODUCT_PRD.md`)
- [ ] Existing features marked with status (✅/🟡/📋)

**Scope Defined:**
- [ ] New features added to backlog
- [ ] Partial features identified for completion
- [ ] Non-goals explicitly stated
- [ ] Feature backlog dependency-ordered

**Approval:**
- [ ] User has reviewed inferred PRD
- [ ] User approved feature backlog priorities
- [ ] User confirmed non-goals

---

## Gate C3: Infer Architecture → Infer Design

**Artifacts Complete:**
- [ ] Architecture document created (`docs/ARCHITECTURE.md`)
- [ ] Existing tech stack documented

**Documentation Complete:**
- [ ] Data models documented from code
- [ ] API patterns captured
- [ ] State management approach documented
- [ ] Security patterns identified
- [ ] Tech debt noted (if any)

**Approval:**
- [ ] User has reviewed architecture documentation
- [ ] User confirms technical accuracy
- [ ] User agrees with tech debt assessment

---

## Gate C4: Infer Design → AI Tooling Audit

**Artifacts Complete:**
- [ ] Design specification created (`docs/DESIGN.md`)
- [ ] Existing design system documented

**Extraction Complete:**
- [ ] Design tokens extracted (colors, spacing, typography)
- [ ] Component library documented
- [ ] Page layouts captured
- [ ] Navigation patterns documented
- [ ] Responsive behavior documented

**Approval:**
- [ ] User has reviewed design documentation
- [ ] User confirms design accuracy

---

## Gate C5: AI Tooling Audit → Planning

**Artifacts Complete:**
- [ ] `.ai-workflow.yaml` exists (created or updated)
- [ ] AI tooling audit report completed

**Audit Complete:**
- [ ] Existing configuration detected (.ai-workflow.yaml, .claude/, MCP configs)
- [ ] Tech stack analyzed from CODEBASE_ANALYSIS.md and ARCHITECTURE.md
- [ ] Gap analysis completed (missing skills, agents, MCP servers)
- [ ] New feature tooling identified (📋 items from PRD)

**Configuration Complete:**
- [ ] Required skills identified and configured
- [ ] MCP servers configured for detected databases
- [ ] Agents configured for project tech stack
- [ ] Workflows defined (on_save, on_commit)

**Approval:**
- [ ] User has reviewed AI tooling recommendations
- [ ] User approved additions/changes
- [ ] Ready to create Feature PRDs

---

## Gates 5-7: Standard Workflow

After the AI tooling audit, continue-project uses the same gates as new-project:

- **Gate 5:** Planning → Development (same as new-project)
- **Gate 6:** Development → Quality (same as new-project)
- **Gate 7:** Quality → Production (same as new-project)

See the New Project Workflow Gates section above for these checklists.
