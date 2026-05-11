<!-- .st3\temp\issue_render.md -->
<!-- template=issue version=8dd42510 created=2026-04-24T13:16Z updated= -->
# Epic: Workflow Intelligence / Agent UX

## Problem
De agent navigeert onbetrouwbaar door het workflow-model. State-tools zijn inconsistent in wat ze rapporteren over fase, cyclus en subphase. De agent moet buiten de MCP-toolset om state afleiden, wat de enforceability ondermijnt en foutgevoelig is.

## Expected Behavior

De agent heeft via MCP tools altijd een correct en consistent beeld van de huidige fase, cyclus en subphase. State tools geven getypeerde snapshots. Geen compensatielogica nodig buiten de tools.
## Actual Behavior

Meerdere openstaande bugs blokkeren betrouwbare navigatie: get_project_plan geeft geen current_phase terug (#139), get_work_context detecteert alleen de TDD-fase (#117), TDD cycle counter reset bij re-entry (#230), state.json structuur inconsistent met documentatie (#45). De agent compenseert door buiten de tools om state af te leiden.
## Context

Ontstaan uit backlog review #288 (2026-04-24). Deze bugs zijn dagelijkse pijnpunten die de agent dwingen om buiten de MCP-toolset om te navigeren. Child issues: #139, #117, #231, #230, #45, #268, #278.
## Related Documentation
- **[docs/development/issue288/backlog-inventory.md][related-1]**
