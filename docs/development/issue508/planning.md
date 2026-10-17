<!-- pgmcp:v1 id=planning pv=1.0.0 pf=OSfLTQ1qMuWvM9fi sf=WI5iXHBKVOU91bYE -->

# Issue 508 — Agent-guided workspace setup and upgrade

**Status:** Proposed — independent Planning review requested  
**Version:** 0.1  
**Last Updated:** 2026-10-17

## Purpose

Make the existing cooperative agent route actionable and discoverable without inventing setup behavior or duplicating an onboarding engine.

## Scope In

One authoritative checklist at docs/setup/agentic-bootstrap.md, with fresh-install and targeted upgrade modes, owner choices, safe invocation/handover, capability-specific verification and explicit status reporting. Reconcile README.md, docs/setup/README.md and docs/setup/workspace-upgrade.md as referring consumers. Record bounded fresh/upgrade walkthrough evidence.

## Scope Out

No production/test/config changes, new CLI/runtime setup engine, startup gate, diagnostic tool, automatic configuration/Git/remote mutations, literal-prose tests, broad suite run or release publication. No changes to host instruction bodies unless an affected source consumer is demonstrated.

## Prerequisites

- Issue #508 and initialized docs workflow, parent main; no Research/Design or implementation cycles are introduced.
- Documentation Standard checked: phase ownership, source/consumer authority, concise tables, metadata and durable invocation/outcome evidence.
- Use current checked-out source for behavior; existing 3.0.0 release artifacts retain their version-specific contents. No publication or wheel rebuild is implied.

## Summary

Replace unsafe automation in the existing agentic bootstrap page with the single authoritative checklist; preserve the existing CLI/config/renewal owners. The manual setup guide retains technical host/quality details, the upgrade guide retains checkpoint/recovery details, and both refer to the checklist rather than duplicating completion policy.

| Authority / evidence | Documentation outcome and consumers |
| --- | --- |
| [CLI](../../../mcp_server/cli.py), [renewal CLI](../../../mcp_server/cli_renewal.py), [upgrade guide](../../setup/workspace-upgrade.md) | Separate installation, --init for an absent server root, template-only --upgrade, owner config reconciliation, restart/reconnect and real issue registration. Preserve existing config/customizations and external roots. |
| [Settings](../../../mcp_server/config/settings.py), [bootstrap](../../../mcp_server/bootstrap.py), [composition contract](../../reference/config-loading-architecture.md) | Verify selected interpreter/package and absolute effective workspace/server/config/template roots. Base/default declarations and owner overrides remain independent of launcher/token configuration. Health does not prove selected-capability completeness or operations. |
| [Quality setup](../../setup/README.md#choose-the-workspace-quality-policy), [GitHub setup](../../manuals/github-setup.md), [quality tools](../../reference/tools/quality.md) | Require deliberate binding/native policy choices only for intended capabilities; distinguish applicable refusal from optional N/A. GitHub identity/token are required for chosen GitHub paths, with enforcement implications visible; secrets never tracked. |
| [Packaged host sources](../../agents/codex/AGENTS.md), [release manifest](../../../.pgmcp/config/release_manifest.yaml) | Deploy/reconcile only selected host instructions with owner changes preserved; docs/setup is already distributed. Plain-language invocation works in a chosen host; installation does not start an agent. No manifest/build change. |

Current unsafe examples are observed in agentic-bootstrap.md: automatic git init/main commit/push, wholesale settings replacement, fabricated issue 1 and an unconditional claim of automatic server activation. These are documentation defects, not new runtime requirements.

## Dependencies

- Use authoritative CLI/settings/config/bootstrap contracts before rewriting the checklist.
- Update central checklist before referring README/setup/upgrade consumers.
- Finish walkthrough/link/parity evidence before independent Documentation → Ready review.

## Risks

### A current source contract can be mistaken for the contents of a previously published wheel.

Tie package instructions to the selected artifact/version; link unreleased configuration/state deltas without claiming an automatic migration or new release.

### Optional GitHub/quality configuration or workspace enforcement can block a selected representative operation despite healthy startup.

Record capability applicability and actual outcome; preserve diagnostics, request owner decisions and never bypass enforcement during setup.

## Work Units

### DOC\_508 — Authoritative checklist and bounded consumers

**Goal:** Deliver a source-backed agent checklist that reports selected-capability readiness honestly and preserves owner-controlled workspaces.

**Owner:** @imp documenter

#### Scope In

Four active Markdown documents plus planning/documentation evidence and normal workflow state.

#### Scope Out

No new setup workflow/skill or duplicate checklist across host instructions; no assertion that an optional capability works merely because it is listed or server health is healthy.

#### Deliverables

##### DOC508.1

Replace docs/setup/agentic-bootstrap.md in place with invocation, fresh versus upgrade/delta paths, owner decision matrix, health/config/operation distinctions and done/open/blocked/N/A handover.

##### DOC508.2

Reconcile README.md, docs/setup/README.md and docs/setup/workspace-upgrade.md navigation and conflicting universal prerequisites/automatic claims; retain their specialist technical authority.

##### DOC508.3

Compact docs/development/issue508/documentation.md evidence: fresh and upgrade read-throughs, exact bounded CLI contract run, link outcomes, reviewed unchanged surfaces and limitations.

#### Exit Criteria

Every #508 expectation maps to the central checklist or an authoritative linked specialist source; no unsafe automatic main/repository/issue setup remains in active instructions. Fresh and upgrade walkthroughs preserve owner decisions and distinguish health/config completeness/representative operation evidence. All changed Markdown links pass; no code/config/test content changes.

#### Verification

##### Fresh and existing workspace routes are executable and bounded by current behavior.

**Method:** Walk through both document routes with explicit inputs/actions/status/limitations. Run only existing CLI contract tests in tests/mcp_server/unit/test_cli.py and tests/mcp_server/integration/test_renewal_cli.py, with -k selecting test_cli_init_result, test_cli_init_already_exists, test_fresh_install_then_normal_upstream_upgrade, test_checkpointless_baseline_publishes_checkpoint_without_copying, test_checkpointless_external_root_requires_action_and_rejects_force, test_checkpointless_force_keeps_verified_backup_bytes and test_first_legacy_upgrade_requires_owner_migration (scope='targets', tests=['python_tests'], timeout_seconds=240).

**Expected Result:** Existing cases pass; preserve-config/refusal/checkpoint/external-root facts substantiate the walkthrough. Report hermetic contract proof separately from a real host deployment; do not claim installation/client activation not performed.

##### One checklist remains discoverable without stale or unsafe consumers.

**Method:** Review changed-source diff and relevant README/setup/upgrade/host entrypoint references; search active targets for fabricated initialization, automatic main writes and health-only completion claims. Inspect selected host package locations, CLI source and settings/bootstrap admission.

**Expected Result:** Plain-language invocation reachable from repository and installed docs; no copied checklist, automatic Git/main/bootstrap issue writes, secret values or invented GitHub/tool availability.

##### Documentation gates and freshness are proportionate.

**Method:** run_checks(scope='targets', targets=[changed Markdown files], checks=['markdown_links'], timeout_seconds=180); read result sizes and relevant outcomes. No Python branch/full-suite gates for a docs-only diff.

**Expected Result:** Local references/anchors pass under configured offline link policy. Exact invocations/outcomes persisted, external exclusions and walkthrough limits explicit; code/test/config diff remains empty.

#### Stop Conditions

- Any runtime change or unclear source-of-truth requirement needs an explicit scope decision; do not repair code under this docs issue.
- Missing owner deployment input is open/blocked in the checklist rather than fabricated; no live mutation of this repo to simulate a fresh target.
- Require independent QA GO before Planning → Documentation and Documentation → Ready.

## Related Documents

- [Issue #508](<https://github.com/MikeyVK/phase-gate-mcp/issues/508>)
- [Authoritative checklist target](<../../setup/agentic-bootstrap.md>)
- [Documentation Standard](<../../coding_standards/DOCUMENTATION_STANDARD.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-17 | @imp planner | Bound documentation-only checklist reconciliation, authoritative sources, consumers and fresh/upgrade verification. |
