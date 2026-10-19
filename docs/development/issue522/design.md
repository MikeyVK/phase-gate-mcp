<!-- pgmcp:v1 id=design pv=1.0.0 pf=Uk1D2XWpiag1c6nn sf=WI5iXHBKVOU91bYE -->

# Issue \#522 — One selected Git worktree per connection

**Status:** REVIEW REQUESTED  
**Version:** 1.0  
**Last Updated:** 2026-10-19

## Problem Statement

An independently created CWD-bound Git adapter disagrees with the connection's selected workspace. A path-only correction would leave implicit constructors and native worktree/index/object redirection capable of splitting the context.

## Functional Requirements

- All ordinary Git tools, workflow/cycle context and branch check selection consume the same selected canonical workspace root.
- Support an explicitly selected ordinary, nested or linked worktree root and external package/server/config roots. Never discover an ancestor or child repository.
- Refuse unavailable/unsupported/native-redirected Git context before mutation, preserving diagnostic facts. Non-Git startup remains independent of Git acquisition.
- Keep native identity/credential/user/system configuration and public tool DTOs intact; require explicit internal dependencies without compatibility bridges.

## Nonfunctional Requirements

- Minimal correction in bootstrap, GitManager and GitAdapter; no new routing/service/configuration architecture.
- Behavior tests through public boundaries; reuse existing adapter/startup/installed families and shared preparation. No legacy/version/content tests or gate weakening.
- One full configured suite and required branch/configured gates in Validation; focused tests/checks during implementation.

## Constraints

- Approved Research37fa53d and independent Research→Design GO are binding.
- Existing Settings/ConfigLoader roots, workflow/state ownership, #520 lock policy and external integration registration remain unchanged.
- No production/process-global chdir or environment mutation; no package search or hidden target fallback.

## Options

### 1. Only inject a root at the current manager call

Removes the observed bootstrap symptom but leaves optional constructors and native context drift.

**Pros:**

- Tiny diff.

**Cons:**

- Does not enforce the shared root contract or native selection boundary.

### 2. Explicit existing dependencies plus adapter-owned exact-root admission

Selected correction. Canonical root supplied to existing adapters; manager no longer constructs one. Native validation and command binding remain inside the existing adapter.

**Pros:**

- One native responsibility boundary, existing call graph and public DTOs.
- Fails closed without a router or global environmental changes.

**Cons:**

- Shared test composition and invalid native mocks need focused migration.

### 3. Discover or dynamically route repositories

Introduces repository enumeration/choice and policy/state rebinding.

**Pros:**

- Could serve a future multi-root workflow.

**Cons:**

- Unnecessary architecture for this defect; no demonstrated consumer need.

## Decision

Use mandatory existing dependency/path injection, lazy exact-worktree admission and native command binding in GitAdapter. Both bootstrap adapters receive the same canonical connection workspace; their current read/write ownership remains separate. No new public tool field or config schema.

## Production Design

### Composition and ownership

bootstrap_target resolves the existing workspace to its canonical absolute root before constructing managers or selectors. _build_manager_graph supplies GitAdapter(repo_path=that root) to GitManager; ScopeResolver receives the same selected root through its existing adapter and FileScopePaths. This is not a shared mutable singleton or new context service.

GitManager requires its adapter and assigns it directly. GitAdapter requires a nonblank absolute repo_path; remove its Settings parameter/import and CWD fallback. Canonicalize the explicitly supplied path once and expose the existing repo_path name read-only. Path syntax/canonicalization is constructor work; repository opening stays lazy. Existing read interfaces and all domain Git operations retain their signatures.

### Exact worktree admission

At public repo access, validate repository-local environment before returning even a cached native handle. On first access, open Repo with parent search and variable expansion explicitly disabled. Absence, invalid .git metadata and native IO errors preserve the original exception through the existing system boundary.

A candidate must be non-bare, have a working_tree_dir, and have that canonical directory equal to the selected workspace. This rejects .git administrative paths as workspace targets and forbids interpreting subdirectories or containers as another root. GitPython continues to resolve genuine .git files/commondir metadata for linked worktrees and submodules; do not parse these formats ourselves.

Before publishing the handle, a read-only native rev-parse --show-toplevel must also resolve to the selected root. This catches a native core.worktree redirection that GitPython's initial worktree field alone can miss. Then use GitPython's public set_persistent_git_options to bind --git-dir to the admitted git_dir and --work-tree to the selected root for subsequent native commands. This keeps native command identity aligned with GitPython's direct index/reference/object access. Ordinary Git policy remains enabled.

Publish the handle only after admission succeeds. Close an unpublished handle on failure; retain the primary exception and attach any secondary cleanup failure as a note. Do not introduce another resource/error framework. Existing cached repository ownership otherwise remains unchanged.

### Bounded inherited-context controls

Reject presence (including an empty declaration) of these native context variables at Git-use time: GIT_DIR, GIT_WORK_TREE, GIT_COMMON_DIR, GIT_INDEX_FILE, GIT_OBJECT_DIRECTORY, GIT_NAMESPACE, GIT_SHALLOW_FILE and GIT_GRAFT_FILE. They select repository/worktree/index/object/ref/history sources. Check again before cached access so a later process-environment change cannot silently redirect an operation.

This is an adapter-local native contract, not a new workspace policy list or general GIT_* ban. Do not reject ordinary GIT_AUTHOR_*/GIT_COMMITTER_* values, credential/SSH settings, HOME or GIT_CONFIG_* user/system mechanisms. Read-only GIT_ALTERNATE_OBJECT_DIRECTORIES may retain its native meaning: it does not select a different worktree/index or write to the alternate directory. Native config that attempts a different initial worktree is caught by exact-root admission; persistent explicit command options keep the selected identity afterwards.

No process-global variable is removed or rewritten. A selector conflict refuses the operation instead of silently clearing the owner's environment. Do not include environment values in diagnostics, only conflicting variable names and the selected workspace.

### Error presentation and unchanged consumers

Reuse existing ExecutionError for factual selection failures and existing native/system wrapping for repository-open failures. Factual error text identifies git_context_unavailable, selected workspace and reason (native_context_override, bare_repository, worktree_mismatch or native_worktree_mismatch), plus variable names where relevant. Preserve causes/tracebacks. This is system/developer diagnosis, not new recovery prose or a policy-specific presenter branch; public error/output models remain unchanged.

Current broad operation wrappers may retain their existing diagnostic chaining; do not redesign all Git error handling. No tool catches/reinterprets the new diagnosis or acquires another repository. Git absence remains a use-time error through current wrapper/enforcement boundaries.

## Test Design

### Existing durable surfaces

| Family | Corrected behavior and negative control |
| --- | --- |
| unit/adapters/test_git_adapter.py and existing real-local-remote scenario | Selected-A status and a real stage/commit affect A while launch repository B's HEAD/index/files remain unchanged. Later CWD changes do not rebind. Include ordinary identity/config behavior. |
| Existing adapter behavior family | Parameterize distinct unavailable inputs (missing path, no-repo container, parent subdirectory, bare/admin path); assert public refusal and no writes to B. Test outer versus explicitly selected nested root and a genuine linked worktree/.git file. |
| Existing native boundary | Inherited selector refusal, including a selector added after successful use; explicit worktree pin versus misleading core.worktree. Assert diagnosis and unchanged nonselected repository, not helper calls/source strings. |
| unit/server/test_bootstrap.py / integration/test_target_startup.py | Public bootstrap/tool status and workflow context agree with selected A from neutral and foreign CWD, with external server/config roots. A valid non-Git workspace still reaches ordinary admission and Git use reports unavailability. Avoid private _build_manager_graph tests. |
| Existing installed candidate startup case | Reuse the one wheel build; initialize/use a target separate from installed package and neutral launch directory, then query public Git status/context and exercise a controlled selected-target mutation with B unchanged. Verify installed module provenance using existing fixture facts. |

Use a reusable repository/adapter preparation helper for existing native mocks when stricter root metadata is required; do not edit semantic assertions en masse. Update test_support's missing-adapter path to supply an explicit adapter for the helper's selected workspace, using the helper's established canonical source root when no workspace was supplied. Tests intentionally avoiding real Git IO keep explicit fakes. Do not substitute a fake for real-history/integration cases.

Remove the existing test_init_default shallow non-None assertion when implicit production construction disappears; it provides no durable behavior. Preserve valuable commit/checkout/restore/history guards. A failed existing setup must receive correct preparation, not weaker admission or a blanket mock. No new permanent diagnostic module, constructor-version matrix, prose/source snapshot or metric-only case.

## Contracts

### Mandatory internal construction

```python
class GitAdapter:
    def __init__(self, repo_path: str) -> None: ...
    @property
    def repo_path(self) -> str: ...
    @property
    def repo(self) -> Repo: ...

class GitManager:
    def __init__(
        self,
        git_config: GitConfig,
        adapter: GitAdapter,
        *,
        workphases_config: WorkphasesConfig,
        scope_encoder: ScopeEncoder,
        scope_decoder: ScopeDecoder,
    ) -> None: ...
```

No method bodies are specified here. A missing constructor argument follows normal Python signature failure; invalid path syntax is ValueError. Repo absence/identity/native-context validation occurs at Git use. Existing manager/tool operations, Git context protocols and response schemas are unchanged.

### Repository eligibility

| Input | Outcome |
| --- | --- |
| Exact ordinary worktree | Admit selected root. |
| Exact outer root containing a nested repository | Admit outer; never descend. |
| Explicit nested/submodule/linked worktree root | Admit that root through native .git-file semantics. |
| Existing folder with no own repository, including a container of two child repositories or a subdirectory of a parent repo | Accurate failure; no search. |
| Bare repository or administrative .git directory | Refuse as a workspace worktree. |
| Inherited context selector | Refuse before native repository acquisition/operation, also after prior successful cached use. |
| Ordinary native Git identity/credential/config setting | Retain normal behavior; never use it as an alternate repository selector. |

## State and Failures

No workflow/state/plan format, config identity or public tool DTO changes. An admitted adapter stays bound to its captured workspace. Repository-local environment conflicts fail at Git use, not general bootstrap. A failed admission publishes no handle and authorizes no alternate operation. Native Git locks still own mutation concurrency; this issue does not promise atomic protection against arbitrary filesystem/config replacement during a call.

## Preservation

Maintain existing CLI/proxy/installation modes, #520 bounded startup admission, original native diagnostics, native Git identity/credentials/user/system policy, ordinary commit/branch conventions and parent/state enforcement. Keep explicit external config roots authoritative. No new global environment changes, package requirement inside the target or automatic repository discovery.

## Transition and Cleanup

Clean break for internal omitted adapters/paths and the Settings-bearing GitAdapter constructor. Migrate the two direct manager test sites and central helper; adapt only invalid adapter fixtures and affected public startup tests. Current developer-isolation limitation is replaced with validated exact-root guidance in Documentation. Historical issue artifacts remain unchanged. No alias/bridge/legacy test or package/host rollout.

## Validation

### One selected repository across reads/mutations/context/checks.

**Method:** Focused public adapter/bootstrap cases plus installed neutral/foreign-CWD acceptance using distinct local repositories and external roots.

**Expected Result:** A is selected regardless of launch/package root; controlled writes affect only A and B's observable state is unchanged.

### Exact-root and native context refusal.

**Method:** Meaningful negative cases and linked/nested positive cases in existing families.

**Expected Result:** No ancestor/child fallback, no redirected index/object/worktree mutation, useful original/factual diagnosis and failed-handle cleanup.

### Preservation and adequate proportional coverage.

**Method:** Existing affected behavior tests and targeted production typing/lint during implementation; complete native suite and required branch/configured gates in Validation.

**Expected Result:** All required evidence passes without new excludes/ignores/skips or threshold changes; no extra coverage gate is introduced.

## Planning Consequences

Plan the smallest coherent defect-correction cycle(s) covering explicit composition, adapter admission/native binding, shared test migration and external installed public acceptance. First demonstrate causal RED on durable selected-target behavior; do not manufacture RED for mechanical fixture cleanup. Reserve full native verification for Validation, with fresh evidence reuse and independent phase QA.

## Sources

- [Approved Research](<research.md>)
- [Composition](<../../../mcp_server/bootstrap.py>)
- [Adapter](<../../../mcp_server/adapters/git_adapter.py>)
- [Manager](<../../../mcp_server/managers/git_manager.py>)
- [Test support](<../../../tests/mcp_server/test_support.py>)
- [Native Git selection/environment](<https://git-scm.com/docs/git#_environment_variables>)
- [GitPython public APIs](<https://gitpython.readthedocs.io/en/stable/reference.html#git.cmd.Git.set_persistent_git_options>)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-19 | @imp designer | Specify explicit Git composition, lazy exact-root admission and bounded native-context control. |
