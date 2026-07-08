<!-- docs\development\issue420\validation.md -->
<!-- template=validation_report version=fe38a66d created=2026-07-08T15:32Z updated= -->
# Validation Report: Issue #420


**Status:** APPROVED  
**Version:** 1.0  
**Last Updated:** 2026-07-08  
**Validation Outcome:** FAIL  
**Issue:** #420  
**Cycle:** C_DOCS.1  

---

## Scope

### Prerequisites
- Config version standardized to `"1.0.0"`
- Python 3.10+ virtual environments (`.venv` and `pgmcp_stable_venv`)
- Mapped assets compiled using `scripts/build_package.py`

### Summary Verdict
**FAIL**

While the entire test suite passes successfully and the core functionality behaves as planned, the validation phase registers a **FAIL** because 29 test files violate the strict quality gates (Pyright type check fails due to unused `Path` imports left after refactoring).

### Full-Suite Test Result
**PASS**
- **Executed**: `run_tests(scope='full')`
- **Result**: `pytest exited with code 0`
- **Stats**: 2890 passed, 4 skipped, 2 xfailed, 1 xpassed, 23 warnings.
- **Evidence**: All core, integration, and scaffolding test cases pass cleanly without regression.

### Branch Quality-Gate Result
**FAIL**
- **Executed**: `run_quality_gates(scope='branch')`
- **Result**: `overall pass: False`
- **Reason**: Gate 4b (Pyright) failed with 29 violations.
- **File Scope**: 29 test files under `tests/mcp_server/scaffolding/` and `tests/mcp_server/` contain `Import "Path" is not accessed` errors.

### Mapping from Planning Deliverables to Observed Evidence
| Ref | Deliverable / Exit Criteria | Observed Evidence | Status |
| --- | --- | --- | --- |
| **D1.1** | Config version validation friendly error | `test_config_version.py` validates custom `ConfigError` raising | **PASS** |
| **D1.2** | 16 config files updated to version `"1.0.0"` | Config files checked under `.pgmcp/config/` | **PASS** |
| **D2.1** | conftest dynamic template root override | `tests/conftest.py` configures `os.environ["MCP_TEMPLATE_ROOT"]` | **PASS** |
| **D2.2** | test_support template root settings query | `tests/mcp_server/test_support.py:get_template_root` | **PASS** |
| **D3.1** | Remove duplicate templates directory | `mcp_server/scaffolding/templates` directory deleted | **PASS** |
| **D4.1** | CLI `--init` flat recursive copy | `mcp_server/cli.py` copytree implementation | **PASS** |
| **D5.1** | VS Code agent instructions partitioned | `docs/agents/vscode/AGENTS.md` | **PASS** |
| **D5.2** | Antigravity agent instructions partitioned | `docs/agents/antigravity/AGENTS.md` | **PASS** |
| **D6.1** | Build manifest release_manifest.yaml exists | `.pgmcp/config/release_manifest.yaml` | **PASS** |
| **D6.2** | Pre-build sync script build_package.py | `scripts/build_package.py` | **PASS** |
| **D7.1** | Developer isolation guide created | `docs/setup/dev-isolation.md` | **PASS** |

### Design and Approved Strategy Alignment
- **CLI --init**: Bypasses developer environment dependencies. Uses generic recursive copy to `.pgmcp` and maintains the idempotency check.
- **Config Versioning**: Centralized validation intercepts version errors declaratively using Pydantic Literal type check validation without complex migration paths.
- **DRY Templates**: Decoupled test suite template lookup from hardcoded paths, dynamically pointing settings-resolved paths to the project root.

### Live Demonstration Proposal
#### Step 1: Config Version Check
Modify any YAML file (e.g. `workflows.yaml`) to `version: "0.9.0"`. Attempt to execute the server.
*Observed Outcome*: Server halts immediately with a human-readable `ConfigError` indicating expected version `1.0.0`, found `0.9.0`.

#### Step 2: Build Package Compilation
Run `python scripts/build_package.py`.
*Observed Outcome*: Pre-build copies assets dynamically and compiles the wheel inside the `dist/` directory.

#### Step 3: Target Initialization
Clean install the wheel in a new environment, run `pgmcp --init`.
*Observed Outcome*: A fresh `.pgmcp` directory is created. Excludes `template_registry.json`. Subsequent run fails with exit code 1.

### Residual Risks & Caveats
- **git_add_or_commit post-commit write**: The tool records sub-phase updates in `state.json` *after* the Git commit, leaving the worktree dirty (documented in `findings.md`).
- **Manual sync of agent instructions**: Propagating rule/persona updates between docs and active runtime remains developer-driven.

### Exact Failure Evidence (Pyright)
Below is the trace for the unused import errors across the 29 test files:
- `tests/mcp_server/scaffolding/test_concrete_code_templates.py` (line 16: Import "Path" is not accessed)
- `tests/mcp_server/scaffolding/test_concrete_test_integration.py` (line 7: Import "Path" is not accessed)
- `tests/mcp_server/scaffolding/test_concrete_test_unit.py` (line 7: Import "Path" is not accessed)
- [Total 29 occurrences of reportUnusedImport for "Path"]

---

## Outcome

Current validation status: **FAIL**.## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-08 | Agent | Initial draft |