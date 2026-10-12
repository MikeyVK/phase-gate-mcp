<!-- pgmcp:v1 id=research pv=1.0.0 pf=lgBwxWMfTAmNNg_O sf=zJbLuUrs_I33kpX4 -->

# Issue 470 — Safe-edit LF policy

**Status:** Research complete; independent review requested  
**Version:** 1.0  
**Last Updated:** 2026-10-11

## Purpose

Resolve the observed mismatch between content_changed and persisted bytes with a small coherent text policy.

## Scope In

All four safe-edit operations, their construction/service/reader boundary, direct tests and the active editing reference.

## Scope Out

Scaffolding output, adapter/check architecture, generic writer behavior, Git/editor configuration, bulk workspace conversion, compatibility layers and historical-document reconciliation.

## Problem Statement

Safe-edit constructs edits on universal-newline text but reconstructs source terminators and reports change from an intermediate text. One existing case explicitly reports changed=true with identical persisted bytes; exact rewrite can conversely change CRLF to LF while its logical comparison is unchanged.

## Goals

- Use LF consistently for every completed safe-edit proposal.
- Keep check-input/write-input identity and exact-original-byte race protection.
- Remove preservation-only machinery and redundant test cases rather than add another text model.

## Background

The #460 CY110 amendment on 2026-09-27 explicitly retained source line endings for targeted edits and exact caller rewrite, while retaining logical change reporting. Commits 937149bf and 5bc44c1f introduced source-span reconstruction and the unchanged-logical shortcut. The associated QA correction and D-VAL-02 explicitly deferred the remaining reporting inconsistency. This is an intentional policy replacement, not evidence that those approved checks failed.

## Findings

| Boundary | Current responsibility and evidence | Impact |
|---|---|---|
| Original reader/snapshot | One byte read, universal-newline text and source-preserving text | Keep original bytes and normalized text; source-only preservation view has no consumer outside reconstruction |
| Construction | Four operations, immutable patches, logical/physical proposal and terminator mapping | Preserve operation matching/cardinality; remove mixed-terminator reconstruction |
| Edit service | Profile selection from original; check and writer both receive physical_text; changed compares logical_text | Keep orchestration/admission; report actual proposed byte difference |
| Writer | UTF-8 encoding, staging, original-byte guard | Remains verbatim; no policy/normalization here |
| Composition/tests | bootstrap injects construct_edit_proposal; two integration harnesses use it; construct_edit is used only by unit tests outside proposal | Cut over actual consumers, avoid a second construction authority |
| Public DTO/tool/presentation | Same four operation shapes; content_changed exists only on completed writes; ordinary success presents written/validation | No new flags or fields; clarify changed semantics in DTO/reference |

Source searches covered mcp_server, tests, .pgmcp/config and .vscode for construct_edit/proposal, logical/physical/source text and content_changed. No production decision consumer of content_changed was found. The writer test suite protects race and persistence behavior; existing construction/integration/public tests cover operations, policy failures and source selection. Preservation-specific cases intentionally encode obsolete policy and should be replaced or removed, not retained as legacy rejection tests.

| Strategy | Cost / consequence |
|---|---|
| Preserve mixed-source model and repair reporting only | Small immediate change but retains terminator mapping, tie policy and separate rewrite semantics; rejected by owner preference |
| One LF output policy within existing construction boundary | Removes reconstruction and simplifies reporting; first successful edit may normalize the entire file, including a no-match edit |
| New edit-plan architecture or configurable per-file modes | Larger surface without a demonstrated need; excluded |

## Questions

## References

- [CY110 approved historical amendment](<../issue460/design-mutation-validation.md#cy110-line-ending-preservation-amendment-2026-09-27>)
- [CY110 historical execution and QA](<../issue460/planning-rollout.md#cy110-completion-evidence-d1d4-2026-09-27>)
- [Construction](<../../../../mcp_server/services/edit_construction.py>)
- [Service](<../../../../mcp_server/services/edit_operation.py>)
- [Reader and writer](<../../../../mcp_server/utils/atomic_file_writer.py>)
- [Existing behavior tests](<../../../../tests/mcp_server/integration/test_edit_operation_v3.py>)
- [Active editing reference](<../../../reference/tools/editing.md>)

## Approved Strategy

Owner authorization in this chat: execute Research through Ready autonomously; use LF consistently; clean break with no legacy paths/compatibility bridges; adapt/run focused behavior tests and shrink the final suite; no retained regression tests for old behavior. Independent Beoordeel designplan is used only for phase-transition GO/NOGO.

| Boundary | Approved strategy |
|---|---|
| Text policy | Every successful safe-edit proposal, including rewrite and no-match, uses LF. CRLF and CR are accepted as input and normalized, not preserved. Initial normalization is an intentional whole-file byte change. Literal search/anchor/pattern operands use the same newline convention; regex patterns and replacement syntax retain Python regex semantics, with final emitted text normalized. No Unicode normalization or automatic final-newline policy is added. Existing append separator behavior remains after text normalization. |
| Public input/output | Preserve DTO shape, matching cardinality, validation policies and failure contracts without aliases. content_changed means final UTF-8 bytes differ from the original invocation bytes; null still means no completed write. written retains completed replacement meaning; no skip-check/write optimization. Exact CRLF rewrite is deliberately superseded. |
| Internal contracts | Remove source-preservation-only snapshot/proposal fields and consumers in one cutover. Keep one authoritative construction route. No migration or alternate preservation mode. |
| Safety/checks | Keep one original read, original profile selection, identical final check/write text, original-byte guard, locks, error/cleanup outcomes. No normalization in writer or adapters. |
| Workspace policy | This issue governs safe-edit writes. Git/editor changes after the call remain external; no machine/global configuration mutation or automatic conversion of unrelated files. |
| Tests | Adapt existing behavior coverage and delete obsolete preservation/redundant cases. No new test files, old-policy regression suite or broad test rewrite. Broad required verification belongs to Validation, once after implementation; phase QA reuses fresh evidence. |

## Expected Results

All four operations produce one LF proposal. A CRLF/mixed input normalization reports changed=true; repeating the same resulting operation can report false where text is unchanged. Check input equals persisted UTF-8 bytes. Blocked checks and original-byte races never claim a completed write. Mixed-terminator reconstruction and unused source views are absent. Existing operation, validation and safety coverage remains with a non-growing focused suite.

## Consumers

### EditOperation and bootstrap

Construction injection, validation and persistence

**Impact:** Internal constructor return contract cuts over once.

### Existing construction, edit operation/public and Markdown integration tests

Operation and boundary behavior

**Impact:** Adapt valuable cases; remove preservation-only cases.

### Agents and external safe-edit callers

Supply operations and interpret response

**Impact:** Same input shape; explicit LF output and byte-change meaning.

## Risks

### First edit of a CRLF/mixed file may create a broad line-ending diff.

Document intentional normalization; do not hide it in content_changed.

### Regex escapes are executable syntax rather than literal newline characters.

Keep regex interpretation native and normalize emitted text; prove behavior through existing focused cases.

### Moving normalization after validation would invalidate evidence.

One final proposal is shared by checks and writer; retain direct integration assertions.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-11 | @imp researcher | Record bounded source/history evidence and owner-approved LF clean break. |
