<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=KoFPQ3-cAAWFeesb -->

# Issue 500 — v3 Release Preparation and Development Archive

**Status:** IN PROGRESS  
**Version:** 0.1  
**Last Updated:** 2026-10-11

## Scope In

Package release-version sources and runtime fallbacks; release notes reconstructed from durable merged work; installation/migration and native prerequisite guidance; #289 inventory reconciliation through Coordination; existing release assembly and installed-package verification; narrow temporary artifact routing; relocation of the baseline issue folders and links affected by that relocation.

## Scope Out

Publishing, tagging or external rollout without separate approval; epic closure or priority changes; parked #121/#462; optional features; generic production refactoring; a new release automation platform; repository-wide historical-document rewrites.

## Problem Statement

The repository contains integrated v3 work while package release sources and release-facing documentation still describe 2.0.0. Existing development issue folders also obscure the next release's working set, but they do not form a complete v2-to-v3 change inventory.

## Goals

- Bound v3.0.0 release preparation using existing version, build, installation and renewal contracts.
- Record the owner's archive addition without making the development folder a release-history source of truth.
- Identify material consumer impacts, verification needs and unresolved decisions before implementation.

## Background

Research-only inspection on chore/500-prepare-validate-v3-release. No version changes, archive moves, builds, test runs, phase transitions or external issue mutations have been performed. Chore has Research followed by Implementation, Validation, Documentation and Ready; no separate Design/Planning artifacts are proposed.

## Findings

| Boundary | Observed state | Release implication |
|---|---|---|
| Package version | `pyproject.toml`, release manifest and final settings fallback still say 2.0.0; Commitlint adapter requirements pin `phase-gate-mcp==2.0.0`. | Reconcile package-version consumers, without treating adapter versions or config schema identities as package versions. |
| Workspace migration | Existing release-assets and workspace-upgrade procedures distinguish package installation, owner config, active suite/checkpoints and restart. | Use the existing paths; do not silently overwrite external or existing workspace roots. |
| Release history | CHANGELOG records v2.0.0 on 2026-07-22. Local tags and remote GitHub tag/release collections were empty. Commit `ee32667ca95bf17ffb4ecd59062ef8cbed930e0b` is a candidate v2 integration point, not a verified publication baseline. | Confirm the owner-used v2 distribution/baseline before claiming a complete v2-to-v3 inventory. Use merged history and durable issue/PR evidence. |
| Epic inventory | #289 still lists #396, #399, #414 and #415 as open. Live queries show #399 and #414 closed; #396 and #415 open. | Coordination should reconcile the inventory without closing the epic or changing priorities implicitly. |
| Archive | 23 direct issue directories exist; none conflicts with its destination name under `archive/`. Existing maintenance guides are direct non-issue files. | Move this fixed set, preserving content. Keep issue500 and the active guides in development. |
| Archive consumers | Active setup/reference/diagram docs link to issue460. Three test-context strings also mention it; the inspected Research occurrence is supplied template context. | Repair affected navigable links; inspect actual consumers before changing tests. Do not rewrite generic future `issueN` workflow destinations. |
| Packaged assets | The manifest packages only `schema-template-maintenance.md` from development, not issue directories or the archive. | No archive asset route or new release-assembly mechanism is needed. |
| Temporary publication artifacts | #500 already approves issue/pr default roots at `.pgmcp/temp/artifacts`, matching the existing commit root. | Preserve unrelated routes and verify effective routing plus ignored temporary output. |

The fixed archive set at HEAD `8770607492aeb6d076dfe5aae1dc78f79515dd07` is:
116, 399, 414, 442, 443, 444, 446, 449, 456, 459, 460, 465, 469, 470, 471, 472, 473, 476, 481, 482, 483, 486 and 491.

#396 requests a separate archive branch and removal from main. The owner's #500 instruction instead retains the documents in the existing in-repository archive. Its administrative disposition belongs to Coordination; it is not silently considered completed by this different route. Existing historical link defects are not a repository-wide cleanup mandate.

## Questions

- What exact v2 distribution/revision did the owner install, given the empty GitHub release/tag collections?
- Which publication destination and artifacts should be prepared, and what procedure will the owner approve for publication?
- Does any version/migration or archive-link finding require a change beyond mechanical maintenance? If so, reopen scope/strategy before implementing it.

## Approved Strategy

**Owner-approved boundaries, not approval to implement or publish this entire issue:**
- Archive the 23 pre-existing direct issue directories into `docs/development/archive/`. Preserve `MAINTENANCE_SCRIPTS.md`, `schema-template-maintenance.md` and the new issue500 working directory. This is relocation, not deletion or a separate archive branch.
- The development-directory inventory is explicitly incomplete and mixed across releases. It must not be the source of truth for v3 release notes. Reconstruct delivered work independently from verified version baseline, merged commits, PRs and issue evidence.
- The existing #500 issue records approval for the narrow issue/pr temporary-root change. No aliases or general scaffolding refactor are intended.
- Release preparation uses the current manifest, build and renewal architecture. Actual publication, tagging and external rollout remain subject to separate human approval, as stated in #500.

The exact publication destination/artifacts, verified v2 baseline and any concrete migration/version behavior changes still need Research resolution before progression. No new compatibility policy for an unexpected defect is inferred from this maintenance request.

## Expected Results

After approved execution, the existing issue folders are preserved under archive and the active development folder contains the current release work plus its guides. Release notes trace to independently reconstructed delivered changes, not folder membership. Package, assembled assets and installed version/catalog evidence agree on the release candidate, while independent adapter/template/schema versions retain their own meaning. Owner migration and publication responsibilities are explicit.

Verification should use the existing tooling and tests: focused checks for changed version/config consumers during implementation; link checks on affected active docs and relocation-induced links; the existing manifest/build procedure followed by installed CLI/version and asset/catalog checks; relevant fresh-init and managed/external renewal routes in isolated workspaces; and final workflow-required tests/gates, reusing only evidence that the final changes have not invalidated. Temporary issue/pr scaffolding must use the effective configured root and leave the tracked worktree unchanged. No new test framework or content-mirroring tests are proposed.

## Evidence

### Epic \#289 has a stale child inventory.

Native get_issue calls on 2026-10-11 returned closed for #399/#414 and open for #396/#415.

- [Epic 289](<https://github.com/MikeyVK/phase-gate-mcp/issues/289>)

### No GitHub release or tag identifies the baseline at inspection time.

GitHub GET releases?per_page=10 and git/matching-refs/tags/ each returned an empty collection on 2026-10-11. The rejected /tags endpoint was not used as evidence.

- [GitHub Releases](<https://github.com/MikeyVK/phase-gate-mcp/releases>)

### The archive addition is a fixed relocation set, not a release-change inventory.

Read-only directory inventory found the 23 listed issue directories and no same-name destinations. Owner explicitly disallowed using this mixed folder set as release-notes SSOT.

- [Development directory](<../>)

## Risks

### Moving issue folders changes relative-link depth and inbound targets.

Inspect links in the moved set and current consumers; repair breakage caused by relocation, without sweeping unrelated historical defects.

### Different version identities can be confused with the server package version.

Classify each consumer, especially workspace .version, package self-pins, independent adapter/template versions and schema literals before editing.

## Related Documents

- [Issue 500](<https://github.com/MikeyVK/phase-gate-mcp/issues/500>)
- [Release Assets Procedure](<../../reference/release-assets-procedure.md>)
- [Workspace Upgrade](<../../setup/workspace-upgrade.md>)
- [Release Manifest](<../../../.pgmcp/config/release_manifest.yaml>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-11 | @imp researcher | Record bounded release research and the owner-approved development archive addition. |
