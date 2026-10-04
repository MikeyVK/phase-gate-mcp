<!-- pgmcp:v1 id=generic_doc pv=1.0.0 pf=xoYbNuJbkallN_DM sf=FAN5Vr-4vcbMMjZ2 -->

# Issue 473 — Implementation Evidence and Hand-over

**Status:** Implementation — independent review requested  
**Version:** 0.2  
**Last Updated:** 2026-10-03

## Scope and authority

Four planned cycles implement [Design 0.2](design.md) under [Planning 0.2](planning.md) and [Research's Approved Strategy](research.md#approved-strategy). The branch is bug/473-first-call-template-quality and integrates into main. Epic #72 is administrative. Issue #476 remains the separately decided generic schema/template-consumption work; this branch corrects the concrete package contracts and records evidence for later triage.

The human chose actual scaffolding and manual agent inspection, with existing valuable test adaptations and native checks. No additional automated content/regression/snapshot suite, permanent context-matrix harness, compatibility bridge, runtime formatter/quality gate or new architectural layer was added. Scaffolds provide valid starting points for further editing, not complete task-specific products.

## Completed cycles and deliverables

| ID | Corrected responsibility | Primary evidence / source |
| --- | --- | --- |
| D1_ENV | Same real filter registration before admission and rendering, in existing engine module and actual bootstrap/CLI/fixtures. | [Engine](../../../mcp_server/services/template_engine.py), [Bootstrap](../../../mcp_server/bootstrap.py), [Renewal CLI](../../../mcp_server/cli_renewal.py), [Delivered fixtures](../../../tests/mcp_server/fixtures/delivered_templates.py), [Installed fixtures](../../../tests/mcp_server/fixtures/installed_distribution.py), C_SHARED inspection. |
| D1_LAYOUT | One text_block boundary primitive; Jinja owns joins/EOF; generic renderer unchanged. | [Shared root](../../../.pgmcp/template_suite/shared/templates/bases/tier0_root.jinja2), [Manual inspection](manual-inspection.md), lossless boundary records. |
| D1_EVIDENCE | Actual shared examples and evidence documents, including intermediate defects. | [First outputs](first-output-evidence.md), C_SHARED inspection and native rows. |
| D2_DOC_INPUTS | Explicit module/class prose in six Python class packages and TypeScript, intentional Pytest module contract retained; clean break. | [Python class schema](../../../.pgmcp/template_suite/python_class/context.schema.json), [TypeScript schema](../../../.pgmcp/template_suite/typescript_dto/context.schema.json), current schema rejections and migrated existing tests. |
| D2_PY_LAYOUT | Imports, top-level/member gaps, empty classes and ConfigDict/Field composition; constraints/defaults preserved; no duplicated Fields or Worker __all__. | [Python imports](../../../.pgmcp/template_suite/shared/templates/patterns/python/imports.jinja2), [Model patterns](../../../.pgmcp/template_suite/shared/templates/patterns/python/pydantic.jinja2), nine-family inspection. |
| D2_TS_LAYOUT | Constructor assignment/optional-block joins, brace edges and empty constructor. | [TypeScript template](../../../.pgmcp/template_suite/typescript_dto/template.jinja2), actual two syntax receipts and existing AST/strict fixture checks. |
| D2_CODE_EVIDENCE | Nine code families, 18 pristine pairs and actual boundary/fix instances. | C_CODE closure, full requests/output/native receipts in first-output evidence. |
| D3_METADATA | Shared required authored metadata schema and one shared header/history, final supplied revision is current. | [Metadata schema](../../../.pgmcp/template_suite/shared/definitions/document-metadata.schema.json), [Markdown base](../../../.pgmcp/template_suite/shared/templates/bases/tier2_markdown_document.jinja2). |
| D3_PRESENTATION | Structural Architecture hierarchy/decisions, direct Generic Doc sections and document/tracking joins. | [Architecture template](../../../.pgmcp/template_suite/architecture/template.jinja2), [Generic Doc](../../../.pgmcp/template_suite/generic_doc/template.jinja2), [Markdown patterns](../../../.pgmcp/template_suite/shared/templates/patterns/markdown/sections.jinja2), six final boundary cases. |
| D3_DOC_CONSUMERS | Seven schemas/tests, shared/docflow consumers and active scaffolding example migrated; tracking envelopes retained. | [Scaffolding reference](../../reference/tools/scaffolding.md), [Contracts consumers](../../../tests/mcp_server/unit/config/test_contracts_loader.py), existing full-document/tracking tests. |
| D3_DOC_EVIDENCE | Ten document/tracking families, 20 pristine pairs, revision/structure/presence/whitespace/raw-data boundaries. | C_DOCS closure and complete final evidence appendix. |
| D4_ACTIVE_DOCS | Standards and template-suite path wording reconciled; create-issue source/mirror corrected. | [Code Style](../../coding_standards/CODE_STYLE.md), [Documentation Standard](../../coding_standards/DOCUMENTATION_STANDARD.md), [Architecture Principles](../../coding_standards/ARCHITECTURE_PRINCIPLES.md), [Create Issue workflow](../../../.agents/workflows/create-issue.md), [Mirrored prompt](../../../.github/prompts/create-issue.prompt.md). |
| D4_19_FAMILIES | Current 19-family/38-pair index; only changed reachable graphs refreshed. | Final index in manual-inspection.md; C4 code schema fingerprints match saved first-output provenance. |
| D4_TOOLS | Actual schema/scaffold/edit/check/test/fix and bounded derived-route practice, F1–F7 findings with disposition. | [Current-tool findings](tool-practice-findings.md), isolated fix requests/results/readback and final preflight/native DTOs. |
| D4_HANDOVER | Outcome-neutral deliverable/preservation/consumer/evidence index and deferred triage. | This report and the authoritative inputs above; independent verdict remains outstanding. |

C_SHARED GREEN: e6e1363874b7b9e7b41218136f784fe9a0689031. C_CODE RED: deb5a2ccfaa3481f631c1bd2475e120d9ebd032a; GREEN: 64a503ebbfb683b81037fc300d720911591ebd70. C_DOCS RED: 1e4915f9a39217b3f9e3681c3ebd45fa3b7dabe4; GREEN: 05798103c8a8f4dc048bc774e0f30fc8618274b2. C_RECONCILE is mechanical documentation/evidence closure; no artificial RED was required. The complete branch diff against main is the full file inventory; primary entry points above are navigation, not a substitute for that diff.

## Preservation and evidence interpretation

| Obligation | Actual evidence and practical limit |
| --- | --- |
| Caller ownership / clean break | Required module/class fields and document_metadata are enforced; removed aliases reject before writing. Pytest's own description and member descriptions are retained. No fallback or compatibility mode. |
| Whitespace interiors and values | Lossless JSON/UTF-8 hashes preserve internal CRLF, hard-break spaces, blank paragraphs, fence/code indentation, literal backslash/pipe, Unicode U+2028 and False/0/None; only selected fragment blank edges normalize. Raw ValidationSpec data is JSON represented rather than prose-trimmed. |
| Explicit presence | Absent TypeScript module comment differs from defined empty; empty document carriers remain where admitted; validates:null and raw-data null retain their association. |
| Generated boundaries | All 38 final outputs have first-line provenance and exactly one terminal LF. Native Ruff clean-fragment evidence plus direct boundary reading establishes generated joins; arbitrary caller quality/dependencies are outside that claim. |
| Metadata facts/order | Seven document families share mandatory header/history. Latest means the final explicit supplied revision, without sorting or invented facts; revision scalar Markdown escaping preserves displayed literal values. Tracking families remain separate. |
| Fresh public catalog | C3 final source identity FAN5Vr-4vcbMMjZ2 and each package fingerprint are archived. C4 complete discovery matches nine code fingerprints, so their C2 evidence remains current despite changed global suite identity. Separate MCP clients require their own refresh. |
| Native versus manual proof | Individual syntax/document/body/message rows were inspected independently of success/written. Actual semantic reading found structure defects despite native preflight passes. No new automated content tests replace that reading. |

The working raw files are in .pgmcp/temp/issue473/. Final code filenames start c2_verified_; final document/tracking filenames start c3_final_. Earlier failures, c3_verified_* and initial delegated boundaries remain identifiable intermediate evidence. Fix instances were separately scaffolded and do not alter pristine outputs. Exact replay contexts, complete preflight/native DTOs, raw text and lossless byte records are in first-output-evidence.md. Cache URIs alone are transient and are not the durable evidence.

## Narrow native evidence

| Surface | Result and freshness |
| --- | --- |
| Shared engine/catalog/startup/public/install family baseline | 183 passed before edits. Later narrow failures exposed CLI and shared-fixture filter registration; installed-handshake closure plus 27 passing renewal/activation/proposal tests close those consumers. Unchanged passing rows are reused with their sources. |
| Changed production Python | Configured format/lint/Mypy/Pyright passed after real formatting correction, C_SHARED receipts. |
| C_CODE contract RED | 32 failed / 2 passed with bounded native traceback request; response_too_large attempt is excluded from RED evidence. |
| C_CODE corrected existing tests | Ten-file subset 52 passed / 1 obsolete expected-order failure, then affected integration file 5 passed closes that exact failure. Do not sum overlapping rows as unique tests. |
| Generated Python pairs | Ruff 0.15.6: format/lint passed on 16 pristine Python outputs plus corrected mixed-import reproduction (17 already formatted). Public Python 3.13.7 / TypeScript 6.0.3 syntax rows passed for all actual code pairs. TypeScript dependency/strict behavior evidence comes separately from its existing provisioned fixture. |
| C_DOCS contract RED | 23 failed / 11 passed / 1 existing warning. |
| C_DOCS final planned subset | 47 passed / 1 existing Pydantic warning / 67.13s in the twelve planned template/install files. |
| Direct docflow consumers | 2 passed / 22 deselected / 9 existing warnings / 2.36s in existing contracts tests. |
| Changed test Python | Format/lint/Pyright passed on affected cycle test/fixture files; C3 final twelve-file gates remain fresh after Jinja-only subsequent correction. |
| C3 final Markdown links | Lychee 0.24.2: 27 successful / 0 errors / 4 excluded internal cache URIs; configured offline fragments, not remote availability. |
| C4 documentation | Enforce edit/scaffold preflights passed. Final affected link review is recorded in the C4 verification appendix before commit. No documentation-only test rerun or full Validation was performed. |

Exact tool calls/native versions/results and warnings are preserved in the evidence documents. Existing tests were adapted for meaningful changed input contracts/obsolete expected import ordering; no new content assertions, snapshots or helper-only filter tests were introduced. Native results prove the stated scopes, not complete workspace verification.

## Known consumers and scope disposition

The concrete/shared tests, CLI/delivered/installed fixtures, current document workflow contexts and public scaffold example adopt the new contracts in their owning cycles. C4 searches were interpreted by context: nested descriptions, unrelated resource metadata and intentionally synthetic template inputs are not mechanically renamed. Both create-issue bodies match after harness front matter. They discover issue fields, use exact file_name, pass admitted body fields only and preserve defined emptiness. Publication removes only the recognized first-line technical provenance and its separator, with the exact reviewed remainder passed as body. No live GitHub issue was created as a probe.

Template Library Usage, schema-template-maintenance and config-loading reference were inspected and remain valid unchanged. Their compact generation-source provenance contract is separate from caller-authored document facts; historical #460/research artifacts were not mass-migrated. Documentation Standard now has an explicit current authored revision while retaining the historical empty date rather than inventing one.

Generic schema/template consumption completeness, automated enforcement and broader analysis remain #476 by explicit human decision. No new universal consumption analyzer was introduced. Concrete package-local defects encountered here were corrected; current tool findings route to separate coordination triage.

## Open work and current-tool findings

No known uncorrected issue473 deliverable is intentionally deferred. Independent QA must assess this producer evidence and may return blockers. Full configured tests, branch-wide checks, Validation/documentation/ready progression and merge remain outstanding.

F1–F7 record Markdown angle-link parser false warnings, supported large-resource reading, oversized failure responses, restart sequencing, missing direct schema-source authoring, confirmed bootstrap/proxy recovery failure and per-client catalog refresh. See tool-practice-findings.md for exact reproduction, impact and uncertainty. F6 is the priority operational follow-up: one rejected template caused process exit, lost actionable diagnostics, false ready events and an unavailable tool recovery path. The approved template correction restores this branch's admission; it does not repair CLI/proxy lifecycle handling. Coordination must retain the human requirement for accessible diagnostics and recovery while continuing to reject invalid suites.

## Bug / Implementation Hand-over

### Scope

- Completed C_SHARED, C_CODE, C_DOCS and C_RECONCILE within the approved clean break and manual-inspection strategy.
- Excluded generic476 work, unrelated tool repair, extra automated content coverage and full Validation.

### Deliverables

- Design/Planning deliverables D1_ENV through D4_HANDOVER are indexed above.
- Primary engine/bootstrap/shared/concrete template seams, migrated existing tests, current standards and create-issue source/mirror are linked above.
- [Manual inspection](manual-inspection.md), [Exact first outputs](first-output-evidence.md) and [Tool practice](tool-practice-findings.md) carry detailed evidence. The branch diff against main is the complete inventory.

### Evidence

- All 19 families / 38 pristine final pairs manually read with current reachable package identities.
- Actual syntax/preflight/native tests/checks/fixes, rejection/presence/whitespace/literal boundaries and fresh narrow gates are indexed above.
- No independent approval or broad Validation claim is made.

### Open Work

- Independent Implementation review; later full configured suite/branch gates and workflow continuation.
- Separate coordination triage for tool findings, especially F6; generic consumption completeness remains #476.
- Remaining implementation cycles: None, subject to independent findings.

### Review Request

- Review requested.

## C_RECONCILE verification appendix

Final configured offline Markdown link review passed with 56 successful links, 0 errors and 4 excluded internal cache URIs (Lychee 0.24.2; receipt `pgmcp://cache/runs/1876802496a94bb896ccbe00fc880f3b`). The complete request/DTO is archived in first-output-evidence.md. The initial review found one producer-authored wrong shared-root link; corrected to the actual tier0_root.jinja2 source before the final checks. Enforce edit/scaffold preflights passed on all changed documents/instructions. Source/mirror readback confirmed identical create-issue instruction bodies. No source/schema/template/test change occurred in C4, so prior affected native evidence remains fresh.

Pre-commit reality check: all fifteen deliverables map to concrete source, actual raw output or current native evidence; the final inventory contains 38 pristine pairs with current package graph identities; material failures and separate fix instances remain distinguishable; caller facts/interiors/presence remain preserved; active known inputs are migrated; F6 is explicit operational follow-up rather than claimed repaired. The current ten-file C4 inventory contains only planned standards/instructions/evidence and tool-maintained cycle state. Full configured tests and broad branch gates have not been run and remain Validation work. Independent review is requested; producer evidence is not GO.

## Receipt-integrity refresh during independent review

The root reader was tightened to independently recompute full UTF-8 SHA256 before parsing. Nine current resolved code schemas, still-available native/test/edit/link receipts and all new repeated scaffold/rejection receipts matched their advertised hashes. Older transient receipts could not be retroactively certified. Twenty-six separately scaffolded c4_receipt_* outputs, using the identical contexts and unchanged final source graph, are byte-for-byte identical to all twenty C3 final pairs and six final boundary outputs. All fresh content-preflight rows passed; the nine repeated schema rejections returned context_invalid/written=false. The twelve changed test-file format/lint/Pyright checks passed again. Exact requests, complete responses, independent hashes and byte-equality records are in first-output-evidence.md. This refresh changes evidence only and does not modify the 38 pristine final outputs, templates, production or tests. Independent QA was notified; no new content test or permanent harness was added.

## C_HEADER_CONSUMER — owner-authorized cycle 5 repair, 2026-10-04

Independent Validation QA returned NOGO on 9c164c4c for a missed existing test consumer. The owner authorized one focused repair cycle and renewed Validation/review. Implementation was reopened through the audited force_phase_transition; cycle 5 was appended through update_planning_deliverables and entered through transition_cycle. This completes the approved known-consumer migration; no new strategy or production feature is introduced.

| Deliverable | Actual correction / evidence |
| --- | --- |
| D5_CONSUMER | [Existing header-reader module](../../../tests/mcp_server/unit/services/test_artifact_header_reader.py) imports and calls the public register_template_filters on its own renderer before template loading. Exact expected output uses the root's approved blank provenance/body separator. |
| D5_EVIDENCE | Whole existing module: 68 passed, 1 existing warning, 0.37 seconds; format, lint and Pyright passed on that module. |

Negative baseline is reused: full suite six failures and focused producer/independent QA repetitions all raised No filter named 'text_block'. No duplicate RED test or ceremonial negative rerun was added. The change adds one import, one real registration call and adjusts the expected separator; it preserves independently authored identity vectors, both length cases, all three frames, first-line maximums and ArtifactHeaderReader round trips.

Exact verification calls:

```json
{"scope":"targets","targets":["tests/mcp_server/unit/services/test_artifact_header_reader.py"],"args":{"python_tests":["-q","-n","0","--tb=short"]},"timeout_seconds":120}
```

```json
{"scope":"targets","targets":["tests/mcp_server/unit/services/test_artifact_header_reader.py"],"checks":["python_format","python_lint","python_pyright"],"timeout_seconds":120}
```

Receipts: pgmcp://cache/runs/56fb72e93cff44708f2ed9a6052ee2af and pgmcp://cache/runs/fc486b1fdf984812a56a937dee34f200. This is existing test maintenance, not a new automated content/regression suite. No fake filter, skip, production/template/adapter/native-configuration change or additional refactor was made. Existing production gates and actual scaffold evidence remain unaffected. A single fresh configured suite belongs to renewed Validation after independent repair review.

### Bug / Implementation Hand-over (cycle 5)

#### Scope

- Complete the missed header-reader consumer migration in one focused cycle.
- Exclude production/template edits, new tests and the deferred branch-selection solution.

#### Deliverables

- [Planning cycle 5](planning.md#owner-authorized-repair-cycle-c_header_consumer--2026-10-04): D5_CONSUMER and D5_EVIDENCE.
- [Changed test consumer](../../../tests/mcp_server/unit/services/test_artifact_header_reader.py), [real shared registration](../../../mcp_server/services/template_engine.py), [delivered root](../../../.pgmcp/template_suite/shared/templates/bases/tier0_root.jinja2).
- Complete repair diff is relative to 9c164c4c; only the existing test module, phase documents and tool-managed workflow state/deliverables changed.

#### Evidence

- Reused causal six-failure baseline and independent QA diagnosis.
- 68 existing tests passed; format/lint/Pyright passed.
- All independent provenance/frame/length/round-trip assertions retained; no production contract modified.

#### Open Work

- Independent targeted Implementation review, then fresh configured full suite.
- Explicit disposition of existing broad Python failures and deployed-instruction link context in Validation.
- Deferred branch-check proposal remains separate; Documentation/Ready await the required reviews.

#### Review Request

- Targeted external review requested; producer does not claim GO.

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-03 | @imp implementer | Record four correction cycles, all fifteen deliverables, nineteen-family first outputs, preservation/native evidence, known consumer closure and deferred tool triage. |
| 0.2 | 2026-10-04 | @imp implementer | Record cycle 5's real filter registration and approved separator migration in the existing header-reader tests, 68 passing cases and scoped quality gates. |

