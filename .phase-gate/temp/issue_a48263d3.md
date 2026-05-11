<!-- .st3\temp\issue_render.md -->
<!-- template=issue version=8dd42510 created=2026-04-24T12:58Z updated= -->
# Phase D: Path-based file creation enforcement (FileOperationPolicy)

## Problem
Fase D vereist een expliciete FileOperationPolicy met padgebaseerde access control. Zonder dit kunnen tools bestanden buiten de toegestane directories aanmaken of muteren.

## Expected Behavior

mcp_server/core/file_policy.py met FileOperationPolicy-klasse die padgebaseerde access control afdwingt bij file-creatie en -mutatie.
## Actual Behavior

file_policy.py bestaat niet. De feitelijke padgebaseerde enforcement verloopt via EnforcementRunner + enforcement.yaml (per #283). Padrestricties zijn onderdeel van de YAML-configuratie en worden via tool-dispatch pre-rules gehandhaafd. Het originele design (aparte FileOperationPolicy-klasse) is achterhaald door het Config-First principe (ARCHITECTURE_PRINCIPLES.md §13).
## Context

Child van #18 (Epic: Enforce TDD & Coverage via Hard Tooling). Onderdeel van de oorspronkelijke stapsgewijze fasering van #18.
## Related Documentation
- **[mcp_server/core/error_handling.py][related-1]**
- **[.st3/config/enforcement.yaml][related-2]**
