<!-- .st3\temp\issue_render.md -->
<!-- template=issue version=8dd42510 created=2026-04-24T12:58Z updated= -->
# Automated 'Close Feature' Workflow

## Problem
Het afsluiten van een feature vereist meerdere handmatige stappen: final commit, PR aanmaken, labels zetten, issue koppelen. Zonder automatisering worden stappen overgeslagen.

## Expected Behavior

Een MCP tool of workflow die het sluiten van een feature/branch automatiseert: final commit, PR aanmaken, labels zetten, issue linken.
## Actual Behavior

Superseded door submit_pr workflow (#283). SubmitPRTool + EnforcementRunner + WorkflowGateRunner dekt de feature-close behoefte volledig: exit gates worden gecontroleerd, branch_local_artifacts worden geblokkeerd van main, en de PR wordt als atomaire operatie ingediend. Een aparte 'close feature' tool is overbodig.
## Context

Geen parent. Aangemaakt in een vroeg stadium van het project voor automatisering van de feature-close cyclus.
## Related Documentation
- **[mcp_server/tools/pr_tools.py][related-1]**
- **[docs/development/archive/issue283/design-submit-pr-prstatus-enforcement.md][related-2]**
