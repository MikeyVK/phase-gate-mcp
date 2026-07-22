<!-- CHANGELOG.md -->
<!-- template=generic_doc version=43c84181 created=2026-07-22T17:47Z updated= -->
# Changelog

**Status:** DEFINITIVE  
**Version:** 2.0.0  
**Last Updated:** 2026-07-22

---

## Purpose

Document all notable changes to Phase-Gate MCP Server

---

## Summary

v2.0.0 release notes and feature changelog

---

## Key Changes

- Workspace Upgrade Service (pgmcp --upgrade): Automated workspace upgrade mechanism orchestrating fail-safe timestamped backups (.pgmcp_backup_YYYYMMDD_HHMMSS/), smart asset renewal, and structured audit logs (.pgmcp/logs/upgrade_YYYYMMDD_HHMMSS.json).
- Workspace Version Validation Manager (WorkspaceVersionValidator): Decoupled manager enforcing .version existence and runtime version matching with explicit CLI remediation advice (pgmcp --upgrade / pgmcp --init).
- Upgrade Log DTO (UpgradeLogDTO): Immutable frozen Pydantic model (extra="forbid") recording upgrade execution telemetry.
- Frictionless safe_edit_file Tool: 4-operation model (replace, append, rewrite, pattern_replace) with strict must_exist=True governance and fuzzy-match difflib error diagnostics.
- Version SSOT Bump: Package version synchronized to 2.0.0 across pyproject.toml, .pgmcp/config/release_manifest.yaml, and mcp_server/config/settings.py.




## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 2.0.0 | 2026-07-22 | Agent | Initial draft |