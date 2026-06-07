<!-- docs\development\issue388\planning.md -->
<!-- template=planning version=130ac5ea created=2026-06-07T14:07Z updated= -->
# Planning: Separate ST3 backend into its own repository (#388)

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-06-07

---

## Scope

**In Scope:**
Pre-migration cleanup of tracked files in current repo. GitHub repo rename operations. New S1mpleTrader repo creation. git filter-repo migration with history. ST3 content removal from phase-gate-mcp. pyproject.toml split. docs/coding_standards/ duplication to new ST3 repo.

**Out of Scope:**
New repo CI/CD setup. Package naming for PyPI publication. History purge of ST3 commits from phase-gate-mcp (destructive, out of scope). AGENTS.md placement in new ST3 repo. Removal of old ST3 history from phase-gate-mcp git log.

## Prerequisites

Read these first:
1. docs/development/issue388/research.md v1.1 APPROVED
2. git-filter-repo installed in active venv (pip install git-filter-repo)
3. gh CLI authenticated with sufficient GitHub permissions (repo rename, repo create)
---

## Summary

Four-cycle plan to separate the ST3 backend from the phase-gate-mcp server. C1 cleans up stranded files in the current repo. C2 renames repos and creates the new S1mpleTrader repo. C3 migrates ST3 content to the new repo via git filter-repo. C4 removes ST3 content from the current (phase-gate-mcp) repo and updates pyproject.toml.

---

## Dependencies

- C2 must complete before C3 (target repo must exist)
- C1 must complete before C3 (stranded files must be moved so filter-repo captures correct state)
- C3 must complete and be verified before C4 (verify before delete)

---

## TDD Cycles


### Cycle 1: C1

**Goal:** Pre-migration cleanup: move 2 stranded MCP test files to tests/mcp_server/unit/config/, delete dead code dirs and empty shell dirs from tracked git state. Verify MCP test suite remains green and quality gates pass.

**Tests:**
- Run full MCP test suite after moves: run_tests(path='tests/mcp_server/')
- Verify moved test files pass in new location
- run_quality_gates(scope='branch')

**Success Criteria:**
D1: tests/unit/config/test_c_loader_structural.py moved to tests/mcp_server/unit/config/ and passing. D2: tests/unit/config/test_c_settings_structural.py moved to tests/mcp_server/unit/config/ and passing. D3: tests/unit/ directory fully removed from git tracking (git ls-files tests/unit/ returns empty). D4: src/copilot_orchestration/, tests/copilot_orchestration/, temp/, proof_of_concepts/ removed from git tracking. D5: Full MCP test suite passes after all moves (run_tests tests/mcp_server/). D6: Quality gates pass (run_quality_gates scope=branch).



### Cycle 2: C2

**Goal:** GitHub repo renames and new repo creation: rename S1mpleTrader to ST1 (frees the name), rename S1mpleTraderV3 to phase-gate-mcp (current repo), create new empty S1mpleTrader repo.

**Tests:**
- Verify S1mpleTrader name is free after rename to ST1
- Verify current repo remote URL reflects phase-gate-mcp rename
- Verify new S1mpleTrader repo exists and is empty

**Success Criteria:**
D7: Existing S1mpleTrader repo renamed to ST1 (GitHub redirect active). D8: Current repo (S1mpleTraderV3) renamed to phase-gate-mcp on GitHub (redirect from old URL active). D9: New empty S1mpleTrader repo created under MikeyVK account.

**Dependencies:** C1 committed and pushed


### Cycle 3: C3

**Goal:** Migrate ST3 content to new S1mpleTrader repo using git filter-repo on a fresh clone. Paths: backend/, tests/backend/, locales/, docs/architecture/, docs/coding_standards/ (copy), docs/reference/platform/, docs/reference/dtos/, docs/system/, docs/implementation/. Push result to new S1mpleTrader remote. Create minimal pyproject.toml for ST3 backend in new repo.

**Tests:**
- Verify new repo contains only ST3 paths (no mcp_server/, .phase-gate/, AGENTS.md)
- Verify git log in new repo contains only ST3-relevant commits (~100 commits)
- Verify backend/ Python imports work (no mcp_server imports remain)
- Verify docs/coding_standards/ is present in new repo

**Success Criteria:**
D10: New S1mpleTrader repo contains backend/, tests/backend/, locales/, docs/architecture/, docs/coding_standards/, docs/reference/platform/, docs/reference/dtos/, docs/system/, docs/implementation/. D11: New repo git history contains only ST3-relevant commits (first commit 2025-10-26). D12: New repo does NOT contain mcp_server/, .phase-gate/, AGENTS.md, scripts/. D13: New repo has a minimal pyproject.toml covering backend* package. D14: docs/coding_standards/ present in new repo.

**Dependencies:** C2 complete (target repo must exist), C1 complete (stranded files moved)


### Cycle 4: C4

**Goal:** Remove ST3 content from current (phase-gate-mcp) repo: delete backend/, tests/backend/, locales/, docs/architecture/, docs/reference/platform/, docs/reference/dtos/, docs/system/, docs/implementation/. Update pyproject.toml to remove backend* from includes and simpletraderv3 from package name. Update README.md for phase-gate-mcp identity.

**Tests:**
- Full MCP test suite passes after ST3 removal: run_tests(path='tests/mcp_server/')
- Verify no backend/ imports remain in mcp_server/ (grep check)
- run_quality_gates(scope='branch')
- Verify pyproject.toml includes only mcp_server*

**Success Criteria:**
D15: backend/, tests/backend/, locales/, docs/architecture/, docs/reference/platform/, docs/reference/dtos/, docs/system/, docs/implementation/ removed from git tracking in phase-gate-mcp repo. D16: pyproject.toml updated: packages.find.include contains only mcp_server*; package name updated. D17: Full MCP test suite passes (run_tests tests/mcp_server/). D18: Quality gates pass (run_quality_gates scope=branch). D19: No backend.* imports found in mcp_server/ source. D20: docs/archive/ and docs/temp/ removed from git tracking (both contain tracked files — docs/archive/execution_refactor_v4/ and docs/temp/ are ST3/deprecated content; docs/archive/ MCP design docs are historical and deleted per research §1e policy).

**Dependencies:** C3 complete and verified

---

## Risks & Mitigation

- **Risk:** git filter-repo rewrites history of the clone — if run on wrong directory, current repo history could be damaged
  - **Mitigation:** Always run filter-repo on a fresh clone, never on the working repo directly. Verify clone target before running.
- **Risk:** gh CLI repo rename may require specific permissions or fail if name is already taken
  - **Mitigation:** Rename S1mpleTrader→ST1 first to free the name. Verify each step before proceeding.
- **Risk:** After C4, old imports in phase-gate-mcp history reference backend/ paths — these are historical, not runtime
  - **Mitigation:** No action needed. Old commits with ST3 references are historical context; runtime code has no coupling.
- **Risk:** pyproject.toml package name update may break installed dev environment
  - **Mitigation:** Run pip install -e . after pyproject.toml update. Document in README.

---

## Milestones

- C1 done: current repo cleaned, MCP tests green
- C2 done: repos renamed, new S1mpleTrader repo exists
- C3 done: ST3 content in new repo with history verified
- C4 done: phase-gate-mcp repo contains only MCP content

## Related Documentation
- **[docs/development/issue388/research.md][related-1]**

<!-- Link definitions -->

[related-1]: docs/development/issue388/research.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-07 | Agent | Initial draft |