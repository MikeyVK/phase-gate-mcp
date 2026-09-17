<!-- C:\temp\pgmcp\temp\issue460-design-workshops-20260910\09-native-settings-migration.md -->
<!-- template=design version=5827e841 created=2026-09-10T09:24Z updated= -->
# W09 — One native configuration authority and honest migration evidence

**Status:** HUMAN-APPROVED AND CONSOLIDATED — 2026-09-11; local W09 closed; independent QA pending  
**Owner:** DI-05; interfaces W02–W05; DI-07 documents; DI-06 packages  
**Decision nucleus:** Preserve useful behavior explicitly, remove hidden parallel settings, and do not mistake renamed gates for completed migration.

## 1. Purpose and authority

Updated after independent QA GO for the concrete code/test and document/tracking contracts.
Those designs are binding inputs, not reopened by W09. This is a temporary discussion artifact;
accepted outcomes will be consolidated into design-execution-adapters.md under DI-05.
The configurable starting-set boundary is now recorded in canonical DI-05 §7.19:
profile composition, template assignments and invocation defaults must not be hardcoded.
The five initial groups are a configurable starting point, not a permanent server taxonomy.
The human-approved contract now lives in [DI-05 §7.20](../../docs/development/issue460/design-execution-adapters.md#720-w09--concrete-starting-adapters-and-migration-contract).
That section supersedes the candidate inventories and unresolved selection sketches below:
it selects a preserved Markdown preflight adapter plus separately selected Lychee,
content-only syntax/message capabilities, and explicitly approved native settings changes.
This temporary document retains earlier preparation as context, not a second current proposal.
Earlier preparation wording about fix proposals, manifest-owned output profiles and model-example
validation is superseded by the canonical contracts listed below.

The workspace currently has two sets of tool settings. A developer can see a clean IDE while PGMCP applies additional isolated rules. The approved direction is one effective native configuration mechanism, with PGMCP selecting operations rather than owning duplicate rules.

## 2. Scope and exclusions

Official capability inventory, current setting disposition and native verification obligations. No installation automation, replacement programming-language parser, new release platform promise or broad unrelated settings cleanup.

## 3. Binding inputs

- [Research](../../docs/development/issue460/research.md): current approved strategy and amendments.
- [DI-05](../../docs/development/issue460/design-execution-adapters.md): §§7.3, 7.14–7.18,
  especially configured args, consumer selection and native fix scope/order/stop behavior.
- [Code/test contracts](../../docs/development/issue460/design-code-test-artifacts.md) and
  [document/tracking contracts](../../docs/development/issue460/design-document-tracking-artifacts.md):
  bounded independent QA GO; nine plus ten retained families.
- [Suite resolution](../../docs/development/issue460/design-suite-resolution.md): policy.yaml owns
  output_profile; neither policy nor external check config enters generation pf/sf.

[quality.yaml](C:/temp/pgmcp/.pgmcp/config/quality.yaml), [pyproject.toml](C:/temp/pgmcp/pyproject.toml), [pyrightconfig.json](C:/temp/pgmcp/pyrightconfig.json), [PythonValidator](C:/temp/pgmcp/mcp_server/validation/python_validator.py), [MarkdownValidator](C:/temp/pgmcp/mcp_server/validation/markdown_validator.py), [RunTestsTool](C:/temp/pgmcp/mcp_server/tools/test_tools.py), and DI-05 Q-ADAPTER-06.

## 4. Proposed decisions

| ID | Proposal |
|---|---|
| W09-A | Consolidate four overlapping Ruff gate commands into native formatting and lint responsibilities |
| W09-B | Keep Mypy and Pyright independent, not deduplicated findings |
| W09-C | One shared Python syntax profile for all eight Python/pytest templates; distinguish Markdown document/body needs, TypeScript and commit preflight |
| W09-D | Move native coverage targets/thresholds and tool rules to their native config |
| W09-E | Record intentional configuration differences separately from preserved behavior |

## 5. Responsibilities and boundaries

Official packages own native invocation/result interpretation. Workspace native config owns settings. checks/tests/fixes config owns binding/selection, deadlines and use-specific default_args under DI-05 §7.16. Explicit check/test/fix callers can replace those lists; scaffold/safe-edit cannot. This is declared invocation configuration, not a duplicate native-rule schema. Generic PGMCP does not interpret tool flags, rewrite severity, dispatch by source language or carry native parser recipes.

## 6. Options and rationale

Blindly moving quality.yaml into adapter code preserves hidden settings and violates the chosen authority. Blindly choosing the current IDE baseline can silently weaken agreed checks. Recommended: explicit value-by-value disposition, with visible native settings and measured preservation/delta evidence during implementation.

## 7. Detailed design

### Consumer coverage: apply existing mechanisms, do not redesign them

| Consumer | How checks/operations are chosen | Defaults and remaining work |
|---|---|---|
| scaffold_artifact | Selected template policy.yaml output_profile, then checks.yaml binding IDs | Configured args only; complete candidate content; no full-workspace quality run |
| safe_edit_file | Existing explicit-template/metadata/extension selection, then the same profile/bindings | Configured args only; same check facts, independently owned edit/persistence result |
| run_checks | Explicit checks or profile, otherwise configured default_profile; mandatory scope | Binding default_args, optionally replaced per selected CheckId |
| run_tests | Existing explicit/default test-selection contract and mandatory scope | Binding default_args, optionally replaced per selected TestId; no check profile is executed |
| apply_fixes | Explicit ordered fixes and scope=targets with existing concrete files | Fix binding defaults, optionally replaced per FixId; direct native mutation, stop-first, no automatic verification |

There is no universal consumer → profile chain: test/fix select their own role bindings, not checks.yaml
profiles. Native rules live in their normal configuration; binding defaults describe a deliberate use.
No caller args are added to scaffold/safe-edit. Selection, scopes and result schemas are already decided.

### Proposed profile coverage for all nineteen retained templates

The table fixes proposed reuse boundaries, not yet an installable or verified capability inventory.

| Proposed profile | Exact template consumers | Minimum intended evidence | Open implementation/selection decision |
|---|---|---|---|
| python_preflight | python_pydantic_dto, python_pydantic_config, python_class, python_protocol, python_adapter, python_worker, pytest_unit_test, pytest_integration_test | Parse complete proposed Python without executing/importing it | Reuse existing syntax behavior behind a process adapter; no DTO/config duplicate profiles |
| markdown_document | architecture, research, design, planning, validation_report, reference, generic_doc | Applicable full-document structure, including H1; preserve separately reported local-link observations | Choose native/adapter rule scope without turning a draft into a final-document quality gate |
| markdown_body | issue, pr | Applicable body structure; no external H1 requirement | Specify a meaningful bounded check, not a successful no-op or a full-document check |
| typescript_preflight | typescript_dto | Native source syntax evidence; no whole-application compilation promise | Select exact parser/API and independent positive/negative evidence |
| commit_preflight | commit | Conventional-message structure after the approved persisted provenance line | Select checker and its settings authority; do not treat provenance as the commit subject |

Previously proposed python_dto_preflight and python_config_preflight are redundant after model-example
validation withdrawal. Their examples remain schema-checked and rendered, not model-validated.
Separate profile names are justified only by an actual difference in selected checks or configured use.

A capability may support both content and selection so run_checks can reuse it. Content support
does not automatically imply selection support; the manifest contract must declare and prove both.
This table lives in Design only; generic code must not contain it. Concrete policy files reference
profile IDs and checks.yaml owns profile composition.

Extension fallback is separate from template-directed selection. Proposed .py and .ts mappings are
their language preflight profiles. The .md choice must be settled explicitly: an unknown Markdown
file is not proof of a full document or an issue body. Do not infer template purpose from suffix.
Do not map all .txt files to conventional commits. No new template-ID or header inference is needed.

### Proposed execution binding inventory

Identifiers below are candidate configuration IDs, not fixed public tool field names or implemented
packages. Role, capability and integration availability must be independently demonstrated.

| Binding / native integration | Role | Consumer purpose | Settings authority |
|---|---|---|---|
| python_syntax / native Python parser | check | Content preflight; explicit syntax-only selection | Python parser/runtime semantics; no invented lint config |
| python_format / Ruff format | check and separately fix | Formatting assessment or caller-authorized native formatting | Native Ruff config |
| python_lint / Ruff check | check and separately fix | Configured lint or caller-authorized native fixes | Native Ruff config |
| python_types / Mypy | check | Deliberate type analysis; preserve relevant existing module-policy differences | Native Mypy config/overrides |
| python_pyright / Pyright | check | Complementary native type analysis; no cross-tool finding deduplication | Native Pyright config |
| markdown structure/body/link integrations | check | Profile-appropriate content or explicit checks | Exact native tool/settings choices remain to be selected |
| typescript syntax integration | check | TypeScript content and declared selection | Exact native TypeScript integration remains to be selected |
| conventional-message integration | check | Saved commit artifact/content assessment | Exact checker/config source remains to be selected |
| pytest / Pytest | test | Behavioral tests and explicit native collection/filter/coverage options | Native pytest and coverage configuration |

Keep formatting and lint as different capabilities even if both live in one Ruff adapter package.
The four current Ruff gate invocations can be consolidated to format plus lint without removing
E501/PLC0415; whether all effective exclusions survive must be proven from actual native behavior.

Do not register several overlapping test bindings merely to replace the old coverage boolean:
a default selecting all test bindings could run the same tests twice. First proposed migration is
one Pytest binding with ordinary native defaults; explicit coverage args select coverage using
native-configured sources/thresholds. Final default selection follows the already approved run_tests
contract, not a new W09 shortcut.

A candidate explicit Python maintenance profile may combine formatting, lint, Mypy and Pyright.
It is not assigned to scaffolding/safe-edit merely because the artifact is Python. Exact type-check
module bindings and the run_checks default remain concrete migration decisions.

### Current evidence and limits

The existing Python pre-write validator calls ast.parse. Moving that operation behind an adapter
does not require generated-model import/execution or full lint/type analysis.

Existing MarkdownValidator checks H1 and missing local inline-link files; missing files are warnings,
pure #anchors are skipped, and referenced-link definitions are not a complete native-link proof.
Preserve the distinction between warning evidence and failure. Do not promote warning-only checks
into blocking results by renaming the capability or return an unchanged verdict after silently broadening it.

DI-05 §7.13 records earlier bounded experiments: markdownlint detected a missing pure TOC anchor;
Lychee with scratch/base/self-remap checked the combined self/neighbor fixture without writing the
target. These prove candidate techniques, not official package selection. A native replacement may
check more constructs or report different severity; record that as an explicit proposed delta.
No new experiment or external tool installation has been performed in this update.

### Current setting disposition

| Current source/value | Proposed owner/value | Preservation or intentional delta |
|---|---|---|
| Ruff format --isolated --line-length=100 | native [tool.ruff] line-length=100; separate read-only format check and authorized native fix | Drop isolated override; preserve 100 |
| Ruff strict lint select E,W,F,I,N,UP,ANN,B,C4,DTZ,T10,T20,ISC,RET,SIM,ARG,PLC | native [tool.ruff.lint].select | Preserve selected families |
| Separate PLC0415 and E501 gates plus lint ignores of those codes | One native lint selection includes both; no gate-number split | Preserve checks, consolidate invocation/report grouping |
| Native ignore ANN401/ARG002 vs stricter isolated run | Proposed remove those blanket ignores; explicitly document necessary scoped exceptions through normal native config | Visible strictness change for IDE; requires evidence and owner review |
| Conflicting test per-file ignores | Preserve explicit justified per-file exceptions in native config, with legacy tests ANN/ARG behavior recorded; do not invent generic server test exceptions | Exact exception list reviewed against current claims before canonical migration |
| Ruff target-version=py311 | native target-version=py311 | Preserve |
| Mypy --strict for DTOs and listed mcp_server flags, while pyproject already sets strict=true | Verify effective native configuration before selecting per-module overrides | CLI labels alone do not prove the mcp_server route is actually less strict |
| Mypy selected backend/mcp_server paths | Native file/module selection for workspace mode; explicit-target handling remains native | No hidden Python path filter in generic scope |
| Pyright command pythonversion3.11 vs native config3.13 | Proposed native pythonVersion3.11 aligned with declared minimum language target; expose change for approval | Intentional native-config delta, not mechanically equivalent |
| Pyright Windows platform override | Keep native platform setting where workspace wants it; remove command override | No portable-host claim from this value |
| Pyright --level warning --warnings | Adapter must preserve warning-fails semantics only through a documented native policy/control with conformance evidence | Do not silently downgrade warning treatment |
| Exclusion of deliberate validation fixtures | Native per-tool exclusions and explicit native target semantics | Preserve purpose, no generic reimplementation of exclusions |
| Test coverage sources backend/mcp_server and threshold90 hardcoded in tool | Native coverage run/report config, branch=true and reviewed source/threshold values | Remove hardcoded workspace knowledge; validate actual workspace sources |
| Native pytest addopts -n auto | Native pytest configuration | Preserve scheduling; generic process owns descendants |
| Tool-specific timeouts 60/120; tests300 | Role bindings retain 60/120/300 as relevant | No timeout in manifest/profile; override explicit |
| artifact_logging / quality baseline/replay | Existing report cache retained; auto-specific logging/state retired where no remaining consumer | No new execution-result cache |

Rows marked review/delta are concrete unresolved choices, not accepted values. The table deliberately does not claim current output equivalence before native comparison evidence.

### Remaining output-profile capability decisions

The first workshop checkpoint is the five-profile partition and consumer mapping above. It does not
close exact Markdown, TypeScript or commit integration, .md fallback, or native-setting deltas.

TypeScript scaffold syntax needs a real native parser integration (for example a provisioned TypeScript package API inside its process adapter), not .ts filename acceptance. DTO/configuration example validation is withdrawn, not an unresolved capability; syntax checks do not certify examples. Plain-text commit content needs a meaningful declared preflight if the nonempty-required-profile rule remains universal.

For TypeScript, the bounded candidate is a separately provisioned native TypeScript parser inside a process adapter, consuming proposed content and logical filename, returning syntax evidence without compiling a whole project or importing generated code. Native availability remains on-use and actual API/config behavior needs independent conformance; no generic compiler service is proposed.

For commit content, the bounded candidate is a conventional-message preflight adapter: consume complete draft text, recognize the already defined first-line provenance using the published dialect, and check the remaining subject/body against the intended conventional-commit content grammar. Any repository-specific type vocabulary must have one explicit native/settings authority, not be hardcoded into generic PGMCP. Whether the existing commit-type config supplies that authority without creating a new layered rule system is an explicit review point.

Human decision 2026-09-11: semantic DTO/configuration example validation is withdrawn. Preserve example authoring/rendering and context-schema shape checks; no example adapter, model execution, hidden context channel, unavailable placeholder or profile requirement. See research.md#example-validation-withdrawal--2026-09-11. This is no longer an open implementation obligation.

These are decisions for existing retained consumers, not new product roles. Do not install an always-pass placeholder, reduce a promised validation to filename acceptance, or promote this proposed inventory as conformance evidence.

### Dependency contributions

Use ecosystem-native dependency metadata/contribution files under each official adapter package. Distinguish runtime prerequisites from adapter-development dependencies. W02's declared file inventory includes these authored files. Workspace owner chooses installation/lockfiles; discovery and execution never pip/npm install automatically. Current pyproject dev extras remain packaging evidence, not a guarantee every native tool is present.

## 8. Flow and state

Scaffolding consumes a small content-capable profile. run_checks consumes maintenance selection. run_tests selects behavioral suites. apply_fixes runs explicitly selected native mutations in caller order and stops on first non-success; agents own follow-up checks and recovery. A native tool may be absent at use; that does not remove its configured schema entry. Tool version is discovered only when invoked.

## 9. Migration and removal

Remove quality.yaml commands/parsing_strategy/fix_command/gate numbers from executable authority; remove duplicate native settings in adapter source or YAML. Keep “quality gate” only for workflow decisions consuming evidence. Root pyproject package-data and release inclusion are DI-05/DI-06 explicit consumers, not forgotten project files.

## 10. Evidence

For each retained capability: same known-good/known-bad input, comparable native version and effective config, old/new evidence comparison; intentional deltas listed and approved separately. Conformance observes no source writes for checks, authorized files-only direct fixes with stop-first and truthful partial-mutation evidence, native config/args semantics without a generic fresh guarantee, dependency-unavailable and no invented warning/error normalization. Direct native/protocol evidence must exist independently of the new public tools.

## 11. Review points

The configurable starting set and ownership boundary are accepted in DI-05 §7.19. Next settle concrete native settings/integrations and the Markdown extension fallback as initial configuration, not permanent code-owned categories. Acceptance does not assert that every native option has already been proven portable. Future implementation evidence may reject an integration technique without changing native ownership.

## 12. Planning consequences

Check, test and fix migration are separately proven. Official package inclusion and direct conformance precede legacy removal; no combined “migrate all tools” cycle.

## 13. Traceability

Q-ADAPTER-06/07/10; F-08/F-19/F-20; root pyproject catalog row; DI-03 profile obligations; I-16/I-19; E-13/E-20/E-23.

## 14. Related documentation and history

Next: [W10 distribution](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/10-distribution-integration.md).  
0.2, 2026-09-11: reconcile approved DI-03/DI-05 contracts; propose five profile families, explicit consumer routes and current migration gaps; no runtime/config/code changes or new native probes.
0.3, 2026-09-11: record accepted configuration-only starting-set boundary and canonical D-ADAPTER-28; exact native settings remain open.
0.4, 2026-09-11: route concrete adapter design to canonical DI-05 §7.20 proposal; earlier candidate tables retained only as preparation history.
0.1, 2026-09-10: temporary proposal; source inspection, no native execution.
