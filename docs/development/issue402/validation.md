<!-- docs\development\issue402\validation.md -->
<!-- template=validation_report version=fe38a66d created=2026-06-14T23:27Z updated= -->
# Validation Report — Issue #402: Expose JSON data in MCP tools


**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-06-15  
**Validation Outcome:** FAIL  
**Issue:** #402  

---

## 1. Scope & Prerequisites

This report documents the branch-wide validation of the implementation of Issue #402 ("Expose JSON data in MCP tools"), which migrated all 51 MCP tools to a new `ITool` and Pydantic DTO architecture, added a Response Cache Resource channel, and implemented the `verbose` options for the `run_quality_gates` tool.

### Prerequisites Checked:
- Research Document: Approved
- Design Document: Approved
- Planning Document: Approved
- Architecture Principles: Conforming (DIP, SRP, CQS, ISP)

---

## 2. Summary Verdict

The overall validation verdict is **FAIL**. 

While the production code migration is fully complete and all 2,886 automated tests pass successfully, the branch cannot be declared as `PASS` because of multiple quality gate violations in the **test files** under `tests/`. Under the non-negotiable rules in `QUALITY_GATES.md` (§3.25), all test files are held to the same strict styling, linting, and typing standards as production code.

---

## 3. Validation Results

### 3.1. Automated Test Suite Result
- **Command:** `run_tests(scope='full')`
- **Verdict:** **PASS**
- **Outcome:** 2886 passed, 5 skipped, 2 xfailed, 1 xpassed, 23 warnings in 48.93s.
- **Evidence:** Clean execution of the complete unit, integration, and E2E test suites with zero unexpected failures.

### 3.2. Branch Quality Gates Result
- **Command:** `run_quality_gates(scope='branch')`
- **Verdict:** **FAIL**
- **Outcome:** 114 files evaluated. Quality gates for Ruff format and Type checking on production code passed, but Ruff Strict Lint, Import Placement, Line Length, and Pyright failed on test files.
- **Exact Failure Evidence:**

| Gate | Status | Violations Count | Target Files / Scope | Example Issues |
|---|---|---|---|---|
| **Gate 0: Ruff Format** | **PASS** | 0 | All 114 files format correctly. | None |
| **Gate 1: Ruff Strict Lint** | **FAIL** | 17 | `tests/mcp_server/unit/test_presenter.py`<br>`tests/mcp_server/unit/test_server.py`<br>`tests/mcp_server/unit/tools/test_base.py` | `ANN201` (Missing return type annotation)<br>`ANN001` (Missing argument type annotation)<br>`ANN401` (Disallowed Any in execute)<br>`ARG001` (Unused function argument)<br>`F811` (Redefinition of unused test function) |
| **Gate 2: Imports** | **FAIL** | 16 | `tests/mcp_server/integration/...`<br>`tests/mcp_server/unit/...` | `PLC0415` (import should be at the top-level of a file) |
| **Gate 3: Line Length** | **FAIL** | 3 | `tests/mcp_server/unit/test_presenter.py` | `E501` (Line too long, e.g. 141 > 100) |
| **Gate 4: Types (DTOs)** | **PASS** | 0 | All production DTO schemas checked. | None |
| **Gate 4b: Pyright** | **FAIL** | 27 | `tests/mcp_server/integration/...`<br>`tests/mcp_server/unit/...` | `reportIncompatibleMethodOverride` (mock tools incorrectly overriding property)<br>`reportAssignmentType` (assigning literal strings to property)<br>`reportOperatorIssue` (operator 'in' not supported for None)<br>`reportOptionalMemberAccess` (member access on optional type) |
| **Gate 4c: Types (mcp_server)** | **PASS** | 0 | Production codebase type check passed. | None |

---

## 4. Deliverables & Exit Criteria Mapping

The validation verifies that the completed implementation cycles have met their defined goals:

| Deliverable ID | Description | Observed Evidence / Verification | Status |
| :--- | :--- | :--- | :--- |
| **D1.1 - D1.7** | Core `ITool` & Factory | `tests/mcp_server/unit/test_server.py` and `test_base.py` verify that tools execute, wrap in envelope, and present via MVP. | **PASS** |
| **D2.1 - D7.3** | Migration of Batches 1 to 4b | Verified by 500+ unit tests. All 51 migrated tools successfully return frozen Pydantic DTOs. | **PASS** |
| **D8.1 - D8.4** | `AutoFixTool` & Resource Cache | Verified by `test_autofix_tool.py`. FIFO eviction at 50 runs operates correctly. | **PASS** |
| **D9.1 - D9.4** | Batch 5 Migration & Cleanup | Verified. All legacy execution paths and `structuredContent` properties are deleted. | **PASS** |
| **D10.1 - D10.4**| Legacy Code Removal & Test Run | Verified. Full suite executes successfully without any references to legacy tools. | **PASS** |
| **D11.1 - D11.5**| Quality Gates Verbose Option | Verified by `test_quality_tools.py` and `test_qa_manager.py`. `verbose=True` successfully populates DTO details in cache; `verbose=False` leaves details empty and returns a `RecoveryNote`. | **PASS** |

---

## 5. Design & Approved Strategy Alignment

- **Separation of Concerns:** Confirmed. Tool execution remains separated from cache publishing (handled by decorator), presentation (handled by `TextPresenter` and `presentation.yaml`), and protocol handling (handled by `MCPServer`).
- **Immutability:** Confirmed. All tool output DTOs are defined with `frozen=True` and `extra="forbid"`.
- **MCP Resource Channel:** Confirmed. JSON payloads are entirely absent from the raw stdio MCP response, which only contains human-readable text and the resource URI.

---

## 6. Live Demonstration Proposal

The following live demonstration is proposed to the user to safely verify the new verbose gates and caching features:

### Step 1: Demonstrate Non-Verbose Failure & Recovery Note
- **Precondition:** Ensure a python file contains formatting or linting errors (e.g., add trailing spaces or omit docstrings).
- **Execution:** Run quality gates on this file with verbose disabled:
  ```json
  run_quality_gates(scope="files", files=["mcp_server/server.py"], verbose=false)
  ```
- **Expected Observation:** The tool returns a clean text summary, a `RecoveryNote` advising to rerun with `verbose=true`, and a resource URI like `pgmcp://cache/runs/abc`. Fetching the resource returns JSON with `"details": ""`.

### Step 2: Demonstrate Verbose Capture
- **Execution:** Run quality gates on the same file with verbose enabled:
  ```json
  run_quality_gates(scope="files", files=["mcp_server/server.py"], verbose=true)
  ```
- **Expected Observation:** The tool returns a lightweight summary text. Fetching the resource URI (e.g., `pgmcp://cache/runs/def`) returns JSON containing exit codes, full stdout, and stderr logs in the `details` field.

### Step 3: Demonstrate Cache FIFO Eviction
- **Execution:** Run 51 sequential simple tool calls (e.g. `health_check`) to populate the cache.
- **Expected Observation:** Attempting to retrieve the first run's resource URI returns an error indicating that the cache entry has been evicted.

---

## 7. Residual Risks & Caveats

- **Linter & Test Quality Gate Violations:** The `tests/` directory contains 57 total violations across Ruff lint, imports, line length, and Pyright. While these do not affect the execution of production tools or the MCP server, they must be refactored to comply with the non-negotiable quality gate baseline.
- **Client-Side URI Resolution:** The architecture relies on the client's ability to fetch data from the resource URI. Clients without resource inspection capabilities will only receive the human-readable text.

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-15 | Agent | Initial draft |
