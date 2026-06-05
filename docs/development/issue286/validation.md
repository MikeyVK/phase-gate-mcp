<!-- docs\development\issue286\validation.md -->
<!-- template=validation_report version=fe38a66d created=2026-06-05T10:30Z updated= -->
# Issue #286 Validation Report


**Status:** IN PROGRESS  
**Version:** 1.0  
**Last Updated:** 2026-06-05  
**Issue:** #286  
**Cycle:** C_286.1–C_286.5 (live scaffold validation)  
**Phase:** validation  

---

## Scope

Branch-wide validation of issue #286 bug-fix cycles: documentation cluster revision, MethodSpec + GenericContext fix, adapter/resource/interface pipeline, validation_report pipeline, generic_doc Layer 1/2 completion. Includes live scaffold testing of all new and repaired template types.

---

## Outcome

Current validation status: **IN PROGRESS**.

---

## Live Scaffold Observations (2026-06-05)

All issue #286 template types scaffolded via `scaffold_artifact` using `scaffold_schema`-driven context discovery. Results:

| Template | Scaffold result | Notes |
|---|---|---|
| `adapter` | ✅ Pass | `@target_interface`, logging, lege import-blokken correct |
| `interface` | ✅ Pass | `Protocol` base, `...` body correct |
| `resource` | ✅ Pass | `@resource_type`, logging correct |
| `validation_report` | ✅ Pass | Schema-validatie enforced `title` as required — correct gate behaviour |
| `generic` | ✅ Pass | `@responsibilities`, `@dependencies`, `@layer` annotaties correct |
| `generic_doc` | ✅ Pass (structurally) | **See Finding F-1 below** |

### Finding F-1: `generic_doc` renders literal `None` for omitted optional fields

**Observed:** scaffolding `generic_doc` without supplying `status` or `version` produces:

```
**Status:** None
**Version:** None
```

**Root cause confirmed:** Jinja2 `| default()` fires only on `undefined`, not on `None`. `GenericDocContext` correctly declares `status: str | None = None`, so Pydantic passes `None` explicitly — which bypasses `| default("DRAFT")`.

**Same defect confirmed in `validation_report`:** `status: str | None = None` with `| default("PENDING")` in the template.

**Contrast:** `research`, `planning`, `architecture` do not declare `status` in their Layer 1 schema, so Jinja2 receives `undefined` and `| default()` fires correctly. This is accidental correctness, not design.

**Fix:** Layer 3 must use `status or "DRAFT"` (falsy check) instead of `status | default("DRAFT")` for any field declared `str | None` in Layer 1. Documented as Finding 8 in `docs/development/issue286/research.md`. Fix cycle added as C_286.6 in `docs/development/issue286/planning.md`.

**Scope impact:** C_286.6 added to branch scope — targeted two-template fix plus Layer 3 rendering contract documentation update.

---

## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-05 | Agent | Initial draft |