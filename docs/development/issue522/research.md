<!-- pgmcp:v1 id=research pv=1.0.0 pf=MBj0BrCWRmEii6mk sf=WI5iXHBKVOU91bYE -->

# Issue \#522 — Explicit workspace ownership of Git

**Status:** REVIEW REQUESTED  
**Version:** 1.0  
**Last Updated:** 2026-10-19

## Scope In

Composition, GitManager/GitAdapter input boundaries, repository selection and directly affected shared tests; current setup/config/Git documentation. Investigate inherited native selection overrides that could redirect or split repository identity.

## Scope Out

#518, #523 and #524; output presentation redesign, MCP roots negotiation, a multi-repository router, arbitrary repository discovery, new config precedence, release/build changes, active host activation and suite-wide cleanup.

## Problem Statement

ServerBootstrapper builds GitManager without an adapter. GitManager creates GitAdapter(), whose independent Path.cwd() fallback can disagree with the explicit workspace used by checks, files and workflow state. A neutral launch can fail Git; a launch in another repository can address that repository. No unintended write is claimed to have been observed.

## Goals

- Bind every Git-facing consumer to the connection's selected workspace, independent of package location, server/config roots and later working-directory changes.
- Define an exact, fail-closed repository selection boundary for ordinary, nested and linked worktrees, without automatic multi-repository discovery.
- Keep effective workspace Git/workflow policy on the existing ConfigLoader route; preserve ordinary native user/system Git configuration.
- Prove public read and mutation isolation with meaningful negative controls and an externally installed server; keep tests proportional.

## Background

The published issue and #517 residual identify a pre-existing composition defect, not a Python/MCP migration regression. #520 startup-lock behavior is preserved. Co initialized bug/522-bind-git-to-target-workspace from main at merge77d790191374a536b3977b0041b4eb3ccda240f0; no child code/test changes preceded Research.

## Findings

### Causal evidence and conditions

1. bootstrap.py resolves settings.server.workspace_root and supplies it to FileScopePaths and the check-selection GitAdapter (around592), but _build_manager_graph creates GitManager without its adapter (around734).
2. GitManager.__init__ substitutes GitAdapter() for a missing/falsy adapter. GitAdapter.__init__ then substitutes Settings or Path.cwd() for a missing/falsy path. These are independent sources of repository identity.
3. WorkflowStatusResolver, ProjectManager/cycle history, SubmitPRTool and every ordinary Git tool use that manager. The read-only ScopeResolver uses the independently workspace-bound adapter. With launch CWD=B and selected workspace=A, those paths can therefore disagree. With neutral non-repository CWD the ordinary path fails; with CWD=A the defect is masked. Installation location itself is not the root source: it often coincides with the launch directory.
4. Direct sources establish this cause without mutating repository B. Historical #517 records the actual neutral-CWD limitation; it did not repair it. No new reproduction test or source patch is introduced in Research.

### Supported roots and configuration

ServerSettings already defines a connection-wide workspace and independent server/config/template roots. An explicit PGMCP_WORKSPACE_ROOT overrides its launcher overlay. The existing documented launcher default resolves the connection workspace from launch CWD; this issue does not silently change that general Settings contract. Git must consume that resolved selection once, never choose CWD independently. For external/neutral launch, supply an absolute explicit workspace. Relative workspace inputs already fail normal FileScopePaths admission; they are not a supported neutral-launch shortcut.

The target need not contain the Python package. Server data and effective config/template roots can be explicitly external. Git/workflow conventions come from the connection's ConfigLoader, not native Git discovery or the installed package's own checkout. External config remains an explicit owner-selected policy source for that workspace; introducing an automatic second target-config lookup would contradict the existing root contract. A package/root move with the same explicit target and effective policy must not change Git selection.

### Repository forms and competing approaches

| Approach | Capability and impact |
| --- | --- |
| Exact workspace root, one repository per connection | Existing root contract suffices; select outer or inner repository by selecting its exact worktree root. A container with several child repositories selects none. No traversal/choice/routing state. Small causal boundary. |
| Separate repository field within a larger workspace | Creates two root identities, path translation and policy/state ownership questions across check selection and mutations. No demonstrated requirement in this issue. |
| Discover repositories or negotiate dynamic MCP roots | Requires selection/lifecycle policy, config/state rebinding and cache/request ownership. Larger architecture; no evidence that this is necessary for the reported defect. |

Design should resolve the smallest viable correction within the exact-workspace strategy, rather than turn discovery into an implicit fallback. An ordinary worktree and a linked-worktree/submodule .git file are candidates for exact-root selection. A subdirectory without its own repository, an absent path, a container of child repositories, a .git administrative path or bare repository must not silently become an alternate workspace. A nested repository existing below an explicitly selected outer root does not itself make that selection ambiguous. No new repository scanning is needed to establish these distinctions.

[GitPython's public Repo contract](https://gitpython.readthedocs.io/en/stable/reference.html#git.repo.base.Repo) defaults parent search to false and accepts worktree/git-directory paths. Its installed3.2.1 source was inspected to distinguish native support from PGMCP's narrower workspace contract. No general dependency/version matrix is proposed.

### Native environment versus ordinary Git configuration

An explicit Repo path alone does not prove every subprocess uses the same context. Installed GitPython reads GIT_COMMON_DIR/GIT_OBJECT_DIRECTORY during construction and inherits os.environ for commands. The [native Git contract](https://git-scm.com/docs/git#_environment_variables) also defines GIT_WORK_TREE and GIT_INDEX_FILE as worktree/index selectors. These are separate from ordinary identity, credentials and user/system configuration.

The corrected boundary must reject unresolved inherited repository/index/object/namespace redirection before Git IO can split read/mutation identities. It must not mutate process-global environment or disable ordinary user/system Git configuration. Exact native controls, meaningful rejection diagnostics and the bounded list of repository-local influences belong in Design; do not broaden this to generic environment sanitization or arbitrary Git configuration policing.

### Proportional test impact

Production has three direct construction expressions: the workspace-bound read adapter, the manager composition, and the manager's fallback. Tests have direct adapters mostly in the existing adapter/check/history families and two direct manager construction sites (shared test_support and workflow_cycle_e2e). Fourteen modules use make_git_manager, including the helper itself; make_project_manager/make_phase_state_engine also rely on it.

The helper currently forwards adapter=None, so removing the fallback needs an explicit test composition decision there. Existing real adapters/fakes should be retained; tests that only exercise conventions should not gain real repository IO. Existing adapter mocks use many /fake/path values; stronger path admission must adapt their preparation mechanically, preferably through a shared helper, without rewriting their behavior assertions. Constructor coupling is not a reason to rewrite every caller or loosen public-boundary tests.

Existing startup/installed-distribution cases prove package and admission mechanics, but do not currently prove Git identity from a neutral/foreign CWD. Extend those valuable public cases and adapter behavior families. Required distinct proofs are selected-A reads/mutations with B unchanged; missing/container/subdirectory/bare refusal; explicit nested and linked worktree selection; native selector conflict; ordinary Git configuration preservation. Reuse setup and combine equivalent scenarios; no source/prose snapshots, version tests, obsolete fallback coverage or metric padding.

## Questions

## Approved Strategy

The human authorized autonomous scoped execution on2026-10-19 and explicitly chose: "Ik wil een clean break en een schone test suite, geen overbodige testen, maar wel een adequate dekking. Geen legacy gedrag of compat." This existing approval applies per affected boundary; it is not a new producer approval.

| Boundary | Binding strategy and consumer impact |
| --- | --- |
| Connection workspace / repository identity | One resolved connection workspace is authoritative. No Git-specific missing-path/CWD/settings fallback, ancestor/child search, arbitrary repository selection or automatic return to the installation repository. Use the existing launcher/root contract; introduce no second configuration precedence or MCP-root mechanism. |
| GitManager and GitAdapter construction | Clean break for implicit dependency/path construction. Direct callers must supply the selected dependency/path. No aliases, optional legacy constructors or fallback bridge. Keep domain Git operations and narrow read interfaces intact. |
| Native repository redirection | Fail closed on unresolved repository-local overrides that can split or redirect the selected context; preserve ordinary user/system Git policy, credentials and identity. No global environment mutation. |
| Absence and unsupported repository context | Accurate existing error/unavailable boundary, original cause where available, and no Git mutation against another repository. Do not require all non-Git capabilities to acquire a Git repository during bootstrap or add tool unlisting. Existing enforcement policy still applies. |
| Config/state/quality consumers | Keep their existing explicit root ownership and public contracts; make Git agree with them. Do not move config into the adapter, hardcode workflow phases, or relocate branch state. |
| Tests and deployment | Adapt valuable behavior cases and shared preparation; adequate durable negative/isolation proof, no legacy/compat/version matrix. External launch setups provide the explicit absolute target and deliberate config roots. No new release or active host switch. |

These are scope/preservation/breakage decisions under the owner's authorization. Concrete signatures, validation timing, native control list and test structure remain Design work. Independent QA governs every forward phase transition; technical findings are repaired and re-reviewed. Standing owner approval2026-10-18 covers audited forced returns only.

## Expected Results

Public Git status/context and branch-scoped check selection agree on the selected target. Controlled mutations affect only that repository, while a different launch repository remains unchanged. Installed imports from outside the target, neutral/foreign CWD, external config/server roots, linked/nested worktrees and meaningful refusal cases are covered through public behavior. Genuine missing/ambiguous native contexts retain diagnostics and authorize no alternate mutation. Workspace conventions and ordinary Git user/system policy retain their existing owners.

## Evidence

### CWD mismatch is directly explained by the composition chain

Manager construction omits adapter; the manager and adapter each supply an implicit fallback. The separate check reader is already rooted in the target. Historical neutral-CWD failure is independently recorded in #517; no new unintended-write reproduction was performed.

- [Server composition](<../../../mcp_server/bootstrap.py>)
- [GitManager](<../../../mcp_server/managers/git_manager.py>)
- [GitAdapter](<../../../mcp_server/adapters/git_adapter.py>)
- [#517 residual findings](<../issue517/validation.md#residual-findings-for-coordination>)

### Ordinary launch/config contract and test seams exist

Settings separates workspace/server/config/template roots; ConfigLoader owns conventions. Public startup and installed distribution families provide reusable isolated setups. Shared test_support currently forwards missing adapters and must migrate together with construction.

- [Settings](<../../../mcp_server/config/settings.py>)
- [Test support](<../../../tests/mcp_server/test_support.py>)
- [Installed startup](<../../../tests/mcp_server/integration/test_target_startup.py>)
- [Developer isolation limitation](<../../setup/dev-isolation.md>)

## Consumers

### bootstrap and check selection

Compose ordinary and read-only Git dependencies.

**Impact:** Remove inconsistent identity; retain one selected root and unchanged branch target policy.

### GitManager / GitAdapter

Conventions and native repository IO.

**Impact:** Explicit construction; precise root/context admission without fallback.

### Git tools / SubmitPRTool

Queries and branch/stage/commit/push/merge/PR operations.

**Impact:** Behavior changes through the injected manager; no per-tool repository selection or duplicated validation.

### ProjectManager / WorkflowStatusResolver / cycle evidence

Branch/state agreement and historical execution evidence.

**Impact:** Read the same selected repository through existing interfaces; no state-format or codec changes.

### test\_support and adapter/startup/installed tests

DI preparation and durable public-boundary proofs.

**Impact:** Centralize explicit test setup and adapt affected cases; no broad synthetic coverage expansion.

### Current setup, configuration and Git references

Explain external launch, exact-root selection and unavailable contexts.

**Impact:** Remove the now-to-be-corrected dev-isolation limitation; document root/native selection contract. Historical issue artifacts remain context.

## Risks

### Correcting only the manager omission leaves a reusable implicit fallback or native redirection.

Design covers constructor boundaries and the native context, with public isolation/error proofs.

### Repository absence could be turned into an unnecessary whole-server startup dependency.

Retain lazy/use-time Git admission and existing operation/error/enforcement boundaries; non-Git startup does not require repository acquisition.

### Test setup coupling could inflate the change.

Adapt shared factories and existing behavior families. Preserve valuable guards; replace only obsolete implicit-construction assumptions.

## Related Documents

- [Published issue](<https://github.com/MikeyVK/phase-gate-mcp/issues/522>)
- [Architecture contract](<../../coding_standards/ARCHITECTURE_PRINCIPLES.md>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-19 | @imp researcher | Establish causal root-selection evidence, supported boundaries and clean-break strategy. |
