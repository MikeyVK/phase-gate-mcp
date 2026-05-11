<!-- .st3\temp\issue_render.md -->
<!-- template=issue version=8dd42510 created=2026-04-24T12:34Z updated= -->
# Enforce terminal-phase exit gates via create_pr hook

## Problem
De documentatiefase is de terminale fase in alle workflows. WorkflowGateRunner.enforce() wordt alleen getriggerd door TransitionPhaseTool, dat nooit wordt aangeroepen voor de terminale fase omdat er geen uitgaande overgang is. Alle exit_requires gates voor de documentatiefase worden systematisch overgeslagen.

## Expected Behavior

Wanneer create_pr wordt aangeroepen voor een branch in de terminale fase, worden de exit gates uit phase_contracts.yaml afgedwongen. Niet-voldane gates blokkeren create_pr met een duidelijke gate violation melding.
## Actual Behavior

Opgelost via #283. CreatePRTool is volledig verwijderd. Enforcement van terminal-fase exit gates verloopt via:
1. SubmitPRTool (mcp_server/tools/pr_tools.py) met enforcement_event='submit_pr'
2. submit_pr pre-enforcement regel in enforcement.yaml via EnforcementRunner
3. branch_local_artifacts in phase_contracts.yaml bewaakt dat state.json/deliverables.json nooit main bereiken
WorkflowGateRunner.enforce() controleert exit_requires van de documentatiefase bij submit_pr aanroep. Dit is architectureel correcter dan een create_pr hook: enforcement punt is SSOT, niet gesplitst over create en submit.
## Context

Child van #257 (gesloten). Parent issue #257 is gesloten op 2026-04-06. Issue #274 is als follow-up aangemaakt op 2026-04-07 en opgelost als onderdeel van #283 (ready-phase enforcement).
## Related Documentation
- **[docs/development/archive/issue283/research-ready-phase-enforcement.md][related-1]**
- **[docs/development/archive/issue283/design-ready-phase-enforcement.md][related-2]**
