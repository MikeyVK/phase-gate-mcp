<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue 505 — Fail-closed asset assembly

**Status:** RESEARCH — STRATEGY APPROVED, QA REQUESTED  
**Version:** 0.3  
**Last Updated:** 2026-10-16

## Purpose

Establish bounded defect evidence and a small existing-builder safety strategy before Design.

## Scope In

Malformed required mapping data, required source/cleanup failures, truthful assembly outcome, disposable output ownership and direct helper/test consumers. The owner-approved repair below additionally covers test preparations and consumers of the existing configuration contracts.

## Scope Out

Neutral content routing, new manifest grammar, configuration layering redesign, staging/transaction frameworks, distribution/upgrade redesign, #506/#507/#508 work, warning cleanup, release/version bump/deployment.

## Problem Statement

The manual package assembly script can silently skip malformed mappings and suppress required cleanup failures, then report successful assembly and invoke the build. Uncontained target joins also permit a scratch reproduction that writes outside the asset root. No contaminated wheel or production data loss has been observed.

## Goals

- Demonstrate actual failure paths and distinguish already-correct missing-source behavior.
- Bound the valid-data/exception/filesystem strategy without replacing the current build architecture.
- Map only direct consumers and meaningful behavior-test impact.
- Obtain explicit human strategy approval before Design.

## Background

Issue319 recorded build/content-policy concerns but deferred their implementation. Issue504 changed configuration source ownership while explicitly leaving the builder and release manifest opaque; its merge9b17132d is the current baseline. Current505 is the independent fail-closed safety bug, not the entire deferred distribution project.

## Findings

## Observed failure paths

| Case | Reproduction scope | Observed result | Meaning |
| --- | --- | --- | --- |
| Missing required mapping fields | copy_assets with {}, source-only and target-only records | Returns normally; no copy | A malformed required record is silently skipped |
| Required file/directory cleanup denied | Real clean_assets/rmtree, injecting PermissionError at shutil.os.unlink on scratch entries | Returns normally; loose file and nested file remain | Both suppression routes conceal failed cleanup |
| Malformed manifest through orchestration | Real scratch manifest/cleanup/copy; module __file__ points only to scratch project; external subprocess.run is mocked | Logs Assets compiled successfully and invokes the mocked build once | An invalid assembly can be represented as success; no wheel was actually built |
| Missing required source, fields present | Real scratch manifest with source=missing and target=copied | FileNotFoundError; external build not invoked; generated cleanup already happened | Explicit missing-source failure exists; early validation is incomplete |
| Target escapes asset root | Scratch input.txt to ../../.pgmcp/state.json from project/mcp_server/assets | Scratch state sentinel is overwritten outside assets | Containment is an actual related safety gap, not a reproduced production incident |

All writes and deletes in the observations were limited to disposable pytest scratch. The real repository's assets, state and recovery material were untouched. The external package build was mocked. These five passing observation cases describe current defects; they are temporary research probes, not tests to retain for the old faulty behavior.

## Root cause and current protection

clean_assets deliberately uses rmtree(ignore_errors=True) and suppress(Exception) around unlink. copy_assets continues when source or target is false-like, and joins authored paths without containment or overlap validation. build_package reads the raw manifest, clears generated assets, copies, reports successful assembly, then invokes python -m build. read_manifest checks only that YAML yields a dictionary. Malformed structural types may raise ordinary Python errors; they are not all silent-success cases.

The active manifest has eleven ordinary source/target records and remains outside any grammar redesign. Every active record uses repository-relative sources and asset-relative targets. Valid directory copying preserves nested dotfiles, already covered by existing tests. The packaging backend is setuptools; the assembly script is a manual preparation command, not an automatic PEP517 hook.

The asset directory is generated and ignored except .gitkeep. That identifies intended disposable material but does not itself enforce path ownership. Target traversal is already reproduced. Cleanup of an aliased root and source/destination overlap remain code-level hazards requiring a strategy decision, not claims of observed data loss.

## Proportional impact

| Surface | Direct relationship | Expected scope |
| --- | --- | --- |
| scripts/build_package.py | Three helpers and the sole assembly orchestrator | Required-data admission, failure propagation and disposable-target safety |
| tests/mcp_server/unit/test_build_package.py | Six current tests | Adapt/add behavior evidence by failure family; preserve valuable copy/dotfile behavior |
| tests/mcp_server/fixtures/installed_distribution.py | Imports read_manifest and copy_assets; builds only in isolated source/staging trees | Preserve valid helper call contract; inspect focused fixture consumer if admission changes |
| tests/mcp_server/integration/test_target_startup.py | Reads manifest and stages current sources | Preserve valid manifest data shape; do not invoke full wheel scenarios merely for Research |
| .pgmcp/config/release_manifest.yaml | One authoritative asset list | Keep existing grammar/content routing; no neutrality/content transform |
| pyproject.toml | Setuptools packages assembled assets and bundled adapters | No build-backend/dependency/version change proposed |
| Release/setup references | Document manual assembly and generated assets | Later bounded reconciliation of failure and ownership guarantees |
| Runtime managers/tools, enforcement, agent workflows | No direct call to these assembly helpers found | No runtime loader, presenter, tool-schema or workflow change justified |

No per-test factory rewrite or runtime dependency-injection refactor is indicated. The large #504 fixture cutover is not a precedent for this issue.

## Strategy assessment and owner decision

| Boundary | Small proposed strategy | Larger alternative / cost |
| --- | --- | --- |
| Invalid mapping and source admission | Preserve assets/source/target shape and valid helper entrypoints; reject malformed required data and absent sources before destructive work where possible; no compatibility path for silent skips | New manifest grammar/model/config layering is excluded and unnecessary for the evidenced bug |
| Failure diagnosis and build outcome | Propagate original IO/native exceptions with operation/path context and original cause; stop before success/build; reuse ordinary script failure exit behavior | A new error DTO/presenter framework has no consumer here |
| Disposable filesystem boundary | Explicitly delimit generated assets; reject escaping/overlapping paths and unsafe linked cleanup endpoints; never modify source/workspace/recovery material | Defer the newly evidenced path hazard, leaving the preservation claim narrower |
| Partial output after runtime IO failure | Stop with failure; allow disposable partial output to remain for diagnosis; do not build or report success | Full staging, atomic promotion, backups and rollback increase scope and are not proposed |

The owner approved the small strategy, including path-boundary enforcement, on 2026-10-16 after the concrete target-escape explanation. Current valid mappings and callers remain supported; unsafe formerly accepted paths deliberately fail. The larger alternatives above are not selected.

## Research checkpoint

Issue505; branch bug/505-fail-closed-asset-assembly; parent main; bug/Research; implementation baseline is merged9b17132d5fe1377860aca45b375a0b49f4ede791. No production or permanent test changes. Six existing unit cases and five isolated observational cases passed. No broad test/check run, actual package build, release or deployment. No #505 QA verdict exists yet. The owner's direct instruction on 2026-10-16 approved the proposed targeted fixes; Research now awaits independent QA for Design admission. The #504 targeted-only exception is not reused as a #505 Validation waiver; later required scope must be resolved in this issue's approved plan.

## Questions

None requiring an owner decision. Design must specify concrete admission, path ownership and error contracts within the approved boundaries.

## References

- [Build script](<../../../scripts/build_package.py>)
- [Current build behavior tests](<../../../tests/mcp_server/unit/test_build_package.py>)
- [Installed-distribution fixture](<../../../tests/mcp_server/fixtures/installed_distribution.py>)
- [Release assets procedure](<../../reference/release-assets-procedure.md>)
- [Issue 319 deferred boundary](<../issue319/deferred.md>)
- [Issue 504 source/assembly separation](<../issue504/research.md#managed-basis-activation-and-distribution>)
- [Architecture principles](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)

## Approved Strategy

Approved by the owner on 2026-10-16: "pak de fixes die je nu voorstelde gericht op en ga verder", with explicit direction to reject paths outside the configured boundaries with a clear diagnostic.

| Boundary | Approved decision |
| --- | --- |
| Manifest and helper consumers | Preserve the existing assets/source/target format and valid helper calls. Reject malformed required mappings and missing sources; no compatibility bridge for silently skipped invalid data. |
| Failure outcome | Required cleanup/copy failures terminate assembly with operation/path context and the primary cause retained. No success message or build invocation after failure. Use ordinary script exceptions, without a new presentation framework. |
| Filesystem ownership | Enforce source and generated-target boundaries, including escaping/overlapping paths and unsafe linked cleanup endpoints. Preserve source, workspace and recovery material. The current eleven ordinary mappings remain valid. |
| Partial output | Runtime IO failure may leave disposable partial generated output, with an explicit failure and no build. No staging transaction, backup or rollback subsystem. |
| Test and change scope | Focused behavioral coverage in the existing builder unit module; retain valuable valid-copy/dotfile coverage. No manifest redesign, content-routing logic, runtime consumer refactor, release or deployment. |

This approval authorizes bounded implementation through the normal independently reviewed phase gates; it does not grant a new full-suite waiver.

### Owner-approved bounded test repair after Validation FAIL

On 2026-10-16 the owner explicitly approved repairing fixtures/consumers and investigating the seven CLI exit failures plus one source-handshake timeout, with independent QA and no gate exception. The owner separately approved force_phase_transition back to Planning after the ordinary backwards transition was rejected. The force operation skipped zero gates; it does not waive the failed suite.

| Boundary | Additional binding decision |
| --- | --- |
| Current configuration consumers in tests | Adopt the existing defaults, keyed collections, id and order contracts directly; no support for old shapes. Keep runtime behavior and the C_1 builder implementation unchanged. |
| Test filesystem preparation | Provision config explicitly in opted-in fixture/setup commands. Loaders, read helpers and factories do not acquire implicit writes or fallback roots. Keep intentional absence and synthetic complete bases intact. |
| Seven CLI failures | They are in-process RenewalCli calls, not subprocess failures. Their common renewal_case fixture copies only checks/adapters overrides; real admission first requires defaults/checks.yaml. Repair that explicit preparation and retain each scenario's behavioral assertions; a post-repair pass is still required. |
| Source handshake | The source process helper already copies config recursively, including defaults. One delegated targeted run of the unchanged test returned python_tests: passed (caller selection); detailed native counts/timing were unavailable. Original full-suite timeout remains unexplained. No timeout, production or environment workaround is justified by that observation. The required full rerun remains the decisive check. |
| Scope and stops | Repair existing failing fixture/consumer surfaces only. No new production behavior/architecture, gate exception, reduced native selection, skip, broad suppression or general warnings cleanup. A newly demonstrated production cause outside scope requires an owner decision. |

The complete failed suite remains historical evidence in [Validation](validation.md). There is no main-baseline comparison and no blanket claim that every failure predated #505. No additional tests are required solely to record this repair; preserve valuable existing behavioral coverage.

## Expected Results

Malformed required data and unsafe paths fail explicitly; a required cleanup/copy failure preserves its primary cause and prevents assembly success/build invocation. Valid current mappings retain copy behavior and dotfiles. Source/workspace/recovery material remains untouched. Claims are limited to this assembly entrypoint; direct external builds and distribution content policy are outside this issue.

## Evidence

### Existing baseline passes but omits the defect families

All six current unit tests passed. They prove happy-path cleanup/read/copy, existing missing-source failure and dotfile preservation, but do not challenge cleanup denials or skipped required fields. Existing SchemaAttachment.schema-shadow warnings were emitted by the shared test environment.

- [Current build behavior tests](<../../../tests/mcp_server/unit/test_build_package.py>)

**Invocation:** run_tests(scope='targets', targets=['tests/mcp_server/unit/test_build_package.py'], tests=['python_tests'], timeout_seconds=180)

**Observed Result:** 6 passed,9 warnings; no broad scope.

### Five bounded observations confirm the causal paths

The five scenarios in the findings table passed as observations of the current script. Probe cleanup injected PermissionError beneath actual shutil.rmtree and Path.unlink. Orchestration used a scratch project manifest and only mocked the external build. The traversal case changed only a scratch .pgmcp/state.json sentinel. Inputs, patches and observed outcomes are recorded above so a transient run/cache is not the evidence authority.

- [Build script](<../../../scripts/build_package.py>)

**Invocation:** run_tests(scope='targets', targets=['.pgmcp/temp/artifacts/issue505/test_issue505_observation.py'], tests=['python_tests'], timeout_seconds=180). Probe was scaffolded through pytest_unit_test and is ignored research scratch.

**Observed Result:** 5 passed as pre-fix observational probes; no real wheel/build or production mutation.

## Risks

### Suppressing only the two cleanup calls leaves target writes outside the disposable root possible.

The owner approved containment/ownership safeguards; Design must make the boundary concrete without expanding into a general filesystem framework.

### Atomic assembly can turn a small safety bug into a distribution redesign.

Present explicit partial-output/failure semantics; defer staging, recovery and neutral asset routing.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-16 | @imp researcher | Record existing-builder failure evidence, direct impact and bounded strategy options for owner decision. |
| 0.2 | 2026-10-16 | @imp researcher | Capture direct owner approval for the targeted fail-closed, path-safety and partial-output strategy. |
| 0.3 | 2026-10-16 | @imp planner | Record owner-authorized bounded test repair and the separate force re-entry, with no gate exception. |


