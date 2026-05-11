<!-- .st3\temp\issue_render.md -->
<!-- template=issue version=8dd42510 created=2026-04-24T12:58Z updated= -->
# Inventory of Test Coverage & TDD Compliance

## Problem
Er is geen overzicht van de actuele test coverage en TDD compliance over de codebase. Zonder dit is het onduidelijk welke modules prioriteit hebben voor extra tests.

## Expected Behavior

Gestructureerde inventaris van test coverage per module + TDD compliance rapport. Inzicht in welke modules onvoldoende getest zijn.
## Actual Behavior

Inventaris gedaan en continu bijgehouden via quality gates: pytest --cov, Gate 6 (≥90% branch coverage). Coverage tracking is geborgd in tooling (phase_contracts.yaml exit_requires, run_quality_gates tool), niet in een apart statisch document. Het issue is inhoudelijk afgerond; de doelstelling (zichtbaarheid en handhaving van coverage) is structureel geïmplementeerd.
## Context

Geen parent. Coverage target is geformaliseerd als Gate 6 in phase_contracts.yaml. Tracking loopt nu via run_quality_gates.
## Related Documentation
- **[.st3/config/phase_contracts.yaml][related-1]**
- **[pyproject.toml][related-2]**
