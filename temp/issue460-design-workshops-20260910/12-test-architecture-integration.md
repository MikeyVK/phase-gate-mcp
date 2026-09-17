<!-- C:\temp\pgmcp\temp\issue460-design-workshops-20260910\12-test-architecture-integration.md -->
<!-- template=design version=5827e841 created=2026-09-10T09:24Z updated= -->
# W12 — Independent proof and a bounded Design closeout

**Status:** HUMAN-APPROVED — consolidated in docs/development/issue460/design-test-architecture.md on 2026-09-12; canonical integration and independent QA pending  
**Owner:** DI-08 shared support / XC-02 assurance; behavioral ownership stays DI-01–DI-07  
**Dependencies:** All workshop contracts  
**Decision nucleus:** Small explicit test seams and a traceable removal graph, not another all-purpose harness or “remaining consumers” bucket.

**Refresh — 2026-09-12:** W09–W11 are human-closed; W07/W08 have bounded independent
QA approval. W12 is human-approved; the canonical DI-08 document owns its decisions. Native fix staging/proposal/rollback,
DTO example validation and generic optimization controls are superseded, not open design
choices. Full canonical cross-package reconciliation and independent review remain required.

## 1. Purpose and authority

The refactor must preserve meaningful behavior while removing tests that encode obsolete implementation. Migrated check/test/fix tools cannot be their own sole evidence.

## 2. Scope and exclusions

Shared fixtures/helpers, independent conformance, cross-package obligation/removal accounting and Design exit conditions. No production test framework, mandatory extra tests per field, execution-result cache, test rewrite unrelated to issue460 or Planning cycle allocation.

## 3. Binding inputs

I-14/E-17; [126-consumer/151-test catalog](C:/temp/pgmcp/docs/development/issue460/template-suite-catalog.md); DI-08/XC-02/RC-01 intake; Architecture Principles. The existing catalog has 128 runtime rows including two governing sources, and 151 test/helper rows.

## 4. Proposed decisions

| ID | Proposal |
|---|---|
| W12-A | Split shared setup by public dependency seam, not by production private class |
| W12-B | Keep behavioral and architectural test dispositions separate |
| W12-C | Independent role conformance and native evidence precede deleting legacy routes |
| W12-D | Ledger-backed whole-set integration is a documentation audit, not new runtime code |

## 5. Responsibilities and boundaries

| Shared support | Supplies | Excludes |
|---|---|---|
| Isolated roots | Explicit workspace/config/template/adapter/temp paths | CWD/environment inference |
| Synthetic suite builder | Caller-supplied manifest/schema/template source for negative/graph tests | Second production template inventory |
| Packaged-suite acceptance | Actual delivered packages and DI-03-owned test contexts through public schema/rendering | Copied “all types” context registry or runtime semantic example validation |
| Role-specific doubles | Typed check/test/fix responses and observed calls | Generic Pytest-shaped runner |
| Process probes | Controlled subprocess fixtures and protocol faults | Fake-only proof of descendant stopping |
| Filesystem fault support | Narrow injected write/guard/recovery observations | Patching private implementation internals |
| Registered tool composition | Real wrappers/cache/presentation with explicit collaborators | Hidden manager construction/global singleton state |

Proposed support interfaces are simple fixture factories returning explicit root values, admitted catalogs, typed invokers or instrumented filesystem boundaries. Do not create a central fixture that manufactures the entire server for every unit test. Full composition exists only for the tests that actually exercise it.

## 6. Options and rationale

Renaming the current God-harness preserves copied config and hidden dependencies. Deleting it without tracing plugin registration breaks unrelated tests. Choose small support seams and preserve actual callers deliberately.

## 7. Detailed design

### Two dispositions per existing test

Record behavior: keep|adapt|replace|remove; architecture: compliant|adapt|replace|remove. Each row additionally identifies its one primary DI owner, durable claim, target public proof seam and removal prerequisite. This is an issue-local Design review ledger, not runtime YAML.

The frozen Research ledger remains the path authority. Do not duplicate 151 rows into every workshop. The exact path and owner must later enter Planning's concrete cycle allocation; no unresolved “remaining tests” row is acceptable.

### Primary behavioral owners

| DI | Own evidence, including removals |
|---|---|
| DI-01 | Resolved schema/refs/optionality/defaults and client exposure |
| DI-02 | Graph, startup snapshot, package isolation/fingerprints and header dialect |
| DI-03 | Every retained artifact's fields/rendering/portability and removed families |
| DI-04 | Create-only, original-byte guard, enforce/report, truthful mutation outputs; no native-fix transaction or recovery admission |
| DI-05 | Catalog/process/roles, selectors, native migration, direct fix application, stop-first and honest partial-mutation evidence; no rollback mechanism |
| DI-06 | Wheel/install/checkpoint/renewal/activation/recovery |
| DI-07 | Workflow carrier alignment and active instruction/document authority |
| DI-08 | Shared helper/plugin topology and cross-package no-gap audit only |

### Directly observed supporting seams

[artifact_test_harness](C:/temp/pgmcp/tests/mcp_server/fixtures/artifact_test_harness.py) changes CWD/environment and copies configuration. [test_support](C:/temp/pgmcp/tests/mcp_server/test_support.py) supplies environment/CWD fallbacks and legacy collaborators. [fake_pytest_runner](C:/temp/pgmcp/tests/mcp_server/fixtures/fake_pytest_runner.py) is framework-shaped.

Additional supporting dependencies found during this preparation:

- [tests/conftest.py](C:/temp/pgmcp/tests/conftest.py): old harness plugin and session-wide legacy template/config environment initialization.
- [integration/mcp_server/conftest.py](C:/temp/pgmcp/tests/mcp_server/integration/mcp_server/conftest.py): shared server factory caller; preserve unrelated GitHub mock behavior.
- [tests/mcp_server/conftest.py](C:/temp/pgmcp/tests/mcp_server/conftest.py): unrelated CreateBranchInput singleton reset; leave unchanged absent an affected dependency.

These are explicit supporting-file dependencies, **not a silent revision of the frozen 126/151 census**. The first two need named DI-08 integration ownership before Planning; the last is a preservation boundary.

### Independent proof

Check: direct adapter protocol/schema and native fixture behavior independently from
run_checks. Test: native Pytest evidence for retained behavior plus a controlled non-Python
protocol fixture independently from the new run_tests; approved V3 deltas are not false
parity failures. Fix: direct native mutation on disposable authorized files, partial
failure and stop-first evidence independently from apply_fixes; never proposal/rollback
fixtures for a removed product promise. A public run passing is useful integration
evidence but not sufficient self-certification.

### Concrete shared support contract

These are bounded test-support seams, not new production APIs or a universal harness:

| Support | Explicit inputs / output | Primary users |
|---|---|---|
| Isolated root values | Caller-selected temporary parent and explicit workspace/server/config/template/bundled-adapter/workspace-adapter/temp roots; frozen path values | DI-01/02/04/05/06 |
| Synthetic package-tree writer | Caller-supplied relative file names and bytes; returns isolated root without inventing template IDs, schemas or profile defaults | DI-01/02 graph rejection, DI-06 component scenarios |
| Role-specific recording double | Explicit typed check, test or fix outcomes; observes invocation requests through the public interface | DI-04/05 orchestration and presentation |
| Controlled adapter process | Known stdout/stderr/exit behavior, delay or child-process behavior; disposable process resources | DI-05 transport, limits and termination |
| Narrow filesystem fault double | Injected public write/guard/activation boundary and named failure point; observations of writes and final bytes | DI-04/06 only where their contracts promise atomicity/recovery |
| Installed-distribution fixture | Built wheel and isolated installation; entrypoints and package resources loaded outside repository checkout | DI-06 delivery and DI-05 bundled-adapter conformance |
| Registered-tool composition | Real wrapper/cache/presentation with explicit domain collaborators and isolated cache | Cross-package public output integration |

Use production config models/readers for admitted fixtures, not a second config parser.
Purpose-built invalid fixtures remain explicit input data. Process-global environment
or CWD changes belong only to tests whose subject is that boundary, scoped and restored;
ordinary manager/schema tests receive explicit values. Do not repeat a full server build
or native installation per unit test. Reuse built-artifact evidence until relevant inputs
change, as permitted by the workflow.

### Three independent levels of evidence

| Level | Concrete example | What it cannot prove |
|---|---|---|
| Adapter/native contract | Invoke the adapter process directly with fixture input; inspect exit code, raw protocol and native effects; validate declared role output | Manager selection, persistence or MCP presentation |
| Domain consumer behavior | Feed a typed failed check to scaffold/safe-edit; verify enforce/report and actual file bytes; feed a failed fix step and verify later bindings remain unstarted | Real native-tool behavior |
| Public composition | Invoke registered tools and read cached structured results; compare operational success, domain outcome and concise presentation | By itself, correctness of both adapter and manager |

Expected values must not come from the production function being tested. Use independent
known byte vectors for the exact header/fingerprint wire contracts, plus relational
properties for package-local/shared/policy changes. Do not build a second full fingerprint
engine in shared fixtures. Synthetic fixtures prove extensibility/negative cases; actual
retained packages and installed files prove delivered behavior.

### Existing support ownership and removal gates

| Existing surface | Required disposition / preserved boundary |
|---|---|
| artifact_test_harness.py | Replace the broad harness with narrow support; preserve each retained caller claim before retiring plugin/fixture names |
| test_support.py | Adapt/split affected helpers, keep unrelated useful builders; DI-05 remains the catalog's primary owner, DI-08 supplies shared architecture constraints |
| fake_pytest_runner.py | Replace generic Pytest-shaped boundary with test/v1 recording double; native Pytest conformance remains adapter-owned |
| tests/conftest.py | DI-08 supporting integration owner for old harness registration/session environment; preserve workflow plugin and unrelated collection behavior |
| integration/mcp_server/conftest.py | DI-08 supporting integration owner for make_test_server caller; preserve GitHub mocking and unrelated integration behavior |
| tests/mcp_server/conftest.py | Preserve unrelated CreateBranchInput singleton reset; no cleanup expansion without an affected dependency |

Supporting dependencies are additions to Design's integration accounting, not a claim that
the frozen 126/151 census has changed or that the new design paths already have cycle owners.
Every touched supporting file must receive a concrete Planning owner as well.

Use exact byte comparisons for genuinely exact protocols, including the new first-line header. Removing prose snapshots does not prohibit testing a published wire format. Use semantic section assertions for documentation and operation outcomes for lifecycle; do not snapshot entire incidental prose or implementation object layouts.

### Obligation closure matrix

| Obligation | Proposal carrying concrete behavior/proof |
|---|---|
| F-01 context/composition/nested structures | W06 defaults/ref rules; W07/W08 concrete records |
| F-02 omission/null/default | W06 unchanged caller context: absence remains absence; no default materialization; W07/W08 exact presence cases |
| F-03 caller vs operation/provenance | W01/W06 field separation; W07 filename-symbol counterexample |
| F-04 selected richer DTO | W07 one immutable DTO package; W06 no hidden override |
| F-05 graph/runtime view | W06 AST admission and snapshot proof |
| F-06 links | W08 typed links and complete definitions |
| F-07 consumed inputs | W07/W08 field-to-render proof; W01 outer vs context errors |
| F-08 output evidence | W01 unchanged policy; W03 profiles; W09 capability gaps |
| F-09 documentation authority | W11 nineteen rows/source-first/reference dispositions |
| F-10 renewal | Existing D-DIST table + W10 installed-package integration |
| F-11 provenance | Bounded first-line header and generation pf/sf; whole-file exclusions; DI-06 operational component identities independently include policy/version |
| F-12 issue/checklist/original-issue coverage | W08 positive IDs, explicit checked/deferred state |
| F-13 success | W01 operation vs check facts; W03/W04 empty/incomplete cases |
| F-14 portability | W07 removals and absence of consumer-project imports |
| F-14A obsolete agent hints | W07/W11 deletion and no repeated authority |
| F-14B test placeholders | W07 explicit real cases; no assert True |
| F-15 persistence target | Existing DI-04 target policy + W01 checked write/result |
| F-16 purpose introspection | W06 catalog/schema view, no derived purpose |
| F-17 qualified identities | Approved DI-03 retained manifest IDs and qualified public identity contracts |
| F-18 discovery | Remains deferred; 50-ID escalation, no runtime truncation |
| F-19 one check authority | W03 bindings; W01 pre-mutation consumers |
| F-20 extension suite | W02–W05/W09 independent roles and migration |

All 22 finding IDs have a workshop or explicit deferral. This is proposal routing, **not completed canonical coverage**. The 44 Approved Strategy rows, 19 invariants and 23 expected results retain their exact [intake ownership](C:/temp/pgmcp/docs/development/issue460/design-intake-map.md); human review and canonical integration must close each row's concrete contract/evidence, not just mark this table green.

## 8. Integration passes

1. Authority/scope: remove superseded assumptions from drafts, preserve current Research and existing approvals.
2. Contract/data flow: follow a concrete template selection through schema, profile, adapter, mutation, cache and presentation; follow separate tests/fixes paths.
3. Failure/cutover/removal: inject conceptual counterexamples, check who reports facts, and trace obsolete source/test/doc roots.
4. Artifact audit: links, section structure, IDs, source paths, proposal markers and canonical file preservation.

The actual findings/corrections are recorded in [the audit](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/13-consistency-audit.md), not advertised as independent QA.

## 9. Compatibility, migration and removal

Every legacy removal requires its behavioral owner and replacement evidence or explicit no-retained-behavior rationale. Re-run hidden-aware root search when canonical cutover is implemented, including pyproject, README and mapped instruction sources. Historical archives are not rewritten into V3. New supported aliases or dual reads remain prohibited.

## 10. Verification performed versus required

Performed here: read-only structural inspection; catalog path/count/uniqueness checks; proposal link/structure checks; cross-package reasoning. Not performed: production changes, runtime adapter conformance, native parity, wheel builds, deployment, full 151-test semantic re-audit or independent QA.

## 11. Review points and Design exit

Review shared support boundaries, supporting conftest ownership, independent evidence
and no-gap criteria. W09 profiles/native values, W05 direct-fix scope/stop policy and
W08 Planning projection are already decided; do not reopen them through test design.
W12 discussion closure still requires canonical DI-08 consolidation and a final audit of
the full canonical set, including stale DTO/URI/status references. Workshop approval
does not substitute for that audit or independent QA.

## 12. Planning consequences

After independent Design review, Planning must assign every 126/151 row to a concrete bounded cycle with write set, preserved behavior, rollback point and independent stop/go evidence. Check/test/fix are separately proven; F-10 activation and F-20 fix application separate; internal routes work before public cutover. This draft assigns no cycles and cannot authorize progression.

## 13. Traceability

DI-08/I-14/E-17; XC-01 architecture; XC-02 complete removal graph; RC-01 Research fidelity; package-owned evidence remains with its package.

## 14. Related documentation and history

Return to [the review guide](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/00-README.md) and use [the audit](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/13-consistency-audit.md) for cross-package issues.  
0.1, 2026-09-10: temporary proposal.
