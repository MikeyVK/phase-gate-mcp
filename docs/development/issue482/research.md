<!-- pgmcp:v1 id=research pv=1.0.0 pf=lgBwxWMfTAmNNg_O sf=5--KpGf2wHUv2qAj -->

# Issue 482 — Configured branch targets research

**Status:** Prepared for independent Research → Design review  
**Version:** 0.14  
**Last Updated:** 2026-10-06

## Scope In

Branch preselection for selection check capabilities, package capability metadata, truthful empty results, deliberate file/directory semantics and the already authorized native Ruff archive/cache policy correction.

## Scope Out

Branch test/fix operations, impacted-test selection, content-check filtering, template consumption (#476), startup/recovery, transport-size work (#469), native discovery helpers and unrelated archive-code or adapter-guard repairs.

## Problem Statement

Branch checks currently send the same mixed Git candidate list to every selected check. This can offer Markdown/JSON/Jinja to Python tools and turn native source-discovery settings into inappropriate explicit-source requests. Separately, generic directory covering removes a deliberately supplied descendant file, which can change native file/directory meaning.

The owner-approved solution is **configured_targets**: a check-specific declarative preselection applied only to branch scope. It does not promise equivalence to native configured discovery.

## Goals

- Filter branch candidates through a common capability declaration without tool-specific code in PGMCP.
- Keep native configuration and invocation behavior unchanged after preselection.
- Preserve other scopes and deliberate directory-plus-file targets.
- Report no applicable work truthfully without full-project fallback.
- Keep the change and its verification proportional.

## Background

[Issue473's deferred audit](../issue473/tool-practice-findings.md#deferred-branch-wide-check-solution--owner-disposition-2026-10-04) and [V-F8](../issue473/validation.md#v-f8--branch-python-profile-sends-mixed-source-kinds-to-native-python-tools) are historical evidence. The original exact native-discovery intersection was investigated, then replaced by the owner's reverse-route decision.

On 2026-10-06 the owner endorsed configured_targets as branch-only check-specific preselection with an unchanged native call. The owner then explicitly supported extending the existing generic reading of package capabilities, provided generic code acquires no adapter-specific knowledge. The final discussion distinguished check/selection capabilities from Pytest's separate test role, after which the owner requested Research closure and independent QA.

Issue481's wire/error strategy is not inherited by this issue. Current user decisions supersede the older exact-resolver framing in the issue body; the technical findings below preserve why that route was not selected.

## Findings

### Current responsibilities and package knowledge

| Boundary | Existing responsibility / source | Effect on this issue |
| --- | --- | --- |
| Git/filesystem scope | [ScopeResolver](../../../mcp_server/execution/check_selection.py) resolves Git candidates and safe existing workspace targets. configured has no targets; workspace supplies the root. | Keep generic scope resolution. Branch filtering only reduces candidates; it does not scan directories. |
| Capability admission | [ConfigLoader](../../../mcp_server/config/loader.py) reads manifest.yaml through [AdapterManifest/CheckCapability](../../../mcp_server/config/schemas/adapter_manifest.py). | A common declared filter can use this existing public metadata boundary. |
| Catalog | [AdapterCatalogLoader](../../../mcp_server/execution/catalog.py) validates inventory/trust, selects launches and builds immutable [AdapterBinding.capability](../../../mcp_server/core/interfaces/execution.py). | The selector can consume the already-read capability; no repeated package/native config reads are needed. |
| Check selection | CheckSelector resolves check bindings/profiles, effective args and one request per check. Each currently receives the same scope.targets. | Each branch check can instead receive its own declared subset. |
| Adapter boundary | [Protocol](../../../mcp_server/execution/protocol.py) sends operation, targets, args and execution_context. Packages own native arguments, source transport, relevant guards and diagnostics. | Native request shape and command construction can be preserved. No intent field is needed solely for server-side filtering. |
| Result execution | [CheckService](../../../mcp_server/execution/check_service.py) suppresses a globally empty branch but currently treats unexecuted rows as incomplete. | Per-check no-applicable planning/result handling is required. Never send a filtered empty list as configured discovery. |
| Deliberate targets | _collapse_targets removes descendants covered by a directory. | Preserve deliberately selected directory plus descendant; exact duplicate removal need not expand sources. |

PGMCP already interprets adapter ID/version, package inventory, roles/contract versions, entrypoints, named capabilities, inputs, content requires_file and fix addresses. Native dependency files are read as inventory bytes for identity, not interpreted by the selector. The examined generic selection/runtime path contains no Ruff/Mypy/Pyright/Lychee configuration interpretation.

Package-authored public metadata and generic enforcement can coexist: the matcher knows one contract, while applicability values remain declared data. An adapter-specific if-chain, native-config parser or tool pattern dialect in generic code would violate this boundary.

### Minimum additional selection knowledge

The selected Research direction is a configured_targets declaration **per selection check capability**:

| Datum | Meaning |
| --- | --- |
| include | Nonempty workspace-relative path-pattern list admitting branch candidates. Patterns can express roots, suffixes and exact filenames. |
| exclude | Workspace-relative path-pattern list removing admitted candidates; [] explicitly means none. |

For a candidate, any include match admits it unless an exclude matches. Only existing Git candidates are considered. No language enum, separate source-type/root list, native-config path, discovery strategy or needs_selection_intent flag is required.

A selection check that accepts every candidate can declare include=["**"], exclude=[] under a common pattern contract where ** means all candidate paths. Do not infer this policy from missing configuration. Selection check capabilities must have explicit automatic-selection behavior; content-only capabilities do not need it.

The exact field/schema syntax, path matching and validation belong to Design. These semantics must be stated there: workspace-relative anchoring, separators, case, wildcard grammar, exclusion precedence, order/deduplication and treatment of invalid/absent declarations. They are PGMCP contract semantics, not native glob/regex semantics.

Package defaults versus repository-specific paths also need a concrete storage choice in Design. Existing bundled manifests are distribution snapshots, and duplicate adapter IDs are rejected. Repository roots such as mcp_server are workspace facts. Keep one authoritative policy value source; do not invent implicit package/workspace/native merges or maintain duplicate include/exclude lists. The selected ownership strategy remains public capability metadata with one generic reader/evaluator; exact storage/reference mechanics are a design question.

### Scope and role behavior

| Route | Required behavior |
| --- | --- |
| run_checks / branch | Apply each selected selection capability's configured_targets to safe Git candidates, then invoke the ordinary adapter/native operation on the resulting subset. |
| run_checks / targets | No configured_targets filter. Preserve deliberate files/directories and explicit descendants. |
| run_checks / configured | No configured_targets filter. Retain native configured invocation. |
| run_checks / workspace | No configured_targets filter. Retain workspace-root input meaning. |
| Content checks | No branch filtering. Existing content admission/preparation remains. Lychee's content route is distinct from its selection route. |
| run_tests | No branch filter or new scope. [TestScope](../../../mcp_server/execution/models.py) permits configured, workspace and targets. [Pytest manifest](../../../mcp_server/bundled_adapters/pytest/manifest.yaml) declares test/tests, not a selection check. |
| apply_fixes | Preserve its explicit-target route; no invented branch operation. |

The discriminator is role, capability input route and requested scope, not adapter identity or whether a wire request happens to contain targets. No Pytest-specific exception is required.

### Native invocation and empty work

For the same effective operation, targets and args, a branch check must use the same adapter/native invocation as an explicit-target check. Do not add branch-only force-exclude, replace configuration, enumerate native sources or switch analysis routes. Existing transport restrictions and native errors remain meaningful.

An offered file is an explicit native input. Its normal native rules apply: preselection does not restore recursive-discovery exclusions. Any automatic boundary we guarantee must be authored in configured_targets. No automatic synchronization with native include/exclude is promised.

A selected check whose branch subset is empty must have a factual no-applicable outcome with no native invocation, coverage, capture or invented native PASS. Keep that distinct from global empty Git selection, incomplete execution and configured scope's intentionally empty request. Design must specify the public row/aggregate semantics.

Changes to native configuration may affect unchanged code. A branch subset is not broad configured verification; the run required by the later phase/plan remains responsible for that evidence.

### Native configuration investigation retained as evidence

Four packages/five operations were investigated at their installed pins. This evidence informs preservation and explains the rejected exact-resolver route; production branch filtering will not interpret these native settings.

| Tool / installed pin | Workspace configuration | Resolution / initial-source facts |
| --- | --- | --- |
| Ruff lint/format / 0.15.6 | [pyproject.toml](../../../pyproject.toml), tool.ruff. Explicit py311, line-length=100, authored lint rules and test per-file ignores. | Closest per-source .ruff.toml/ruff.toml/applicable pyproject; no implicit parent merge, optional extends. Operation-specific lint/format admission differs. |
| Mypy / 1.19.1 | Same TOML, files=["mcp_server"], Python 3.11, strict and tests.* override. | One discovered config plus native CLI precedence/module overrides. Explicit sources replace configured start sources while retaining analysis settings. |
| Pyright / 1.1.408 | [pyrightconfig.json](../../../pyrightconfig.json), include=["mcp_server"], Python 3.11/Windows, strict with diagnostic overrides. | One project configuration; optional extends, replacement arrays and declaring-directory path bases. Execution environments affect analysis rather than initial roots. |
| Lychee / 0.24.2 | No root native config/section or .lycheeignore. Binding --offline --cache=false --include-fragments. | First recognized cwd config, field-specific merges. Current binding supplies no native initial input roots. |

#### Ruff defaults, precedence and admission

At 0.15.6 stable include is *.py, *.pyi, *.ipynb, **/pyproject.toml; global preview adds *.pyw and *.md, with extension mappings also affecting default inclusion. Defaults are force-exclude=false, respect-gitignore=true, empty extend-include/extend-exclude and empty lint.exclude/format.exclude. Lint defaults are F/E4/E7/E9; target-version fallback is py310 when no configured/inferred project value applies. Formatter defaults are line-length=88, indent-width=4, double quotes/spaces, auto line ending, magic trailing comma respected, docstring-code-format=false and dynamic docstring code line length.

The exact pinned default exclude set is .bzr, .direnv, .eggs, .git, .git-rewrite, .hg, .ipynb_checkpoints, .mypy_cache, .nox, .pants.d, .pyenv, .pytest_cache, .pytype, .ruff_cache, .svn, .tox, .venv, .vscode, __pypackages__, _build, buck-out, dist, node_modules, site-packages, venv. build and __pycache__ are absent from this pin's built-in set.

A metadata-only ruff check --show-settings mcp_server/bundled_adapters/ruff/check.py exited 0 and resolved the root TOML: stable include/default exclude, force-exclude=false, respect-gitignore=true, py311, line-length=100 and the four authored extend-exclude entries. It reported resolver/formatter settings for that resolved source; it was not analysis or proof of every file's settings.

Native discovery considers common and operation exclusions and Git-ignore sources. Direct files bypass include and normally bypass exclusion; force-exclude alters exclusion handling. At this pin it does not reproduce complete include/Git-ignore discovery for direct files. check --show-files omits lint.exclude and filters source kinds; it is not exact lint/format admission. Format has no public enumeration-only CLI, and the Python package is a binary launcher rather than a resolver library.

Explicit --config fixes configuration globally and changes path bases; --isolated ignores files; CLI settings override native file settings. If no project config exists, user config fallback is possible. RUFF_OUTPUT_FORMAT, RUFF_OUTPUT_FILE and cache-related environment values have separate effects; no generic RUFF_CONFIG override was found. Workspace configuration must remain authoritative; this issue does not select a global overriding config.

Primary pin sources: [resolver](https://github.com/astral-sh/ruff/blob/0.15.6/crates/ruff_workspace/src/resolver.rs), [defaults](https://github.com/astral-sh/ruff/blob/0.15.6/crates/ruff_workspace/src/settings.rs), [format](https://github.com/astral-sh/ruff/blob/0.15.6/crates/ruff/src/commands/format.rs), [show-files](https://github.com/astral-sh/ruff/blob/0.15.6/crates/ruff/src/commands/show_files.rs), [configuration](https://github.com/astral-sh/ruff/blob/0.15.6/docs/configuration.md). Current online defaults are not substituted for these pinned facts.

#### Mypy configuration and admission

Native discovery searches upward from cwd in order mypy.ini, .mypy.ini, pyproject.toml, setup.cfg, stopping at repository/root boundaries; shared files lacking the section are skipped. A project config prevents user/XDG fallback. Configs are not layered. Relative configured source paths are ordinarily cwd-relative; MYPY_CONFIG_FILE_DIR can anchor authored paths. Native parsing expands file globs, env/home references, strict and module overrides. MYPYPATH affects imports, MYPY_CACHE_DIR affects caches and omitted Python/platform settings can depend on the host.

Bare defaults observed on Python 3.13.7/Windows: files/modules/packages=None, exclude=[], exclude_gitignore=false, namespace_packages=true, explicit_package_bases=false, Python 3.13/win32, follow_imports=normal, mypy_path=[], plugins=[], cache_dir=.mypy_cache; disallow_untyped_defs/warn_return_any/warn_unused_configs=false. Effective workspace values select files=["mcp_server"], Python 3.11 and authored strict settings.

A metadata-only process_options([], stdout=StringIO(), stderr=StringIO()) returned pyproject.toml and 188 initial BuildSource entries under mcp_server, without analysis or diagnostic output. It includes mcp_server/#Archief/supervisor_old.py; no further archive exclusion was authorized. clone_for_module("tests.example") retained disallow_untyped_defs=false.

Recursive discovery selects .py/.pyi, prefers same-stem stubs and skips dot names, __pycache__, site-packages, node_modules and configured regex/optional Git-ignore exclusions. Direct files bypass recursive exclusion and can use other suffixes. Import following is later analysis, not initial admission.

The adapter already uses native parsing for its guard, rejects diagnostics and restores MYPY_CONFIG_FILE_DIR. process_options is a practical internal pin-coupled seam, not a public enumeration API; the selected solution does not need it for branch preselection.

Primary sources: [parser](https://github.com/python/mypy/blob/v1.19.1/mypy/config_parser.py), [main](https://github.com/python/mypy/blob/v1.19.1/mypy/main.py), [source discovery](https://github.com/python/mypy/blob/v1.19.1/mypy/find_sources.py), [Options](https://github.com/python/mypy/blob/v1.19.1/mypy/options.py).

#### Pyright configuration and admission

CLI --project selects a file/directory; otherwise native JSON discovery precedes TOML. JSON comments are supported. extends applies bases before derived config, anchors paths at their declaring directories and reports cycles. Native arrays replace inherited arrays; no closest-child per-source hierarchy is used.

An empty effective include becomes ".". An empty effective exclude adds **/node_modules, **/__pycache__, **/.* and enables automatic venv exclusion if unspecified. Our nonempty exclude list (**/__pycache__, **/.pytest_cache, **/node_modules, results, source_data) does not receive those defaults. ignore=[] suppresses diagnostics rather than admission. Native typeCheckingMode default is standard, library-code use defaults true; Python/platform can be inferred, with pinned stable Python fallback 3.14. Workspace explicitly supplies 3.11/Windows and stubPath=""; an authored empty path must not be replaced by an omitted-value default.

Directory discovery uses native file-spec matching for Python/stub sources. Explicit files can bypass recursive suffix discovery, but native excludes remain. CLI sources replace include, not exclude; imports can inspect further files. Existing adapter source-channel/path restrictions remain.

The installed package ships bundled CLI files without an established public enumeration-only export/CLI. --dependencies follows analysis. No Pyright analysis was run for this research.

Primary sources: [service](https://github.com/microsoft/pyright/blob/1.1.408/packages/pyright-internal/src/analyzer/service.ts), [config options](https://github.com/microsoft/pyright/blob/1.1.408/packages/pyright-internal/src/common/configOptions.ts), [SourceEnumerator](https://github.com/microsoft/pyright/blob/1.1.408/packages/pyright-internal/src/analyzer/sourceEnumerator.ts), [Python defaults](https://github.com/microsoft/pyright/blob/1.1.408/packages/pyright-internal/src/common/pythonVersion.ts).

#### Lychee configuration and admission

Pinned default loader order in cwd is lychee.toml, Cargo.toml metadata, pyproject.toml tool.lychee, package.json lychee object. First recognized config wins. Repeated explicit --config files use later precedence before CLI values. Optional fields such as extensions/hidden/files_from replace by precedence; list fields such as include/exclude/exclude_path/remap combine. .lycheeignore adds URL exclusions, not filesystem source roots.

Default directory extensions: md, mkd, mdx, mdown, mdwn, mkdn, mkdown, markdown, html, htm, css, txt, xml. hidden=false/no_ignore=false skip hidden files and honor native ignore sources, including parent/global Git ignores. glob_ignore_case=false, skip_missing=false, default_extension/files_from=None, exclude_path=[], offline/cache=false. Binding enables offline/fragments and explicitly disables cache. exclude_path is a source-path regex; include/exclude are URL filters.

Direct files/globs bypass directory extension filtering but retain exclude_path. Public --dump-inputs can enumerate supplied roots before links are extracted. A metadata-only call with --offline --cache=false --include-fragments docs/development/issue482 exited 0 and returned docs/development/issue482\research.md. No links were checked. The chosen branch filter needs no enumeration invocation.

Current adapter projection omits the native fourth package.json loader and does not project explicit JSON config. No root package.json exists here: this is a separate guard-boundary observation, not a reproduced current failure or prerequisite repair. Native configured Lychee needs valid input roots; configured_targets does not redefine that existing requirement.

Primary sources: [loaders](https://github.com/lycheeverse/lychee/blob/lychee-v0.24.2/lychee-bin/src/config/loaders/mod.rs), [config merge/defaults](https://github.com/lycheeverse/lychee/blob/lychee-v0.24.2/lychee-bin/src/config/mod.rs), [InputResolver](https://github.com/lycheeverse/lychee/blob/lychee-v0.24.2/lychee-lib/src/types/input/resolver.rs), [dump-inputs](https://github.com/lycheeverse/lychee/blob/lychee-v0.24.2/lychee-bin/src/commands/dump_inputs.rs).

### Alternatives and disposition

| Investigated alternative | Cost / risk | Disposition |
| --- | --- | --- |
| Exact intersection with native configured discovery | Tool-specific config/default/hierarchy/ignore interpretation; no proven light exact seam for Ruff format/Pyright. | Superseded by independent declared configured_targets. |
| Native helpers / internal APIs / enumeration | Mypy internal parser and Lychee public enumeration feasible, but add coupling/cost and do not solve every tool uniformly. | Not needed by selected strategy. |
| Branch-only force-exclude | Ruff exclusion cooperation without solving exact admission. Changes native invocation by intent. | Not selected; owner requires ordinary invocation. |
| Full configured analysis whenever branch changes | Broader work than applicable changed candidates. | Not the selected branch behavior. |
| Generic interpretation of native tool settings | Tool knowledge and dialects leak into PGMCP. | Excluded. |
| Adapter-side filtering with new request intent | Preserves private policy ownership but changes request/receivers unnecessarily for standardized metadata. | Not the selected public-metadata route. |
| Common declared capability policy, generic matcher | One metadata/selection contract; risks are pattern ambiguity and missing/empty policy handling. | Selected direction. |

## Approved Strategy

The owner closed the research discussion after endorsing the public capability-metadata route and confirming the role/scope distinction. This records strategy approval, not QA approval or permission to start a later phase.

| Affected boundary | Approved strategy / preservation |
| --- | --- |
| Applicability ownership | Package capability metadata declares configured_targets; generic code applies the same common include/exclude contract. No native tool-specific decisions in PGMCP. |
| Branch behavior | Preselect each check's Git candidates only for branch. This intentionally replaces exact native configured-discovery equivalence. |
| Native tool boundary | Preserve command construction, native configuration precedence, guards and source transport after preselection. No intent-specific flags or resolver invocation. |
| Other scopes/roles | Preserve configured/workspace/explicit-target, content, test and fix meanings. No new Pytest branch scope. |
| Metadata consumers | Extend the public selection-check capability declaration and migrate affected bundled declarations coherently. Explicit policy, no implicit allow-all or parallel legacy filter. Exact schema/version/admission mechanics belong to Design. |
| Adapter request consumers | Preserve the current request/response wire where no-applicable work is determined before invocation. No universal intent field or receiving-entrypoint rewrite is required by filtering itself. |
| Deliberate file/directory inputs | Preserve explicit descendants beside directories; do not replace directories with generic scans. |
| Public result | No applicable work is distinct from native PASS, incomplete execution and configured discovery. Define the row/aggregate contract in Design; do not fabricate native facts. |
| Native Ruff scope correction | Keep the owner-authorized cache/archive exclusions and reuse passing configured evidence. No global force-exclude. |
| Verification scope | No tests added/run in Research and no new permanent harness approved. Later evidence must prove the approved behavior proportionally. |

## Expected Results

- A mixed branch offers only each check's declared matching candidates.
- Adding an adapter/capability policy does not require native tool-specific code in PGMCP.
- Branch and explicit-target calls with identical effective targets/args use the same native invocation.
- Other scopes and test/fix/content roles retain their behavior.
- Explicit directory-plus-descendant intent survives.
- An empty per-check branch subset neither launches discovery nor claims native success.
- Native settings still govern the offered sources with their ordinary meanings.

## Design Inputs

Research leaves implementation contracts to Design, within the approved boundaries:

- Exact declaration schema/version and authoritative placement/reference for package defaults versus workspace path values; no duplicated policy source or implicit merge system.
- Common matching/normalization, validation, order and duplicate semantics.
- Per-check empty planning state and public row/aggregate meaning.
- Concrete declarations for Ruff lint/format, Mypy, Pyright and Lychee selection, and coupled existing consumers/evidence.

These are how-questions, not unresolved preserve/bridge/clean-break alternatives or permission to revive exact native discovery.

## Blast Radius and Existing Evidence

Production surface: manifest/capability schemas and admission, check selector, per-check execution/public result and explicit target preservation. Native entrypoints and wire construction are preservation surfaces. [Execution adapters reference](../../reference/execution-adapters.md) and [quality tools](../../reference/tools/quality.md) are later active documentation surfaces.

Existing [selection tests](../../../tests/mcp_server/unit/execution/test_check_selection.py) pin mixed Git targets, configured/global-empty behavior and directory covering. Existing [adapter integration cases](../../../tests/mcp_server/integration/adapters) protect native configured versus explicit behavior; [process fixture](../../../tests/mcp_server/fixtures/adapter_process.py) and [role doubles](../../../tests/mcp_server/fixtures/test_role_double.py) expose contract coupling. They were inspected, not rerun. Required behavioral evidence concerns per-capability branch subsets, untouched other scopes/native calls, explicit descendants and empty-result truthfulness. No regression harness or test rewrite is prescribed here.

## Evidence

| Claim / operation | Observed evidence |
| --- | --- |
| Historical mixed-source defect | Issue473 V-F8 reproduced mixed native inputs; its six-case audit passed with 207 deselected / two warnings, receipt 902905bb03fd44d387d59792b2ec9b30. Historical, not fresh #482 tests. |
| Historical Ruff baseline | Issue481 found 130 T201 diagnostics in archived examples and format exit 3/OS error 5 with 473 formatted files. T201 follows authored T20 rules; it is not proof an intentional console demo is defective. |
| Bounded access diagnostics | Earlier configured format failed with/without cache (3fef9c7469004c7ca7bc5a7765ca48a8, af2fd5bf15f7436ea3548c2d7cf70026). Explicit .pytest_cache_ci format failed, lint passed with warning (0b7a7b8ffdbb4e24a8feb468c220c8ef, fe6946d86324419f946fcdde5055a31e). The warning did not identify a complete causal path. |
| Owner-authorized native correction | Root Ruff extend-exclude now lists tests/mcp_server/validation_fixtures, docs/development/archive, .pytest_cache*, __pycache__. No force-exclude, include/rule change or archive repair. |
| Configured Ruff after correction | run_checks(scope="configured", checks=["python_format","python_lint"], timeout_seconds=600), no caller args: both passed; format: 467 already formatted, lint All checks passed. Receipt 8b1e415f27f44e43b33ee6079b835a87. This resolves the retained Ruff portion; no further access investigation is required for the selected correction. |
| Native metadata feasibility | Ruff show-settings, Mypy process_options and Lychee dump-inputs observations are described above. They did not perform type/link analysis or establish an implemented candidate resolver. |
| Research editing | safe_edit_file validation enforced. Only research.md is consolidated here; the earlier authorized pyproject change and branch initialization files are also part of the research commit. |
| Research links before consolidation | Latest prior directed markdown_links passed, receipt 52cce7aee669444cafef1921cff522b7. The final consolidated revision is checked separately before QA. |

## Assumptions

- Human strategy approval does not substitute for independent Research → Design GO/NOGO.
- No production/test implementation or phase progression is claimed.
- The informal impacted-test question is outside #482 and does not introduce run_tests branch scope.


## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-10-05 | @imp researcher | Initial structural research, native feasibility and bounded access diagnosis. |
| 0.2 | 2026-10-05 | @imp researcher | Recover original issue473 discussion and Mypy example; withdraw broad A/B/C framing, preserve discussed intent and isolate unresolved feasibility/migration decisions. |
| 0.3 | 2026-10-05 | @imp researcher | Retain recent issue481 Ruff findings explicitly; separate native archive/cache scope policy from the still-unproved access cause and branch candidate behavior. |
| 0.4 | 2026-10-05 | @imp researcher | Record Ruff purpose and actual native settings; carry owner cache/archive scope guidance and correct diagnosis-before-scope framing. |
| 0.5 | 2026-10-05 | @imp researcher | Apply owner-authorized native archive/cache exclusions; record passing configured Ruff format/lint, with force-exclude unset and explicit-target enforcement deferred. |
| 0.6 | 2026-10-05 | @imp researcher | Record owner-confirmed explicit-source admission versus native eligible branch candidates; configured Ruff findings are resolved and global force-exclude is not selected. |
| 0.7 | 2026-10-05 | @imp researcher | Verify pinned Ruff-format admission; correct show-files feasibility and distinguish per-invocation exclusions from the complete configured-source intersection. |
| 0.8 | 2026-10-05 | @imp researcher | Map pinned raw/resolved configuration, verify native effective settings, and capture owner workspace/package requirements without global overriding configuration. |
| 0.9 | 2026-10-06 | @imp researcher | Extend pinned configuration/default/admission analysis to Mypy, Pyright and Lychee; observe native metadata seams, record loader/root gaps and compare shared contracts with tool-specific mechanisms. |
| 0.10 | 2026-10-06 | @imp researcher | Investigate independent adapter-owned automatic-selection policy, existing configuration seams, native cooperation and explicit trade-off against exact discovery equivalence; retain pending strategy decision. |
| 0.11 | 2026-10-06 | @imp researcher | Capture owner-confirmed branch-only configured_targets preselection with unchanged native invocation; establish existing-wire feasibility and isolate per-check empty-result work. |
| 0.12 | 2026-10-06 | @imp researcher | Distinguish server-side technical feasibility from policy ownership; verify examined native-knowledge isolation and retain adapter-side preselection as a boundary-preserving alternative with unchanged native calls. |
| 0.13 | 2026-10-06 | @imp researcher | Trace existing interpreted capability metadata and establish include/exclude path-pattern data as the minimal common branch-filter candidate, with package/workspace placement and matching semantics explicit. |
| 0.14 | 2026-10-06 | @imp researcher | Consolidate Research into one current strategy and bounded evidence; confirm generic capability filtering, unchanged native calls and Pytest exclusion for independent QA. |
