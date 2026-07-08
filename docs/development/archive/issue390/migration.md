<!-- docs\development\issue390\migration.md -->
<!-- template=generic_doc version=43c84181 created=2026-06-11T06:17Z updated= -->
# Deliverables Migration Guide — Rename tdd_cycles to cycles

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-06-11

---

## Purpose

Provide migration instructions for legacy branches when integrating the cycles refactoring.

---

## Summary

This migration guide covers renaming the planning deliverables cycles property to remove the confusing TDD prefix.

---

## Key Changes

- Rename the 'tdd_cycles' property to 'cycles' in deliverables.json.
- All internal managers and validators expect the 'cycles' property instead of 'tdd_cycles'.

---

## Migration Steps

1. Open deliverables.json in the .phase-gate/ folder at the workspace root.
2. Locate the planning_deliverables dictionary for your active issue number.
3. Rename the 'tdd_cycles' key to 'cycles'.
4. Verify by running the local validation or quality gates tool.



## Related Documentation
- **[docs/development/issue390/design.md][related-1]**

<!-- Link definitions -->

[related-1]: docs/development/issue390/design.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-11 | Agent | Initial draft |