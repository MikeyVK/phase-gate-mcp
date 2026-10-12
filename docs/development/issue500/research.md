<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=KoFPQ3-cAAWFeesb -->

# Issue 500 — v3 Release Preparation and Development Archive

**Status:** REVIEW REQUESTED  
**Version:** 0.3  
**Last Updated:** 2026-10-11

## Scope In

Package release-version sources and runtime fallbacks; release notes reconstructed from durable merged work; installation/migration and native prerequisite guidance; #289 inventory reconciliation through Coordination; existing release assembly and installed-package verification; narrow temporary artifact routing; relocation of the baseline issue folders and links affected by that relocation; retrospective GitHub release notes and reconstructed wheel/sdist for the selected v1/v2 boundaries.

## Scope Out

Publishing, tagging or external rollout without separate approval; PyPI; historical runtime repair and old full-suite campaigns; epic closure or priority changes; parked #121/#462; optional features; generic production refactoring; a new release automation platform; repository-wide historical-document rewrites.

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

### Owner Scope Update — Historical Installation Packages

On 2026-10-11 the owner selected **installation packages for v1/v2 as well**, in addition to the proposed GitHub release preparation. The earlier source-only minimum is superseded. Prepare wheel and sdist for each historical source boundary, alongside v3; PyPI is not selected. Actual publication/tagging still needs separate approval.

Historical build inputs must remain distinguishable: original SHA, original runtime and manifest-mapped assets, reconstruction date/toolchain and any packaging-only correction. Both historical pyprojects use only `assets/**/*`; both retained sdists also omit the seven Copilot dotfile assets. The proposed minimal correction is explicit hidden/nested asset inclusion in the isolated reconstruction's packaging declaration. Do not transplant v3 runtime, owner config, templates or later agent assets into those packages. Do not describe regenerated packages as the original byte-identical historical binaries.

Verify each exact reconstructed wheel/sdist against that historical source and manifest; confirm installation, CLI version, fresh init and a bounded startup/handshake in isolated workspaces. The sdist must be usable to rebuild its corresponding complete wheel. No old full-suite rerun or historical runtime repair campaign is proposed. If historical code cannot run with the selected dependency environment, report the concrete blocker and reopen the boundary before patching runtime code.

The active tools expose release reads but no native release/tag publication operation. Prepare local reviewed notes and exact-target publication inputs; the eventual separately approved action can use GitHub's Release API or `gh release create --target <SHA>` with explicit assets/notes and latest policy. No tag/release/draft creation is part of Research. v3 should explicitly become the current release when it is published.

## Remaining Release Scope — Findings and Execution Boundary

### Delivered v3 Changes

The merged range is the proposed v2 boundary `ee32667ca95bf17ffb4ecd59062ef8cbed930e0b` through main `8770607492aeb6d076dfe5aae1dc78f79515dd07`: 23 first-parent merge PRs. Their bodies and current active references were inspected proportionally. This reconstructs material release behavior; it is not a semantic audit of every historical epic child.

| Release-facing subject | Durable merge evidence | Final behavior to explain |
|---|---|---|
| Core v3 suite and execution cutover | [#464](https://github.com/MikeyVK/phase-gate-mcp/pull/464) | Explicit package manifests/schemas/policies and graph composition; separate scaffold/edit contracts; native checks/tests/fixes replace old quality routes. Old aliases and configuration shapes require manual migration. |
| Native execution and branch selection | [#479](https://github.com/MikeyVK/phase-gate-mcp/pull/479), [#489](https://github.com/MikeyVK/phase-gate-mcp/pull/489) | Complete native invocations, dependency/version refusal and truthful outcomes; per-check configured filtering overlays Git candidates only for check branch scope. Explicit targets remain intentional. |
| Recovery | [#488](https://github.com/MikeyVK/phase-gate-mcp/pull/488) | Rejected startup exposes health/restart with actionable textual JSON diagnosis; fix then restart. Restart acknowledgement does not prove healthy admission. |
| Planning, scope and state | [#496](https://github.com/MikeyVK/phase-gate-mcp/pull/496) | Whole-block mutations, named ordered input, derived references/totals, commit-protected cycle identity, configured Planning admission and explicit resume; shared scope codec and initialization guard. |
| LF edits and checked diagnostics | [#497](https://github.com/MikeyVK/phase-gate-mcp/pull/497), [#490](https://github.com/MikeyVK/phase-gate-mcp/pull/490) | One LF proposal for checks/write, actual byte-change reporting, candidate-source syntax diagnostics and durable evidence guidance. |
| Template contracts and new families | [#480](https://github.com/MikeyVK/phase-gate-mcp/pull/480), [#487](https://github.com/MikeyVK/phase-gate-mcp/pull/487), [#499](https://github.com/MikeyVK/phase-gate-mcp/pull/499) | Authored document metadata/history, shared composition/spacing, ASCII structured Python identifiers; YAML configuration, JSON Schema, ADR and arc42 SAD packages. |
| Markdown and semantic assurance | [#494](https://github.com/MikeyVK/phase-gate-mcp/pull/494), [#493](https://github.com/MikeyVK/phase-gate-mcp/pull/493), [#495](https://github.com/MikeyVK/phase-gate-mcp/pull/495) | Lychee replaces owned Markdown preflight; no runtime H1/template-preservation claim. Evidence-based package release review belongs to the existing maintenance guide. Active links were repaired. |
| Public discovery and workflow policy | [#451](https://github.com/MikeyVK/phase-gate-mcp/pull/451), [#454](https://github.com/MikeyVK/phase-gate-mcp/pull/454), [#450](https://github.com/MikeyVK/phase-gate-mcp/pull/450), [#457](https://github.com/MikeyVK/phase-gate-mcp/pull/457) | Removed documentation search; mandatory positive issue number on branch creation; compact configured Chore and streamlined phase instructions. Refresh client tool discovery. |
| Git push and release/agent boundaries | [#453](https://github.com/MikeyVK/phase-gate-mcp/pull/453), [#447](https://github.com/MikeyVK/phase-gate-mcp/pull/447) | Truthful remote/upstream results and canonical distributable host-agent sources; current packaging includes hidden assets. |
| Presentation and earlier quality fixes | [#455](https://github.com/MikeyVK/phase-gate-mcp/pull/455), [#458](https://github.com/MikeyVK/phase-gate-mcp/pull/458), [#461](https://github.com/MikeyVK/phase-gate-mcp/pull/461), [#452](https://github.com/MikeyVK/phase-gate-mcp/pull/452) | Compact configured presentation and complete DTO evidence. Summarize current native execution/results, without reviving later-retired quality DTOs or numbered gates. |

Current Unreleased notes cover only #443/#473. Reconcile v1/v2 overlap and write the v3 narrative around final public behavior, breaking inputs/configuration, owner migration and limits.

### Version and Migration Consumers

Update only the package-release values in `pyproject.toml`, `.pgmcp/config/release_manifest.yaml`, the final `_default_server_version()` fallback and Commitlint's `phase-gate-mcp` requirement. Correct the two stale setup claims. Adapt existing CLI parity and missing-metadata tests at their actual dependency boundary: installed host metadata has priority over the checkout manifest, so a repository-parity test must isolate that observation rather than require an owner installation upgrade to pass.

Preserve schema/config identities, independent adapter/template versions, runtime resolution policy and workspace markers. `installation.json` and suite checkpoints must be published through renewal. Current health is healthy/2.0.0; it is not v3 installation evidence. The current installation checkpoint predates new #465 packages; an installed3.0.0 runtime can reject this old installation until owner-led upgrade/reconciliation.

Migration guidance must distinguish package installation; owner config; managed suite staging/verified backup or explicit baseline acceptance; external-suite owner action; and server restart/client reconnect. Do not mutate the working release-preparation workspace merely to manufacture isolated install proof.

Native prerequisites remain declared per adapter: Ruff0.15.6, Mypy1.19.1, Pyright1.1.408, Lychee0.24.2, Pytest9.0.2 and its pinned test dependencies, check-jsonschema0.38.2 and parser dependencies, Commitlint21.2.2/Node>=22.12.0, and TypeScript6.0.3. The release notes link to those authoritative package declarations; no new global installation layer is needed.

### Archive, Routing and Coordination

The fixed archive set contains **23 directories / 124 files**. Seven active inbound link occurrences exist in five setup/reference/diagram documents. Relocation also changes outbound relative-link depth inside historical documents; fix only relocation-induced breakage. Generic future issue paths and historical narrative/example path strings are not automatic replacement targets. Historical reports are not added to wheel assets. Links from packaged docs to intentionally unbundled history require an explicit reading route, not an assumption that the history exists in the installation.

Issue/PR policies use workspace persistence, so their configured defaults directly select the output directory. Change their two roots to `.pgmcp/temp/artifacts`; commit already uses it and `.gitignore` already excludes `.pgmcp/temp/`. Existing resolver/create-only behavior can prove effective paths and no worktree pollution without new routing code or new tests.

Coordination owns #289 inventory reconciliation: #399/#414 closed, #396/#415 open. #396's separate-archive-branch request differs from this approved in-repository archive route. Record that disposition explicitly. Live open-priority queries found only #500 and umbrella #289 at high priority and none critical; do not reopen medium/low backlog, #121 or #462.

### Verification and Stop Conditions

- During Implementation, adapt/run existing CLI/settings and build/target-resolver tests at changed boundaries, with focused Python and YAML checks. No new content-mirroring or legacy-preservation tests are proposed.
- Use the existing manifest/build procedure for v3. Verify the **exact final wheel and sdist**, all mapped files including hidden Copilot/template members, adapter/contracts data, installed module origins/catalog and CLI version; distinguish this from tests that build their own candidate.
- Reuse existing installed-distribution, target-startup, cutover and renewal tests for fresh init, managed checkpoint/backup/baseline behavior, external-root refusal and handshake. Record package install and owner migration as separate observations.
- Chore Validation requires one fresh `run_tests(scope='configured', timeout_seconds=1200)` and `run_checks(scope='branch')` after final implementation. Use the configured per-check branch policies; add only narrowly justified doc/data checks. Preserve native arguments and the approved1800-second client window.
- Check affected documentation links and historical relocation against its pre-move state; do not equate a move with a mandate to fix unrelated pre-existing archive defects. Preserve source content and inspect Git rename/diff inventory.
- Historical artifacts need bounded exact-package install/init/startup proof, not full old suites. Missing asset members, failed catalog/startup, owner-root overwrite, incompatible dependency environment or sdist unable to rebuild the intended complete wheel are explicit stop conditions.
- Any runtime/code repair beyond release values, unrelated configuration/instruction changes, legacy bridge, new release platform, owner rollout or publication requires renewed scope/strategy authority. Independent QA reviews final evidence; producer delegates return findings only.

Primary verification entry points: [CLI tests](../../../tests/mcp_server/unit/test_cli.py), [settings tests](../../../tests/mcp_server/unit/config/test_settings.py), [build tests](../../../tests/mcp_server/unit/test_build_package.py), [installed distribution](../../../tests/mcp_server/integration/test_installed_distribution_v3.py), [target startup](../../../tests/mcp_server/integration/test_target_startup.py), [renewal routes](../../../tests/mcp_server/integration/test_renewal_cli.py), [target resolver](../../../tests/mcp_server/unit/services/test_artifact_target_resolver.py).

## Questions

- Final artifact hashes, build/install outcomes and the release publication date remain execution evidence, not Research facts.
- Publication approval remains outstanding by design. Present reviewed notes, exact SHAs, wheel/sdist identities and the concrete GitHub API/CLI procedure before asking to create tags/releases or upload assets.
- If historical installation or final v3 verification reveals a runtime defect, return the exact finding for triage rather than implicitly widening this Chore.

## Approved Strategy

**Owner-approved preparation scope and its bounded maintenance strategy:**
- Archive the 23 pre-existing direct issue directories into `docs/development/archive/`. Preserve `MAINTENANCE_SCRIPTS.md`, `schema-template-maintenance.md` and the new issue500 working directory. This is relocation, not deletion or a separate archive branch.
- The development-directory inventory is explicitly incomplete and mixed across releases. It must not be the source of truth for v3 release notes. Reconstruct delivered work independently from verified version baseline, merged commits, PRs and issue evidence.
- The existing #500 issue records approval for the narrow issue/pr temporary-root change. No aliases or general scaffolding refactor are intended.
- Release preparation uses the current manifest, build and renewal architecture. Actual publication, tagging and external rollout remain subject to separate human approval, as stated in #500.

- Following the owner's 2026-10-11 continuation and artifact choice, prepare GitHub release notes plus wheel/sdist for v1 at PR #426, v2 at PR #441 and the final v3 revision. These are canonical reconstruction boundaries, not invented evidence of historical GitHub publication. PyPI is outside scope.
- Preserve historical runtime and declared asset contents. Limit reconstruction corrections to build-time inclusion of those declared hidden assets; document the overlay and verify resulting wheel/sdist. No historical runtime repair or old full-suite campaign is included.
- Reconcile v3 package-release literals and existing affected tests, preserve independent version identities and runtime resolution behavior. Use current package-data declarations first, not a speculative packaging rewrite.
- Existing/external workspace config and suite migration remain owner-led through renewal. Release verification uses isolated workspaces. No automatic upgrade of the active owner environment is included.
- Use existing verification mechanisms and phase-owned broad runs. Scope growth, any new compatibility bridge or a concrete runtime defect needs renewed triage. Publication/tagging/rollout approval is a later, separate decision.

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
| 0.3 | 2026-10-11 | @imp researcher | Incorporate owner-selected historical installation packages; complete v3 merge ledger, consumer/migration/archive impact and bounded verification strategy. |
