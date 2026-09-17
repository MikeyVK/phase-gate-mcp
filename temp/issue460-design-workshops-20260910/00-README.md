<!-- C:\temp\pgmcp\temp\issue460-design-workshops-20260910\00-README.md -->
<!-- template=design version=5827e841 created=2026-09-10T09:24Z updated= -->
# Issue 460 — Prepared Design workshop bundle

**Status:** TEMPORARY REVIEW BUNDLE — W07/W08 independent QA GO reported; W09–W12 human-approved and consolidated; canonical closeout audit in progress; combined independent QA pending  
**Prepared:** 2026-09-10, @imp designer  
**Workspace:** C:/temp/pgmcp  
**Purpose:** Complete the remaining workshop preparation in advance, then review and integrate one coherent topic at a time.

## Current closeout update — 2026-09-12

W06's schema dialect/reference boundary and fingerprint-free active-catalog URI are
human-approved and consolidated in DI-01/02 §7.2.3 and Shared §7.6. DI-05
§§7.15.1–7.15.5 now contains the accepted W04 tests.yaml and request/result/error graph.
Use those canonical owners rather than older proposal prose below. Registered wrapper/
serialization integration, full per-path dispositions and combined independent review
remain open; no runtime tests or whole-Design approval are claimed.

## What is ready

Twelve separate workshop proposals cover the remaining DI-01–DI-08 Design boundaries, followed by a cross-package audit. Each proposal explains the consumer need, recommendation, alternatives, typed contract, failure cases, migration and proof obligations. They are large enough to discuss a responsibility as a whole, not another single-field workshop.

This is an **internal review bundle**, not the canonical Design set. It lives in the workspace temp directory so Codex can display it; it has not been committed, published or used to advance a phase. Some material choices intentionally remain open for your review. “Prepared” does not mean “accepted,” “implemented” or “independently QA-reviewed.”

## How to review without waiting for another design draft

Current W07/W08 update (2026-09-11): the human delegated source-led design for both families.
Use [code/test](../../docs/development/issue460/design-code-test-artifacts.md) and
[document/tracking](../../docs/development/issue460/design-document-tracking-artifacts.md)
as the review entries. The older notes below are preparation history, not current decisions.
Their detailed preflight and bounded QA request are indexed in the canonical Design hub.
W09 is now human-approved and consolidated in canonical DI-05 §7.20; its bounded
independent QA request is in the Design hub §11. Whole-package integration remains open.

Current work: canonical closeout audit after W12 approval. W11 is consolidated in design-workflow-documentation.md. W10 closed on 2026-09-12 in DI-06 §§7.6–7.7; use the canonical Design hub's
bounded QA input. Human direction on 2026-09-11 is to continue W10–W12 and request
independent review of the remaining packages together; W09 is not a separate blocking
review gate before W10. Earlier W05/W06
workshop pointers below are preparation history. Remaining role integration, shared
serialization and independent conformance stay tracked; no full-package closure is implied.



After your response, I will update the affected proposal and its dependent proposals, integrate **only approved decisions** into their single canonical owner, and identify the next already prepared workshop. Do not copy all twelve documents into canonical Design at once. The guide and audit are navigation/evidence indexes, never competing product authority.

## Review sequence and decision menu

| Workshop | Topic and main review decision | Primary owner after approval |
|---|---|---|
| [W01 — Mutation results](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/01-mutation-results.md) | What an agent sees after a successful check but refused write; expected failures, selection explanation and diagnostic disclosure | DI-04 + Shared Contracts |
| [W02 — Adapter packages](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/02-adapter-packages.md) | Minimal package declarations, explicit trust source, fingerprint inputs and native-version return channel | DI-05 |
| [W03 — run_checks](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/03-run-checks.md) | Reusable checks/profiles, exact selection/defaults, targets/branch/workspace, expansion and honest incomplete results | DI-05 |
| [W04 — run_tests](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/04-run-tests.md) | Preserve current targeted/full/native-test selection; align shared rationale without copying check semantics; justify exact options/results | DI-05 |
| [W05 — apply_fixes](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/05-apply-fixes.md) | Closed: explicit files/order, direct native mutation, stop-first and typed results; no staged copies or rollback | DI-05 §7.18; DI-07 recovery guidance; DI-08 evidence |
| [W06 — Suite/shared integration](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/06-suite-contract-integration.md) | Defaults/ref semantics, profile fingerprint projection, one startup-built input contract and schema attachments | DI-01/DI-02 + Shared Contracts |
| [W07 — Code and test artifacts](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/07-code-test-artifacts.md) | Retained package IDs, structured fields, native fragments, portable rendering and removed artifacts/patterns | DI-03 code/test |
| [W08 — Documents and tracking](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/08-document-tracking-artifacts.md) | Named workflow carriers, exact Planning projection and persisted tracking draft versus downstream body | DI-03 document/tracking |
| [W09 — Native settings and capabilities](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/09-native-settings-migration.md) | One native config authority, explicit setting deltas and the real validation needs of all retained packages | DI-05 |
| [W10 — Distribution integration](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/10-distribution-integration.md) | Asset/wheel completeness, adapter authoring source and profile-config integration with approved renewal | DI-06 |
| [W11 — Workflow and documentation](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/11-workflow-documentation.md) | Nineteen workflow carriers, source-first agent instructions and removal of drifting invocation examples | DI-07 |
| [W12 — Test architecture and closeout](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/12-test-architecture-integration.md) | Small shared fixtures, independent conformance, supporting-file ownership and whole-set Design completion | DI-08/XC-02 |

The order is a **conversation route, not an implementation plan**. W05 is consolidated. W07–W09 have mutual dependencies and must be reconciled before those package contracts are closed.

## Cross-package consequences to keep visible

| A decision changes in… | Revisit… | Why |
|---|---|---|
| W01/W02 diagnostics or role-result metadata | W03/W04/W05/W12 | All consumers must receive the same typed process facts without presenter-specific error knowledge |
| W03 profile/binding shape | W05/W06/W07/W08/W09/W10 | Template provenance and candidate admission consume the same references; fix/check relationships are discovery only |
| W05 native execution/results | W01/W09/W11/W12 | Shared result serialization, native settings, explicit owner recovery guidance and independent partial-mutation/stop-first proof |
| W06 schema/default rules | W02/W04/W07/W08/W12 | Package schemas, startup selector/args-recipient projections and durable contract cases must agree |
| W07/W08 package IDs or content needs | W09/W10/W11/W12 | Official profiles, shipped assets, workflow instructions and preservation evidence must follow |
| W09 native rules/capability coverage | W03/W05/W07/W08/W10 | A declared profile must be honest and usable for its actual consumer |

No one workshop can silently weaken a neighboring package's approved promise. Where a choice would contradict frozen Research, stop that affected integration and ask for an explicit authority decision; do not amend Research as a drafting convenience.

## The important choices are not hidden

1. **Approved diagnostic disclosure — W01-F, 2026-09-10.** Keep operation fields relative and routine output concise; existing on-demand cached diagnostics may retain incidental absolute paths. Cache retrieval is not local-only or necessarily human-confirmed. The separate private-log/diagnostic-ID alternative was withdrawn; DI-04 §4.6 owns the approved policy. W01-A–E were subsequently approved; subsequent W02/W03 approvals are recorded below.
2. **Approved native provenance — W02.** DI-05 now explicitly adds external_tools to ordinary role results and updates the closed scaffold payload. No new query tool; invalid_request stays minimal. adapters.yaml is the approved trust authority.
3. **Fix recovery — W05 closed.** Native mutation is direct and stops on first non-success. Earlier and attempted changes may remain. Agent-selected Git recovery is external; no generic recovery state or overlap admission is added.
4. **Source-fragment validity and DTO examples — W07/W09.** JSON shape validation cannot certify arbitrary source fragments. DTO example checks also lack a defined source of model semantics under the current check input. No hidden context propagation, source execution, duplicate model parser or always-pass capability is assumed.
5. **Document versus body profiles — W08/W09.** Research/Design documents can require H1; issue/PR bodies cannot. TypeScript and conventional-message preflight need actual declared capability behavior, not extension-only success.
6. **Worker disposition — W07.** The conversation recalled removal; the canonical catalog retains it. This bundle follows the catalog and flags the discrepancy rather than silently changing inventory.
7. **Commit draft versus Git message — W08.** A persisted artifact's first metadata line is not a conventional-commit subject. The proposed downstream-use boundary needs explicit agreement.
8. **Native setting differences — W09.** Removing the double configuration layer still requires visible choices about Python target, warning behavior, strictness and exclusions; none are claimed behavior-equivalent without evidence.

These are review points, not new Research findings or automatic scope expansion. The audit distinguishes drafting errors already corrected from genuine remaining decisions.

## Canonical sources and preparation baseline

The table records initial preparation versions, not current authority. Current hub v1.72 and DI-05 v0.81 consolidate W05. W06–W12 and cross-package proof remain open; no completed runtime conformance is claimed.

| Source | Role / inspected baseline |
|---|---|
| [Issue documentation README](C:/temp/pgmcp/docs/development/issue460/README.md) | Form/topology authority, v1.19; its old paused-navigation text is stale, not the current gate |
| [Research](C:/temp/pgmcp/docs/development/issue460/research.md) | Frozen approved strategy and latest reported independent QA GO |
| [Design intake](C:/temp/pgmcp/docs/development/issue460/design-intake-map.md) | DI ownership; 44 strategies, 19 invariants and 23 expected results |
| [Catalog](C:/temp/pgmcp/docs/development/issue460/template-suite-catalog.md) | 126 consumers + 2 governing sources; 151 tests/helpers; no duplicate inventory here |
| [Design hub](C:/temp/pgmcp/docs/development/issue460/design.md) | v1.56, integration authority after review |
| [Suite resolution](C:/temp/pgmcp/docs/development/issue460/design-suite-resolution.md) | v1.20; existing topology, compact header and fingerprints preserved |
| [Mutation validation](C:/temp/pgmcp/docs/development/issue460/design-mutation-validation.md) | v1.28; existing selection/policy/checked-write behavior preserved except highlighted proposed dependencies |
| [Execution adapters](C:/temp/pgmcp/docs/development/issue460/design-execution-adapters.md) | v0.66; generic process and scaffold check baseline |
| [Shared contracts](C:/temp/pgmcp/docs/development/issue460/design-shared-contracts.md) | v1.7; existing untracked canonical working file, preserved |
| [Distribution](C:/temp/pgmcp/docs/development/issue460/design-distribution.md) | v1.7; existing untracked canonical working file, preserved |
| [Deferred work](C:/temp/pgmcp/docs/development/issue460/deferred-work.md) | Exclusion authority; no health blockade, sandbox, discovery or deferred artifact expansion here |

The current get_work_context Design/designer instructions and the user's Design GO govern this task. Historical Research excerpts or stale navigation do not reopen approvals by implication. Conversely, a proposal label never grants authority to override a genuine current strategy.

## Procedure followed and work deliberately not done

- Used pgmcp-imp as @imp designer; loaded work context and phase instructions before drafting.
- Read applicable documentation/architecture boundaries and the Research/intake/canonical Design sources.
- Inspected concrete code/config/test seams before proposing mechanisms; used two bounded read-only producer reviewers for additional findings, not QA authority.
- Made repeated authority, contract, failure/removal and artifact-consistency passes; recorded their concrete effects in [the audit](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/13-consistency-audit.md).
- Scaffolded the fourteen temporary documents through the existing artifact tool, then edited only those temporary documents.
- Initial preparation did not change Research, canonical Design, production/tests/config, phase, cycle state or Git history. Subsequent W01-F approval is integrated only into DI-04, DI-05 and the Design hub; Research and runtime/config/tests remain unchanged. Commit 491c4879 also contains the PGMCP commit tool's automatic state metadata update; no phase transition was requested.
- Did not run native adapters, application tests, quality gates, wheel builds or deployment; those are future evidence obligations, not completed proof.
- Did not assign Planning cycles or issue an independent QA verdict.

## Review hand-over

**Scope:** Remaining Design prework, plus explicit cross-package corrections and unresolved contract choices.  
**Deliverables:** This guide, W01–W12, and [the consistency audit](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/13-consistency-audit.md).  
**Evidence:** Source/contract inspection and artifact checks recorded in the audit.  
**Open work:** Human workshop review, approved canonical integration, then separately invoked independent Design QA.  
**Review request:** Continue with W04 test results; later proposals are available but are not approved automatically.
