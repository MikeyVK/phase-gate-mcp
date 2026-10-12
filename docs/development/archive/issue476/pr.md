<!-- pgmcp:v1 id=pr pv=1.0.0 pf=hG0a9tLUxIzayxH4 sf=5--KpGf2wHUv2qAj -->

## Summary

Schema admission rejects undeclared Jinja reads but does not prove that every schema declaration influences output. A bounded source audit found no demonstrated silently ignored field in the delivered suite. This change establishes a source-bound template development and release review procedure, integrated into the existing documentation and its declared delivery route.

## Changes

- Record the historical analysis, contextual audit of all 19 delivered packages (195 root-property occurrences and relevant nested/shared consumers), approved boundaries and targeted whole-documentation research in `docs/development/issue476/research.md`.
- Integrate five substantive steps into the existing maintenance guide: contract/impact, effective consumption review, actual behavior evidence, independent review and a durable source-bound release decision. Limit the claim to reviewed sources and evidence.
- Connect ordinary template usage to that single authority without duplicating instructions in agent files or phase contracts.
- Add precisely the maintenance guide to the release manifest using the existing single-file copy mechanism, and synchronize the release-assets procedure. Preserve its current relative documentation path.
- No engine, template, schema, test or general agent-instruction behavior changes.

## Testing

- `safe_edit_file(path="docs/development/issue476/research.md", validation="enforce")`: reported written=True, validation=passed. `run_checks(scope="targets", targets=["docs/development/issue476/research.md"], checks=["markdown_links"], timeout_seconds=120)`: passed with configured arguments.
- `safe_edit_file(..., validation="enforce")` for the maintenance guide, Template Library Usage and release-assets procedure: each reported written=True, validation=passed.
- `run_checks(scope="targets", targets=["docs/development/schema-template-maintenance.md", "docs/reference/TEMPLATE_LIBRARY_USAGE.md", "docs/reference/release-assets-procedure.md"], checks=["markdown_links"], timeout_seconds=120)`: passed with configured arguments; fresh evidence reused in Ready.
- The manifest's enforce-mode edit was not written because no validation profile was selected. The supported report-mode write succeeded with validation=not_executed. This is not a YAML-check pass. Its exact source/target mapping, source-file existence and existing single-file build/copy mechanism were inspected by producer and independent QA.
- Independent QA in `Beoordeel designplan`: Research review on `03a64ab5047d2289cab218ac1ad34e48f1f2dc9f`; GO for the documented Research → Documentation exception on `0eff4603424907225231be1f0c1bf50937cb937f`; no P1/P2 findings and GO Documentation → Ready on `37982eeab5064385feabdf48c0dd35c24485c4a6`. The last review assessed the complete instruction route, substantive procedure, bounded claim and declared delivery.
- Human explicitly approved Research → Documentation → Ready; separate Design, Planning, Implementation and runtime Validation were skipped through the audited force transition. The plan's phase display is not evidence those skipped phases were performed. Native Documentation → Ready passed with no required gates.
- No tests, renders, builds, installations or upgrades were run for this documentary closeout. Existing tests inspected in Research are source evidence, not execution results.

Residual limits: the documentation and declared delivery route were reviewed, not an assembled wheel or updated installation. Template renewal does not refresh all installed documentation. This PR does not certify every valid input combination or the behavior of all packages. The issue closes under the human-approved research and release-assurance strategy; no generic reverse-consumption analyzer or runtime rejection gate was selected.

Tracking: Ready reached through the explicit exception. Merge and issue closeout are handed to Coordination using end-issue after PR submission.

## Breaking Changes

None. Public schema, rendering, startup, renewal and scaffold behavior remain unchanged.

## Deferred Work

No deferred work identified.

## Closes

Closes #476

## Related Documents

- [Research, audit and approved strategy][related-1]
- [Authoritative development and release procedure][related-2]
- [Template Library Usage][related-3]
- [Release asset procedure][related-4]

[related-1]: <https://github.com/MikeyVK/phase-gate-mcp/blob/refactor/476-schema-template-consumption/docs/development/issue476/research.md>
[related-2]: <https://github.com/MikeyVK/phase-gate-mcp/blob/refactor/476-schema-template-consumption/docs/development/schema-template-maintenance.md#develop-and-release-a-package>
[related-3]: <https://github.com/MikeyVK/phase-gate-mcp/blob/refactor/476-schema-template-consumption/docs/reference/TEMPLATE_LIBRARY_USAGE.md>
[related-4]: <https://github.com/MikeyVK/phase-gate-mcp/blob/refactor/476-schema-template-consumption/docs/reference/release-assets-procedure.md>
