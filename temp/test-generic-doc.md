<!-- temp\test-generic-doc.md -->
<!-- template=generic_doc version=43c84181 created=2026-06-05T14:35Z updated= -->
# Migration Guide: SimpleTrader v2 to v3

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-06-05

---

## Purpose

Guide users through the migration from SimpleTrader v2 to v3.

## Scope

**In Scope:**
API changes, configuration migration, and breaking changes.

**Out of Scope:**
Internal architecture details not relevant to end users.

---

## Summary

Summarizes the key changes and migration steps required to upgrade to v3.

---

## Key Changes

- Config format changed from YAML to TOML
- New required field: workflow_name in project config
- Removed deprecated V1 pipeline flag

---

## Migration Steps

1. 1. Back up your .phase-gate/ directory
2. 2. Run migration script: python scripts/migrate_v2_to_v3.py
3. 3. Update your config files per the new schema
4. 4. Validate with: phase-gate health-check

---

## Validation Checklist

- [ ] All tests pass after migration
- [ ] Config files load without errors
- [ ] Artifact scaffolding produces expected output


## Related Documentation
- **[docs/reference/mcp/tools/README.md][related-1]**
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-2]**

<!-- Link definitions -->

[related-1]: docs/reference/mcp/tools/README.md
[related-2]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-05 | Agent | Initial draft |