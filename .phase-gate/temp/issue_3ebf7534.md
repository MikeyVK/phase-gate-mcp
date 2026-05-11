<!-- .st3\temp\issue_render.md -->
<!-- template=issue version=8dd42510 created=2026-04-24T10:27Z updated= -->
# Phase B: Implement TransitionPhaseTool for agent phase control

## Problem
Agenten hebben geen MCP tool om faseovergangen te initiëren met validatie tegen het project plan.

## Expected Behavior

TransitionPhaseTool in mcp_server/tools/phase_tools.py met invoervalidatie, integratie met PhaseStateEngine, en registratie in server.py.
## Actual Behavior

Geïmplementeerd. TransitionPhaseTool bestaat als mcp_server/tools/phase_tools.py en is geregistreerd in mcp_server/server.py. Integreert met PhaseStateEngine voor validatie en uitvoering van faseovergangen. WorkflowGateRunner controleert exit_requires per fase via phase_contracts.yaml.
## Context

Child van epic #18. Afhankelijkheid van #31 (PhaseStateEngine). Gerelateerd aan #41 (phase-entry guidance) dat nog open staat — de Focus/Avoid/Criteria guidance tekst is nog niet in de tool-output geïmplementeerd.
## Related Documentation
- **[docs/development/archive/issue257/design_threshold_b_minimal_refactor.md][related-1]**
