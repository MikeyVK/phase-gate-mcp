<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=QEtFztWtFehT8R5U sf=9PfER5JkyAoFQLRi -->

# Issue 469 — Documentation and Separate Disposition

**Status:** Completed — independent Documentation review requested
**Version:** 1.0
**Last Updated:** 2026-10-02


## Purpose

Index the active execution guidance and preserve separate issue 469/474/475 disposition under the approved development contract.

## Scope In

Current internal adapter contract, public operator guidance, scoped guarantees, tested boundaries and coordination hand-off.

## Scope Out

External migration, legacy adapter routes, OS confinement, release installation work and issue closure authorization.



## Summary

The active execution reference documents the one directly corrected unreleased identity-1 contract. Public callers retain the live tool schemas; PGMCP injects the mandatory internal JSON context. The guidance describes ownership, complete native transports, actual prerequisites, truthful results and accepted ordinary native effects.






## Sections


### DOC\_GUIDANCE — current active guidance


**Content:**

| Entry point | Current documentation |
|---|---|
| Internal protocol and execution | [Native adapter execution contract](../../reference/execution-adapters.md) links strict DTOs, role JSON schemas, runtime and composition. |
| Public check/test/fix use | [Quality tools](../../reference/tools/quality.md) distinguishes public intent from required internal context, links native filename/argument channels and records resource-failure evidence. |
| Navigation | [MCP tool index](../../reference/tools/README.md) exposes the execution reference beside the public tools. |

These are source-linked descriptions of the current contract. No alternative envelope, version bump, compatibility adapter or external migration procedure is introduced.





### DOC\_DISPOSITION — separate acceptance and coordination


**Content:**

| Issue | Evidence and disposition |
|---|---|
| [469](https://github.com/MikeyVK/phase-gate-mcp/issues/469) | E469-1 through E469-4: complete native transports, causal diagnostic classification, faithful unsupported-input boundaries and observed prerequisites. [Validation](validation.md) records the actual full configured result and independent review is a separate authority. |
| [474](https://github.com/MikeyVK/phase-gate-mcp/issues/474) | E474-1: pure resource description, exclusive invocation ownership and termination-sensitive cleanup; ordinary native caches/state and compatible reports remain allowed. @co must align the issue body's superseded strict destination wording with approved B4 before accepting or closing this issue. Policy approval or observations alone do not close it. |
| [475](https://github.com/MikeyVK/phase-gate-mcp/issues/475) | E475-1: metadata/early-return operations do not become passed analysis. Existing deliberate Ruff exit-zero and Pytest collect-only/exit-5 policies are retained. Its acceptance remains separately traceable. |

The Ready hand-off requests @co to perform the required wording alignment and then use the end-issue lifecycle on the reviewed branch. Issue relationships do not imply closure of every linked issue. The producer documentation supplies evidence and navigation, not independent approval.





### Accepted guarantees and remaining limits


**Content:**

| Boundary | Current guarantee or limit |
|---|---|
| Pyright 1.1.408 explicit selection | One literal native filename per line. Ordinary spaces, CR/LF, native leading/trailing trimming and invalid UTF-8 are unrepresentable; the entire explicit selection is refused. Empty configured discovery is retained. |
| Lychee files_from already occupied | Preserve the caller/config channel and positional route; native argv-size limitations remain. |
| Host access and native effects | Trusted local/personal account execution. Role, selection and captured-result guards supply no OS/filesystem/network/credential isolation. Operational caches/state and compatible reports may be outside selected sources. |
| Invocation cleanup | Remove only exclusively owned resources after confirmed termination; retain them if termination is unconfirmed. Preserve preceding response/outcome and expose cleanup causes. Do not sweep native caches. |
| Fix effects | Ordered execution can leave earlier actual source modifications. No atomic rollback is promised. |
| Evidence | Cached DTOs are process-local/transient; preserve durable exact outcomes, vectors and limitations in the Validation report. Allow sufficient client budget for invocation, termination and result processing. |





### Verification and review boundary


**Content:**

Documentation-only changes reuse the fresh full-suite and complete changed-Python evidence in [Validation](validation.md). Applicable Markdown preflight and offline link outcomes accompany the Documentation hand-over. Source links and direct boundary descriptions are independently reviewable. Independent QA determines Documentation → Ready; @co owns end-issue, remote lifecycle and merge.





### Material surfaces reviewed but unchanged


**Content:**

| Surface | Review result |
|---|---|
| [Root README](../../../README.md) and [server configuration](../../reference/server-configuration.md) | They describe public configuration/root selection without an adapter scratch environment channel; the new execution reference owns the internal context contract. |
| [Agent protocol](../../../AGENTS.md), [.agents instructions](../../../.agents/AGENTS.md), role skills and workflow sources | Existing tool routing, independent QA, strategy and lifecycle authority remain applicable; runtime changes do not require instruction synchronization. |
| [Delivered template suite](../../../.pgmcp/template_suite) | Its templates describe authored artifact content, not the adapter JSON execution envelope. No changed template contract or derived template consumer is required. |
| Research, Design, Planning and historical effect probe | Authoritative accepted inputs/historical observations remain unchanged; current operator guidance does not rewrite them. |
| [Validation](validation.md) | It retains complete passing/failed evidence and test-maintenance disposition. Independent QA's Validation GO on 7934cf5c is indexed below; production/test evidence remains fresh. |





### Independent Validation input


**Content:**

Independent QA in Beoordeel designplan returned GO for Validation → Documentation on commit 7934cf5c and closed the remaining P2. Its complete configured run: 2775 passed, 1 skipped, 1 xpassed, 229 warnings in 276.28 seconds, all 2777 items and existing eight workers. Receipt dae1c5841e1f4dd8a33bdc6405f6a529: 796093 Unicode characters; UTF-8 SHA256 ac89838b6cd116575bb731a8653a3a6632dc5adaaa16767c9fcf3fb5498ee865. Independent gates also passed all 48 changed Python files and configured 186-source Mypy. This is attributed independent evidence, not producer authority for the next transition.







## Related Documents

- [Research and approved B1–B6](<research.md>)
- [Design](<design.md>)
- [Planning DOC\_GUIDANCE/DOC\_DISPOSITION](<planning.md>)
- [Validation](<validation.md>)


## Documentation verification

All two scaffold writes and four existing-file edits passed their configured Markdown content preflight under validation='enforce'. Scaffold receipts: c4b58e9a3dca4b11b15f5e575256f496 and a06d8b7ae54649a1a06febd757f664fd. Quality/navigation edit receipts: 7385117bff064dd08ad09ed742e39e8e, 0ef3c9375f7c468c80cf2856648fd68b, 61980436d8904a52944ce796b7d2290c and d5b0cd524d8444deb4675ecd1b461272.

run_checks(scope='targets', targets=<the four Documentation deliverables>, checks=['markdown_links']) passed: 75 links, 72 successful, 3 excluded, zero errors; receipt 6d2d062b3780432fab207124f4b845cd. Complete cached DTOs were paged and length/hash-verified before parsing. An earlier request also selected markdown_document, which is content-only and therefore not admitted by selection checks; receipt 00f799ea57284a018635dff3b1960dba records selection_unsupported and no executed checks. The enforce write-preflight receipts supply content verification; the corrected selected markdown_links request supplies link evidence.

Only four Markdown deliverables and the workflow transition are changed in Documentation. No runtime, test, template or configuration content is changed. Fresh producer and independent Validation results are reused. Source-linked claims, navigation parity and the internal JSON request example were reviewed against the strict schemas, runtime, native entrypoints and installed-consumer fixture. No deferred documentation gap remains; accepted native transport/host-effect limitations and the separate @co issue-474 wording responsibility are explicitly documented.
