<!-- docs/development/issue460/rollout-rehearsal.md -->
<!-- template=generic_doc version=43c84181 created=2026-09-17T16:47Z updated=2026-09-17 -->
# CY071: Target Startup Composition and Launch Rehearsal

**Status:** PREREQUISITES REPAIRED — CY071 OPEN  
**Version:** 1.0.2  
**Last Updated:** 2026-09-23

## Purpose

Record the interrupted CY071 takeover, verified prerequisites, unfinished work, and the evidence needed before launch rehearsal can continue. This is not a successful rehearsal or cutover authorization.

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
- This repair does not fulfill CY071.D1/D2. Target bootstrap composition, isolated installed candidate startup, candidate readback rehearsal, and the planned normal-dispatch diff remain open under CY071.

## Unfinished takeover work

The previous agent left modified `bootstrap.py` and state plus untracked process support, startup tests, and this report. Production startup was not repaired during this takeover. Its independently identified issues remain:

1. Placeholder generation fingerprints instead of identities derived from admitted source bytes.
2. A renderer environment without a loader; immutable catalog rendering is not yet wired.
3. Missing installation compatibility validation in target startup.
4. Target construction still depends on legacy configuration/managers and fabricates a registry after a broad exception.
5. Scratch-root wiring does not use the central validation directory.

The process fixture was changed to accept explicit command/CWD/environment and drain stdout/stderr with bounded waits. This is **unfinished, unverified work**: inherited startup tests still use its old invocation API and must be adapted before the complete file can run. At the 2026-09-17 takeover, only the two then-present migration regression cases were run. The durable replacement now lives in the existing renewal integration test. No successful startup, separate installed candidate, normal-entrypoint switch, immutable-catalog rehearsal, or candidate readback migration is claimed.

## Resume and recovery boundary

The named prerequisite corrections were completed and reviewed on 2026-09-23. Resume with the actual CY071 startup composition and isolated installed rehearsal under its approved write-set. Reuse the focused passing migration regression and preservation tests; do not add an unrelated test campaign.

The normal entrypoint and running server were not switched. The 2026-09-17 takeover made no commit, cycle transition, deployment, or server restart. The later blocker repair has separate RED and GREEN commits; CY071 is still active. Existing work and the runtime lock were preserved. Do not reset the branch or remove inherited untracked files: dirty preimages were not captured before the other agent began CY071, so a complete cycle-owned inverse is not yet available.

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
