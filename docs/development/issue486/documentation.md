<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=xoYbNuJbkallN_DM sf=5--KpGf2wHUv2qAj -->

# ASCII Python identifier contract — Documentation (#486)

**Status:** DOCUMENTATION COMPLETE — independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-05

## Purpose

Index the current consumer guidance and preserved documentation boundaries for the approved #486 cutover.

## Scope In

Current scaffolding tool reference, issue486 phase evidence and documentation inventory.

## Scope Out

Historical workflow rewrites, copied package inventory, runtime/generic schema policy, generated release assets and unrelated warning/xpass cleanup.

## Prerequisites

- Independent Validation GO on 2dc1c1ac from Beoordeel designplan; no P1/P2 blockers.

## Summary

The public scaffolding reference describes the ASCII-only structured identifier boundary and explicit caller migration. It retains Unicode content and existing schema discovery/native output responsibilities. Phase reports preserve exact observed evidence and independent QA authority.

## Key Changes

- Added Python structured identifier contract to docs/reference/tools/scaffolding.md: ASCII names/imports/decorators/factories, existing guards, Unicode content and explicit clean-break migration.
- Kept catalog/schema ownership and native syntax responsibility in current discovery guidance; no static package-ID or field inventory promoted to authority.

## Migration Steps

1. Rediscover the selected package schema after the installed suite is refreshed through the supported server restart.
2. If a caller context uses a non-ASCII structured name, choose an explicit ASCII name. No fallback, normalization, transliteration, compatibility profile or automatic rewrite is supplied.
3. Retain Unicode caller content where the schema admits it; still inspect generated artifacts and run required native checks for raw code/dependencies.

## Documentation inventory

| Surface | Disposition | Reason |
| --- | --- | --- |
| docs/reference/tools/scaffolding.md | Updated | Owns current input contract, migration and generated-output responsibilities. |
| docs/reference/TEMPLATE_LIBRARY_USAGE.md | Reviewed, unchanged | Links the public scaffold reference; deliberate schema-driven discovery, no duplicated ID/field policy. |
| docs/development/schema-template-maintenance.md | Reviewed, unchanged | Already explains package/shared ownership and immutable startup refresh; no contradictory identifier claim. |
| docs/reference/tools/README.md and README.md | Reviewed, unchanged | Existing navigation/schema-guided overview remains correct. |
| docs/coding_standards/CODE_STYLE.md | Reviewed, unchanged | General code/output responsibilities remain correct; selected schema owns exact admission. |
| docs/development/issue486/{research,design,planning,validation}.md | Retained | Approved strategy/design/plan and exact native evidence remain authoritative phase inputs. |
| Other historical issue documents | Unchanged | Historical facts are not rewritten into the new contract. |
| Generated packaged suite assets | Not built or edited | Existing release assembly owns distribution; source suite is the implementation surface. |

## Evidence and review boundary

[Validation](validation.md) maps structural deliverables, cleanup, invariants, package-generation measurements and representative live scaffolds. The producer full configured suite completed with 2807 passed, 1 skipped, 1 xpassed and 229 warnings, native exit 0. Fresh targeted Python gates remain reusable while sources are unchanged; documentation changes do not invalidate that behavior evidence.

Independent Validation QA rerun `5dda614caf124fb8bb007c851cf22e31` confirmed the same counts in 489.41s, exit 0, without truncation, rejection or termination problems. QA branch-link receipt `5d459af0ee534266b0f0c3fd7ef7a0c0` passed with 26 successes, 3 exclusions and 0 errors. QA explicitly accepted the existing manual skip, non-strict C8 XPASS and warnings as non-blocking for #486, preserving their separate counts. Exact live measurements remain producer-evidence; QA independently proved the public bound below 25000 codepoints per package. This disposition does not authorize publication.

Documentation-only checks: both the reference safe edit and report scaffold passed their native Markdown preflight; `run_checks(scope='targets', targets=[scaffolding.md, documentation.md], profile='markdown_link_review', timeout_seconds=300)` passed in receipt `64cd1563e4cc4e988f3c08153db8551a`. No implementation or test source changed in this phase.

## Open publication work

Automatic approval review denied outbound push to GitHub repository MikeyVK/phase-gate-mcp because trusted human destination evidence was missing. Explicit human authorization is pending; no push/PR is claimed and no cross-chat, CLI or UI workaround is authorized. At Ready the producer will send the requested handover to Coordinatie with this blocker explicit. Publication and the normal PR/merge gate remain dependent on the pending human destination authorization.

## Related Documents

- [Current scaffolding contract](<../../reference/tools/scaffolding.md#python-structured-identifier-contract>)
- [Validation evidence](<validation.md>)
- [Planning](<planning.md>)
- [Design](<design.md>)
- [Approved strategy](<research.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-05 | @imp documenter | Document current ASCII contract, preservation, migration and review evidence. |
