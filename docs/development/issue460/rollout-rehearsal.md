<!-- docs/development/issue460/rollout-rehearsal.md -->
<!-- template=generic_doc version=43c84181 created=2026-09-17T16:47Z updated=2026-09-17 -->
# CY071: Target Startup Composition and Launch Rehearsal

**Status:** CY071 EVIDENCE READY FOR INDEPENDENT QA  
**Version:** 1.0.5  
**Last Updated:** 2026-09-23

## Purpose

Record the CY071 startup composition, isolated installed candidate rehearsal, verified prerequisites, and remaining release conditions. This is not cutover authorization.

## Blockers identified on 2026-09-17

| Owner | Finding | Required correction before CY071 resumes |
|---|---|---|
| CY064/CY066/CY067 renewal preparation | [cli_renewal.py](../../../mcp_server/cli_renewal.py) selects managed `template_suite`; [TemplateRenewalService](../../../mcp_server/services/template_renewal.py) treats its absence as fresh without distinguishing an existing legacy installation. The force route also rejects absent V3 actual content. | Preserve the legacy installation, return `checkpoint_required` on ordinary first upgrade, then support explicit owner migration with verified legacy backup. Do not disguise legacy migration as fresh initialization. |
| CY068 workflow preparation | [Prepared workflow input](rollout-workflow-input.md) retains obsolete `name`, `run_tests(path=...)`, `scope='full'`, `scope='files'`, and `verbose=True` invocations. | Reconcile instructions with the actual target input models before preparing the exact candidate patch. |
| CY069 host preparation | [Prepared host input](rollout-host-input.md) advertises invalid safe-edit fields and invalid `bindings`, `options`, and `files` parameters. Three AGENTS diff hunk headers describe four lines while containing five. | Correct the prepared source patches and their exact application evidence before candidate installation. |
| CY068 byte-level input | The recorded workflow postimage hash assumes complete LF normalization; preserving existing CRLF gives `d6ab256ffc19b6b96b9ea4e7a47b24b2c86b70ce26aa952da6f500e49a6a0e3b`. | Specify the exact byte convention and matching pre/postimages rather than silently normalizing during activation. |

These findings were independently checked by a delegated read-only reviewer. That review is findings-only, not workflow GO/NOGO. [CY071's stop boundary](planning-rollout.md#cy071) requires returning mismatched preparation to its owning cycle.

On 2026-09-17 the owner chose **“Leg blokkade vast en stop hier”**. On 2026-09-23 the owner explicitly authorized repairing the CY071 blockers first; the later instruction supersedes that stop for this bounded prerequisite work.

## 2026-09-17 takeover evidence

- Current branch: `refactor/460-audit-scaffolding-schema-template-contracts`.
- Takeover HEAD: `275f27f0659c6a41fb29842129612fa593e024df`.
- Stored project plan read completely through the MCP cache windows; contiguous offsets, 161524 Unicode codepoints and SHA-256 `dab2d2b3b02dc8dcff1838ffa34d23b516eb945777b9baacacd1017c88121d6d` verified.
- One focused PGMCP call:
  `run_tests(path="tests/mcp_server/integration/test_target_startup.py::test_first_legacy_upgrade_requires_explicit_migration", timeout=120, verbose=True)`.
  Result: **0 passed, 2 failed, 0 errors**, exit 1, 36.58 seconds.
  Cached DTO read: `pgmcp://cache/runs/8f8cb06caf28479a9a7b90ecb4ba7a03`.
- The two regression cases assert the required ordinary-upgrade refusal and explicit force-migration backup. They use an isolated temporary legacy tree and the real prepared renewal composition.
- Evidence limitation: the cached failure tracebacks contain xdist progress lines rather than assertion details. The failed counts are confirmed; the causal classification above is supported by source inspection. No speculative runtime outcome is claimed.
- All eight CY069 mapped source/copy pairs are byte-identical. Six recorded host preimages match, and literal intended text replacements yield their recorded postimages. This does not validate the invalid hunk headers or public invocations.
- The lazy cache guide agrees with the current presenter/configuration and packaged resource. No independent fresh-agent discovery rehearsal was completed.
- No full suite, branch-wide gates, or additional reruns were performed after the stop decision.

## Blocker repair, 2026-09-23

- Renewal now distinguishes an existing managed legacy root from a fresh installation. Ordinary upgrade stages the admitted V3 candidate and returns `checkpoint_required` while preserving legacy bytes. Explicit managed force migration backs up `.pgmcp/templates/`, including empty directories, and `.pgmcp/.version` outside the active root. It verifies files and directories before activation and records their facts for interrupted recovery. External roots remain ineligible for forced replacement. A pre-existing backup-name collision is preserved.
- [Prepared workflow input](rollout-workflow-input.md) now has 33 exact source-matching hunks with all changed V3 `run_tests` calls represented as deletions/additions. Its recorded LF postimage hash is `008a84d242a7fc5c3d56f211553348d5a820905874bf237dab42f90c01f2ce50`.
- [Prepared host input](rollout-host-input.md) now uses the target V3 input names. All six host diffs match their recorded source preimages and apply at exact line positions. The three corrected AGENTS postimage hashes use CRLF-preserving raw-byte application and are recorded in that document.
- Focused `run_tests` on the new legacy migration regression, existing fresh and V3 force paths, fresh activation, backup collision, and four interruption recovery cases: **9 passed, 0 failed**; cached result `pgmcp://cache/runs/70ce3959074843779718554d119a9b5c`.
- File-scoped `run_quality_gates` on the three production files and renewal integration test: **all applicable gates passed** (Ruff format/lint, imports, line length, Pyright, mypy); cached result `pgmcp://cache/runs/08ebbd028f9d44389a13eb33e200a535`.
- Independent findings-only reviewer rechecked migration ownership, backup and recovery facts, exact prepared diffs/hashes, and V3 signatures; **no remaining material finding** in this bounded repair. This is not independent workflow GO/NOGO.
- The prerequisite repair was a separate bounded episode. CY071 startup composition and installed candidate evidence are recorded below.

## CY071 target rehearsal, 2026-09-23

`bootstrap_target()` now explicitly reads the target root, installation checkpoint and V3 configuration under the DI-06 lock, admits one immutable template/catalog snapshot, derives source identities, and composes the six V3 schema/mutation/check/test/fix tools with unchanged unrelated tools. `bootstrap()` remains the legacy normal entrypoint. The candidate uses an isolated source copy and wheel; only that copy applies the prepared `cli.py` dispatch, configuration and `[tool.pyright]` changes. The live CLI, configuration and TOML remain unchanged.

The candidate test initializes an independent workspace, performs a real stdio MCP handshake, checks unique V3 tool names, reads a large stored planning result through cache windows with a SHA-256 check, resolves the candidate's actual budget-triggered `pgmcp://docs/cache-reading` hint, and verifies that an admitted schema remains available after its source manifest is temporarily renamed. It then exercises ordinary legacy-upgrade refusal, explicit owner-force migration, and a second real handshake. Target unit/integration checks cover lock exclusion and unresolved-recovery refusal. Focused startup/config tests: **18 passed**, `pgmcp://cache/runs/55b397973b084be485bae83b996457f4`; installed-candidate readback, cache hint, six exact host patches and packaged-asset parity: **1 passed**, `pgmcp://cache/runs/c45879105823461580df81addb7831f3`. Focused prospective configuration tests: **11 passed**, `pgmcp://cache/runs/c13d37b35d5d47cb9e9a2ae928a67b3e`. File-scoped quality gates on seven affected code/test files passed after the package-data correction, `pgmcp://cache/runs/079af2ea0bbd4995bdd347c50ffb07ad`. The latter supersedes the earlier installed-candidate-only pass `pgmcp://cache/runs/fa7587e2909e4264b1351d66357abc41`.

Exact rehearsed live input SHA-256 values: `mcp_server/cli.py` `c78e86beb0294ce8e9ac890338e55d5842861ac526743b7d3588d8f8856271dc`; `pyproject.toml` `e91b9079e91c2c7ea4c43433c0e635053533696016dfb16160624c994e3cd66f`; `.pgmcp/config/artifacts.yaml` `e17c98ebd7bc03771ea0b7faab55b05b9b02b16d0b5c34cada21443c962f5157`; `.pgmcp/config/presentation.yaml` `2a51cbf0d6a62cb92b6ba2d302477410de299104185da4170aa64dfa67f70217`; `.pgmcp/config/release_manifest.yaml` `564dd20dccfde4229e73a5888ed55f9367e18a402fba14d785c13d2a54162f3b`. The prepared presentation postimage is `d03744fc142852abe4e5eac53bbf2d04f374f44916fa11fc82121e59320b8e33`; the prepared `pyproject.toml` LF postimage, including the explicit hidden `.github` agent-asset package-data glob, is `6d3fe1e3738140a3699c1664894e06e00ff38b3d7a88e206097bf7b46cdedaae`. The candidate CLI substitutions use exact single-occurrence preimages in `test_target_startup.py` and fail on drift. The `[tool.pyright]` deletion is likewise exact; the focused configuration tests recheck preserved native values.

The R004/R005/R006 test-source rehearsal now runs against a separately installed candidate. The exact live preimage SHA-256 values are R004 `0fcf8f42276c80e2ee109a49ed72cdd1f3eaeb1873bf7e3d20d3dd2ae55f517f`, R005 `13312592a6a8e7aaf30de69ade42f878a3c9d5ed10291c4fee74c54f3b3384ed`, and R006 `efa2500e004ea5e83f200493cca1c92ef4876682bbe66ede7cf80309a46513e1`. R004/R005 need no semantic hunk: selected stored-plan, invalid-query-byte and command-recovery tests run unchanged with isolated candidate config. The isolated R006 copy acquires the installed `assets/template_suite`, writes a matching version-only installation state, selects that suite root and `bypass_version_check=False`, and changes its two direct `bootstrap()` calls to `bootstrap_target()`; every save/update/fresh-cache/full-window assertion remains unchanged. These changes use exact single-occurrence preimage replacements in `test_target_startup.py`; the live R004/R005/R006 bytes remain unchanged for CY072. Focused nested candidate result: **15 passed**, outer PGMCP result `pgmcp://cache/runs/01e3112aa6504f1c8c5c419c56479b85`. The unchanged live R006 tests also passed, **2 passed**, `pgmcp://cache/runs/4b63ef2913db441b974e09af9dba0010`. File-scoped quality gates on the rehearsal test passed, `pgmcp://cache/runs/241f4d5432d44be783fc22c6b634ccca`. All six CY069 host instruction patches were applied with exact preimage and postimage hashes to isolated candidate sources, then byte-compared with their packaged `mcp_server/assets/agents` destinations; the live host files remain unchanged. Independent findings-only QA identified three stop conditions before the subsequent owner decision: isolated R004/R005/R006 source-hunk rehearsal was missing; dirty intermediate preimages were unavailable; and the schema-reference and CY070 input corrections were outside the original CY071 write-set. The owner explicitly resolved the latter two on 2026-09-23 as recorded below. QA did not verify a code defect, run tests, or independently read the cached results. No live activation, server restart or phase transition has occurred.

## Owner decision, provenance, and recovery boundary

On 2026-09-23 the owner explicitly added two bounded corrections to CY071 scope: the schema-reference edge capture in `mcp_server/services/template_contract_loader.py` (original owner CY003), and the prospective configuration/package corrections in `docs/development/issue460/rollout-config-input.md` plus `tests/mcp_server/integration/test_rollout_configuration.py` (original owner CY070). Commit `677b291489092d1d4e202dde6a74016c7658fb2c` names both additions and their original CY003/CY070 ownership for provenance. This decision does not authorize unrelated changes in those files.

The last commit before CY071 was `275f27f0659c6a41fb29842129612fa593e024df`, not `a84ff8ed05ccdbdd1afb8a42f0ead8fb2502bafc` as an earlier draft incorrectly stated. The owner formally accepts that committed pre-CY071 state as the source-code recovery baseline, including the loss of later CY071 work if that baseline is ever chosen. Four verified later Git checkpoints exist: `e88aa3489031dc4c226a99258c8d96d3530bb888` (legacy-migration regression), `2f8f4e39461a4d384370a069ddb072ad87f4a7f3` (migration and prepared-contract repairs), `a84ff8ed05ccdbdd1afb8a42f0ead8fb2502bafc` (repair evidence), and `677b291489092d1d4e202dde6a74016c7658fb2c` (target startup, installed rehearsal and owner-approved scope corrections). At the first target rehearsal, `677b291489092d1d4e202dde6a74016c7658fb2c` was the nearest committed checkpoint; the subsequent candidate readback test-source rehearsal is recorded by a separate CY071 commit. The intermediate dirty bytes before this continuation were not recorded and are not asserted recoverable.

CY071 has no live dispatch or installation activation to roll back. Its Git checkpoints are optional source-code recovery choices if implementation evidence fails; use a reviewed, scoped revert of cycle-owned changes while preserving unrelated state. `.pgmcp/template_upgrade.lock` is operational state, not a cycle-owned source artifact. CY072's later live activation needs a different recovery route: if MCP cannot start, stop the launcher and use verified code/config/suite and installation backups plus the DI-06 activation journal and renewal recovery command described in [DI-06](design-distribution.md). Do not hand-edit an installation checkpoint or clear the lock. The remaining CY071 release action is independent QA on the final evidence and its commit, followed by the prescribed cycle transition only if that review permits it.

## Related documentation

- [CY071 approved scope and stop conditions](planning-rollout.md#cy071)
- [DI-06 migration and recovery contract](design-distribution.md)
- [Prepared workflow input](rollout-workflow-input.md)
- [Prepared host input](rollout-host-input.md)
- [Prepared configuration input](rollout-config-input.md)

## Version history

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0.0 | 2026-09-17 | Prior implementation agent | Initial draft |
| 1.0.1 | 2026-09-17 | @imp implementer | Record takeover blockers, focused failed evidence, unfinished work and owner stop decision |
| 1.0.2 | 2026-09-23 | @imp implementer | Record bounded prerequisite repair, focused evidence, and remaining CY071 work |
| 1.0.3 | 2026-09-23 | @imp implementer | Record installed target startup/readback evidence, hashes, open rehearsal requirements and recovery limit |

| 1.0.4 | 2026-09-23 | @imp implementer | Record owner-approved CY071 scope additions, corrected Git checkpoints, and pre-CY071 recovery baseline |
| 1.0.5 | 2026-09-23 | @imp implementer | Record isolated installed-candidate R004/R005/R006 rehearsal and focused evidence |
