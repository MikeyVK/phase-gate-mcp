<!-- docs\development\issue460\rollout-host-input.md -->
<!-- template=generic_doc version=43c84181 created=2026-09-17T09:42Z updated=2026-09-17 -->
# Issue 460 Rollout Host Input: Host Instruction Source Parity

**Status:** PRELIMINARY  
**Version:** 1.0  
**Last Updated:** 2026-09-17

---

## Purpose

Record reviewed source-authoritative host instruction mappings, direct-copy byte equality verification, and prospective V3 clean-break diffs for CY072 live installation.

## Scope

**In Scope:**
All 21 catalogued host instruction sources, mapped runtime consumers, release manifest mapping, byte equality checks, and prospective V3 diffs.

**Out of Scope:**
Direct mutation of live host instruction files (AGENTS.md, .agents/, .github/) prior to CY072; modification of server proxy or MCP transport logic.

## Prerequisites

Read these first:
1. docs/development/issue460/design-workflow-documentation.md
2. docs/development/issue460/planning-rollout.md#cy069
3. docs/reference/copilot-agent-instructions-model.md
---

## Summary

Implementation evidence for Cycle 69 (Host instruction source parity) under Issue #460. Verifies source-first host instruction mapping and byte parity, and stages prospective V3 patches without premature live advertisement.

---

## Key Changes

- Document exact host-authoritative source mappings to live runtime consumers
- Verify byte parity across all 8 direct-copy source-consumer pairs
- Prepare prospective clean-break V3 tool and procedure diffs for CY072 installation

---

## Migration Steps

1. CY069: Record parity baseline and prospective diffs in rollout-host-input.md
2. CY071: Rehearse prospective host patches against isolated candidate copies
3. CY072: Atomically apply prospective host diffs to live workspace files alongside server switch

---

## Validation Checklist

- [x] DOCFLOW-E03: All 8 direct-copy host instruction pairs are byte-identical
- [x] DOCFLOW-E05: Prospective V3 diffs agree with registered V3 tool/schema contracts
- [x] No inactive V3 contracts advertised in live workspace files prior to CY072

---

## 1. Mapping and Parity Register (DOCFLOW-E03)

Under DI-07 §7.3 and Planning Path Ownership, host instruction files originate in `docs/agents/<host>/` (the single source of truth) and are synchronized to active workspace and harness locations. Machine-specific connections and credentials are strictly excluded.

### 1.1 Direct-Copy Pairs and Verification

All eight direct-copy pairs are byte-identical in the repository baseline:

| Source ID | Authoritative Source Path | Mapped Consumer Path | Size | SHA-256 Checksum | Byte Parity Status |
|---|---|---|---|---|---|
| C025 -> C017 | `docs/agents/vscode/copilot/AGENTS.md` | `AGENTS.md` | 18,914 B | `2812cc4072e1982ea8080a94adbde8860cfdf75117f2fc16b4857985d232ec11` | IDENTICAL |
| C021 -> C008 | `docs/agents/codex/AGENTS.md` | `.agents/AGENTS.md` | 18,893 B | `4a7cbab1a3446f1cbd1cbfd53dcd2c13fdbcb1d03b63cc39e46cea7693e1ef7d` | IDENTICAL |
| C022 -> C009 | `docs/agents/codex/reboot.md` | `.agents/reboot.md` | 341 B | `989b89f77b38c2b1308487fe20004b6d8f5a08cc06bfd80fc24b3c1ed5a5f702` | IDENTICAL |
| C023 -> C010 | `docs/agents/codex/rules/research.agent.md` | `.agents/rules/research.agent.md` | 6,429 B | `109835c19b2286930fc4e432524722fba44a5c601c0f73b814543cdd820f46d4` | IDENTICAL |
| C024 -> C011 | `docs/agents/codex/workflows/create-issue.md` | `.agents/workflows/create-issue.md` | 3,200 B | `e515904083455d446889fd57c7cdc8cec8c87fd99ae7da24e2fbac9f34f73bd5` | IDENTICAL |
| C123 -> C121 | `docs/agents/codex/rules/qa.agent.md` | `.agents/rules/qa.agent.md` | 10,353 B | `895fb5e5632a19b8057ca25f8fd8ce367def2baab15775fdfa2131f50335b4bb` | IDENTICAL |
| C014 -> C013 | `docs/agents/vscode/copilot/.github/agents/qa.agent.md` | `.github/agents/qa.agent.md` | 11,439 B | `43421c76e0cff1fd2d9505067030c8c6f9189c08d54a41b4b4a47f40c818a5e3` | IDENTICAL |
| C015 -> C012 | `docs/agents/vscode/copilot/.github/agents/co.agent.md` | `.github/agents/co.agent.md` | 10,233 B | `516b44a3f667a8583a042567e7846801b0931b44656255eb9b825202b7a86dcd` | IDENTICAL |

### 1.2 Deliberate Host Differences and Unmapped Surfaces

In alignment with DI-07 §7.3 and `docs/reference/copilot-agent-instructions-model.md`:
1. **Host-Specific Frontmatter**: `AGENTS.md` (VS Code) specifies `chat.useAgentsMdFile: true`, while `.agents/AGENTS.md` (Codex) declares `Auto-loaded by Codex`, and `docs/agents/antigravity/AGENTS.md` declares `Auto-loaded by Antigravity`. The operational content (Architecture Contract, Tool Priority Matrix, TDD rules, Prime Directives) is otherwise identical.
2. **Harness Capability Profiles**:
   - `docs/agents/vscode/copilot/.github/agents/*.agent.md` define VS Code Copilot agent YAML headers with explicit `tools` arrays.
   - `.agents/rules/*.agent.md` and `docs/agents/antigravity/rules/*.agent.md` declare lightweight `trigger: manual` without Copilot-specific tool arrays.
3. **Workflow Invocation Formats**:
   - `.github/prompts/create-issue.prompt.md` (C016) is a Copilot prompt format (`agent: co`, `argument-hint:`).
   - `docs/agents/codex/workflows/create-issue.md` (C024) and `docs/agents/antigravity/workflows/create-issue.md` (C020) declare Markdown frontmatter with `@co` text routing.
4. **Machine Configuration Exclusion**:
   - `docs/agents/antigravity/mcp_config.json` contains template placeholders (`<PATH_TO_WORKSPACE_ROOT>`, `<PATH_TO_VENV_PYTHON_EXE>`); machine-specific settings are excluded from parity tracking.
5. **Release Manifest Mapping (S040)**:
   - `.pgmcp/config/release_manifest.yaml` maps `docs/agents` -> `agents` as generated distribution assets, not a competing instruction authority.

---

## 2. Resource Caching Procedure Alignment

CY011 implemented generic bounded presentation, schema-aware caching, and the dynamic server hint:
`Paged result; see pgmcp://cache/runs/{run_id}`.

### 2.1 Uniform Directive Across All Hosts
All host instruction sources (`AGENTS.md`, `.agents/AGENTS.md`, `docs/agents/antigravity/AGENTS.md`) already share the exact text for Prime Directive 9:
> **9. Resource Caching:** All MCP tools cache their structured Pydantic DTO outputs as MCP Resources (`pgmcp://cache/runs/{run_id}`). Tools return a presented text summary and the resource URI. When you need to inspect complete structured data or verbose process logs (e.g. from `run_quality_gates` or `run_tests`), you MUST read the cached resource URI (do not try to parse or scrape the text output).

### 2.2 Proportional Alignment
No artificial prompt bloat or complex multi-step procedural text is needed in host instructions. The server dynamically delivers the pagination hint and resource URI when truncated, and the reference documentation (`pgmcp://docs/cache-reading` and `docs/reference/cache_reading.md`) documents window-offset traversal. In CY072, the reference to `run_quality_gates` in Prime Directive 9 will be cleanly updated to `run_checks`.

---

## 3. Prospective Target Source Diffs (for CY072 Cutover)

Under CY069 requirements, inactive V3 contracts (`run_checks`, `apply_fixes`, `safe_edit_file` with `validation=enforce|report`) must **not** be advertised in live host files prior to CY072. Below are the reviewed prospective unified diffs staged for atomic installation during CY072.

### 3.1 `AGENTS.md` / `docs/agents/vscode/copilot/AGENTS.md` Prospective Diff
Preimage SHA-256: `2812cc4072e1982ea8080a94adbde8860cfdf75117f2fc16b4857985d232ec11`  
Postimage SHA-256: `c830c25a072054ff8e7bcfdf9f0868f0efd91244bb0c41fc86a51d28beec9db8`

```diff
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -73,6 +73,6 @@
 ### File Operations
 | Action | ✅ USE THIS | ❌ NEVER USE |
 |--------|-------------|------------|
-| Edit file | `safe_edit_file(path, operation, mode)` | `run_in_terminal("Set-Content")` |
+| Edit file | `safe_edit_file(path, content/line_edits/insert_lines/search+replace, mode)` | `run_in_terminal("Set-Content")` |
 | Scaffold code/docs | `scaffold_artifact(artifact_type, name, context)` | Manual creation |
 | Inspect artifact context schema | `scaffold_schema(artifact_type)` | Guessing context fields or trial-and-error calls |
@@ -80,6 +80,6 @@
 ### Quality & Testing
 | Action | ✅ USE THIS | ❌ NEVER USE |
 |--------|-------------|------------|
-| Run quality gates | `run_quality_gates(files)` | `run_in_terminal("pylint")` or `run_in_terminal("mypy")` |
-| Run tests | `run_tests(path, markers, timeout, verbose)` | `run_in_terminal("pytest")` |
-| Validate template | `validate_template(path, template_type)` | Manual review |
+| Run checks | `run_checks(scope, targets, profile, bindings)` | `run_in_terminal("pylint")` or `run_in_terminal("mypy")` |
+| Run tests | `run_tests(scope, targets, options)` | `run_in_terminal("pytest")` |
+| Apply fixes | `apply_fixes(files, bindings)` | Manual mass edits |
@@ -116,4 +116,4 @@
 ❌ **FORBIDDEN (use MCP tool instead):**
 - **File operations** → use `safe_edit_file` / `scaffold_artifact`
 - **Git operations** → use `git_*` tools (see matrix above)
 - **Test execution** → use `run_tests` tool
-- **Quality gates** → use `run_quality_gates` tool
+- **Quality checks** → use `run_checks` / `apply_fixes` tool
@@ -157,1 +157,1 @@
-9. **Resource Caching:** All MCP tools cache their structured Pydantic DTO outputs as MCP Resources (`pgmcp://cache/runs/{run_id}`). Tools return a presented text summary and the resource URI. When you need to inspect complete structured data or verbose process logs (e.g. from `run_quality_gates` or `run_tests`), you MUST read the cached resource URI (do not try to parse or scrape the text output).
+9. **Resource Caching:** All MCP tools cache their structured Pydantic DTO outputs as MCP Resources (`pgmcp://cache/runs/{run_id}`). Tools return a presented text summary and the resource URI. When you need to inspect complete structured data or verbose process logs (e.g. from `run_checks` or `run_tests`), you MUST read the cached resource URI (do not try to parse or scrape the text output).
```

### 3.2 `.agents/AGENTS.md` / `docs/agents/codex/AGENTS.md` Prospective Diff
Preimage SHA-256: `4a7cbab1a3446f1cbd1cbfd53dcd2c13fdbcb1d03b63cc39e46cea7693e1ef7d`  
Postimage SHA-256: `955743b2d183dcfae29ec97b1ebff954e7d17431e78eb3dc8d1e39b980277dfd`

```diff
--- a/.agents/AGENTS.md
+++ b/.agents/AGENTS.md
@@ -73,6 +73,6 @@
 ### File Operations
 | Action | ✅ USE THIS | ❌ NEVER USE |
 |--------|-------------|------------|
-| Edit file | `safe_edit_file(path, operation, mode)` | `run_in_terminal("Set-Content")` |
+| Edit file | `safe_edit_file(path, content/line_edits/insert_lines/search+replace, mode)` | `run_in_terminal("Set-Content")` |
 | Scaffold code/docs | `scaffold_artifact(artifact_type, name, context)` | Manual creation |
 | Inspect artifact context schema | `scaffold_schema(artifact_type)` | Guessing context fields or trial-and-error calls |
@@ -80,6 +80,6 @@
 ### Quality & Testing
 | Action | ✅ USE THIS | ❌ NEVER USE |
 |--------|-------------|------------|
-| Run quality gates | `run_quality_gates(files)` | `run_in_terminal("pylint")` or `run_in_terminal("mypy")` |
-| Run tests | `run_tests(path, markers, timeout, verbose)` | `run_in_terminal("pytest")` |
-| Validate template | `validate_template(path, template_type)` | Manual review |
+| Run checks | `run_checks(scope, targets, profile, bindings)` | `run_in_terminal("pylint")` or `run_in_terminal("mypy")` |
+| Run tests | `run_tests(scope, targets, options)` | `run_in_terminal("pytest")` |
+| Apply fixes | `apply_fixes(files, bindings)` | Manual mass edits |
@@ -116,4 +116,4 @@
 ❌ **FORBIDDEN (use MCP tool instead):**
 - **File operations** → use `safe_edit_file` / `scaffold_artifact`
 - **Git operations** → use `git_*` tools (see matrix above)
 - **Test execution** → use `run_tests` tool
-- **Quality gates** → use `run_quality_gates` tool
+- **Quality checks** → use `run_checks` / `apply_fixes` tool
@@ -157,1 +157,1 @@
-9. **Resource Caching:** All MCP tools cache their structured Pydantic DTO outputs as MCP Resources (`pgmcp://cache/runs/{run_id}`). Tools return a presented text summary and the resource URI. When you need to inspect complete structured data or verbose process logs (e.g. from `run_quality_gates` or `run_tests`), you MUST read the cached resource URI (do not try to parse or scrape the text output).
+9. **Resource Caching:** All MCP tools cache their structured Pydantic DTO outputs as MCP Resources (`pgmcp://cache/runs/{run_id}`). Tools return a presented text summary and the resource URI. When you need to inspect complete structured data or verbose process logs (e.g. from `run_checks` or `run_tests`), you MUST read the cached resource URI (do not try to parse or scrape the text output).
```

### 3.3 `.github/agents/qa.agent.md` / `docs/agents/vscode/copilot/.github/agents/qa.agent.md` Prospective Diff
Preimage SHA-256: `43421c76e0cff1fd2d9505067030c8c6f9189c08d54a41b4b4a47f40c818a5e3`  
Postimage SHA-256: `cbebbd2cf771d18bc3fa908e7cf8faecf06368d44747ebc7dbb94879feaa60c4`

```diff
--- a/.github/agents/qa.agent.md
+++ b/.github/agents/qa.agent.md
@@ -24,2 +24,2 @@
-  - phase-gate-mcp/run_quality_gates
-  - phase-gate-mcp/validate_template
+  - phase-gate-mcp/run_checks
+  - phase-gate-mcp/scaffold_schema
@@ -90,1 +90,1 @@
-  - running quality gates
+  - running checks
```

### 3.4 `.github/agents/co.agent.md` / `docs/agents/vscode/copilot/.github/agents/co.agent.md` Prospective Diff
Preimage SHA-256: `516b44a3f667a8583a042567e7846801b0931b44656255eb9b825202b7a86dcd`  
Postimage SHA-256: `52d4e6ba5f5fb244a19b222956cfbfd77eb572cc695e69e4ce136dfca56fdfc9`

```diff
--- a/.github/agents/co.agent.md
+++ b/.github/agents/co.agent.md
@@ -49,1 +49,2 @@
-  - phase-gate-mcp/run_quality_gates
+  - phase-gate-mcp/run_checks
+  - phase-gate-mcp/scaffold_schema
@@ -164,1 +165,1 @@
-  - epic phase transitions, commits, quality gates, PR submission, and merge
+  - epic phase transitions, commits, quality checks, PR submission, and merge
```

---

## 4. Rollback (R-CY069)

In case of rollback:
- **Pre-cycle Git Commit SHA:** `7ac179e4ece5003b75b32ce9968eaf7dc6632c14`
1. Remove `docs/development/issue460/rollout-host-input.md` (the sole new cycle-owned file in write-set).
2. Live workspace host files remain untouched during CY069 and require no rollback.

---

## Related Documentation
- **[docs/development/issue460/design-workflow-documentation.md][related-1]**
- **[docs/development/issue460/planning-rollout.md][related-2]**
- **[docs/development/issue460/rollout-workflow-input.md][related-3]**
- **[docs/reference/copilot-agent-instructions-model.md][related-4]**

<!-- Link definitions -->

[related-1]: docs/development/issue460/design-workflow-documentation.md
[related-2]: docs/development/issue460/planning-rollout.md
[related-3]: docs/development/issue460/rollout-workflow-input.md
[related-4]: docs/reference/copilot-agent-instructions-model.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-09-17 | @imp implementer | Initial release: mapping & parity register, resource caching alignment, prospective V3 host diffs, and verification checklist. |
