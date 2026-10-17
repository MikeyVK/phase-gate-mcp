<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=WI5iXHBKVOU91bYE -->

# Issue 508 — Documentation and Walkthrough Evidence

**Status:** Completed verification — independent Documentation review requested  
**Version:** 0.1  
**Last Updated:** 2026-10-17

## Purpose

Make the documentation proof reproducible without claiming a fresh-machine installation or new runtime behavior.

## Scope In

Fresh setup and targeted upgrade/delta documentation, explicit invocation, owner decisions, secret-safe reporting and health/config/operation evidence.

## Scope Out

No package/build publication, new setup engine/CLI/gate, automatic Git/main/issue writes, target deployment, new tests or broad runtime verification.

## Summary

One authoritative checklist now lives at [agentic-bootstrap.md](../../setup/agentic-bootstrap.md). README, the runtime/host reference and upgrade guide navigate to it; specialist sources retain CLI, config and policy meanings. Four active Markdown files changed; production, config, host instruction bodies and test code remain unchanged.

## Authority and Consumer Review

| Surface | Review outcome |
| --- | --- |
| [Checklist](../../setup/agentic-bootstrap.md) | Single fresh/upgrade procedure and completion/status authority. Replaced automatic Git/main/remote writes, invented issue registration, wholesale settings copying and automatic activation assumptions. |
| [Root README](../../../README.md) | Explicit chat invocation and both checkout and installed-document paths; older packages keep their supplied behavior. |
| [Runtime/host reference](../../setup/README.md) | Capability-specific prerequisites, selected interpreter/artifact, optional credentials/native tools and field-by-field host reconciliation. Existing Codex timeout policy retained; health-only completion removed. |
| [Upgrade guide](../../setup/workspace-upgrade.md) | Refers to the checklist's delta mode; retains checkpoint, baseline, verified-backup, external-root and owner-state details. |
| [CLI](../../../mcp_server/cli.py), [renewal composition](../../../mcp_server/cli_renewal.py), [renewal operation](../../../mcp_server/services/template_renewal.py) | Source authority for init/refusal and template-only renewal; no config/host migration is invented. |
| [Settings](../../../mcp_server/config/settings.py), [bootstrap](../../../mcp_server/bootstrap.py) | Root/package resolution and token-dependent discovery. A read-only launcher probe proves its own context, not an uninspected live child. |
| [Release manifest](../../../.pgmcp/config/release_manifest.yaml) | Existing docs/setup→docs/setup mapping already carries the checklist; docs/agents→agents supplies host material. No builder/manifest change required. The installed path is explicitly stated instead of assuming checkout-relative root README links work in a package. |

## Fresh Setup Walkthrough

This is an authored scenario/read-through backed by existing hermetic CLI cases, not a target-owner deployment decision. Inputs: an existing owner-provided repository, absent server root, a chosen package/interpreter, selected local artifact/quality use and GitHub not selected.

| Step through the checklist | Observed source/contract proof and honest status |
| --- | --- |
| Find and invoke it | Repository README and setup reference link the same file; installed invocation names `<server-root>/docs/setup/agentic-bootstrap.md`. Pip/CLI do not create the agent chat. |
| Resolve package and roots | Settings supports the named roots; selected-artifact metadata owns its requirements. Host/interpreter/roots remain open until supplied; no fictitious target values are persisted. |
| Initialize only the absent root | test_cli_init_result passes three returned-result branches (with the renewal operation mocked in those unit cases); supplied config/acknowledgements are copied unchanged. test_cli_init_already_exists proves refusal instead of overwrite. |
| Review choices and host | Artifact/quality/workflow/root/label choices are explicit; native pins come from selected adapter manifests. GitHub is N/A only for this scenario's deliberate nonselection; any GitHub-dependent enforcement still requires a resolved policy/dependency. Existing host settings are reconciled, not replaced. |
| Connect and prove operation | CLI success is not health/config completeness. The procedure requests refreshed discovery, health, live identity and one approved narrow operation per selected family; unavailable/unexecuted proof stays open/blocked. No fabricated initialize_project or main commit is used. |
| Hand over | The central status matrix carries decisions, safe invocations/outcomes, owners and remaining limitations separately. Real issue registration returns to coordination. |

Result: the route is internally executable and has bounded primitive proof. No new environment was installed, host activated, credential delivered or external service exercised by this walkthrough.

## Existing Workspace Upgrade Walkthrough

Scenario/read-through inputs: an existing server root with owner config/customizations, a selected package delta and a managed or external template suite. These are walkthrough assumptions, not changes performed in this repository.

| Step through the checklist | Observed source/contract proof and honest status |
| --- | --- |
| Inventory and select the delta | Existing interpreter/package/roots/config/native policy/host settings/checkpoints are recorded before authorized changes; unaffected reviewed choices/evidence are retained with scope/version. |
| Install and reconcile | The selected artifact owns Python requirements; an older-interpreter environment is recreated deliberately. Config/state/input changes are owner reconciliation, not effects of --upgrade or a healthy status. |
| Renew managed templates | test_fresh_install_then_normal_upstream_upgrade proves actual managed-suite activation through the renewal CLI operation. Owner config/host routes remain separate in CLI composition. |
| Missing checkpoint | test_checkpointless_baseline_publishes_checkpoint_without_copying proves explicit acceptance without replacement; test_checkpointless_force_keeps_verified_backup_bytes proves the alternative's verified backup; those are owner choices, not automatic fallback. |
| External or older root | test_checkpointless_external_root_requires_action_and_rejects_force returns checkpoint_required then refuses external force while preserving bytes. test_first_legacy_upgrade_requires_owner_migration preserves the owner-migration boundary. The checklist records those outcomes blocked/open until resolved, not as activation success. |
| Activate and verify the delta | Package/startup-config/suite changes trigger the existing restart/reconnect route. Health, selected config completeness and representative outcomes remain separate. Host/live process inspection not performed here is explicitly unverified. |

Result: the delta route preserves ownership and does not reset all configuration. The tests exercise isolated temp roots; they do not prove a full OS/host installation or every owner's native policy.

## Exact Executed Verification

Existing contract run:

```text
run_tests(
  scope="targets",
  targets=["tests/mcp_server/unit/test_cli.py", "tests/mcp_server/integration/test_renewal_cli.py"],
  tests=["python_tests"],
  args={"python_tests": ["-k", "test_cli_init_result or test_cli_init_already_exists or test_fresh_install_then_normal_upstream_upgrade or test_checkpointless_baseline_publishes_checkpoint_without_copying or test_checkpointless_external_root_requires_action_and_rejects_force or test_checkpointless_force_keeps_verified_backup_bytes or test_first_legacy_upgrade_requires_owner_migration"]},
  timeout_seconds=240,
)
```

Observed: **9 passed in 11.89 seconds**, 8 workers, Python 3.13.7/pytest 9.0.2, native exit 0; no warnings/skips/XPASS, timeout or termination problem reported, capture untruncated. Seven selected functions exist; the three init-result parameters explain nine cases. Supplemental receipt bc2cbb8947154d32bf6debdd33a13026 (3763 characters, read in full). No test content changed.

```text
run_checks(
  scope="targets",
  targets=["README.md", "docs/setup/agentic-bootstrap.md", "docs/setup/README.md", "docs/setup/workspace-upgrade.md", "docs/development/issue508/planning.md"],
  checks=["markdown_links"],
  timeout_seconds=180,
)
```

Observed: native exit 0, **62 occurrences / 34 unique, 55 successful, 7 excluded, 0 errors** (supplemental f72e26cfd50f44ffa0464e531a6de234). The existing offline policy excludes external URLs; no external liveness claim. Subsequent same-file wording edits were individually link-validated and added no link targets. The final run used the same call with `docs/development/issue508/documentation.md` added to targets: native exit 0, 77 occurrences / 38 unique, 68 successful, 9 excluded, 0 errors (supplemental 5596351efdbf4c848ac9d1e93c77ef60). Final wording changed no link targets and safe-edit validation passed again. Direct source/consumer review found no remaining automatic Git/main/issue setup commands or wholesale settings writes in the four active targets.

No source/test behavior changed and no branch/full-suite gate was run for this docs workflow.

## Reviewed but Unchanged and Limitations

- Current configuration/quality/GitHub/adapter references retain field and policy authority; the checklist links rather than duplicates their contracts. The existing Codex 1800-second client/1200-second required-full-run policy is preserved, not invoked as a setup requirement.
- Distributable host instruction bodies and selected skills/workflows were reviewed for paths/roles; this change adds no new instruction contract, so no derived instruction copies require synchronization. Host discovery is verified by the target host, not guaranteed from file presence.
- Source/packaged locations are established by the existing release manifest. No wheel is built or existing published artifact rewritten. A previously published package may lack this new guide; the invocation states that limitation.
- The read-only context example prints only selected nonsecret identity/paths; it was source-reviewed, not executed in a target launch environment. Health alone cannot prove live roots/interpreter.
- No real target workspace was provisioned. The two walkthroughs and existing behavioral tests substantiate document routes and primitives, not OS credential setup, a host restart, GitHub permissions or every native policy.

## Deferred Work

None identified within #508's documentation boundary. SDK 2/higher Python/checker-suppression assessment remains tracked separately in [#513](https://github.com/MikeyVK/phase-gate-mcp/issues/513), already coordinated and intentionally not started here. No runtime gap was found that requires expansion of this issue.

## Related Documents

- [Approved Planning](<planning.md>)
- [Issue #508](<https://github.com/MikeyVK/phase-gate-mcp/issues/508>)
- [Documentation Standard](<../../coding_standards/DOCUMENTATION_STANDARD.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-17 | @imp documenter | Record source-backed fresh/upgrade walkthroughs, bounded native contract proof, document links and consumer parity. |
