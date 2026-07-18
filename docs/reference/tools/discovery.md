<!-- docs/reference/mcp/tools/discovery.md -->
<!-- template=reference version=064954ea created=2026-02-08T12:00:00+01:00 updated=2026-05-24 -->
# Discovery & Admin Tools

**Status:** DEFINITIVE  
**Version:** 3.0  
**Last Updated:** 2026-06-15  

**Source:** [mcp_server/tools/discovery_tools.py](../../../../mcp_server/tools/discovery_tools.py), [health_tools.py](../../../../mcp_server/tools/health_tools.py), [admin_tools.py](../../../../mcp_server/tools/admin_tools.py)  
**Tests:** [tests/mcp_server/unit/tools/test_discovery_tools.py](../../../../tests/mcp_server/unit/tools/test_discovery_tools.py)  

---

## Purpose

Complete reference documentation for discovery and administration tools covering documentation search, work context aggregation, server health checks, and hot-reload functionality.

These tools support agent onboarding, project awareness, and server lifecycle management.

---

## Overview

The MCP server provides **4 discovery/admin tools**:

| Tool | Purpose | Key Features |
|------|---------|-------------|
| `search_documentation` | Semantic/fuzzy search across docs/ | Scope filtering, ranked results with snippets |
| `get_work_context` | Aggregate branch + workflow context | Orientation header, phase instructions, invalid-state recovery warning, hand-over template |
| `health_check` | Server health status | Uptime, memory, registered tools count |
| `restart_server` | Hot-reload server via proxy | Zero-downtime restart for code changes |

---

## API Reference

### search_documentation

**MCP Name:** `search_documentation`  
**Class:** `SearchDocumentationTool`  
**File:** [mcp_server/tools/discovery_tools.py](../../../../mcp_server/tools/discovery_tools.py)

Semantic/fuzzy search across all docs/ files. Returns ranked results with snippets for understanding project structure.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | `str` | **Yes** | Search query (e.g., `"how to implement a worker"`, `"DTO validation rules"`) |
| `scope` | `str` | No | Optional scope: `"all"`, `"architecture"`, `"coding_standards"`, `"development"`, `"reference"`, `"implementation"` (default: `"all"`) |

#### Returns

```json
{
  "success": true,
  "results": [
    {
      "file": "docs/architecture/worker-pattern.md",
      "score": 0.92,
      "snippet": "Workers must inherit from BaseWorker and implement the execute() method...",
      "section": "Worker Implementation",
      "context": "architecture"
    },
    {
      "file": "docs/coding_standards/backend-conventions.md",
      "score": 0.85,
      "snippet": "Worker classes follow the pattern: <Name>Worker (e.g., OrderProcessingWorker)...",
      "section": "Naming Conventions",
      "context": "coding_standards"
    }
  ],
  "count": 2,
  "query": "how to implement a worker"
}
```

#### Example Usage

**Search across all docs:**
```json
{
  "query": "how to implement a worker"
}
```

**Search architecture docs only:**
```json
{
  "query": "DTO validation rules",
  "scope": "architecture"
}
```

**Search coding standards:**
```json
{
  "query": "naming conventions",
  "scope": "coding_standards"
}
```

#### Search Scopes

| Scope | Directories | Use Case |
|-------|-------------|----------|
| `all` | `docs/**` | Broad search when you don't know where to look |
| `architecture` | `docs/architecture/` | Design patterns, architectural decisions |
| `coding_standards` | `docs/coding_standards/` | Style guides, conventions |
| `development` | `docs/development/` | Issue tracking, research, planning |
| `reference` | `docs/reference/` | API docs, tool references |
| `implementation` | `docs/implementation/` | Implementation guides |

#### Behavior Notes

- **Semantic Matching:** Uses TF-IDF and fuzzy matching (not just exact string match)
- **Ranking:** Results sorted by relevance score (0.0 to 1.0)
- **Snippets:** Returns relevant text snippet (50-100 words) around match
- **Section Detection:** Identifies which section of document contains match
- **Case-Insensitive:** Search is case-insensitive

---

### get_work_context

**MCP Name:** `get_work_context`  
**Class:** `GetWorkContextTool`  
**File:** [mcp_server/tools/discovery_tools.py](../../../../mcp_server/tools/discovery_tools.py)

Aggregates the active branch and workflow state into an operator-facing orientation response. The response is formatted text, not a JSON work-queue payload, and is designed to be the authoritative startup context for the current branch.

#### Parameters

None. `GetWorkContextInput` is fieldless.

#### Returns (via MCP Resource Cache)

`get_work_context` returns a single `TextContent` block containing the formatted presentation text (including active branch details, phase instructions, and handover template) and the resource cache link pointing to the cached `GetWorkContextOutput` DTO.

The DTO is stored in the MCP Resource cache at `pgmcp://cache/runs/{run_id}` and contains the following fields:
- `current_branch`: `string`
- `workflow_name`: `string`
- `phase`: `string`
- `issue_number`: `int`
- `parent_branch`: `string`
- `sub_phase`: `string`
- `current_cycle`: `int`
- `phase_source`: `string`
- `phase_confidence`: `string`
- `sub_role_hint`: `string`
- `phase_instructions`: `string`
- `handover_template`: `string`
#### Text Fallback

```text
Branch: `feature/123-oauth` | Workflow: feature | Issue: #123
Phase: 🧪 implementation | Role: implementer
Parent: main
TODO discipline: create or refresh your TODO list now; keep exactly one item in progress and update it after each material step.

---

### 🎯 Phase Instructions

[ ] Call get_project_plan(issue_number=N)
[ ] Execute the current TDD cycle

---

### Hand-over Template

### Imp → QA hand-over
#### Scope
- Cycles executed: <list>
```

#### Example Usage

```json
{}
```

#### Behavior Notes

- **State Source:** Reads workflow, phase, issue number, parent branch, cycle, and sub-phase from branch-local `.pgmcp/state.json` when available.
- **Phase Script Delivery:** Reads `sub_role_hint`, `phase_instructions`, and optional `handover_template` from `.pgmcp/config/contracts.yaml` for the active workflow and phase.
- **Dominant Instructions Block:** Renders `### 🎯 Phase Instructions` as the first major section after the orientation header.
- **No Legacy Work Queue Payload:** Does not return `open_issues`, `recent_closed`, `suggestions`, `active_issue`, `recent_commits`, or `tdd_cycle_info`.
- **Bootstrap Degradation:** If branch state is unavailable, the tool still returns a branch-oriented response with an explicit `No instructions defined` fallback instead of failing.
- **Invalid Workflow-Phase Recovery:** If the workflow is known but the stored phase is invalid, the response stays non-error and renders a warning before `### 🎯 Phase Instructions` with the valid phases plus `force_phase_transition` / `get_work_context` recovery guidance.
- **Context-Loaded Side Effect:** Marks the current branch context as loaded in the in-memory cache when the writer is wired, which unblocks later branch-mutating tools behind `check_context_loaded`.
- **Gate Bootstrap Tool:** Remains callable even when `check_context_loaded` is active, because it is the tool that reloads branch context after phase, cycle, checkout, or non-noop pull changes.

---

### health_check

**MCP Name:** `health_check`  
**Class:** `HealthCheckTool`  
**File:** [mcp_server/tools/health_tools.py](../../../../mcp_server/tools/health_tools.py)

Check server health status.

#### Parameters

None.

#### Returns

```json
{
  "success": true,
  "health": {
    "status": "healthy",
    "uptime": 3600,
    "memory_usage_mb": 245.5,
    "registered_tools": 46,
    "github_token_set": true,
    "workspace_root": "/workspace",
    "python_version": "3.11.7",
    "server_version": "2.0.0"
  }
}
```

#### Example Usage

```json
{}
```

#### Health Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `status` | `str` | Overall status: `"healthy"`, `"unhealthy"` |
| `uptime` | `int` | Server uptime in seconds |
| `memory_usage_mb` | `float` | Current memory usage in megabytes |
| `registered_tools` | `int` | Number of registered MCP tools |
| `github_token_set` | `bool` | Whether `GITHUB_TOKEN` is configured |
| `workspace_root` | `str` | Absolute path to workspace root |
| `python_version` | `str` | Python runtime version |
| `server_version` | `str` | MCP server version |

#### Behavior Notes

- **Always Available:** No dependencies (doesn't require GitHub token)
- **Performance:** Minimal overhead (<10ms execution time)
- **Use Case:** Debugging, CI/CD health checks, agent diagnostics

#### Degraded Mode (Safe Mode)

If the server encounters domain-level configuration errors during startup (e.g., syntax errors or version mismatches in `.pgmcp/config/`), it boots into a **degraded mode**:
- Only the `health_check` tool is registered; all other tools are disabled.
- The `status` field returns `"unhealthy"`.
- The diagnostic error reason is populated in the `reason` field of the output.
---

### restart_server

**MCP Name:** `restart_server`  
**Class:** `RestartServerTool`  
**File:** [mcp_server/tools/admin_tools.py](../../../../mcp_server/tools/admin_tools.py)

Hot-reload MCP server to reload code changes via proxy mechanism.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `reason` | `str` | No | Description of why restart is needed (for audit logging) (default: `"code changes"`) |

#### Returns

```json
{
  "success": true,
  "message": "Server restart initiated",
  "restart": {
    "reason": "Updated safe_edit_file validation logic",
    "timestamp": "2026-02-08T12:00:00Z",
    "downtime_ms": 0
  }
}
```

#### Example Usage

**Restart after code changes:**
```json
{
  "reason": "Updated safe_edit_file validation logic"
}
```

**Restart without reason:**
```json
{}
```

#### Behavior Notes

- **Zero Downtime:** Proxy mechanism ensures no client disconnections
- **Code Reload:** Reloads all Python modules (tools, managers, services)
- **State Preservation:** Maintains client connections during restart
- **Wait Time:** **⏳ WAIT 3 SECONDS** after restart before calling next tool (server initialization time)
- **Audit Trail:** Records restart reason and timestamp in server logs

#### When to Use

- After modifying MCP tool code
- After updating validation logic
- After changing configuration files
- After updating templates

#### Proxy Architecture

The restart mechanism uses a transparent proxy:

1. **Proxy intercepts `restart_server` call**
2. **Proxy spawns new server process**
3. **Proxy waits for new process to be ready**
4. **Proxy switches traffic to new process**
5. **Proxy terminates old process**
6. **Zero client downtime** (connections maintained)

**See Also:** [docs/reference/mcp/proxy_restart.md](../proxy_restart.md) for detailed architecture.

---

## Common Use Cases

### Agent Onboarding: Discover Project Structure

```
1. search_documentation(query="project structure overview")
2. search_documentation(query="coding standards", scope="coding_standards")
3. search_documentation(query="how to implement a worker", scope="architecture")
4. get_work_context() → load the current branch orientation and phase script
```

### Find Relevant Documentation During Implementation

```
1. scaffold_artifact(artifact_type="worker", name="OrderWorker")
2. search_documentation(query="worker validation rules")
3. search_documentation(query="async patterns")
4. Implement worker based on documentation
```

### Load Branch Context And Phase Script

```
1. get_work_context()
2. Review the orientation header and current `### 🎯 Phase Instructions`
3. git_checkout(branch="feature/123-oauth") → switch to issue branch
4. get_project_plan(issue_number=123) → review phase plan
```

### Recover From Invalid Workflow-Phase State

```
1. get_work_context() → inspect the invalid workflow-state warning and valid phases list
2. force_phase_transition(branch="feature/123-oauth", to_phase="documentation", skip_reason="Repair invalid branch state", human_approval="Approved by workflow owner to repair invalid phase state")
3. get_work_context() → reload the current phase context and instructions
```

### Development Iteration with Hot-Reload

```
1. safe_edit_file(path="mcp_server/tools/safe_edit_tool.py", ...)
2. restart_server(reason="Updated validation logic")
3. Wait 3 seconds
4. health_check() → verify server restarted
5. Test updated tool
```

---

## Configuration

### Documentation Search Paths

Search scopes map to directories:

```yaml
scopes:
  all: "docs/**/*.md"
  architecture: "docs/architecture/**/*.md"
  coding_standards: "docs/coding_standards/**/*.md"
  development: "docs/development/**/*.md"
  reference: "docs/reference/**/*.md"
  implementation: "docs/implementation/**/*.md"
```

### Restart Proxy Configuration

Proxy behavior configured in [mcp_server/core/proxy.py](../../../../mcp_server/core/proxy.py):

- **Startup timeout:** 10 seconds
- **Health check interval:** 500ms
- **Graceful shutdown timeout:** 5 seconds
- **Connection buffer:** 100 concurrent connections

---

## Performance Characteristics

### search_documentation

- **Index Size:** ~100 documents (≈1MB total)
- **Search Time:** 50-200ms (depends on query complexity)
- **Memory:** ~20MB for search index
- **Optimization:** Results cached for repeated queries (5 min TTL)

### get_work_context

- **State Reads:** Current branch plus local `.pgmcp/state.json` and `.pgmcp/config/contracts.yaml`
- **Execution Time:** Local-only path with no GitHub network dependency
- **Side Effect:** Sets the in-memory `context_loaded` flag for the active branch when the writer is configured

### health_check

- **Execution Time:** <10ms
- **Memory Overhead:** Negligible (<1MB)
- **Always Available:** No external dependencies

### restart_server

- **Downtime:** 0ms (proxy maintains connections)
- **Restart Time:** 2-3 seconds (new process initialization)
- **Memory:** Temporary 2x memory usage during overlap

---

## Related Documentation

- [README.md](README.md) — MCP Tools navigation index
- [docs/reference/mcp/proxy_restart.md](../proxy_restart.md) — Hot-reload proxy architecture (detailed)
- [docs/reference/mcp/mcp_vision_reference.md](../mcp_vision_reference.md) — MCP server architecture and vision
- [docs/development/issue268/validation.md](../../../development/issue268/validation.md) — Validation evidence for the delivered `get_work_context` contract and `context_loaded` behavior

---

## Version History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 2.2 | 2026-05-24 | Agent | Document the invalid workflow-phase recovery warning and recovery path for `get_work_context` |
| 2.1 | 2026-05-23 | Agent | Update `get_work_context` reference to the delivered text contract, phase instructions, hand-over template, and context-loaded behavior |
| 2.0 | 2026-02-08 | Agent | Complete reference for 4 discovery/admin tools: documentation search, work context, health check, server restart |
