<!-- docs\development\issue295\research.md -->
<!-- template=research version=8b7bb3ab created=2026-05-05T15:52Z updated= -->
# submit_pr Atomicity: Upstream Check, Dirty-Tree Guard, and Rollback on Failure

**Status:** FINAL (v3.1 — residuals R-1/R-2 resolved)  
**Version:** 3.1  
**Last Updated:** 2026-05-05

---

## Purpose

Research phase findings and expected result for issue #295. Provides the factual foundation for design and planning phases. Does not prescribe implementation details beyond what is needed to scope design choices.

## Scope

**In Scope:**
SubmitPRTool.execute() in mcp_server/tools/pr_tools.py; GitManager public API expansion; GitAdapter public API (read-only, identify gaps); existing test files test_submit_pr_atomic_flow.py and test_submit_pr_tool.py

**Out of Scope:**
initialize_project changes (belongs to issue #283/upstream); GitPushTool refactoring; enforcement.yaml changes; MergePRTool; any backward-compatibility shim — this is a clean break. Existing assertions in the following test files will break and require updates: `test_submit_pr_atomic_flow.py` (mock setup for neutralize_to_base / commit_with_scope / push that currently targets the tool body directly), `test_submit_pr_tool.py` (structural LoD-assertion scope — design will specify the updated assertion), `test_model1_branch_tip_neutralization.py` (integration coverage overlaps with new GitManager unit tests; design must determine whether these integration scenarios remain in scope or move to GitManager layer)

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

**Failure D — Push fails after neutralization commit (non-upstream reason):**
After neutralize_to_base() + commit_with_scope() succeed, push() fails for a non-upstream reason (network timeout, remote rejection, protected-branch policy). The branch has a local-only neutralization commit with artifacts at merge-base state. A retry of submit_pr finds no artifacts to neutralize (has_net_diff_for_path returns False) and either re-attempts the stranded push or produces an incorrect commit — neither path recovers the original state.

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

**Layer 2 (post-push rollback — constraints):** If create_pr() raises ExecutionError after successful push, the rollback mechanism must satisfy three constraints:
1. Undo the neutralization commit so HEAD returns to the pre-submit state
2. Restore the working tree to the pre-submit state (artifacts back, `is_clean()` = True after rollback)
3. Overwrite the remote with the restored HEAD so a retry finds a consistent, idempotent state

The `--force-with-lease` flag is appropriate because we own the last pushed commit. The exact reset sequence is a design decision.

## Finding 4: API changes needed on GitManager and GitAdapter *(superseded by Findings 6-10)*

> **Note:** This finding reflects the v1 design direction. Findings 6-10 (QA design review) supersede the specific API choices below. The constraints that replace this are in the Design Constraints section. Preserved for audit trail.

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

**Constraint:** De nieuwe GitManager-methode mag geen `MergeReadinessContext` accepteren als parameter — dit zou fase-contract-kennis in `GitManager` introduceren (§10 Cohesion). De aard van de data die de tool doorgeeft aan de methode (concrete typen, naamgeving, hoeveel parameters) is een design-beslissing; zie Open Questions.

## Design Constraints (voor design fase)

De volgende constraints, afgeleid uit Findings 1-10, sturen de designbeslissingen. De design fase beslist over exacte API-signaturen, interne algoritmen en test-asserties.

**Verantwoordelijkheidsverdeling (§1.1 SRP + §9 Canonical Pattern):**
- Een nieuwe GitManager-methode moet de volledige git-transactie bezitten: preflight (is_clean + has_upstream), artifact-selectie, neutralisatie, commit, push én lokale rollback bij partieel falen
- Een tweede GitManager-methode moet de remote rollback bezitten voor het scenario: push geslaagd + create_pr gefaald
- `SubmitPRTool.execute()` wordt gereduceerd tot orchestratie van git-methode + GitHub API + status-update; geen directe git-stappen in de tool body (neutralize_to_base / commit_with_scope / push / has_net_diff_for_path)

**Failure-dekking (alle vier modes):**
- Failure A (geen upstream): afgevangen vóór elke mutatie; geen state-wijziging; tool ontvangt PreflightError
- Failure B (dirty tree): afgevangen vóór elke mutatie; geen state-wijziging; tool ontvangt PreflightError
- Failure C (create_pr gefaald na push): remote rollback via de rollback-methode op GitManager
- Failure D (push gefaald na commit): lokale rollback binnen de git-transactie-methode

**Rollback-constraints:**
- Lokale rollback (Failure D): neutralization commit ongedaan maken; working tree moet clean zijn na rollback (`is_clean()` = True)
- Remote rollback (Failure C): local HEAD terugzetten + remote overschrijven met force-push-with-lease
- Na elke rollback: `is_clean()` = True zodat retry mogelijk is zonder extra cleanup

**LoD- en cohesion-constraints:**
- GitManager mag geen `MergeReadinessContext` accepteren (§10 Cohesion — zie Finding 10)
- Artifact-selectielogica (`has_net_diff_for_path` per pad) hoort intern in de git-transactie-methode
- Tool mag na wijziging geen `_git_manager.adapter` bevatten; ook niet neutralize_to_base / commit_with_scope / push / has_net_diff_for_path direct in de tool body

**Error-reporting:**
- Preflights (geen mutatie): `BlockerNote` + `PreflightError`
- Post-mutatie recovery: `RecoveryNote` + `ToolResult.error()`
- Rollback-meta-failure: `RecoveryNote` met manuele recovery-instructie + propageer `ExecutionError` (nooit swallow)

**Vervallen t.o.v. v1 design:** publieke `is_clean()`, `has_upstream()`, `rollback_neutralization(remote: bool)` als aparte GitManager public methods — waren symptomen van het verkeerde patroon; logica zit nu intern in de twee nieuwe methoden.

## Blast Radius

### Production Code

| File | Change |
|------|--------|
| `mcp_server/managers/git_manager.py` | Add new method encapsulating full git transaction: preflight + artifact-selection + neutralize + commit + push + local rollback |
| `mcp_server/managers/git_manager.py` | Add new method for remote rollback (hard reset + force-push-with-lease) |
| `mcp_server/adapters/git_adapter.py` | Add `hard_reset(ref: str)` — `git reset --hard {ref}` |
| `mcp_server/adapters/git_adapter.py` | Add `force_push_with_lease(remote: str)` — `git push --force-with-lease` |
| `mcp_server/tools/pr_tools.py` | `SubmitPRTool.execute()` vereenvoudigt: git-stappen verdwijnen uit de tool body, vervangen door 2 manager-aanroepen |

**Vervallen adapter-methoden t.o.v. v1:** `soft_reset(steps)`, `hard_reset_to_head()` — niet meer nodig; `hard_reset(ref)` dekt beide gevallen.
**Vervallen manager-methoden t.o.v. v1:** publieke `is_clean()`, `has_upstream()`, `rollback_neutralization(remote: bool)`.

### Test Code

| File | Change |
|------|--------|
| `tests/mcp_server/unit/managers/test_git_manager.py` | Nieuwe tests voor de git-transactie-methode (preflight A, B, artifact-selectie, commit-fail, push-fail) en de rollback-methode (success + force-push-fail) |
| `tests/mcp_server/unit/adapters/test_git_adapter.py` | Nieuwe tests voor `hard_reset(ref)` en `force_push_with_lease()` |
| `tests/mcp_server/integration/test_submit_pr_atomic_flow.py` | Update bestaande tests; voeg integratietests toe voor Failure A, B, C, D via tool |
| `tests/mcp_server/unit/tools/test_submit_pr_tool.py` | Update structurele LoD-test (extended assertion scope — design specificeert); update mock-setup |
| `tests/mcp_server/integration/test_model1_branch_tip_neutralization.py` | Review vereist: neutralization coverage overlapt met nieuwe GitManager unit tests; design bepaalt scope-herpositionering |

**Geen wijzigingen nodig in:** `enforcement.yaml`, `contracts.yaml`, `MergePRTool`, `GitCommitTool`, `test_ready_phase_enforcement.py`

## Open Questions

- ❓ **git-transactie data-interface**: Welk type geeft de tool door aan de nieuwe GitManager-methode voor de artifact-paden? Constraint: `MergeReadinessContext` mag de laaggrens niet oversteken (§10 Cohesion). Kandidaten: (a) `frozenset[str]` — puur data, GitManager blijft git-gericht; (b) een light DTO zonder fase-contract-kennis. Design bepaalt de keuze.
- ✅ **rollback meta-failure semantics**: `RecoveryNote` met manuele recovery-instructie + propageer `ExecutionError` (nooit swallow) — vastgelegd in Design Constraints.
- ✅ **IGitManager Protocol/ABC**: bestaat niet in de codebase (QA bevestigd). Geen interface-update nodig.
- ✅ **PreflightError**: bestaat al in `mcp_server/core/exceptions.py:112`. Geen nieuw exception type nodig.
- ✅ **soft_reset / hard_reset_to_head**: VERVALLEN. Alleen `hard_reset(ref)` en `force_push_with_lease()` nodig op adapter-niveau.
- ✅ **remote: bool flag op rollback**: VERVALLEN. Twee afzonderlijke methoden met duidelijke namen.


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
| 3.0 | 2026-05-05 | Agent | QA phase-separation review: added Failure D to Problem Statement; replaced Expected Result (design content) with Design Constraints; replaced Finding 3 algorithm with rollback constraints; removed concrete API signature from Finding 10; removed line estimates from Blast Radius; added test_model1_branch_tip_neutralization.py; anchored "clean break" in Scope. |