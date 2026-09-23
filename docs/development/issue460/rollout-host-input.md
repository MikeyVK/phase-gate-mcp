<!-- docs\development\issue460\rollout-host-input.md -->
<!-- template=generic_doc version=43c84181 created=2026-09-17T09:42Z updated=2026-09-17 -->
# Issue 460 Rollout Host Input: Host Instruction Source Parity

**Status:** PRELIMINARY  
**Version:** 1.0  
**Last Updated:** 2026-09-17

---

## Purpose

Record reviewed source-authoritative host instruction mappings, direct-copy byte equality verification, complete disposition of all 21 catalogued host instruction sources, and prospective V3 clean-break diffs for CY072 live installation.

## Scope

**In Scope:**
All 21 catalogued host instruction sources, mapped runtime consumers, release manifest mapping, byte equality checks, lazy cache discovery alignment, explicit human scope approval for `.gitignore` maintenance, and prospective V3 diffs.

**Out of Scope:**
Direct mutation of live host instruction files (AGENTS.md, .agents/, .github/) prior to CY072; modification of server proxy or MCP transport logic; inclusion of cache-reading procedural steps in agent startup instructions.

## Prerequisites

Read these first:
1. [design-workflow-documentation.md](design-workflow-documentation.md)
2. [planning-rollout.md](planning-rollout.md#cy069)
3. [copilot-agent-instructions-model.md](../../reference/copilot-agent-instructions-model.md)
4. [cache_reading.md](../../../mcp_server/resources/cache_reading.md)

---

## Summary

Implementation evidence for Cycle 69 (Host instruction source parity) under Issue #460. Verifies source-first host instruction mapping and byte parity, accounts for all 21 catalogued preservation sources, documents lazy cache-reading resource alignment, records explicit human scope approval for `.gitignore` maintenance, and stages prospective V3 patches without premature live advertisement.

---

## Key Changes

- Document exact host-authoritative source mappings to live runtime consumers.
- Verify byte parity across all 8 direct-copy source-consumer pairs.
- Provide explicit disposition for all 21 catalogued host instruction sources.
- Clarify contractual separation for cache responses and lazy discovery of packaged reference `mcp_server/resources/cache_reading.md` via `pgmcp://docs/cache-reading`.
- Record human scope approval for repository-level `.gitignore` exclusion of `temp/`.
- Prepare prospective clean-break V3 tool and procedure diffs for CY072 installation across all affected host instruction files.

---

## Migration Steps

1. CY069: Record parity baseline, 21-source disposition, lazy cache discovery alignment, and prospective diffs in `rollout-host-input.md`.
2. CY071: Rehearse prospective host patches against isolated candidate copies.
3. CY072: Atomically apply prospective host diffs to live workspace files alongside server switch.

---

## Validation Checklist

- [x] DOCFLOW-E03: All 8 direct-copy host instruction pairs are byte-identical.
- [x] DOCFLOW-E03: All 21 catalogued host instruction sources have explicit disposition.
- [x] DOCFLOW-E05: Prospective V3 diffs agree with registered V3 tool/schema contracts across all affected host instructions.
- [x] Lazy cache reading contractually aligns with `text_presenter.py` and `cache_reading.md` (budget-triggered `pgmcp://docs/cache-reading` reference) without agent startup prompt bloat.
- [x] Explicit human scope approval obtained and recorded for `.gitignore` inclusion of `temp/`.
- [x] No inactive V3 contracts advertised in live workspace files prior to CY072.

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

### 1.3 Complete Inventory & Preservation Disposition for all 21 Catalogued Sources

All 21 sources identified in `planning-rollout.md#cy069` (DOCFLOW-E03) have an explicit reviewed disposition:

| ID | Repository Path | Nature / Host Authority | CY069 Status | Target Disposition for CY072 Cutover |
|---|---|---|---|---|
| C008 | `.agents/AGENTS.md` | Codex live consumer of C021 | Reviewed; preserved unchanged in CY069 | Apply prospective diff in Section 3.2 |
| C009 | `.agents/reboot.md` | Codex live consumer of C022 | Reviewed; preserved unchanged in CY069 | Retain byte parity with C022; no V3 tool changes required |
| C010 | `.agents/rules/research.agent.md` | Codex live consumer of C023 | Reviewed; preserved unchanged in CY069 | Apply prospective diff in Section 3.6 |
| C011 | `.agents/workflows/create-issue.md` | Codex live consumer of C024 | Reviewed; preserved unchanged in CY069 | Retain byte parity with C024; no V3 tool changes required |
| C012 | `.github/agents/co.agent.md` | Copilot live consumer of C015 | Reviewed; preserved unchanged in CY069 | Apply prospective diff in Section 3.5 |
| C013 | `.github/agents/qa.agent.md` | Copilot live consumer of C014 | Reviewed; preserved unchanged in CY069 | Apply prospective diff in Section 3.4 |
| C014 | `docs/agents/vscode/copilot/.github/agents/qa.agent.md` | Authoritative source for C013 | Reviewed; preserved unchanged in CY069 | Apply prospective diff in Section 3.4 (retained byte-identical with C013) |
| C015 | `docs/agents/vscode/copilot/.github/agents/co.agent.md` | Authoritative source for C012 | Reviewed; preserved unchanged in CY069 | Apply prospective diff in Section 3.5 (retained byte-identical with C012) |
| C016 | `.github/prompts/create-issue.prompt.md` | Copilot prompt file | Reviewed; preserved unchanged in CY069 | Retain; no V3 tool changes required |
| C017 | `AGENTS.md` | Copilot live consumer of C025 | Reviewed; preserved unchanged in CY069 | Apply prospective diff in Section 3.1 |
| C019 | `docs/agents/antigravity/AGENTS.md` | Antigravity authoritative instructions | Reviewed; preserved unchanged in CY069 | Apply prospective diff in Section 3.3 |
| C020 | `docs/agents/antigravity/workflows/create-issue.md` | Antigravity workflow file | Reviewed; preserved unchanged in CY069 | Retain; no V3 tool changes required |
| C021 | `docs/agents/codex/AGENTS.md` | Authoritative source for C008 | Reviewed; preserved unchanged in CY069 | Apply prospective diff in Section 3.2 (retained byte-identical with C008) |
| C022 | `docs/agents/codex/reboot.md` | Authoritative source for C009 | Reviewed; preserved unchanged in CY069 | Retain byte parity with C009; no V3 tool changes required |
| C023 | `docs/agents/codex/rules/research.agent.md` | Authoritative source for C010 | Reviewed; preserved unchanged in CY069 | Apply prospective diff in Section 3.6 (retained byte-identical with C010) |
| C024 | `docs/agents/codex/workflows/create-issue.md` | Authoritative source for C011 | Reviewed; preserved unchanged in CY069 | Retain byte parity with C011; no V3 tool changes required |
| C025 | `docs/agents/vscode/copilot/AGENTS.md` | Authoritative source for C017 | Reviewed; preserved unchanged in CY069 | Apply prospective diff in Section 3.1 (retained byte-identical with C017) |
| C121 | `.agents/rules/qa.agent.md` | Codex live consumer of C123 | Reviewed; preserved unchanged in CY069 | Retain byte parity with C123; read-only role rules remain valid |
| C122 | `docs/agents/antigravity/rules/qa.agent.md` | Antigravity QA role rules | Reviewed; preserved unchanged in CY069 | Retain; read-only role rules remain valid |
| C123 | `docs/agents/codex/rules/qa.agent.md` | Authoritative source for C121 | Reviewed; preserved unchanged in CY069 | Retain byte parity with C121; read-only role rules remain valid |
| S040 | `.pgmcp/config/release_manifest.yaml` | Release manifest suite asset mapping | Reviewed; preserved unchanged in CY069 | Retain; maps docs/agents -> agents as release distribution assets |

### 1.4 Explicit Human Scope Approval: Repository `.gitignore` Maintenance

On 2026-09-17, the human operator explicitly directed and approved the inclusion of `temp/` in `.gitignore` alongside `.pgmcp/temp/`. This repository maintenance prevents local ephemeral scratch and probe artifacts from accidentally becoming tracked in git across implementation cycles.

---

## 2. Resource Caching Procedure Alignment

CY011 implemented generic bounded presentation, schema-aware caching, and dynamic server hints.

### 2.1 Uniform Directive Across All Hosts
All host instruction sources (`AGENTS.md`, `.agents/AGENTS.md`, `docs/agents/antigravity/AGENTS.md`) share the exact text for Prime Directive 9:
> **9. Resource Caching:** All MCP tools cache their structured Pydantic DTO outputs as MCP Resources (`pgmcp://cache/runs/{run_id}`). Tools return a presented text summary and the resource URI. When you need to inspect complete structured data or verbose process logs (e.g. from `run_quality_gates` or `run_tests`), you MUST read the cached resource URI (do not try to parse or scrape the text output).

### 2.2 Contractual Separation and Lazy Cache Discovery
The implementation (`mcp_server/presenters/text_presenter.py:359` and `mcp_server/resources/cache_reading.md:3`) strictly enforces this contract:
1. **Always Cached:** Every successfully cached response receives a `pgmcp://cache/runs/{run_id}` resource URI.
2. **Budget-Triggered Reference:** Only when the response size exceeds the configured read budget (`size_chars > cache_read_budget_chars`, default 6,000 Unicode codepoints), the response presentation dynamically appends the reference hint:  
   `Paged result; see pgmcp://docs/cache-reading`.
3. **Packaged Reference:** The complete window traversal, integrity hash validation, and safe retry protocol are packaged directly at [cache_reading.md](../../../mcp_server/resources/cache_reading.md) (`mcp_server/resources/cache_reading.md`). The resource `pgmcp://docs/cache-reading` reads and serves this document directly without external repository checkout dependencies.
4. **Proportionality and Lean Startup Instructions:** Host instructions deliberately omit verbose window traversal, retry, or recovery algorithms. Agents discover and read `pgmcp://docs/cache-reading` lazily only when encountering truncated responses exceeding the read budget.
5. In CY072, the tool reference in Prime Directive 9 will be updated from `run_quality_gates` to `run_checks`.

---

## 3. Prospective Target Source Diffs (for CY072 Cutover)

Under CY069 requirements, inactive V3 contracts (`run_checks`, `apply_fixes`, `safe_edit_file` with `validation=enforce|report`) must **not** be advertised in live host files prior to CY072. Below are the reviewed prospective unified diffs staged for atomic installation during CY072.

### 3.1 `AGENTS.md` / `docs/agents/vscode/copilot/AGENTS.md` Prospective Diff
Preimage SHA-256: `2812cc4072e1982ea8080a94adbde8860cfdf75117f2fc16b4857985d232ec11`  
Postimage SHA-256 (CRLF retained): `0cf5faeddc019a01d847bb06aab15dddb380cfee69eb1549c9630b67c25c5a07`

```diff
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -73,6 +73,6 @@
 ### File Operations
 | Action | ✅ USE THIS | ❌ NEVER USE |
 |--------|-------------|------------|
-| Edit file | `safe_edit_file(path, operation, mode)` | `run_in_terminal("Set-Content")` |
+| Edit file | `safe_edit_file(path, operation, validation)` | `run_in_terminal("Set-Content")` |
-| Scaffold code/docs | `scaffold_artifact(artifact_type, name, context)` | Manual creation |
+| Scaffold code/docs | `scaffold_artifact(artifact_type, file_name, context)` | Manual creation |
 | Inspect artifact context schema | `scaffold_schema(artifact_type)` | Guessing context fields or trial-and-error calls |
@@ -80,6 +80,6 @@
 ### Quality & Testing
 | Action | ✅ USE THIS | ❌ NEVER USE |
 |--------|-------------|------------|
-| Run quality gates | `run_quality_gates(files)` | `run_in_terminal("pylint")` or `run_in_terminal("mypy")` |
-| Run tests | `run_tests(path, markers, timeout, verbose)` | `run_in_terminal("pytest")` |
-| Validate template | `validate_template(path, template_type)` | Manual review |
+| Run checks | `run_checks(scope, targets, profile, checks, args, timeout_seconds)` | `run_in_terminal("pylint")` or `run_in_terminal("mypy")` |
+| Run tests | `run_tests(scope, targets, tests, args, timeout_seconds)` | `run_in_terminal("pytest")` |
+| Apply fixes | `apply_fixes(scope, targets, fixes, args, timeout_seconds)` | Manual mass edits |
@@ -115,5 +115,5 @@
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
Postimage SHA-256 (CRLF retained): `56777b9ff7931a92e96ac3b4480f33356b425b683368d6c30ee5693240b77e32`

```diff
--- a/.agents/AGENTS.md
+++ b/.agents/AGENTS.md
@@ -73,6 +73,6 @@
 ### File Operations
 | Action | ✅ USE THIS | ❌ NEVER USE |
 |--------|-------------|------------|
-| Edit file | `safe_edit_file(path, operation, mode)` | `run_in_terminal("Set-Content")` |
+| Edit file | `safe_edit_file(path, operation, validation)` | `run_in_terminal("Set-Content")` |
-| Scaffold code/docs | `scaffold_artifact(artifact_type, name, context)` | Manual creation |
+| Scaffold code/docs | `scaffold_artifact(artifact_type, file_name, context)` | Manual creation |
 | Inspect artifact context schema | `scaffold_schema(artifact_type)` | Guessing context fields or trial-and-error calls |
@@ -80,6 +80,6 @@
 ### Quality & Testing
 | Action | ✅ USE THIS | ❌ NEVER USE |
 |--------|-------------|------------|
-| Run quality gates | `run_quality_gates(files)` | `run_in_terminal("pylint")` or `run_in_terminal("mypy")` |
-| Run tests | `run_tests(path, markers, timeout, verbose)` | `run_in_terminal("pytest")` |
-| Validate template | `validate_template(path, template_type)` | Manual review |
+| Run checks | `run_checks(scope, targets, profile, checks, args, timeout_seconds)` | `run_in_terminal("pylint")` or `run_in_terminal("mypy")` |
+| Run tests | `run_tests(scope, targets, tests, args, timeout_seconds)` | `run_in_terminal("pytest")` |
+| Apply fixes | `apply_fixes(scope, targets, fixes, args, timeout_seconds)` | Manual mass edits |
@@ -115,5 +115,5 @@
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

### 3.3 `docs/agents/antigravity/AGENTS.md` Prospective Diff
Preimage SHA-256: `a147cea6d8f0a598ad6855561631819a5b39e002cb05ccf2aa15fe90264dddcb`  
Postimage SHA-256 (CRLF retained): `856c51f663a5a9a0ec3087d2f9b12cb69012043f92de12e0d6561818a1454f38`

```diff
--- a/docs/agents/antigravity/AGENTS.md
+++ b/docs/agents/antigravity/AGENTS.md
@@ -73,6 +73,6 @@
 ### File Operations
 | Action | ✅ USE THIS | ❌ NEVER USE |
 |--------|-------------|------------|
-| Edit file | `safe_edit_file(path, operation, mode)` | `run_in_terminal("Set-Content")` |
+| Edit file | `safe_edit_file(path, operation, validation)` | `run_in_terminal("Set-Content")` |
-| Scaffold code/docs | `scaffold_artifact(artifact_type, name, context)` | Manual creation |
+| Scaffold code/docs | `scaffold_artifact(artifact_type, file_name, context)` | Manual creation |
 | Inspect artifact context schema | `scaffold_schema(artifact_type)` | Guessing context fields or trial-and-error calls |
@@ -80,6 +80,6 @@
 ### Quality & Testing
 | Action | ✅ USE THIS | ❌ NEVER USE |
 |--------|-------------|------------|
-| Run quality gates | `run_quality_gates(files)` | `run_in_terminal("pylint")` or `run_in_terminal("mypy")` |
-| Run tests | `run_tests(path, markers, timeout, verbose)` | `run_in_terminal("pytest")` |
-| Validate template | `validate_template(path, template_type)` | Manual review |
+| Run checks | `run_checks(scope, targets, profile, checks, args, timeout_seconds)` | `run_in_terminal("pylint")` or `run_in_terminal("mypy")` |
+| Run tests | `run_tests(scope, targets, tests, args, timeout_seconds)` | `run_in_terminal("pytest")` |
+| Apply fixes | `apply_fixes(scope, targets, fixes, args, timeout_seconds)` | Manual mass edits |
@@ -115,5 +115,5 @@
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

### 3.4 `.github/agents/qa.agent.md` / `docs/agents/vscode/copilot/.github/agents/qa.agent.md` Prospective Diff
Preimage SHA-256: `43421c76e0cff1fd2d9505067030c8c6f9189c08d54a41b4b4a47f40c818a5e3`  
Postimage SHA-256: `0e197ce0e232912cc8fc6e435b0bb232881766cfd7ae62ec29859fcc3b62a47b`

```diff
--- a/.github/agents/qa.agent.md
+++ b/.github/agents/qa.agent.md
@@ -24,2 +24,2 @@
-  - phase-gate-mcp/run_quality_gates
-  - phase-gate-mcp/validate_template
+  - phase-gate-mcp/run_checks
+  - phase-gate-mcp/scaffold_schema
@@ -90,1 +90,1 @@
-- running quality gates
+- running checks
```

### 3.5 `.github/agents/co.agent.md` / `docs/agents/vscode/copilot/.github/agents/co.agent.md` Prospective Diff
Preimage SHA-256: `516b44a3f667a8583a042567e7846801b0931b44656255eb9b825202b7a86dcd`  
Postimage SHA-256: `eeb3c623076200c018943a647d242753149bc77901054fb0ce2326dba043dba1`

```diff
--- a/.github/agents/co.agent.md
+++ b/.github/agents/co.agent.md
@@ -49,1 +49,2 @@
-  - phase-gate-mcp/run_quality_gates
+  - phase-gate-mcp/run_checks
+  - phase-gate-mcp/scaffold_schema
@@ -164,1 +165,1 @@
-- epic phase transitions, commits, quality gates, PR submission, and merge
+- epic phase transitions, commits, quality checks, PR submission, and merge
```

### 3.6 `.agents/rules/research.agent.md` / `docs/agents/codex/rules/research.agent.md` Prospective Diff
Preimage SHA-256: `109835c19b2286930fc4e432524722fba44a5c601c0f73b814543cdd820f46d4`  
Postimage SHA-256: `742e967fad5b977590feb454030d7f02b28a5fa9fa52cd9617b21170a4ee3f60`

```diff
--- a/.agents/rules/research.agent.md
+++ b/.agents/rules/research.agent.md
@@ -73,1 +73,1 @@
-| **Diagnostics & Validation** | `validate_template`, `health_check`, `send_message` | `restart_server`, `transition_phase`, `auto_fix` |
+| **Diagnostics & Validation** | `scaffold_schema`, `health_check`, `send_message` | `restart_server`, `transition_phase`, `run_checks`, `apply_fixes` |
```

---

## 4. Rollback (R-CY069)

In case of rollback:
- **Pre-cycle Git Commit SHA:** `7ac179e4ece5003b75b32ce9968eaf7dc6632c14`
1. Remove `docs/development/issue460/rollout-host-input.md` (the sole new cycle-owned documentation deliverable).
2. Live workspace host files remain untouched during CY069 and require no rollback.

---

## Related Documentation
- [design-workflow-documentation.md](design-workflow-documentation.md)
- [planning-rollout.md](planning-rollout.md)
- [rollout-workflow-input.md](rollout-workflow-input.md)
- [copilot-agent-instructions-model.md](../../reference/copilot-agent-instructions-model.md)
- [cache_reading.md](../../../mcp_server/resources/cache_reading.md)

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-09-17 | @imp implementer | Initial release: mapping & parity register, 21-source disposition, lazy cache discovery alignment, prospective V3 host diffs, and verification checklist. |
