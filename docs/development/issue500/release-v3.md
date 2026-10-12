<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=WfqMtGpITDXzqFVQ sf=KoFPQ3-cAAWFeesb -->

# Phase-Gate MCP 3.0.0

**Status:** PREPARED FOR PUBLICATION  
**Version:** 1.0  
**Last Updated:** 2026-10-12

## Purpose

Describe the v3 contracts, bundled artifacts, installation prerequisites and owner migration route for GitHub release publication.

## Summary

Version 3 moves scaffolding and native quality execution to explicit package contracts, makes planning mutations deliberate, and provides recovery tools after rejected startup. The installed distribution contains 23 template packages, 9 adapters and a 49-tool catalog. The change range starts at reconstructed v2 source `ee32667ca95bf17ffb4ecd59062ef8cbed930e0b` and includes merged work through [PR #499](https://github.com/MikeyVK/phase-gate-mcp/pull/499), followed by release preparation in [issue #500](https://github.com/MikeyVK/phase-gate-mcp/issues/500). Release notes derive from merged changes, not membership of the development folder.

## Breaking contracts

- Template packages combine manifests, context schemas, policies and shared Jinja tiers under `template_suite/`. Rediscover artifact IDs and context through live tool schemas and `scaffold_schema`. Removed aliases and old configuration shapes have no compatibility fallback. Scaffold creation and existing-file editing have separate contracts ([PR #464](https://github.com/MikeyVK/phase-gate-mcp/pull/464)).
- Full-document contexts require `document_metadata` with status and ordered revision history. Python identifiers are explicit ASCII fields; title and labels belong to publication inputs rather than issue/PR scaffold bodies ([PR #480](https://github.com/MikeyVK/phase-gate-mcp/pull/480), [PR #487](https://github.com/MikeyVK/phase-gate-mcp/pull/487)).
- `run_checks`, `run_tests` and `apply_fixes` replace numbered quality routes. Bind native adapters explicitly and assess native results alongside operation success. Per-check `configured_targets` filter branch candidates; explicit targets retain native targeting semantics. Tests have no branch scope ([PR #479](https://github.com/MikeyVK/phase-gate-mcp/pull/479), [PR #489](https://github.com/MikeyVK/phase-gate-mcp/pull/489)).
- Planning save accepts ordered named cycles and complete phase blocks; the server assigns totals and `C_#` / `D_#.#` references. Updates use complete-block operations and explicit removals. Qualifying execution commits protect cycles against replacement, removal and renumbering. Re-entry requires an explicit current-plan cycle reference ([PR #496](https://github.com/MikeyVK/phase-gate-mcp/pull/496)).
- `search_documentation` is removed; use host-native search. Lychee replaces owned Markdown link/preflight code; the adapter no longer enforces H1 structure ([PR #451](https://github.com/MikeyVK/phase-gate-mcp/pull/451), [PR #494](https://github.com/MikeyVK/phase-gate-mcp/pull/494)).

## New and improved

- YAML configuration, JSON Schema, ADR and arc42-based SAD join the bundled suite. ADR/SAD reuse Markdown tiers; YAML/JSON output uses native syntax/schema checks and declared identity reading ([PR #499](https://github.com/MikeyVK/phase-gate-mcp/pull/499)).
- Rejected startup retains `health_check` and `restart_server`. Textual JSON diagnostics support manual repair and restart; restart acknowledgement alone does not establish healthy admission ([PR #488](https://github.com/MikeyVK/phase-gate-mcp/pull/488)).
- Safe editing uses LF consistently across proposed, validated and persisted text; byte comparisons describe actual writes. Syntax feedback identifies candidate content. Shared templates own metadata/history and section joins ([PR #497](https://github.com/MikeyVK/phase-gate-mcp/pull/497), [PR #490](https://github.com/MikeyVK/phase-gate-mcp/pull/490)).
- Positive branch issue numbers, compact configured Chore, bounded presentation and truthful Git upstream feedback improve workflow use. Canonical agent assets include nested/dotfiles. Issue/PR scaffold bodies default to the ignored `.pgmcp/temp/artifacts` directory; previous development issues are archived.

## Installation and owner migration

Use Python 3.11 or newer and an isolated environment. Install the attached `phase_gate_mcp-3.0.0-py3-none-any.whl` with pip; the demonstrated environment resolves MCP 1.30.0 normally. This GitHub publication does not publish to PyPI.

Fresh workspaces use `pgmcp --init`; an existing server root is refused. For existing workspaces, install the package, reconcile owner configuration against shipped defaults, then run `pgmcp --upgrade`. First v3 suite migration may return `checkpoint_required` with exit 2 without activating the staged candidate. For a managed root, `--force-template-upgrade` backs up and replaces the suite. To retain customization, reconcile a valid complete v3 suite and use `--accept-template-baseline`. External roots remain owner-controlled.

Restart after package, active-suite or startup configuration changes, and reconnect the client when launch environment or discovery changed. Follow the [workspace upgrade guide](https://github.com/MikeyVK/phase-gate-mcp/blob/v3.0.0/docs/setup/workspace-upgrade.md) and [release procedure](https://github.com/MikeyVK/phase-gate-mcp/blob/v3.0.0/docs/reference/release-assets-procedure.md).

## Native prerequisites

Provision native tools separately; package installation and renewal do not install them. Bundled declarations specify Ruff 0.15.6, Mypy 1.19.1, Pyright 1.1.408, Lychee 0.24.2, Pytest 9.0.2, check-jsonschema 0.38.2, Commitlint 21.2.2 with Node >=22.12.0, and TypeScript 6.0.3, with their declared parser/test dependencies. Apply the [native adapter contract](https://github.com/MikeyVK/phase-gate-mcp/blob/v3.0.0/docs/reference/execution-adapters.md) and the shipped adapter requirements for each enabled binding.

## Verification and limits

Isolated artifact checks observed all 258 manifest assets, complete template/adapter catalogs, CLI 3.0.0, fresh initialization and server handshake. Renewal demonstrations covered baseline acceptance, managed replacement with exact backup and external-root force refusal. These observations do not stand in for final branch Validation; its scope and outcomes belong in the durable issue evidence.

Native syntax/schema acceptance does not prove application semantics or continued conformance to a template after free-text editing. Template release review uses the existing maintenance procedure; automatic template-compliance enforcement is outside this release. Offline Markdown checks do not certify external reachability. Presentation and response caches are bounded and transient: retain invocation/outcome evidence for independent review. Cycle commit protection does not imply completion. Automatic external rollout and parked #121/#462 remain outside scope.

## Downloads and source identity

The final wheel and sdist were rebuilt on 2026-10-12 after aligning publication-facing guides. Python3.13.7 and build1.5.0 drove the existing manifest assembly/build procedure; the wheel was built from the sdist. All 191 runtime Python sources, 258 manifest assets, adapter data and execution contracts are present without bytecode/cache members. The downloadable payload is bound to the reviewed release source; the `v3.0.0` tag identifies that exact source commit.

| Download | SHA-256 |
| --- | --- |
| `phase_gate_mcp-3.0.0-py3-none-any.whl` | `c77366dae59e77464da01b4e7f83bce1d4558d02f84fe5dc76a7269c2a1d5570` |
| `phase_gate_mcp-3.0.0.tar.gz` | `c9f86c6cbac840a054ae5a4b05deeca5fbcf4cbc0c1387244b9090e2b973d411` |
The source payload corresponds to commit `fcde44d2368399b080c82546c899d49b37ae759a`. Git checkout CRLF/LF conversion accounts for byte differences from raw Git blobs; no code or data differs beyond those line endings. Exact artifact/installed comparisons use the packaged bytes. This does not claim a byte-reproducible build.
## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-12 | @imp documenter | Prepare distinct GitHub release notes from the selected source boundary and verified installation artifacts. |
