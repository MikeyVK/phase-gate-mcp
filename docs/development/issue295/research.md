<!-- docs\development\issue295\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-05T15:52Z updated= -->
# submit_pr Atomicity: Upstream Check, Dirty-Tree Guard, and Rollback on Failure

**Status:** DRAFT (v2 — revised after QA design review)  
**Version:** 1.0  
**Last Updated:** 2026-05-05

---

## Purpose

Research phase findings and expected result for issue #295. Provides the factual foundation for design and planning phases. Does not prescribe implementation details beyond what is needed to scope design choices.

## Scope

**In Scope:**
SubmitPRTool.execute() in mcp_server/tools/pr_tools.py; GitManager public API expansion; GitAdapter public API (read-only, identify gaps); existing test files test_submit_pr_atomic_flow.py and test_submit_pr_tool.py

**Out of Scope:**
initialize_project changes (belongs to issue #283/upstream); GitPushTool refactoring; enforcement.yaml changes; MergePRTool; any backward-compatibility shim — this is a clean break

## Prerequisites

Read these first:
1. Understanding of the GitManager/GitAdapter layering (§7 Law of Demeter: tools talk to managers, not adapters)
2. GitManager.pull() preflight pattern as the canonical model for pre-mutation safety checks
3. branch_local_artifacts config in contracts.yaml and MergeReadinessContext dataclass
4. commit_with_scope() behavior: calls git add . when files=None (stages all untracked+modified)
---

## Problem Statement

SubmitPRTool.execute() has three distinct atomicity failure modes that leave the branch in a degraded, non-recoverable state after a partial mutation:

**Failure A — No upstream configured:**
neutralize_to_base() + commit_with_scope() succeed, then push() raises ExecutionError('no upstream tracking branch'). The branch is now on local only, HEAD has the neutralization commit (state.json gone), and a second submit_pr call finds no artifacts to neutralize — branch is stranded.

**Failure B — Unexpected untracked files consumed silently:**
initialize_project writes state.json and deliverables.json to disk without committing them. has_net_diff_for_path checks committed git history only and returns False for untracked files — so neutralize_to_base is correctly skipped for those files. However, commit_with_scope calls `git add .` which blindly stages ALL untracked files. They land in the ready commit and propagate to main after merge. This is precisely how state.json ended up on main after PR #310.

**Failure C — GitHub API failure after successful push:**
After push() succeeds, create_pr() may fail (e.g., 422 PR already exists, 403 insufficient scope, 5xx GitHub outage). The branch is already on remote at HEAD with the neutralization commit. State.json is gone from HEAD. There is no rollback. A second submit_pr attempt finds no artifact to neutralize and tries to create a second PR, potentially duplicating.

## Research Goals

- Determine the correct preflight sequence for SubmitPRTool (what checks, in what order, before any mutation)
- Clarify responsibility boundary: submit_pr must NOT set upstream automatically — that belongs to initialize_project or the agent (SRP §1.1)
- Define dirty-tree guard semantics: what constitutes an acceptable working tree state at the entry of submit_pr
- Specify rollback mechanism for Failure C: post-push API failure must not leave the branch stranded
- Map the blast radius: which production files change and which test files need to be added or updated
- Verify compliance with ARCHITECTURE_PRINCIPLES.md §1.1 (SRP), §4 (Fail-Fast), §7 (Law of Demeter), §8 (Explicit over Implicit), §14 (Test via Public API)

---

## Background

## Existing Code Context

### GitAdapter public API (adapter layer)
- `is_clean() -> bool`: `not self.repo.is_dirty() and not self.repo.untracked_files` — returns True only if working tree has zero staged/unstaged/untracked changes
- `has_upstream() -> bool`: `self.repo.active_branch.tracking_branch() is not None`
- `neutralize_to_base(paths, base)`: `git restore --source=<merge_base_sha>` per path — silently does nothing for paths that never existed in merge-base (new untracked files)
- `has_net_diff_for_path(path, base)`: `git diff --name-only merge-base..HEAD` — checks committed history only, misses untracked
- `push(set_upstream=False)`: `origin.push()` — raises ExecutionError if no upstream tracking branch

### GitManager public API (manager layer)
- `push(set_upstream=False)` → delegates to adapter
- `pull(note_context, ...)` → preflight: is_clean + has_upstream + not detached HEAD → then pull
- `merge(branch_name, note_context)` → preflight: is_clean → then merge
- `has_net_diff_for_path(path, base)` → delegates to adapter
- `neutralize_to_base(paths, base)` → delegates to adapter
- `commit_with_scope(...)` → delegates to adapter.commit() which does git add . when files=None
- **MISSING**: `is_clean()` not exposed as public GitManager method *(v2: methoden zijn intern in `prepare_submission()` — geen publieke exposure nodig — zie Findings 6-9)*
- **MISSING**: `has_upstream()` not exposed as public GitManager method *(v2: idem)*

### SubmitPRTool.execute() current sequence (pr_tools.py ~L130)
1. get_current_branch()
2. For each branch_local_artifact: has_net_diff_for_path → collect paths_to_neutralize
3. neutralize_to_base(paths_to_neutralize) — may be skipped
4. commit_with_scope(...) ← git add . here, untracked files consumed
5. push() ← may fail if no upstream
6. create_pr(...) ← may fail after successful push
7. set_pr_status(OPEN)

### Law of Demeter constraint
The existing test `test_submit_pr_tool_execute_has_no_adapter_calls` (test_submit_pr_atomic_flow.py:218) asserts that SubmitPRTool.execute() must NOT contain `_git_manager.adapter`. Any new preflight methods (is_clean, has_upstream) must be exposed via GitManager, not accessed from SubmitPRTool directly on the adapter. *(v2: de checks zitten intern in `prepare_submission()` — de tool roept ze niet aan; LoD-constraint geldt onverminderd maar de conclusie "exposed via GitManager" is v1-redenering — zie Findings 6-9)*

### GitManager.pull() as canonical preflight pattern
```python
def pull(self, note_context, ...):
    if not self.adapter.is_clean():
        note_context.produce(BlockerNote('Commit or stash changes before pulling'))
        raise PreflightError('Working directory is not clean')
    if not self.adapter.has_upstream():
        note_context.produce(BlockerNote('Set upstream tracking ...'))
        raise PreflightError('No upstream configured for current branch')
    return self.adapter.pull(...)
```
This is the exact pattern that SubmitPRTool must adopt, implemented via new GitManager public methods.

---

## Findings

## Finding 1: Preflight sequence must match GitManager.pull() pattern

GitManager already implements the canonical preflight pattern in pull() and merge(): check invariants → produce BlockerNote → raise PreflightError → return without mutating. SubmitPRTool must adopt the same pattern. The correct preflight sequence before any mutation:

1. **is_clean check**: `git_manager.is_clean()` — if False, produce `BlockerNote` listing dirty files, raise `PreflightError`. ANY uncommitted/untracked file that is not in the list of artifacts already being neutralized is a problem. But simpler and safer: require COMPLETELY clean tree before submit_pr starts. If state.json is untracked, the agent must commit it first. This makes the contract explicit and aligns with §8 Explicit over Implicit.
2. **has_upstream check**: `git_manager.has_upstream()` — if False, produce `BlockerNote('Run git_push with --set-upstream before submit_pr')`, raise `PreflightError`. submit_pr must NOT auto-push or auto-set upstream. Responsibility belongs to initialize_project or the agent explicitly.

Both checks require new public methods on GitManager. Current adapter-level methods cannot be called from SubmitPRTool (LoD constraint). *(v2: de checks zijn intern in `prepare_submission()` — géén aparte publieke methoden nodig op GitManager — zie Findings 6-9)*

## Finding 2: Dirty-tree guard semantics

The dirty-tree check (is_clean) must run BEFORE neutralize_to_base, not after. Rationale: neutralize_to_base itself modifies files (it is a mutation). If the tree is dirty before neutralization, it means uncommitted work exists that was not authored by submit_pr. That work should be committed explicitly by the agent before invoking submit_pr.

The branch_local_artifacts exclusion for the dirty-tree check is NOT needed: the artifacts (state.json, deliverables.json) SHOULD be committed into the branch history. The neutralization removes them from the HEAD commit just before the PR. If they are untracked at submit_pr time, it means the agent ran initialize_project but forgot to commit — this must be caught and surfaced explicitly.

Conclusion: `is_clean()` must return True for the entire working tree. No exceptions, no exclusions. This is the simplest, most robust contract.

## Finding 3: Rollback mechanism for post-push API failure

After push() succeeds but create_pr() fails:
- The branch is on remote with the neutralization commit at HEAD
- state.json is in merge-base content (or absent) from the last commit  
- A retry of submit_pr will find no artifacts to neutralize (has_net_diff_for_path returns False) — broken state

Rollback strategy (single layer — Layer 2 only):

**Why Layer 1 (GitHub API pre-flight for duplicate PR check) is dropped:** The existing `check_pr_status` enforcement in `enforcement.yaml` already blocks `submit_pr` if an open PR exists on the current branch. Adding a redundant GitHub API round-trip would violate §9 YAGNI. The "does base exist?" check is also unnecessary — base is always `main` and always exists. Layer 2 rollback handles the edge case correctly.

**Layer 2 (post-push rollback):** If create_pr() raises ExecutionError after successful push:
  1. `git reset --soft HEAD~1` — undoes the neutralization commit; HEAD moves back one commit; staged index now holds the neutralization changes
  2. `git reset --hard HEAD` — discards staged index entirely and restores working tree to the new HEAD state (pre-neutralization). This is safe because `is_clean()` was True before execute() started, so no in-flight user changes exist.
  3. `git push --force-with-lease` — force-push to overwrite remote, reverting it to the pre-neutralization HEAD
  4. Produce `RecoveryNote` explaining: "PR creation failed: {reason}. Remote branch rolled back to pre-submit state. Working tree is clean. Retry submit_pr once the API issue is resolved."

The combined `soft HEAD~1` + `hard HEAD` is equivalent to `git reset --hard HEAD~1` but more explicit about the two concerns it addresses (commit history vs. working tree). The design phase may simplify to `hard HEAD~1` if preferred. *(v2: besloten — `hard_reset("HEAD~1")` is de implementatie)*

**Why NOT `git restore --staged <artifact_paths>`:** After soft-reset, the staged index contains artifact deletions/restorations. `git restore --staged` on specific paths would only unstage those paths to the HEAD state but leave the working tree in the merge-base artifact state (neutralize_to_base modified the working tree). `is_clean()` would return False post-rollback, causing Failure B on retry — the exact problem we are fixing.

The `--force-with-lease` is safe: we own the commit we just pushed (neutralization commit from this execute() call). No concurrent pushes can occur because BranchMutatingTool blocks concurrent branch mutations.

## Finding 4: API changes needed on GitManager and GitAdapter *(superseded by Findings 6-10)*

> **Note:** This finding reflects the v1 design direction. Findings 6-10 (QA design review) supersede the specific API choices below. The correct API shape is in the v2 Expected Result. Preserved for audit trail.

New public methods required on GitManager (tools must not access adapter directly per §7 LoD):
- `is_clean() -> bool` (wraps adapter.is_clean()) — *moved inside prepare_submission() in v2*
- `has_upstream() -> bool` (wraps adapter.has_upstream()) — *moved inside prepare_submission() in v2*
- `rollback_neutralization(artifact_paths: frozenset[str]) -> None` — *split into prepare_submission() + rollback_push() in v2*

New methods needed on GitAdapter:
- `soft_reset(steps: int = 1)` — `git reset --soft HEAD~N` — *dropped in v2; hard_reset(ref) covers it*
- `hard_reset_to_head()` — `git reset --hard HEAD` — *dropped in v2; merged into hard_reset(ref)*
- `force_push_with_lease()` — `git push --force-with-lease` — *retained in v2*

Note: `is_clean()` and `has_upstream()` already exist on GitAdapter. No adapter changes needed for those.

## Finding 5: Error transparency requirements

All failure paths must use the NoteContext pattern:
- Failure A (no upstream): `BlockerNote('No upstream tracking branch configured. Run git_push(set_upstream=True) before submit_pr.')` + `PreflightError`
- Failure B (dirty tree): `BlockerNote(f'Working tree is not clean. Uncommitted/untracked files prevent submit_pr. Commit all changes before submit_pr.')` + `PreflightError`
- Failure C rollback: `RecoveryNote('GitHub PR creation failed: {reason}. Remote branch has been rolled back to pre-submit state. Working tree is clean. Retry submit_pr once the API issue is resolved.')`
- Failure D rollback: `RecoveryNote('Push failed: {reason}. Local neutralization commit rolled back. Working tree is clean. Retry submit_pr after resolving the remote issue.')`
- Rollback-of-rollback failure: `RecoveryNote('CRITICAL: Rollback failed: {reason}. Branch may be in degraded state. Manual recovery: git reset --hard HEAD~1 && git push --force-with-lease. Do not commit until resolved.')`

Preflights (no mutation) → `BlockerNote + PreflightError`. Post-mutation recovery → `RecoveryNote + ToolResult.error()`.

---

## Finding 6: Bestaande SRP-schending in SubmitPRTool.execute() (QA design review)

`SubmitPRTool.execute()` heeft drie onafhankelijke verantwoordelijkheden in één methode:

1. **Git-transactie-orchestratie** — artifact-selectie (`has_net_diff_for_path`), neutralisatie (`neutralize_to_base`), commit (`commit_with_scope`), push (`push()`)
2. **GitHub API-orkestratie** — `create_pr()`
3. **Status-boekhouding** — `set_pr_status(OPEN)`

Per §1.1 SRP verandert de methode op drie onafhankelijke assen. Dit is een God-method-patroon. De failure modes A, B, C en D zijn directe symptomen van verantwoordelijkheid 1 die niet bij de tool hoort.

## Finding 7: Law of Demeter-schending — artifact-selectie in de tool

```python
# Huidige code in SubmitPRTool.execute()
paths_to_neutralize = frozenset(
    artifact.path
    for artifact in self._merge_readiness_context.branch_local_artifacts
    if self._git_manager.has_net_diff_for_path(artifact.path, base)
)
```

De tool bereikt door `_merge_readiness_context` heen om `branch_local_artifacts` te itereren, en gebruikt die resultaten om `_git_manager` aan te sturen. De tool functioneert als bemiddelaar tussen twee objecten. Per §7 LoD: de beslissing *welke artifacts geneutraliseerd moeten worden* is git-domeinkennis die in `GitManager` thuishoort — die bezit al `has_net_diff_for_path` én `neutralize_to_base`.

## Finding 8: Implicit ordering dependency — §8 Explicit over Implicit

De verplichting dat `commit_with_scope` pas na `neutralize_to_base` mag worden aangeroepen is een impliciet caller-contract. Het is niet afdwingbaar via de type-handtekening en niet zichtbaar voor andere callers. Dit is de directe oorzaak van failure B: `git add .` in `commit_with_scope` consumeert untracked files omdat de caller (de tool) verantwoordelijk is voor een volgorde die de manager niet afdwingt.

## Finding 9: SubmitPRTool doorbreekt het canonieke GitManager-patroon

Alle bestaande GitManager-methoden die een multi-step git-transactie uitvoeren, encapsuleren hun preflights intern:

| Methode | Preflight | Gedrag |
|---------|-----------|--------|
| `GitManager.pull()` | is_clean → has_upstream | volledig intern afgehandeld |
| `GitManager.merge()` | is_clean | volledig intern afgehandeld |
| `GitManager.create_branch()` | is_clean | volledig intern afgehandeld |
| **`SubmitPRTool.execute()` (huidig)** | **geen** | **git-stappen in de tool** |

`SubmitPRTool` is de enige caller die de git-transactie zelf orkestreert. De failures A t/m D zijn het gevolg van dit gebroken patroon: preflights ontbreken omdat de manager ze niet afdwingt, en volgordedependencies zijn impliciet omdat de tool de stappen zelf sequenceert.

## Finding 10: Dependency-richting voor prepare_submission()

`MergeReadinessContext` leeft in `managers/phase_contract_resolver.py` (zelfde layer als `GitManager`). Een same-layer import is technisch toegestaan, maar semantisch problematisch: `GitManager` zou dan fase-contract-kennis nodig hebben, wat §10 Cohesion schendt (een methode die uitsluitend `phase_contract` domeinkennis nodig heeft hoort bij de klasse die dat modeleert).

**Aanbeveling:** `prepare_submission(artifact_paths: frozenset[str], base: str, note_context: NoteContext)` — de tool extraheert de paden uit zijn eigen config-injectie (`self._merge_readiness_context.branch_local_artifacts`) en geeft puur data mee. `GitManager` blijft git-gericht. De filterlogica (`has_net_diff_for_path` per pad) verhuist naar `prepare_submission()` intern — de tool geeft de volledige set te controleren paden mee, de manager beslist welke te neutraliseren.

## Expected Result (Design Contract — v2)

De root cause (Findings 6-9) bepaalt de designrichting. De correcte verantwoordelijkheidsverdeling:

**`GitManager.prepare_submission(artifact_paths: frozenset[str], base: str, note_context: NoteContext)`**
Bezit de volledige git-zijde van de submit-transactie. Intern:
1. `is_clean()` → if False: `BlockerNote` + `PreflightError` (geen mutatie)
2. `has_upstream()` → if False: `BlockerNote` + `PreflightError` (geen mutatie)
3. Voor elk pad in `artifact_paths`: `has_net_diff_for_path(pad, base)` → verzamel te neutraliseren paden
4. `neutralize_to_base(te_neutraliseren, base)` (indien niet leeg)
5. `commit_with_scope(...)` → if fails: `hard_reset("HEAD")` + `RecoveryNote` (working tree hersteld)
6. `push()` → if fails: `hard_reset("HEAD~1")` + `RecoveryNote` (commit ongedaan, nothing reached remote)

**`GitManager.rollback_push(note_context: NoteContext)`**
Bezit de remote rollback na een geslaagde push maar gefaalde `create_pr`:
1. `hard_reset("HEAD~1")` lokaal
2. `force_push_with_lease()` → if fails: `RecoveryNote` met manuele recovery-instructie + propageer `ExecutionError`

**`SubmitPRTool.execute()`** — vereenvoudigd tot 3 high-level aanroepen:
```
1. [GIT]    artifact_paths = frozenset(a.path for a in self._merge_readiness_context.branch_local_artifacts)
            self._git_manager.prepare_submission(artifact_paths, base, context)
              → bij preflight-failure: BlockerNote + PreflightError → tool geeft ToolResult.error()
              → bij commit/push-failure: RecoveryNote in context → tool geeft ToolResult.error()

2. [GITHUB] pr = self._github_manager.create_pr(...)
              → bij failure: self._git_manager.rollback_push(context)
                             ToolResult.error(str(exc))

3. [STATUS] self._pr_status_writer.set_pr_status(branch, PRStatus.OPEN)
            return ToolResult.text(f"PR #{pr['number']} created: {pr['url']}")
```

De tool heeft geen kennis van artifact-selectie, commit-volgorde, of git-reset-mechanismen. `SubmitPRTool` heeft één reden om te veranderen: de orchestratie van Git + GitHub + status — niet de interne git-transactie-logica.

**Vervallen t.o.v. v1 design:** publieke `is_clean()`, `has_upstream()`, `rollback_neutralization(remote: bool)` als aparte GitManager public methods — waren symptomen van het verkeerde patroon. De logica zit nu intern in `prepare_submission()` en `rollback_push()`.

## Blast Radius (herzien — v2)

### Production Code

| File | Change | Scope |
|------|--------|-------|
| `mcp_server/managers/git_manager.py` | Add `prepare_submission(artifact_paths, base, note_context)` — encapsuleert preflight + neutralize + commit + push + lokale rollback | ~50 lines |
| `mcp_server/managers/git_manager.py` | Add `rollback_push(note_context)` — hard reset HEAD~1 + force-push-with-lease | ~15 lines |
| `mcp_server/adapters/git_adapter.py` | Add `hard_reset(ref: str)` — `git reset --hard {ref}` | ~5 lines |
| `mcp_server/adapters/git_adapter.py` | Add `force_push_with_lease(remote: str = "origin")` — `git push --force-with-lease` | ~5 lines |
| `mcp_server/tools/pr_tools.py` | `SubmitPRTool.execute()` vereenvoudigt: artifact-selectie + git-stappen verdwijnen uit de tool, vervangen door 2 manager-aanroepen | ~-30 lines netto |

**Vervallen adapter-methoden t.o.v. v1:** `soft_reset(steps)`, `hard_reset_to_head()` — niet meer nodig; `hard_reset(ref)` dekt beide gevallen.
**Vervallen manager-methoden t.o.v. v1:** publieke `is_clean()`, `has_upstream()`, `rollback_neutralization(remote: bool)`.

**Totale productie-delta: ~75 lines netto across 3 files**

### Test Code

| File | Change |
|------|--------|
| `tests/mcp_server/unit/managers/test_git_manager.py` | Nieuwe tests voor `prepare_submission()` (preflight A, B, artifact-selectie, commit-fail, push-fail) en `rollback_push()` (success + force-push-fail) |
| `tests/mcp_server/unit/adapters/test_git_adapter.py` | Nieuwe tests voor `hard_reset(ref)` en `force_push_with_lease()` |
| `tests/mcp_server/integration/test_submit_pr_atomic_flow.py` | Update bestaande tests (tool heeft nu minder mocks nodig); voeg integratietests toe voor Failure A, B, C, D via tool |
| `tests/mcp_server/unit/tools/test_submit_pr_tool.py` | Update structurele tests; LoD-test blijft maar de assertion verifieert dat `prepare_submission` en `rollback_push` worden aangeroepen |

**Geen wijzigingen nodig in:** `enforcement.yaml`, `contracts.yaml`, `MergePRTool`, `GitCommitTool`, `test_ready_phase_enforcement.py`

## Open Questions (herzien — v2)

- ❓ **prepare_submission signature**: research raadt `frozenset[str]` aan (tool geeft pure paden, manager doet filterlogica). Design fase moet bevestigen dat dit §10 Cohesion correct toepast en dat de tool's verantwoordelijkheid (paden extraheren uit config) acceptabel is.
- ❓ **rollback_push meta-failure**: wat als `force_push_with_lease()` zelf faalt (rejected, network)? Design moet specificeren: `RecoveryNote` met manuele recovery-instructie + propageer `ExecutionError` (nooit swallow).
- ✅ **IGitManager Protocol/ABC**: bestaat niet in de codebase (QA bevestigd). Geen interface-update nodig.
- ✅ **PreflightError**: bestaat al in `mcp_server/core/exceptions.py:112`. Geen nieuw exception type nodig.
- ✅ **soft_reset / hard_reset_to_head**: VERVALLEN. Alleen `hard_reset(ref)` en `force_push_with_lease()` nodig op adapter-niveau.
- ✅ **remote: bool flag op rollback**: VERVALLEN. Twee aparte methoden met duidelijke namen: `rollback_push()` (remote) intern in `prepare_submission()` impliciet (lokaal).


## Related Documentation
- **[mcp_server/tools/pr_tools.py — SubmitPRTool.execute() (current implementation)][related-1]**
- **[mcp_server/managers/git_manager.py — GitManager.pull() preflight pattern (lines 234-265)][related-2]**
- **[mcp_server/adapters/git_adapter.py — is_clean() line 70, has_upstream() line 299][related-3]**
- **[mcp_server/core/operation_notes.py — BlockerNote, RecoveryNote, PreflightError][related-4]**
- **[tests/mcp_server/integration/test_submit_pr_atomic_flow.py — existing integration tests][related-5]**
- **[tests/mcp_server/unit/tools/test_submit_pr_tool.py — existing unit tests][related-6]**
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md — §1.1 SRP, §4 Fail-Fast, §7 LoD, §8 Explicit, §14 Public API only][related-7]**

<!-- Link definitions -->

[related-1]: mcp_server/tools/pr_tools.py — SubmitPRTool.execute() (current implementation)
[related-2]: mcp_server/managers/git_manager.py — GitManager.pull() preflight pattern (lines 234-265)
[related-3]: mcp_server/adapters/git_adapter.py — is_clean() line 70, has_upstream() line 299
[related-4]: mcp_server/core/operation_notes.py — BlockerNote, RecoveryNote, PreflightError
[related-5]: tests/mcp_server/integration/test_submit_pr_atomic_flow.py — existing integration tests
[related-6]: tests/mcp_server/unit/tools/test_submit_pr_tool.py — existing unit tests
[related-7]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md — §1.1 SRP, §4 Fail-Fast, §7 LoD, §8 Explicit, §14 Public API only

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-05-05 | Agent | Initial draft — Findings 1-5, v1 Expected Result |
| 2.0 | 2026-05-05 | Agent | QA design review: added Findings 6-10, revised Expected Result v2 (prepare_submission pattern), revised Blast Radius and Open Questions. Force-transitioned back to research. |