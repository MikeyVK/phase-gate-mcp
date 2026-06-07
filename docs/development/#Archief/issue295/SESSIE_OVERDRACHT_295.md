# Sessie Overdracht — Issue #295
<!-- template=manual version=issue295 -->

## Branch
`fix/295-submit-pr-atomicity-upstream-dirty-tree-rollback`

## Status
**submit_pr atomicity fix is volledig geïmplementeerd (5 TDD-cycles), gevalideerd, gedocumenteerd en staat klaar voor PR.**

## Wat er gedaan is

### Doelstelling
Issue #295 + #304: `submit_pr` hardenen met drie garanties die voorheen ontbraken:
1. **Upstream-check (pre-flight):** blokkeert vóór elke mutatie als de branch geen upstream tracking heeft.
2. **Dirty-tree guard (pre-flight):** blokkeert als de working tree niet clean is bij aanvang.
3. **Rollback bij API-failure:** als `create_pr()` faalt nadat de branch al gepusht is, wordt de neutralization-commit lokaal én remote teruggedraaid via `hard_reset("HEAD~1")` + `force_push_with_lease`.

### Gewijzigde productiecode

**`mcp_server/adapters/git_adapter.py`** (C1)
- `hard_reset(ref: str) -> None` toegevoegd — wraps `git reset --hard <ref>`
- `force_push_with_lease(remote: str = "origin") -> None` toegevoegd — wraps `git push --force-with-lease`

**`mcp_server/managers/git_manager.py`** (C2/C3/C4 + QA-fix)
- `prepare_submission(artifact_paths: frozenset[str], base: str, note_context: NoteContext) -> bool` toegevoegd:
  - Stap 1: `is_clean()` — PreflightError + BlockerNote als dirty
  - Stap 2: `has_upstream()` — PreflightError + BlockerNote als geen upstream
  - Stap 3: filter artifacts via `has_net_diff_for_path`
  - Stap 4: conditioneel `neutralize_to_base` + `commit_with_scope("ready", ...)`; bij commit-fout: `hard_reset("HEAD")` + RecoveryNote + re-raise
  - Stap 5: `push()` altijd; bij push-fout + commit gemaakt: `hard_reset("HEAD~1")` + RecoveryNote + re-raise
  - Retourneert `bool(to_neutralize)` — CQS trade-off gedocumenteerd inline
- `rollback_push(note_context: NoteContext) -> None` toegevoegd:
  - `hard_reset("HEAD~1")` + RecoveryNote bij fout
  - `force_push_with_lease()` + RecoveryNote bij fout
- 4 broad `except Exception`-handlers vernauwd naar `except ExecutionError` (QA M-1)

**`mcp_server/tools/pr_tools.py`** (C5 + QA-fix)
- `SubmitPRTool.execute()` volledig herschreven: delegeert aan `prepare_submission` + `create_pr` + conditionele `rollback_push`
- Verwijderd: directe aanroepen van `neutralize_to_base`, `commit_with_scope`, `push` (Law of Demeter)
- Geen toegang meer tot `_git_manager.adapter` vanuit de tool
- Imports opgeschoond: `inspect` naar top-level, ongebruikte imports verwijderd

### Gewijzigde tests

**`tests/mcp_server/unit/adapters/test_git_adapter.py`** (C1)
- 5 tests toegevoegd: `hard_reset` (happy path + fout), `force_push_with_lease` (happy path + fout + custom remote)

**`tests/mcp_server/unit/managers/test_git_manager.py`** (C2/C3/C4 + QA-fix)
- `TestGitManagerPrepareSubmission`: 8 tests (preflights, artifact filter, conditioneel commit, push-rollback, commit-rollback)
- `TestGitManagerRollbackPush`: 3 tests (happy path, force-push failure, hard-reset failure)
- `mock_adapter.push.assert_called_once()` toegevoegd aan no-diffs test (QA m-1)

**`tests/mcp_server/integration/test_submit_pr_atomic_flow.py`** (C5 + QA-fix)
- `TestSubmitPRAtomicRefactored`: 8 integration tests (failure A, B, C-rollback, C-no-rollback, C-meta-failure, D, happy path × 2)
- Alle `asyncio.get_event_loop().run_until_complete()` → `asyncio.run()` (13 plaatsen) — QA NOGO B-1
- Module docstring bijgewerkt naar `prepare_submission`-encapsulatie

**`tests/mcp_server/unit/tools/test_submit_pr_tool.py`** (C5 + QA-fix)
- `TestSubmitPRToolLoD`: 2 structurele tests (tool roept geen git-internals direct aan, geen toegang tot adapter)
- `asyncio.run()` fix
- `inspect` naar top-level, ongebruikte imports verwijderd

**Totaal nieuwe tests: 26** (5 + 11 + 8 + 2)

### Gewijzigde documentatie

- `docs/reference/mcp/tools/github.md` — Atomic Execution Flow herschreven naar nieuwe 3-stappen API; failure-table (PreflightError / ExecutionError / rollback); enforcement guards uitgebreid met interne preflights; error message bijgewerkt
- `docs/reference/mcp/MCP_TOOLS.md` — submit_pr notitie bijgewerkt: nadruk op preflights vóór mutatie + automatische rollback
- `agent.md` — atomaire flow-beschrijving bijgewerkt: stap 1 = preflights, stap 5 incl. `rollback_push` bij API-fout
- `docs/development/issue295/research.md` — v3.1 FINAL (pre-implementatie)
- `docs/development/issue295/design.md` — v1.3 FINAL
- `docs/development/issue295/planning.md` — v1.0 FINAL

## Validatie

- Volledige testsuite: **2580 passed**, 1 pre-existing failure (geen regressies)
- Quality gates (6/6 groen): ruff lint, ruff format, mypy, coverage ≥ 90%, test totaal, complexity
- Smoke test live op branch: phase guard, no-upstream error path, dirty-tree error path, happy path — alle 4 geverifieerd
- Branch worktree: **clean** na laatste commit

## Commits (chronologisch, C1 → documentatie)

| SHA | Sub-fase | Beschrijving |
|-----|----------|-------------|
| `da2987d1` | C1 RED | add failing tests for `hard_reset` and `force_push_with_lease` |
| `2fa389fa` | C1 GREEN | implement `GitAdapter.hard_reset` and `force_push_with_lease` |
| `0ee3aba1` | C1 REFACTOR | quality gates pass on git_adapter.py and test_git_adapter.py |
| `6dadf014` | C2 RED | add 4 failing tests for `prepare_submission` preflights and artifact filter |
| `7e6f9f1c` | C2 GREEN | implement `prepare_submission` skeleton: preflights + artifact filter + push |
| `44eeb020` | C2 REFACTOR | ruff format + import sort |
| `940e51d4` | C3 RED | 4 failing tests for conditional commit, push, and rollbacks |
| `8b373730` | C3 GREEN | complete `prepare_submission` with conditional commit, push, and rollbacks |
| `4c967d9b` | C3 REFACTOR | ruff format + fix QA C2 minor |
| `c68dbb94` | C3 REFACTOR | fix `commit_with_scope`, Commit-failed message, add message assertions (QA NOGO F1-F3) |
| `f9c0c4a1` | C4 RED | 3 failing tests for `rollback_push` |
| `3711521a` | C4 GREEN | implement `rollback_push` with `hard_reset` and `force_push_with_lease` rollbacks |
| `ce3db534` | C4 REFACTOR | fix line lengths for ruff E501 |
| `bb7e76f1` | C5 RED | 8 integration + 2 LoD tests for refactored `SubmitPRTool.execute()` |
| `6a9fe30f` | C5 GREEN | `SubmitPRTool.execute()` delegates to `prepare_submission` + `rollback_push` |
| `cdf31b81` | C5 REFACTOR | fix unused imports, move `inspect` to top-level, fix line lengths |
| `b0c20142` | QA-fix | `asyncio.run()`, narrow `except ExecutionError`, CQS note, push assertion, update docstring |
| `6d08dff5` | DOCS | update submit_pr reference docs to reflect `prepare_submission` encapsulation |

## Follow-up

- Issue #304 is afgedekt door deze fix (rollback na API-failure geïmplementeerd).
- Issue #297 (`create_branch` hardening met upstream setup) is verwant en nog open.
- API-gebaseerde base-branch existence check (oorspronkelijk item 1 van #295 Expected Behavior) is bewust uitgesteld als afzonderlijke verbetering.
