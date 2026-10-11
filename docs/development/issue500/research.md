<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=KoFPQ3-cAAWFeesb -->

# Issue 500 — v3 Release Preparation and Development Archive

**Status:** IN PROGRESS  
**Version:** 0.2  
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

## Historical Release Reconstruction — Additional Research

The owner requested feasibility research for retrospective GitHub releases 1.0.0 and 2.0.0. This authorizes investigation and preparation of a proposal, not tag creation or publication.

### GitHub Capabilities and Practical Value

GitHub releases associate a tag, authored notes and optional downloadable assets. A new tag can target an exact historical commit SHA without rewriting repository history. GitHub supplies source ZIP/tar archives for the tagged revision; a Python wheel is a separately supplied asset. Historical source dates and the new publication date should be stated separately: the release creation API does not accept a caller-specified `published_at`. Explicit latest-release selection prevents historical publication from displacing the intended current release.

This provides stable version references, comparable release boundaries, discoverable changes/migration notes and downloads. Publishing on GitHub does not publish to PyPI or establish new quality guarantees for old software. Generated notes can help inventory merged PRs, but require review for product meaning and correct range.

Sources:
- [GitHub: About releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- [GitHub: Create a release](https://docs.github.com/en/rest/releases/releases#create-a-release)
- [GitHub: Generated release notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes)

### Repository Evidence

| Version | Proposed canonical source boundary | Supporting observations | Remaining limitation |
|---|---|---|---|
| 1.0.0 | `3bfcef80fa97303d2b51738005b022edbcb0afbd`, merged PR #426, 2026-07-08 | PR #426 completes standalone packaging, CLI/init, environment naming and documentation. Archived #416 validation records a built/installed v1 wheel. Local `C:/temp/packages/phase_gate_mcp-1.0.0-py3-none-any.whl` has 212 Python files matching this revision after CRLF/LF normalization; all 132 present assets likewise match the manifest-mapped sources. | Current changelog dates v1 to July 6; PR #389 introduced the package name/version earlier, June 7. Selecting the complete standalone release on July 8 is a proposal, not proof that a public release occurred then. |
| 2.0.0 | `ee32667ca95bf17ffb4ecd59062ef8cbed930e0b`, merged PR #441, 2026-07-22 | PR #441 explicitly releases 2.0.0 with upgrade CLI, workspace version checks/preservation and version-source parity. Its package and manifest versions are 2.0.0. | Local `dist/phase_gate_mcp-2.0.0-py3-none-any.whl` is a later build: 171 Python files match both this revision and August 18 PR #447, but its assets match the latter. |

The asset inspection found seven manifest-mapped Copilot files absent from both wheels: the three `.github/agents/{co,imp,qa}.agent.md` files and four `.github/prompts/{create-issue,end-issue,go,start-issue}.prompt.md` files under the Copilot asset subtree. The v2 wheel additionally contains 20 assets absent from the July 22 manifest-source set and one changed common asset; at August 18, all its 182 present assets match. These are historical artifact observations, not a mandate to fix or retest old versions.

Evidence method: read-only `zipfile.ZipFile` metadata/content inspection; `git ls-tree -r <revision>` plus `git cat-file --batch` supplied tracked source blobs. Python file inventories and historical manifest-mapped assets were compared, with CRLF/LF equivalence reported explicitly. This is not byte-identical build proof: v1/v2 have 19 exact Python-file byte matches each; the remaining matching files differ in line endings. No wheel was installed, rebuilt, executed or uploaded. Local sdists were found but their parity was not investigated.

The existing changelog is a starting point, not ready-to-publish notes: its v2 section includes standalone packaging and environment naming already delivered by #426. Reconstruct each release's actual capabilities and additions from the selected boundaries, rather than copying overlapping bullets or using development-folder membership.

Primary evidence:
- [PR #389 — rebrand to v1](https://github.com/MikeyVK/phase-gate-mcp/pull/389)
- [PR #426 — standalone v1 package](https://github.com/MikeyVK/phase-gate-mcp/pull/426)
- [PR #441 — explicit v2 release](https://github.com/MikeyVK/phase-gate-mcp/pull/441)
- [Historical #416 validation](../archive/issue416/validation.md)

### Smallest Feasible Route — Proposed

Agree the two canonical SHAs; prepare reviewed notes identifying the historical revision/date and retrospective publication; after separate approval publish `v1.0.0` and `v2.0.0` with their exact targets and automatic source downloads. Optional old wheel/sdist uploads require a separate artifact decision and honest limitations. A later rebuilt package must be identified as a reconstruction and verified against its chosen source; do not relabel the August v2 package as the original July distribution.

No old-version repair campaign, broad historical test rerun, new release architecture or history rewrite is needed for source-based historical releases. The active tools expose release reads but no native release/tag publication operation; the eventual approved publication procedure therefore needs an explicit route, such as the GitHub release UI or authorized API/CLI use. The final v3 release should explicitly become the current release.

## Questions

- Does the owner approve PR #426 (July 8) and PR #441 (July 22) as the canonical reconstructed v1/v2 release boundaries? This is distinct from the particular later v2 wheel installed in another workspace.
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
| 0.2 | 2026-10-11 | @imp researcher | Investigate retrospective GitHub releases, candidate source boundaries, historical wheel/asset correspondence and publication limits. |
