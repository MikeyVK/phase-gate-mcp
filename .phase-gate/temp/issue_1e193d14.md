<!-- .st3\temp\issue_render.md -->
<!-- template=issue version=8dd42510 created=2026-04-24T12:32Z updated= -->
# Research: Git as SSOT for phase tracking vs local state.json

## Problem
Onduidelijkheid over of git de SSOT moet zijn voor fase-tracking versus lokale state.json, en hoe state te synchroniseren over meerdere machines.

## Expected Behavior

Research document dat huidige fase-tracking mechanismen documenteert, alle opties evalueert voor git-gebaseerde fase-tracking, afwegingen identificeert, en een aanpak aanbeveelt.
## Actual Behavior

Volledig beantwoord. Beslissing: state.json blijft git-tracked (multi-machine continuïteit), maar bereikt nooit main via MCP-native enforcement. Rationale:
1. Git-tracking van state.json is vereist voor multi-machine workflow (machine A commit → machine B haalt op)
2. Alternatief A (gitignore) is bewust afgewezen: PR #284 gesloten zonder merge
3. Correcte oplossing: branch_local_artifacts in phase_contracts.yaml + submit_pr pre-enforcement in EnforcementRunner (#283)
4. SSOT voor de lijst van branch-local artifacts: phase_contracts.yaml → merge_policy → branch_local_artifacts
Volledige redenatie gedocumenteerd in docs/development/archive/issue283/research-ready-phase-enforcement.md.
## Context

Child van epic #18 (parent:issue-18). Getriggerd tijdens issue #42 werk. De onderzoeksvraag is volledig beantwoord als onderdeel van issue #283.
## Related Documentation
- **[docs/development/archive/issue283/research-ready-phase-enforcement.md][related-1]**
