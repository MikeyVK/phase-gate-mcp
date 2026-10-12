<!-- pgmcp:v1 id=validation_report pv=1.0.0 pf=dfPHW469kz8S1nLL sf=KoFPQ3-cAAWFeesb -->

# Issue 500 — release and workspace evidence

**Status:** Validation complete; publication verified  
**Version:** 0.2  
**Last Updated:** 2026-10-12

## Purpose

Record source-bound maintenance, package, installation and publication facts without relying on transient tool receipts.

## Scope In

Owner-approved historical v1/v2 reconstruction, v3 release values and guides, temporary issue/PR routing, development archive, selective cleanup, active owner installation and GitHub publication.

## Scope Out

PyPI, historical runtime repairs, new regression tests, general release infrastructure, external owner rollout and epic289 administration.

## Issue Number

#500

## Validation Status

PASS

## Evidence

### Focused implementation checks passed

The last pre-issue full suite was #465 snapshot d84811c4. This branch subsequently updates the final version fallback and two existing version tests; prior full-suite evidence is therefore insufficient for the final branch.

**Sources:**

- [CLI parity](<../../../tests/mcp_server/unit/test_cli.py>)
- [Settings](<../../../tests/mcp_server/unit/config/test_settings.py>)

**Invocation:** run_tests(scope='targets', targets=['tests/mcp_server/unit/test_cli.py','tests/mcp_server/unit/config/test_settings.py','tests/mcp_server/unit/test_build_package.py','tests/mcp_server/unit/services/test_artifact_target_resolver.py'], timeout_seconds=600); targeted python_format/python_lint; settings.py python_pyright; artifacts.yaml/release_manifest.yaml yaml_configuration.

**Observed Result:** 40 passed, 48 warnings, 7.59s, native exit0. Formatting, lint, production Pyright and both YAML files passed. The first parity assertion was outside its metadata patch; its location was corrected and all40 reran successfully. No new tests added.

### Historical installation artifacts preserve canonical sources

v1 source3bfcef80fa97303d2b51738005b022edbcb0afbd (PR426,2026-07-08); v2 sourceee32667ca95bf17ffb4ecd59062ef8cbed930e0b (PR441,2026-07-22). Reconstruction2026-10-11 uses Python3.13.7/build1.4.0/setuptools84.0.0. Only original pyproject package-data is extended with assets/**/.* and assets/**/.github/**/*; runtime and historical declared assets are unchanged.

**Sources:**

- [v1 notes](<release-v1.md>)
- [v2 notes](<release-v2.md>)

**Invocation:** git archive exactSHA into isolated vN-source; MCP safe-edit hiddenasset overlay; python scripts/build_package.py; wheel built from sdist; isolated exactwheel install; explicit mcp==1.25.0; --version; first/second --init; bounded initialize/list_tools; pipcheck; compare source/manifest/wheel/sdist/install inventories.

**Observed Result:** v1:212 Python sources,139 manifestassets,352 installedfiles; v2:171 Python sources,169 manifestassets,341 installedfiles. Asset/install comparisons exact; source bytes match git archive (raw Git blobs differ only CRLF/LF). Seven missing Copilot assets restored. CLI identifies1.0/2.0; init0/reinit1; 51 tools each; pipcheck passed. Original mcp>=1 permits2.3.0, which fails list_resources before handshake; the proven installation requires mcp1.25.0 without changing historical metadata/runtime. Handshake serverInfo.version reports SDK1.25.0.

### V3 installed candidate and renewal routes are evidenced

Only release-facing documentation changed after the existing isolated runtime/renewal proof. Final wheel identity and exact install/catalog checks were refreshed for those docs as recorded below; the unchanged runtime/renewal observations remain reusable.

**Sources:**

- [Installed catalog probe](<../../../tests/mcp_server/fixtures/installed_distribution.py>)
- [Renewal CLI](<../../../mcp_server/cli_renewal.py>)
- [v3 notes](<release-v3.md>)

**Invocation:** Existing build script; exactwheel install outside checkout; installed CATALOG_PROBE under -I; CLI --version/--init twice; bounded stdio handshake; isolated managed and external --upgrade/--accept-template-baseline/--force-template-upgrade; pipcheck.

**Observed Result:** Initial candidate:258 assets,191 runtimepy,23 templates/schemas,9 adapters,476 installedfiles;67 loaded PGMCP modules originate in installedvenv. CLI3.0,init0/reinit1,pipcheck0,handshake49tools(protocol2025-11-25,MCP1.30). Changed managed suite: normal2 preservesbytes; acceptbaseline0 preservesbytes and recordscheckpoint; force0 makes exact backup and activates exact candidate. Externalnormal2 preservesbytes; externalforce1 external_root_force_forbidden. The final clean build has258 asset/191runtime exact parity and0bytecode; final installed proof completed as recorded below.

### Owner-authorized upgrade restored the active server

The owner explicitly authorized installation on2026-10-12. Earlier restart rejected source-metadata3 versus workspace2; the normal upgrade resolved that mismatch without force or manual marker changes.

**Sources:**

- [Upgrade guide](<../../setup/workspace-upgrade.md>)

**Invocation:** Verify reviewedcandidatewheel identity; active .venv python -I -m pip install --upgrade --no-deps exactwheel; pipcheck; -I -m mcp_server --upgrade; native restart_server/health_check; fresh MCP tools/list/get_work_context; normal get_work_context after clientrestart.

**Observed Result:** Installed2.0 replaced3.0; pipcheck passed. Renewal exit0, actual suite unchanged, checkpoint advanced23, candidate removed. Active healthhealthy3.0; all49 tools available in the current chat. No force; source runtime continues through the configured development launch.

### Archive and live routing preserve intended boundaries

The 23-directory inventory is a relocation set, never the release-note source of truth. Installed docs intentionally do not include old issue history.

**Sources:**

- [Approved Research](<research.md>)
- [Archive](<../archive/>)
- [Artifact defaults](<../../../.pgmcp/config/artifacts.yaml>)

**Invocation:** Bounded Move-Item; native safe-edit relocation hrefs; compare124 files and URL-decoded linktargets to Git originals with LF normalization. scaffold_schema then scaffold_artifact(issue/pr/commit, issue500-routing-*), no target override; git check-ignore exact outputs.

**Observed Result:** 23 folders/124 files preserved;3816 formerlyvalid local linkoccurrences retain the same targets;0 remaining relocationbreaks and0 nonlink authored changes. One untouched YAML checkout differs from its Gitblob only CRLF. Seven active inboundlinks now use pinned GitHub source URLs for unbundled history. Issue/pr/commit each wrote .pgmcp/temp/artifacts and passed validation; all ignored. Only issue/pr defaultroots changed; no routingcode or aliases.

### Selective cleanup is complete for accessible candidates

The owner authorized cleanup and publication on2026-10-12. Nearblanket deletion of pgmcp/temp was rejected by automatic review; the accepted safer operation names only three writertrace targets there and preserves all other temp content.

**Sources:**

- [Ignore policy](<../../../.gitignore>)

**Invocation:** PowerShell Remove-Item with prevalidated absolute workspace targets, protectedpath overlap/reparse/tracked-member checks; two explicitlyorphaned registries allowed; separate accessible scratchchildren deleted after parent accesserrors.

**Observed Result:** 286 selected targets removed plus13 accessible scratchchildren. Removed10.8GiB writerETL and NGENPDB/analysis, oldcheckcaches/proposal/logs and two unused tracked template_registry.json files. Proposal was byte-identical144files to active suite, no activationjournal. Releasefiles, issue500, co-drafts, backups, runtime/dependencies and active lock kept. Protected leftovers remain in .pytest_cache_ci, .tmp/pytest-of-1Voudig and temp/cy08*-ruff; no ACL change. .gitignore now covers proposal and cachevariants.

### Final v3 wheel and source distribution

Existing `python scripts/build_package.py` built the final wheel from the sdist after the publication-facing documentation refresh. The exact wheel contains 191 runtime Python sources, 258 manifest assets and 475 total package payload members. Every payload byte matches the current sources, all seven hidden Copilot files are included, and no bytecode/cache members remain. Its pyproject matches the sdist. Final installed catalog: 23 templates, nine adapters and 67 observed module origins in the isolated prefix; CLI3.0/exit0; init0/reinit1; 49 unique tools; actual health_check healthy3.0; pip check passed. SDK transport metadata reports1.30.0. Unchanged renewal runtime/config/template observations above remain valid.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| phase_gate_mcp-3.0.0-py3-none-any.whl | 796852 | c77366dae59e77464da01b4e7f83bce1d4558d02f84fe5dc76a7269c2a1d5570 |
| phase_gate_mcp-3.0.0.tar.gz | 589206 | c9f86c6cbac840a054ae5a4b05deeca5fbcf4cbc0c1387244b9090e2b973d411 |

Reproduction: clean only untracked generated build/ and phase_gate_mcp.egg-info/ after containment/reparse/tracked-file checks; run the existing build script; install this exact wheel with --no-index --no-deps --no-compile into an isolated prefix using the admitted dependency environment; run the existing CATALOG_PROBE under -I, CLI/init and bounded MCP calls. The build driver uses Python3.13.7, build1.5.0, setuptools82.0.1, wheel0.46.3 and PyYAML6.0.3; build backend isolation is retained. Local reproduction inputs/logs are .pgmcp/temp/issue500/final-v3-proof/{inventory,payload,catalog,runtime}.json and build.log; these paths supplement the durable invocation/outcome facts, not replace them.
Source binding: all 475 final payload members map to commit `fcde44d2368399b080c82546c899d49b37ae759a`. Comparison against Git blobs found 28 exact byte matches and 447 differences solely from checkout CRLF/LF conversion, with zero content mismatches. Exact wheel/sdist/installed comparisons use the actual checkout bytes; this is not a claim of byte-reproducible builds from raw Git archives. This commit is the reviewed v3 release payload source; subsequent issue evidence/state changes are not packaged.

Final wheel metadata identifies isolated backend `setuptools (84.0.0)`, separately from the build driver's installed setuptools82.0.1. The focused release/report Markdown link selection passed with native configured arguments.
### Final phase-owned configured suite and branch checks

On reviewed snapshot `d24d8dfb94f03e2c79fee10e0b9c0e4a3d56cef5` (only the Validation state transition was uncommitted), `run_tests(scope='configured', timeout_seconds=1200)` retained the native Pytest arguments and reported **2923 passed, 1 skipped, 1 xpassed, 269 warnings in 383.39s**, native exit0. Python3.13.7, Pytest9.0.2, eight xdist workers and tests/mcp_server. No coverage flags, exclusions or new tests were added. The existing skip/XPASS and warning categories are reported as observed.

`run_checks(scope='branch', timeout_seconds=900)` used configured profile python_review and passed python_format, python_lint, python_types and python_pyright. Both complete result DTOs were read as needed: test header plus final native summary/capture fields, and the entire 8597-character branch DTO. Supplemental receipts: tests3cc54103d74e44019f0eec6c94c8083a; checks59cd536171a342ff9e1779aafa029d47. They supplement these durable invocation/outcome facts.

The earlier full #465 result is no longer used as final #500 evidence. Source changes are complete; remaining edits concern unbundled evidence, release records and workflow state. Independent QA owns the phase verdict.
### GitHub publication and online issue reconciliation

Owner-authorized publication completed on 2026-10-12. GitHub release API and tag references independently confirm:

| Release | Exact tag/source commit | Published UTC |
| --- | --- | --- |
| [v1.0.0](https://github.com/MikeyVK/phase-gate-mcp/releases/tag/v1.0.0) | 3bfcef80fa97303d2b51738005b022edbcb0afbd | 2026-10-12T07:10:18Z |
| [v2.0.0](https://github.com/MikeyVK/phase-gate-mcp/releases/tag/v2.0.0) | ee32667ca95bf17ffb4ecd59062ef8cbed930e0b | 2026-10-12T07:10:21Z |
| [v3.0.0](https://github.com/MikeyVK/phase-gate-mcp/releases/tag/v3.0.0) | fcde44d2368399b080c82546c899d49b37ae759a | 2026-10-12T07:10:24Z |

Invocation: `gh release create vN.0.0 exact-wheel exact-sdist --repo MikeyVK/phase-gate-mcp --target full-source-SHA --title release-title --notes-file -`; v1/v2 use `--latest=false`, v3 uses `--latest`. Each command exited0. No native publication tool exists; the owner explicitly authorized this fallback. Notes are the corresponding release document from Summary up to, excluding, Version History; local provenance and authored header are not published.

Observed result: each release is published, not draft/prerelease, with exactly two uploaded installation assets. All six remote asset sizes and SHA-256 digests match the tables in [v1](release-v1.md), [v2](release-v2.md) and [v3](release-v3.md). All three tag refs point to the exact source commits above. Release bodies match the authored excerpts after normalizing Windows stdin CRLF transport and removing the blank line immediately after `## Summary`, as performed by the publication excerpt extraction. No other content differs. The latest-release API returns v3.0.0. Historical release dates are described in their notes; publication dates are not backdated. PyPI is excluded.

`scaffold_artifact(artifact_type='issue', file_name='issue500-publication-body.md', validation='enforce')` produced the body in the configured temporary root. Native `update_issue(issue_number=500, body=...)` published it after removing only the recognized first-line provenance marker. A subsequent GitHub API read matched the submitted body exactly after CRLF normalization. [Issue500](https://github.com/MikeyVK/phase-gate-mcp/issues/500) remains open; labels/state and epic289 were not changed.

### Compact Documentation reconciliation

Reviewed authoritative CHANGELOG, setup upgrade/bootstrap guides, release-assets procedure, artifact defaults, agent instructions, template packages and their derived installed consumers. Release-facing sources were already synchronized and validated before the immutable package build; no further source/config/template/agent edits are needed. This phase changes only these four unbundled issue records and workflow state. Existing technical and source/installed parity evidence remains fresh. Publication records are now reconciled with live GitHub facts; focused link verification covers the four modified records. No new document, test or runtime repair is added.

## Caveats

- Independent QA returned GO for Implementation → Validation on d24d8dfb94f03e2c79fee10e0b9c0e4a3d56cef5 and Validation → Documentation on b82eb1e99c8c5f9903c950b11adbb576b87fc49b. Documentation → Ready GO was returned on ed03a15626d724a033dcaa21fec2ff288539e769; its non-blocking P3 request to specify publication whitespace normalization is corrected here.
- V3 artifact payload and published tag are bound to fcde44d2368399b080c82546c899d49b37ae759a. Subsequent issue evidence/state changes are unbundled; merging this maintenance branch remains separate.
- ServerInfo.version reports the SDK version; PGMCP CLI/distribution metadata identify the release. Existing SchemaAttachment.schema warning does not block proven routes.

## Deferred Work

### Epic289 inventory and old396/415 disposition

Owner explicitly leaves this administration to Coordination.

### OS-protected old scratch leftovers

Deletion denied; ownership/ACL intervention is excluded from the safe release cleanup.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-12 | @imp implementer | Persist focused, package, archive, routing, cleanup and owner-migration observations. |
| 0.2 | 2026-10-12 | @imp documenter | Record full Validation gates, independent phase reviews, verified GitHub publication and compact documentation reconciliation. |
