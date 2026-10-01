<!-- pgmcp:v1 id=research pv=1.0.0 pf=i6OWAIfugGkQJPIz sf=9PfER5JkyAoFQLRi -->

# Issue 469 — Native Adapter Robustness and Related Scope Research

**Status:** RESEARCH REOPENED — ownership and release principles approved; concrete write-policy decision pending
**Version:** 1.1
**Last Updated:** 2026-10-01

## Purpose

Establish observed defects, causal evidence and affected consumers for the approved combined issue-469/474/475 delivery. Record the owner's corrected responsibility boundary and proportional release principles; reopen the concrete operational-write strategy before dependent Design choices.

## Scope In

Accepted issue 469 scope: audit all nine shipped packages, ten implemented roles and thirteen capabilities for native invocation size, quoting, selection/discovery/exclusions, inaccessible paths, output classification and version conformance. Human-approved extension on 2026-10-01: issue 475 check completion and issue 474 adapter-directed filesystem effects are active deliverables on this branch, with separate issue identities and acceptance criteria.

## Scope Out

Production implementation and permanent regression-test design; the approved isolated Research effect probe is permitted. Detailed fix structure and cycle sequencing; OS sandboxing and execution of untrusted adapters/code (R-06); generic automatic batching; broad archive cleanup, ACL changes, dependency installation and startup-health redesign; GitHub issue reassignment/closure; reinterpretation of historical issue-460 approvals.

## Prerequisites

- Active bug/469-native-adapter-robustness branch, now in Design after the owner's explicit phase-entry request. This owner-directed Research amendment reopens strategy without a backward/forced phase transition; dependent Design selection is paused.
- Read current phase instructions, Documentation Standard and Architecture Principles.
- S1, the original approval and the subsequent explicit ownership/release correction are recorded below. B1 ownership is amended, B4's concrete policy is reopened; B2 is constrained by the revised resource-ownership boundary. B3/B5/B6 and the isolated probe authorization remain unchanged. Independent QA remains separate.

## Problem Statement

Large explicit selections exceed native Windows command-line limits even though the adapter request arrives through stdin. Ruff discovery encounters inaccessible paths and verbose output misclassifies the access failure. Several check adapters also claim passed for metadata-only invocations. The approved isolated effect probe demonstrates cache routing through CLI, configuration and environment in Ruff check/fix and Mypy check outside the simulated B4-authorized destination. The writes are observed facts; whether such operator-configured operational writes should be prohibited in this release is now an explicit reopened policy question. Selected-source admission alone does not confine arbitrary process effects.

## Goals

- Separate symptoms, root causes, counterevidence and unverified applicability for every shipped adapter/role.
- Compare coordinated versus separate delivery of 474/475 with concrete cost and risk.
- Define corrected behavior and compatibility strategy per affected boundary without selecting implementation mechanisms.
- Preserve honest evidence: native unavailable and failed runs are never passing certificates.
- Separate PGMCP execution/write-policy ownership from native translation; compare achievable and desirable restrictions against the personal-use release audience and communicate accepted risk.

## Background

Issue 469 owns D-VAL-01 from issue 460. Issues 474 and 475 retain D-VAL-06 and D-VAL-07 identity. The source notices explicitly required separate issues. The human approved their shared delivery branch on 2026-10-01 while preserving those separate issue identities and acceptance criteria. Their issue bodies are follow-up boundaries, not approved designs.

Startup found only untracked .pgmcp/state.json and .pgmcp/deliverables.json. The project plan has Research active and later phases pending, with no planning deliverables. There is no issue-469 Research artifact or QA verdict to supersede. Issue-460 Validation records independent QA NOGO and owner dispositions; it is historical evidence here, not a verdict on 469. Historical cache receipts a7bf3cd5498640069bdba82274bf5fc0, c3115667351b48dab1e6e22c44e731aa and bfb9ce644ab842f39d000ce974851cf4 were unavailable on this server, so the decisive read-only observations were reproduced.

## Findings

### Defects and causal boundaries

| ID / owner | Observed versus expected | Cause and counterevidence |
|---|---|---|
| F469-01 / 469 | 1,171 existing file targets make Ruff format/lint and Mypy unavailable with WinError 206 and Pyright unavailable with ENAMETOOLONG; one selected Python file completes all four checks | Selection arrives through JSON stdin, then each adapter appends all absolute paths to one child argv. Native extension filtering happens too late to reduce launch size. This is a native-child launch limit, not proof of a long individual filename, timeout or generic JSON transport failure |
| F469-02 / 469 | Configured Ruff format reports access denied; --verbose changes reason from execution_error to invalid_configuration and selects a benign configuration debug line as message | Ruff's classifier scans all output for broad configuration markers; its message selector takes the first meaningful text line. The native evidence still contains the same os error 5; changing verbosity did not repair access or make configuration invalid |
| F475-01 / 475 | Mypy, Ruff lint and Pyright report passed for --help on an explicit file; Ruff format does the same, and lint --show-files returns passed with only a pathname | Metadata/early-exit admission is missing and native exit 0 is accepted as completion. Mypy's parser SystemExit(0) guard explicitly returns None, permitting the second native help invocation. Generic protocol validation checks declared status/exit agreement, not whether the native tool analysed sources |
| F474-01 / 474 | Approved isolated probes show cache writes in a simulated unauthorized location for CLI, native config and environment in Ruff check/fix and Mypy check; allowed/default-cache and disabled-cache controls distinguish effects | Native option-source routing reaches a process without destination-authority validation. Ruff fix token/file admission constrains sources, not caches; Mypy's write guard does not constrain native cache destinations. Fifteen redirected cases wrote files; five existing report-output guards refused with no writes. See [effect-probe.md](effect-probe.md) |

[ScopeResolver and CheckSelector](../../../mcp_server/execution/check_selection.py) own configured=[] versus workspace=[root], explicit paths, branch deletions and collapse of covering directories. [CheckService](../../../mcp_server/execution/check_service.py) aggregates adapter decisions. [Process runtime](../../../mcp_server/execution/process_runtime.py) owns transport, timeout and process-tree lifetime. None of those responsibilities justifies tool-specific parsing or silently replacing a large explicit selection with workspace/configured discovery.

Fresh configured access evidence does not name the denied child path. Archive discovery is documented in the historical issue-460 notice and current Ruff config has no general docs/archive exclusion, but this new run alone cannot identify the denied path or attribute every finding to archived examples.

### Individual applicability audit

All rows are source-inspected. Fresh tests exercise ordinary native success, negative diagnostics, configuration and guard behavior; they do not prove every large-selection or effect candidate below.

| Package / implemented role and capabilities | Invocation, selection, quoting and access boundary | Completion and filesystem-effects boundary | Version basis |
|---|---|---|---|
| [python_syntax check: syntax](../../../mcp_server/bundled_adapters/python_syntax/check.py) | One supplied content snapshot via JSON; ast.parse in-process; no target-list child argv or native discovery. Logical filename is diagnostic context | Rejects all args; parses without importing source. No adapter-directed source/cache writes in this entrypoint; interpreter effects remain a separate audit item | Reports actual Python; stdlib-only declaration, runtime 3.13.7 observed |
| [typescript_syntax check: syntax](../../../mcp_server/bundled_adapters/typescript_syntax/check.cjs) | One snapshot via language-service API, no target-list child. Reads nearest tsconfig and native config discovery, whose access failures need distinct evidence | Rejects all args; syntactic diagnostics only, no emit. Configuration/import effects are not an OS confinement guarantee | Dependency/test pin 6.0.3; reports ts.version |
| [markdown_preflight check: document/body](../../../mcp_server/bundled_adapters/markdown_preflight/check.py) | One content snapshot; local link existence checks. No target-list subprocess; H1 required only for document; broken local links are warnings | Rejects all args. No entrypoint writes. Limited preflight semantics must not be relabelled a full link/lint check | Actual Python; stdlib-only declaration |
| [commitlint check: message](../../../mcp_server/bundled_adapters/commitlint/check.py) | Message supplied on stdin; argv carries native args, including JSON args for parser guard. Target count cannot cause the bulk-path defect, but very large args can; native JS config remains trusted executable behavior | Native parser guard refuses help/version/print-config and alternate message sources; disables JITI_FS_CACHE. Custom config/formatter effects require an individual authority audit | Pin 21.2.2; guard reads actual package version; tests verify pin |
| [ruff check: format/lint](../../../mcp_server/bundled_adapters/ruff/check.py) | Direct argv, no shell; every target appended. Fresh size failure. Native discovery and explicit-target exclusions differ; no -- separator in check call. Verbose classification defect reproduced | Fresh help/show-files false PASS. Fix/stdin/output-file args and RUFF_OUTPUT_FILE are blocked, but the effect probe demonstrates cache destination writes through CLI, native config and RUFF_CACHE_DIR; check source-byte preservation alone is insufficient | Pin and fresh actual 0.15.6 |
| [ruff fix: format/lint](../../../mcp_server/bundled_adapters/ruff/fix.py) | Direct argv with -- before literal existing selected files. Same all-target launch-risk by source; large fix launch and verbose classification not reproduced through a new mutation | Guard blocks metadata, watch, diff/check and added positional sources. cache-dir remains admitted, with CLI/config/environment cache effects reproduced. Selected-source mutation and partial native mutation are already intentional; cache/report authority is distinct | Pin 0.15.6; existing native fix tests exercised |
| [mypy check: types](../../../mcp_server/bundled_adapters/mypy/check.py) | Direct all-target argv, fresh size failure; native parser/config guard; rejects caller @files. Imported modules and explicit/configured roots must remain native semantics | Fresh help false PASS. Blocks shadow files, reports, JUnit, installation and selected other writes. Cache routing through CLI, cache_dir configuration and MYPY_CACHE_DIR is reproduced; native defaults and disabled-cache controls are documented | Pin and fresh actual 1.19.1 |
| [pyright check: types](../../../mcp_server/bundled_adapters/pyright/check.cjs) | Workspace-resolved native package, spawnSync all-target argv; fresh ENAMETOOLONG. Explicit targets override configured roots. Caller '-' rejected | Fresh help false PASS. Blocks createstub/stdin; verifytypes/watch and additional native modes require individual role-conformance assessment, not a blanket metadata claim | Pin and fresh actual 1.1.408 |
| [pytest test: tests](../../../mcp_server/bundled_adapters/pytest/test.py) | Direct argv to fresh --native child; all targets appended, so large argv is a static applicability candidate. Native testpaths/norecursedirs, plugins and xdist own discovery/behavior; '::' literal paths rejected | Help/version guarded after all native option sources. collect-only and native exit 5 are deliberately passed in existing tests, not automatically issue-475 defects. Cache, bytecode, reports/coverage and trusted test-code writes require separate effect classification | Pin/fresh 9.0.2; cov/xdist/coverage/asyncio pins in requirements |
| [lychee check: links, content/selection](../../../mcp_server/bundled_adapters/lychee/check.py) | Selection paths appended to direct argv, so large-selection risk applies by source; glob metacharacters escaped. Content uses one managed file with logical-base/self-remap | Fresh --help rejected. Guards cache/output/cookie/preprocess/dump/generate and inspects native TOML precedence; GET/HEAD only. Args/config/defaults/environment still need per-version audit; no identical defect is inferred from Ruff | Declared/tested and fresh actual 0.24.2 |

Pins/declarations live in each package's requirements.txt/package.json/dependencies.json, not in generic code. Current metadata reporting is not enforcement of a supported-version range. Fresh observed versions match the declared/tested versions; no live version-drift defect is claimed.

### Native-strategy feasibility evidence

Mypy 1.19.1 documents @file inputs, while the shipped adapter refuses caller-provided @arguments. Adapter-owned input construction could be evaluated without reopening caller admission. Pyright 1.1.408 documents file-list stdin, while the current adapter refuses caller '-' and launches native stdin as ignore. These are feasible research options, not selected mechanisms or equivalence proof. Ruff needs its own evaluation; no response-file support or universal batching is assumed. Independent batching can change Mypy cross-module checks, Pytest fixture/session/xdist behavior, configured discovery, diagnostics and failure ordering.

Microsoft documents a 32,767-character CreateProcessW command-line bound including NUL. The fresh probe is decisive live size evidence; no newly measured exact Windows command-line length is claimed.

### Blast radius and consumers

| Surface / consumer | Impact and required preservation |
|---|---|
| Bundled adapter code and package declarations | Native request/result translation, role-preserving mode admission, classification and version interpretation. They consume PGMCP's execution/resource authority; they do not invent filesystem rights, sandbox policy or the host environment |
| [check configuration](../../../.pgmcp/config/checks.yaml), [tests](../../../.pgmcp/config/tests.yaml), [fixes](../../../.pgmcp/config/fixes.yaml), pyproject.toml | default_args/caller replacement, configured roots, exclusions and native caches; no silent policy weakening or synthetic production-tree substitute for broad requested scope |
| [Native adapter integration tests](../../../tests/mcp_server/integration/adapters) | Reuse public entrypoints and valuable native fixtures. Extend actual selection, metadata/effect and version evidence where missing; no private helper tests or tautological return-code assertions |
| Generic selectors/services, runtime, protocol models and content preparer | PGMCP owns requested scope, execution conditions, any chosen write policy, process lifetime and allocated-resource lifecycle. Investigate the smallest required boundary changes rather than presuming these surfaces are immutable; preserve factual outcomes and existing consumers |
| run_checks; scaffold_artifact and safe_edit_file configured preflight; workflow enforcement | Incorrect completion can certify unperformed analysis; stronger adapter guards can now produce unavailable and block enforced writes. Do not change enforce/report or aggregate factual semantics by stealth |
| run_tests and apply_fixes consumers | Preserve intentionally admitted native testing modes and partial fix changes. Cache/report effects need explicit permission independently of selected source files |
| [Active quality reference](../../../docs/reference/tools/quality.md), [QUALITY_GATES](../../../docs/coding_standards/QUALITY_GATES.md), AGENTS.md/phase prompts/template policy | Update only active text proven inconsistent with adopted behavior in the owning documentation phase. No new generic flag parser, template family or independent QA authority |
| Historical issue-460 artifacts | Reviewed as origin/contract evidence and kept unchanged; they do not become current approval records |
| Third-party adapters and native configuration owners | Trusted admission is distinct from confinement. Native configuration remains tool-settings authority. Any execution-context/resource-contract change or restriction of accepted native destinations needs explicit per-boundary compatibility review; no such migration is silently authorized |

### Scope options

| Option | Cost, risk and impact |
|---|---|
| S1 — deliver 469, 474 and 475 on this branch; keep each issue's acceptance identity (**human-approved**) | One coherent audit of the same native admission/invocation/evidence code; avoids a length fix introducing unmanaged temp writes or retaining false completion. More research/design/regression work and a larger review surface. 474 has isolated effect reproduction and approved ownership/release principles, while its concrete write policy has been reopened; separate issue identities and evidence cannot disappear |
| S2 — deliver 469 and 475 together; leave 474 separate | Removes the closest completion/robustness overlap while limiting policy breadth. Any 469 length strategy requiring new writes must wait for compatible 474 authority or remain write-free; potentially duplicates adapter work |
| S3 — keep all delivery separate | Smallest per-issue review, preserves original scheduling. Duplicated guards/tests and conflict risk across the same adapter files; unresolved effect/completion dependencies must still be coordinated |

No issue is closed or its GitHub scope rewritten here. @co retains external coordination ownership.

### Per-boundary strategy — original approval and current amendment, 2026-10-01

| Boundary | Approved strategy | Alternatives, cost and risk |
|---|---|---|
| B1 generic public/wire contracts and role ownership — amended by owner | Adapters are thin native input/output translators and uphold the requested role. PGMCP owns execution conditions, allocated-resource lifecycle and any chosen filesystem authority. Preserve public contracts where coherent; do not let contract preservation force security policy into adapters. Any needed wire/consumer change requires a separate explicit strategy decision | Centralizing native parsers in PGMCP violates tool ownership; duplicating execution/write policy in every adapter violates responsibility and increases maintenance. A general policy framework is not presumed necessary |
| B2 selection and large invocation | Preserve requested selection and native config/exclusions; require length-safe adapter-local behavior or honest actionable unsupported/unavailable outcomes, never a silently narrower or broader scope. Fix source selection remains explicit files. An actionable launch-limit failure remains a limitation and does not satisfy the supported-large-selection success criterion | Automatic workspace fallback reduces implementation effort but changes coverage/authority. Naive batching risks cross-source/session semantics. Concrete mechanism and equivalence proof remain Design work |
| B3 check completion (475) | Deliberately stop admitting metadata-only or check-replacing bypasses as successful quality checks, using existing truthful non-success vocabulary. Preserve genuine native analysis, diagnostic failure, normal native config and existing explicit diagnostic policies | Keeping false PASS preserves a defective result. Adding a parallel metadata API is unneeded scope. Ruff --exit-zero diagnostics and Pytest collect-only/no-tests are deliberately tested native semantics; changing them would require a separate explicit policy decision |
| B4 filesystem effects (474) — concrete policy reopened | Separate role-contract correctness, operational-write policy and actual OS enforcement. PGMCP owns any chosen authority; adapters translate it where native integration requires that knowledge. The owner requires a feasible and desirable boundary proportionate to personal local use, simple controls for credible obvious defects, and honest residual-risk communication. Mandatory named cache roots, adapter-owned security policy and universal pre-write destination rejection from the original B4 are not current selected requirements | Compare trusted local execution, targeted cooperative controls and OS/deployment confinement below. Exact permitted destinations, enforceable guarantee and accepted residual risks remain undecided; no option is automatically selected |
| B5 supported native versions | Preserve package-local prerequisite authority and actual-version evidence. Require on-use adapter failure for unsupported versions where semantics depend on the tested version; evaluate supported versions individually, with no startup health probe or blanket stdlib pin | Report-any-version accepts unverified parser/exit behavior. Broad ranges require extra conformance evidence; every supported upgrade needs package/tests updates. Exact policy per tool belongs in Design within the approved support boundary |
| B6 diagnosis and active documentation | Correct access/usage/config classification and substantive messages regardless of verbosity while retaining bounded native evidence; document the adopted observable restrictions | Scanning any occurrence of configuration perpetuates misclassification. Reducing logs or changing diagnostics into successful outcomes hides evidence |

Original decision: the human owner accepted S1, B1–B6 and the isolated effect-probe route on 2026-10-01 with: "Ja ik accepteer je voorstel". Original B4 permitted only named workspace caches, owned temporary roots and explicitly approved workspace reports, and required rejection of other native destinations. Subsequent decision: the owner agreed to reopen the insufficiently researched ownership boundary and required explicit investigation of whether restrictions are possible and desirable for this personal-use release. The amended B1 and proportionality principles bind the current discussion; the original concrete B4 restriction is superseded as a selected requirement pending the replacement decision. This is not independent QA approval or a chosen implementation mechanism.

### Approved isolated effect-probe authority

The human authorized an isolated temporary test workspace under .pgmcp/temp/issue469-effect-probe (or its run_tests-owned temporary equivalent). The source selection, permitted cache, and simulated unauthorized destination are distinct sibling paths within that one owned root; no real external destination is targeted. Invoke trusted bundled adapters/native tools through the test boundary, inspect before/after file inventories and source bytes, and retain truthful decisions plus evidence. Vary native CLI, isolated config, child-local environment and defaults separately. Include allowed cache/write controls and denied-destination controls; a positive reproduction of the current gap is diagnostic evidence, not a passing regression assertion. Do not expose host environment values or change repository source, ACLs or host configuration. A public apply_fixes probe or actual external write requires its own selected route.

The human approved this route on 2026-10-01. Execution/effect evidence is recorded separately below; approval alone does not establish effect or acceptance closure. Python/Node runtime import caches and trusted test/plugin/config code must be inventoried separately; adapter admission is not technical confinement of arbitrary executable code. R-06 remains excluded.

## Questions

- S1/probe authorization and ownership/proportionality principles are resolved. Replacement B4, trusted-execution assumptions, acceptable operational writes, enforceable guarantees and any narrow contract-migration strategy remain Research decisions. Concrete native mechanisms and supported-version details remain Design-owned. The original xdist timeout is still an observed infrastructure uncertainty.

## References

- [Issue 469](<https://github.com/MikeyVK/phase-gate-mcp/issues/469>)
- [Issue 474](<https://github.com/MikeyVK/phase-gate-mcp/issues/474>)
- [Issue 475](<https://github.com/MikeyVK/phase-gate-mcp/issues/475>)
- [CreateProcessW command-line bound](<https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw>)
- [Mypy 1.19.1 file-list documentation](<https://raw.githubusercontent.com/python/mypy/v1.19.1/docs/source/running_mypy.rst>)
- [Pyright 1.1.408 CLI documentation](<https://github.com/microsoft/pyright/blob/1.1.408/docs/command-line.md>)
- [Ruff configuration (current, not pin-specific proof)](<https://docs.astral.sh/ruff/configuration/>)

## Approved Strategy

S1 combined delivery and separate issue acceptance identities remain approved. The owner explicitly corrected responsibility ownership: PGMCP owns the execution environment and any filesystem authority; adapters are thin native request/result translators. The release targets the owner's local use, with no current ambition for commercial security guarantees. Security work must be feasible, proportionate and honest about accepted risk. B3/B5/B6 remain approved; B2 must respect this corrected ownership boundary. Exact B4 operational-write restrictions and any resulting contract migration are **pending**, not inferred from the earlier blanket acceptance. Dependent Design selection must wait for the replacement boundary decision.

### Reopened Research: release audience, feasibility and desirable restrictions

The owner agreed that the previous ownership analysis was insufficient and added: "We zijn geen bank app aan het bouwen op dit moment maar een tool die IK gebruik." The owner permits security trade-offs when costs, guarantees and residual risks are explicit. This authorizes the Research correction; it does not automatically choose unrestricted writes, environment sanitization or a sandbox.

| Responsibility | Owner | Boundary |
|---|---|---|
| Scope, operation intent, any write policy and execution environment | PGMCP | Policy is defined once at the logical execution boundary; no native option parser or generic security DSL is presumed |
| Native argument/input encoding, role-preserving modes and result interpretation | Adapter | Rejecting a native mode that turns check into fix or help is contract translation. It does not establish process confinement |
| Temporary resource allocation and lifecycle | PGMCP | Existing controlled content-input ownership is relevant precedent. Adapter-specific formatting may remain translation; resource interfaces are Design work |
| Native rules, config discovery and tool behavior | Native tool/configuration | Preserve ordinary settings; tool options are not proof of OS authority |
| Host filesystem, network and credential permissions | Host/deployment, with PGMCP integration only if selected | A cwd, environment filter or destination guard is not an OS access boundary |

The owner targets personal local operation. A proposed release assumption is that the operator admits adapters and toolchains and intentionally executes workspace tests/plugins/configuration. This must be explicitly confirmed in the replacement B4 decision; local use alone does not establish that every repository, dependency or generated argument is trusted. Credible accidental or adversarial inputs still require proportional review. Unsupported hostile-code execution must not be marketed as confined.

#### What the current implementation establishes

| Evidence | Established behavior | Limit |
|---|---|---|
| [Adapter catalog](../../../mcp_server/execution/catalog.py) and [trust declaration](../../../mcp_server/config/schemas/adapter_manifest.py) | Official/workspace admission and workspace trust IDs; package file resolution checks containment | Admission is an operator trust decision, not verification that executing code is harmless |
| [Process runtime](../../../mcp_server/execution/process_runtime.py) | Direct argv launch, workspace cwd, managed Windows process lifetime and bounded response handling | No explicit restricted env at this launch, access-token restriction or filesystem/network sandbox is established by the inspected route. No secret values were inspected |
| [Content preparation](../../../mcp_server/execution/content_input.py) | PGMCP allocates and removes invocation-owned scratch files | Owned cleanup does not deny other host paths to executing tools |
| [Selection resolution](../../../mcp_server/execution/check_selection.py) and [fix admission](../../../mcp_server/execution/fix_service.py) | Component-aware resolved scope and selected-source admission, including re-resolution before fixes | These checks govern routed requests; they do not confine arbitrary native/test/plugin code |
| [Isolated effects](effect-probe.md) | CLI/config/environment redirect native caches outside the probe's initially approved cache location; controls distinguish actual effects | All destinations were simulated within an approved temporary root. This is not a demonstrated host escape or credential exploit; release desirability of these operational writes is reopened |
| [General filesystem adapter](../../../mcp_server/adapters/filesystem.py) | Existing resolve_path uses resolved-string prefix comparison | A sibling prefix can satisfy that comparison. No live exploit or current public consumer path was proved here; investigate exposure before routing a separate correctness fix, without broadening this branch by assertion |

Microsoft documents Job Objects as process/resource management and says process security limits require separate treatment. AppContainer provides a possible OS boundary for file/network access, but compatibility and deployment feasibility for PGMCP have not been demonstrated. Child environment inheritance is documented platform behavior; no claim is made about which credentials are present. Sources: [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects), [AppContainer isolation](https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation), [Environment variables](https://learn.microsoft.com/en-us/windows/win32/procthread/environment-variables).

#### Can versus want: proportional strategy alternatives

| Alternative, not yet selected | Can: feasibility and actual guarantee | Want: cost, compatibility and residual risk |
|---|---|---|
| L1 trusted local execution with honest role/launch contracts | Existing launch and native behavior provide a concrete baseline. Fix false completion, encoding and mode translation; preserve PGMCP-owned resources. No general native write/read/network restriction is claimed | Lowest additional policy complexity and broad native compatibility. Tools/tests/plugins retain access available under the host account and inherited environment; ordinary configured cache/report writes may be accepted explicitly |
| L2 targeted cooperative operational controls owned by PGMCP | Known unwanted routes can be checked or translated before relevant native operations; selected child environment/resource controls can reduce specific risks. Scope and feasibility must be proved per control. No general arbitrary-code confinement follows | Adds bounded contract/integration work and potentially rejected native settings. Native defaults/config/plugins can invalidate a blanket guarantee; do not reimplement every native parser, silently sanitize settings or claim prevention of all writes |
| L3 OS/deployment-enforced isolation | Windows has OS isolation mechanisms; a supported deployment can potentially enforce specific rights. Current PGMCP/tool compatibility, descendant behavior and enforcement evidence are absent | Greater integration/support cost for toolchains, imports, caches, test plugins and required network access. No current owner requirement makes this mandatory. R-06 implementation remains separate; requiring this level would reopen that scope explicitly |

L1 is a candidate release baseline; narrow L2 controls are candidates only for evidenced, credible paths with favorable cost/benefit. L3 is a feasibility alternative, not an automatic requirement or selected implementation. This recommendation is not an Approved Strategy decision.

#### Decision and evidence still required

For replacement B4, decide whether ordinary operator-configured native operational writes outside selected source files are accepted; which specific destinations or role-conflicting routes must be rejected; whether restrictions are cooperative contract controls or OS-enforced rights; and which environment, read, network and plugin/test-code risks are knowingly accepted. Assess each proposed restriction against its observable threat, PGMCP owner, achievable guarantee, compatibility cost and evidence. Keep concrete mechanisms, interfaces and code changes in Design.

The release must distinguish promised prevention, specific tested rejection, ordinary native side effects and unconfined host access. Check intent is not a claim that arbitrary test/plugin/config code cannot mutate sources. Document material accepted limits in the active execution/tool guidance when documentation owns the change; no warning-per-call, security framework or commercial assurance scope is introduced by this amendment.

Issue 474 and the historical D-VAL-06 notice currently prefer adapter-local corrections and pre-write rejection. That conflicts with treating adapters as independent write-policy owners or accepting previously prohibited operational destinations. Their text is follow-up input, not a replacement strategy. Record the selected owner disposition and route GitHub coordination to @co before claiming the issue's acceptance fulfilled or closing it.

## Expected Results

| ID | Required observable result |
|---|---|
| E469-1 | Large and bounded selections preserve intended native analysis/selection semantics; per-adapter/role applicability and limits are evidenced without silently omitting targets |
| E469-2 | Access, config, usage and launch errors are actionable and retain the same correct class under verbosity/output changes |
| E469-3 | Literal paths, spaces/metacharacters, configured discovery, native exclusions and inaccessible paths are verified individually; unknown coverage is explicit |
| E475-1 | Metadata/early-return paths cannot become passed check evidence; genuine clean analysis, real diagnostics and ordinary native settings retain correct outcomes |
| E474-1 — reopened | State the owner-selected source/operational effects, PGMCP policy ownership, achievable enforcement level and accepted limits. Prove the specific allowed/refused behavior that the replacement B4 actually promises; do not retain universal destination rejection or OS confinement as an unselected acceptance assumption |
| E469-4 | Actual versus supported native versions and unsupported-version outcomes are visible per package; no host/version generalization from a different tool |
| E-CROSS | Existing role/wire/public contracts, ordered fix stop behavior, partial mutations, caches and independent QA authority remain truthful |

## Evidence

### Fresh large-selection native-child launch failure

1171 existing files selected using host-native rg --files over mcp_server, tests/mcp_server, docs, scripts, .agents and .github before this Research artifact existed. Four checks unavailable/execution_error: Ruff format/lint and Mypy WinError 206; Pyright spawnSync ENAMETOOLONG. Native tools did not analyse this selection. Full cache reconstructed through contiguous windows with run ID, total codepoint length and UTF-8 SHA-256 verified.

- [Full large-selection DTO](<pgmcp://cache/runs/57b52ef905ce4418879df4b57db0f190>)

**Invocation:** run_checks(scope="targets", targets=<the 1171-file rg inventory>, profile="python_review", timeout_seconds=60)

**Observed Result:** incomplete; all four unavailable

### Bounded positive control

One existing python_syntax adapter source completed Ruff format/lint, Mypy and Pyright. Mypy evidence says 1 source file; Pyright JSON filesAnalyzed=1. Versions Ruff 0.15.6, Mypy 1.19.1 and Pyright 1.1.408.

- [Bounded DTO](<pgmcp://cache/runs/e3aec4a836a9476a90131c670904a285>)

**Invocation:** run_checks(scope="targets", targets=["mcp_server/bundled_adapters/python_syntax/check.py"], profile="python_review", timeout_seconds=60)

**Observed Result:** passed; genuine native analysis evidenced

### Fresh metadata and discovery-only false PASS

All three help requests returned passed with native help output; Ruff format --help and Ruff lint --show-files likewise passed. --show-files evidence is only the selected pathname. All complete DTOs were window-read and hash-verified.

- [Mypy/Ruff/Pyright help DTO](<pgmcp://cache/runs/b44ae8b074b942d99c7aa182b42e6827>)
- [Ruff format help / lint show-files DTO](<pgmcp://cache/runs/c1026cb2c1014097b1b342b8f054821d>)

**Invocation:** run_checks(scope="targets", targets=["mcp_server/tools/scaffold_tool.py"], checks=["python_types","python_lint","python_pyright"], args={"python_types":["--help"],"python_lint":["--help"],"python_pyright":["--help"]}, timeout_seconds=60); second probe targets python_syntax/check.py with python_format:["--help"], python_lint:["--show-files"]

**Observed Result:** aggregate/per-check passed, without requested analysis

### Fresh completion guard counterexample

Lychee 0.24.2 rejects help before link checking with unavailable/unsupported_input. Do not infer that every check adapter has the reproduced defect.

- [Lychee help rejection DTO](<pgmcp://cache/runs/8b4d0a2e543444cd8aa4121c3464e7f0>)

**Invocation:** run_checks(scope="targets", targets=["docs/reference/tools/quality.md"], checks=["markdown_links"], args={markdown_links:["--help"]}, timeout_seconds=60)

**Observed Result:** incomplete; unsupported_input

### Fresh discovery/access and verbose-classification comparison

Configured Ruff format reports execution_error and access denied (os error 5), 470 files already formatted. Same operation with --verbose reports invalid_configuration and a Using configuration file debug line; full evidence still ends in os error 5. Full verbose DTO window-read and hash-verified.

- [Ordinary configured DTO](<pgmcp://cache/runs/b93c67478d534689bea1a90aa9a1ac23>)
- [Verbose configured DTO](<pgmcp://cache/runs/35f022fd9e954c2082363f72217206a9>)

**Invocation:** run_checks(scope="configured", checks=["python_format"], timeout_seconds=60); repeat with args={python_format:["--verbose"]}

**Observed Result:** both incomplete; classifier/message changes although actual access error persists

### Existing all-package native conformance baseline with explicit failure

159 integration items across all nine adapter packages: 158 passed and one failed in 128.00s. Failure is direct native Pytest xdist subprocess timeout at the fixture's 45s limit, before that case compares the adapter. A narrow serial-outer rerun passed one selected item with 14 deselected in 13.85s. This is evidence of existing guard/config/diagnostic behavior; the original run remains failed and the timeout cause is not proven.

- [Original native suite DTO](<pgmcp://cache/runs/414bd776ec63440fb26b9b884174bddb>)
- [Focused rerun DTO](<pgmcp://cache/runs/23f80367a3714eda88fa218eb3fa7f6a>)
- [Native test fixture](<../../../tests/mcp_server/integration/adapters/test_pytest.py>)

**Invocation:** run_tests(scope="targets", targets=["tests/mcp_server/integration/adapters"], tests=["python_tests"], args={python_tests:["-q","-n","4"]}, timeout_seconds=300); focused rerun targets test_pytest.py, args=["-q","-n","0","-k","native_outcomes_and_options and xdist"], timeout_seconds=90

**Observed Result:** original 158 passed/1 failed; focused rerun 1 passed

### Write-authority evidence: static admission and approved live probe

Initial static inspection found Ruff fix --cache-dir admitted without destination authority. After human approval, the isolated [effect probe](effect-probe.md) observed 30 cache cases across Ruff check/fix format/lint and Mypy check types. All 15 CLI/config/environment misrouting cases created cache files at the simulated unauthorized location. Ten allowed/default cases wrote the named native cache, and five disabled-cache cases created no files. Five additional output/JUnit controls returned unavailable/unsupported_input with unchanged file inventories. Every unselected source remained unchanged; checks preserved selected source bytes; Ruff fixes changed only the selected source.

The probe runner completed its observation assertions; this is not a repaired-adapter conformance result. No actual external destination or repository source was targeted. Detailed invocations, source, per-case effects, inventory hashes and evidence limits are persisted in effect-probe.md; complete DTOs are `pgmcp://cache/runs/310efd1225fe42828f73f881e982701d` and `pgmcp://cache/runs/7ef68a12f021414bb07cfcfa99906281`.

- [Ruff fix entrypoint](<../../../mcp_server/bundled_adapters/ruff/fix.py>)
- [D-VAL-06 origin](<../issue460/deferred-work.md#d-val-06--adapter-write-effects-boundary>)

**Observed Result:** admitted cache destinations produce observed operational writes outside the original B4-approved destination; their release-policy classification is reopened. Existing report-output refusal controls remain effective.

### Research artifact verification

Scaffolding and subsequent safe edits passed the configured Markdown document preflight. The original version-1.0 offline link review recorded 36 successful links, 18 excluded external/cache links and zero errors: `pgmcp://cache/runs/2d50d34da1db4f09bcb857058071752e`. This is historical evidence. The ownership/release amendment was re-verified through markdown_link_review: 45 successful links, 21 excluded external/cache links and zero errors, receipt `pgmcp://cache/runs/65d2aa8137e741a397553c89efca49b5`. Recording these counts does not alter the checked link inventory. External/cache exclusions are not external validation. The final Research deliverables are research.md and effect-probe.md. Production, permanent tests and configuration are unchanged. The ignored diagnostic probe was scaffolded/refined under the approved temporary root; its source is archived in effect-probe.md. Original approval and the current reopened boundary are recorded; commit/push status is reported in the hand-over. The owner subsequently directed entry to Design. This amendment takes no phase transition and claims no independent QA verdict.

## Risks

### Scope combination can conceal independent acceptance gaps

Track E469, E474 and E475 separately. Resolve replacement B4 and the issue-body conflict; do not close 474 from observations or a changed risk label alone.

### Length workaround changes selection or native whole-program/session behavior

Demand per-tool native equivalence evidence; use honest unavailable outcomes if no coverage-preserving representation is demonstrated.

### Operational writes and native/version restrictions alter existing callers

Capture a human decision per boundary; document observable restrictions and tested support. Reopen a decision if later evidence contradicts it.

### Transient cache loss and xdist timing

Persist exact observations/invocations here and the effect-probe source/observations in effect-probe.md; retain cache links as supplementary transient evidence and preserve the original native-suite failure alongside the narrow rerun.

## Related Documents

- [Origin notice](<../issue460/deferred-work.md>)
- [Issue-460 native selection/fix authority](<../issue460/research.md>)
- [Documentation Standard](<../../coding_standards/DOCUMENTATION_STANDARD.md>)
- [Architecture Principles](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)
- [Active quality reference](<../../reference/tools/quality.md>)
## Bug / Research Hand-over

### Scope

Investigated 469 native invocation, selection/discovery, error classification and per-package conformance, plus human-approved active 474 write-effect and 475 check-completion scope. OS isolation, production implementation and fix design remain excluded.

### Deliverables

- [Research and approved boundary strategies](research.md)
- [Isolated write-effect evidence and reproducible probe source](effect-probe.md)
- [Native adapter source/test inventory](../../../mcp_server/bundled_adapters)

### Evidence

Fresh large-selection failures, bounded genuine-analysis control, false-PASS reproductions and verbose classification comparison are indexed above. The isolated probe recorded 30 cache cases plus five no-write refusal controls. Document preflight and focused link verification are reported with their exact scope; the original 158-pass/one-timeout native-suite run is retained alongside its successful focused rerun. Human approval covers S1 and the current ownership/proportionality principles; the original B4 concrete restriction is reopened. No replacement B4 decision, QA progression or fix design is inferred.

### Open Work

Replacement B4 decision with explicit trusted-execution assumptions, achievable guarantee and accepted risks; any resulting narrow compatibility decision; independent Research review. Dependent Design selection is paused. Native mechanisms, per-tool supported-version detail and implementation regression boundaries remain Design-owned. Investigate the original outer-parallel xdist timing if it recurs; no causal attribution or test-budget change is selected here. GitHub coordination/issue closure remains with @co; 474/475 retain identity and are not closed by this Research.

### Review Request

Review requested. Open or resume the independent interactive pgmcp-qa task for Research review; do not infer GO from this producer hand-over.


