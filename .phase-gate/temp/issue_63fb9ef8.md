<!-- .st3\temp\issue_render.md -->
<!-- template=issue version=8dd42510 created=2026-04-24T12:32Z updated= -->
# Phase workflow contradicts TDD principles: component→tdd sequence

## Problem
De volgorde component → tdd in de feature-workflow impliceert dat implementatie vóór tests komt. Dit contradiceert TDD-principes en stimuleert test-after development.

## Expected Behavior

Fasenamen die de werkelijke TDD-workflow weerspiegelen. Tooling voorkomt test-after patroon. Coverage/verificatiefase heeft duidelijke afrondingscriteria.
## Actual Behavior

Opgelost via #257. De fasenamen zijn hernoemd in workphases.yaml:
- 'component' hernoemd naar 'implementation' (TDD-cycli: red → green → refactor ingebouwd)
- 'tdd' hernoemd naar 'validation' (verificatie van coverage, ontbrekende edge cases)
De workflows.yaml bevestigt de correcte volgorde: research → design → planning → implementation → validation → documentation. Geen backward-compat laag, directe flag-day wijziging.
## Context

Child van epic #18. Was geblokkeerd door Epic #49 (MCP Platform Configurability - workflows.yaml). De blokkade is opgeheven via issue #257 dat workflows.yaml heeft gemigreerd naar de Config-First architectuur.
## Related Documentation
- **[docs/development/archive/issue257/TIJDLIJN_ISSUE257.md][related-1]**
