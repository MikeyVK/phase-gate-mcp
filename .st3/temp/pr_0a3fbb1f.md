<!-- .st3\temp\pr_render.md -->
<!-- template=pr version=93bb9b4e created=2026-04-07T11:05Z updated= -->
# refactor(#270): remove dead config fields from workphases.yaml and policies.yaml

Removes dead YAML fields that were never read after the #257 migration. No behaviour change. Follow-up issues #273 (commit_prefix_map DRY) and #274 (terminal-phase exit gates) created.
## Changes
Remove exit_requires/entry_expects from all phase definitions in workphases.yaml. Remove allowed_prefixes from all operation rules in policies.yaml. Fix test_operation_policies.py: remove assertions on removed fields, fix test_validate_commit_message_required.

## Testing
2659 tests passing, all quality gates green (ruff format/lint, imports, line length, mypy, pyright).
## Checklist

- [ ] Code follows project standards
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Quality gates passing
## Related Documentation
- **[docs/development/issue270/SESSIE_OVERDRACHT_270.md][related-1]**
- **[docs/development/issue270/validation-report.md][related-2]**

---

Closes: #270