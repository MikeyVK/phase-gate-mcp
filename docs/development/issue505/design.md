<!-- pgmcp:v1 id=design pv=1.0.0 pf=Uk1D2XWpiag1c6nn sf=WI5iXHBKVOU91bYE -->

# Issue 505 — Fail-closed asset assembly

**Status:** DESIGN — QA REQUESTED  
**Version:** 0.2  
**Last Updated:** 2026-10-16

## Purpose

Specify the smallest correction to the existing standalone builder, within the owner-approved Research strategy.

## Scope In

Required manifest admission, source/target ownership, cleanup/copy failure propagation and direct behavioral coverage.

## Scope Out

Manifest grammar/content routing, runtime architecture, staging transactions/rollback, release/deployment and issues506–508.

## Problem Statement

The builder skips malformed mappings, suppresses cleanup failures and trusts path joins. Research confirms false-success/build reachability and a scratch target escape; no contaminated wheel or production incident is claimed.

## Functional Requirements

- Reject missing/non-list/empty assets, non-object records and missing/non-string/blank source or target with mapping-index/field diagnostics. Extra manifest metadata remains admitted.
- Resolve every mapping and check all required sources and filesystem boundaries before orchestration cleanup or any copy. Current valid source/target shape and direct helper calls remain supported.
- Keep sources inside the explicit project root and destinations strictly below the explicit asset root. Reject absolute/drive/rooted mapping values and parent traversal; do not change manifest syntax.
- Reject source/output overlap in either direction. Reject symlinks and Windows reparse points in involved path components and traversed source/output trees; reject multiply linked existing output files to prevent copy-through hardlink writes.
- Never suppress required cleanup/copy failure. Preserve its exception type, primary cause, native details and traceback; add factual operation/path notes. Do not log assembly success or invoke the build after any required admission, cleanup or copy failure.
- Successful real scratch assembly clears stale output, copies files/directories including dotfiles, then invokes the external build exactly once. Runtime IO failures may leave only disposable partial output.

## Nonfunctional Requirements

- Keep the C_1 production correction in scripts/build_package.py and its behavior evidence in the existing builder unit module; use standard-library validation helpers and PyYAML already in use. The separately approved test-only repair is bounded below.
- No Pydantic/runtime loader, presenter, new error framework, configurable safety bypass, automatic backup or rollback subsystem.
- No production/test private helper calls in durable tests. Test behavior through read_manifest, clean_assets, copy_assets or build_package.
- Static boundary checks do not claim protection against hostile concurrent filesystem replacement. No ACL/sandbox or filesystem transaction is introduced.

## Options

### 1. Inline suppression-only correction

Remove skips/suppression, retaining unchecked joins.

**Pros:**

- Small textual patch.

**Cons:**

- Leaves the reproduced target escape and cleanup ownership requirement unresolved.

### 2. Local preflight and ordinary exceptions

One local mapping/path admission boundary shared by direct copying and orchestration; preserve the current public utility functions.

**Pros:**

- Removes causal failure paths without changing package architecture or fixture contract.

**Cons:**

- Adds a bounded filesystem preflight pass.

### 3. Transactional staging engine

Build a new stage/promote/rollback subsystem.

**Pros:**

- Could recover prior generated output.

**Cons:**

- Outside approved scope and unnecessary for disposable assets.

## Decision

Use local preflight and ordinary exceptions. The orchestrator fixes its output root at project_root/mcp_server/assets; direct copy callers explicitly provide their own asset root, including staging outside the source repository.

## Rationale

This enforces the existing release mapping responsibility rather than redesigning it. Immutable prepared path pairs keep one authoritative admission path while allowing orchestration to validate before cleanup without repeating parsing.

## Production Design

Retain read_manifest(manifest_path: Path) -> dict[str, Any], clean_assets(assets_dir: Path) -> None, copy_assets(project_root: Path, assets_dir: Path, manifest: dict[str, Any]) -> None and build_package() -> None. Private local preparation returns tuple[tuple[Path, Path], ...] with admitted source/target pairs. A private copier consumes these pairs. copy_assets prepares then copies; build_package reads and prepares, cleans, consumes the same prepared pairs, logs success and invokes the existing subprocess. No external consumer imports new helpers.

## Test Design

Consolidate durable behavior cases in tests/mcp_server/unit/test_build_package.py. Parameterize invalid manifest families and path escapes through public entrypoints. Assert external/recovery sentinels and generated contents, exception type/cause/context and external build non-invocation. Exercise actual scratch cleanup/copy, injecting native IO errors only at the filesystem seam, and replace only the external build process. Preserve valid external staging and nested dotfile behavior. Replace the existing manifest-content/legacy assertion with behavior evidence rather than expanding content snapshots. Link/reparse coverage must execute on Windows through a junction if symlink creation is unavailable; no silent safety-case skip.

## Contracts

### Manifest admission

read_manifest owns YAML/top-level/record shape validation; copy_assets repeats that same shape validator for callers supplying dictionaries directly. Require a nonempty assets list of mappings and nonblank string source/target fields. Return the original dictionary without transformation; version and extra metadata are not reinterpreted. All records are admitted before any copy. Missing sources retain FileNotFoundError, malformed mapping/path ownership uses ValueError; unsuitable filesystem node types fail explicitly.

### Filesystem ownership

The explicit project root owns source reads; the explicit asset root owns generated writes/deletes. Mapping strings must be relative and contain no parent traversal; target '.' is invalid. Prepared source paths must remain within project_root and resolved targets strictly within assets_dir. A source may neither contain nor lie inside the asset root. Existing source/output components and trees must not traverse symlinks/reparse points; generated files with multiple hardlinks are refused. Roots may be separate siblings or staging outside the repository. A root's location alone never licenses deleting source data. clean_assets treats its explicit argument as caller-designated disposable output and refuses linked roots/descendants before removing any entries.

### Diagnostics and effects

Use ValueError for manifest/ownership admission with mapping index, field and offending path. Existing native OSError subclasses and shutil.Error propagate unchanged; Python3.11 exception notes attach operation/source/target facts while retaining complete diagnostics. YAML errors retain their native diagnostic. Cleanup preflights its output tree, then removes entries without suppression. A later IO error aborts immediately; previous disposable output removal/copies need not roll back. External build failure retains subprocess failure semantics. No success/build follows failed assembly.

## Flow

Read and admit manifest → prepare all source/target pairs and inspect ownership → clear explicit disposable asset tree → copy prepared pairs → log assembly success → invoke existing package build. Any admission/cleanup/copy exception exits that path immediately.

## Preservation

Current eleven records, direct valid helper signatures, dictionary shape, staged external output roots and hidden-file copying remain supported. Workspace/state/recovery sentinels are not disposable. No manifest or builder helper signature rewrite is needed. The owner-approved repair below adopts already-existing configuration contracts in affected test consumers.

## Validation

### Invalid required inputs never mutate output or reach build.

**Method:** Public copy/build scratch scenarios with stale output and build spy.

**Expected Result:** Explicit contextual failure, preserved sentinels, zero build calls.

### Ownership guards prevent escapes, aliases and overlap.

**Method:** Public helper/orchestrator scenarios using sibling/external sentinels and a real filesystem link/reparse point.

**Expected Result:** Failure before destructive work; valid separate staging succeeds.

### Cleanup/copy errors retain diagnosis and stop build.

**Method:** Inject PermissionError in actual cleanup/copy seams; inspect original exception and notes.

**Expected Result:** Original diagnostic retained; no success/build; only disposable partial output may remain.

### Valid assembly ordering and supported copies.

**Method:** Scratch build_package with external process substituted, plus dotfile/staging case.

**Expected Result:** Stale output removed, required bytes/dotfiles copied before exactly one build call.

## Risks

### New filesystem safety checks can accidentally reject legitimate external staging.

Keep roots explicit and test the existing fixture's separate source/stage topology.

### Filesystem can change after preflight.

State the non-concurrent mutation boundary; native subsequent IO errors remain failures. Do not claim a transactional security sandbox.

## Test repair addendum

The owner-approved repair adopts the existing configuration architecture; it does not change the production design above.

| Test seam | Contract |
| --- | --- |
| Delivered workflow configuration | Add one explicit config-only configured_workspace(tmp_path: Path, pytestconfig: pytest.Config) -> Path fixture in the existing suite_roots fixture module. It copies the current config tree, including defaults and overrides, into that test's temporary workspace. Only tests requesting it receive prepared configuration; no autouse seeding. |
| Synthetic configuration | Test setup owns complete minimal defaults when testing a custom basis; root files remain genuine overrides. Preserve intentional absent-config tests and already-migrated synthetic defaults. |
| Current consumers | Use keyed collections and id for configuration identity, values() for phase objects and explicit order for ordered entries. Label.name remains a real payload; GitHub API names do not become config IDs. |
| CLI/activation/proposal | Existing setup helpers create complete check/adapter bases and explicit check configuration_choice. Public CLI/services, exit codes, diagnostics and native tool execution policy remain unchanged. |
| Source startup | Fix the proven root-YAML-only in-process fixture by copying the whole config tree. Keep the separate successful source-handshake path unchanged unless a concrete fixture cause is demonstrated; do not increase timeouts speculatively. |
| Proof | Reuse existing failing behavioral tests as repair evidence; no duplicate regression suite or source-string assertions. Existing failure reports remain inspectable. A new production cause is a stop, not permission to redesign. |

## Planning Consequences

One compact implementation cycle can own production and corresponding behavioral tests. Use strict RED/GREEN for changed behavior as required by the bug workflow. Focus implementation tests/checks; reserve the required native-configured full suite and branch checks for Validation. Do not import the #504 waiver. Stop for a real strategy contradiction rather than broadening into a filesystem framework.

## Related Documents

- [Approved Research](<research.md>)
- [Builder](<../../../scripts/build_package.py>)
- [Existing tests](<../../../tests/mcp_server/unit/test_build_package.py>)
- [Architecture principles](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-16 | @imp designer | Define bounded admission, path ownership and original-exception contracts. |
| 0.2 | 2026-10-16 | @imp planner | Bound the owner-approved test-only adoption of existing config contracts; production design unchanged. |

