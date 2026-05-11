<!-- .st3\temp\issue_render.md -->
<!-- template=issue version=8dd42510 created=2026-04-24T12:32Z updated= -->
# Phase C: Retrofit GitManager with PolicyEngine integration

## Problem
GitManager heeft geen toegang tot PolicyEngine voor fase-validatie op git-operaties (commit, push, branch creation).

## Expected Behavior

PolicyEngine geïnjecteerd in GitManager zodat alle git-operaties fase-validatie ondergaan voor uitvoering.
## Actual Behavior

De architectuur is geëvolueerd naar een beter patroon. Enforcement verloopt via EnforcementRunner + YAML-gedeclareerde events in enforcement.yaml (#283). Directe PolicyEngine-injectie in GitManager is nooit de juiste aanpak geworden: git-operaties worden bewaakt via tool-dispatch enforcement events ('git_commit', 'submit_pr') die pre-rules aanroepen via server._run_tool_enforcement(). Dit is architectureel correct (Principle 13: Enforcement is Config-First) en beter dan directe manager-koppeling.
## Context

Child van epic #18. De oorspronkelijke aanpak (directe PolicyEngine-injectie in GitManager) zou de Law of Demeter en het Config-First principe schenden. Het EnforcementRunner-patroon dat via #283 is gerealiseerd is de correcte oplossing voor dezelfde doelstelling.
## Related Documentation
- **[docs/development/archive/issue283/research-ready-phase-enforcement.md][related-1]**
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-2]**
