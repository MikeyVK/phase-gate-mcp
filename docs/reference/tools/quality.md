<!-- template=reference version=6.1 updated=2026-10-02 -->
# Checks, Tests, and Fixes

The V3 execution surface has three distinct operations: `run_checks`, `run_tests`, and
`apply_fixes`. Their roles and configurations are separate. The tools report operational
facts and native outcomes; a successful operation is not itself proof that every check or
test passed.

Input schemas are prepared from live configuration. Inspect the tool's exposed schema
for currently admitted profile, check, test, and fix IDs rather than copying a catalog
here. Native executable options retain their native meanings.

PGMCP injects a mandatory `execution_context.scratch_directory` into the internal
adapter JSON request after exclusively allocating its invocation directory. Public
callers continue to use the tool schemas below; they do not supply this internal
context. See the [native adapter execution contract](../execution-adapters.md) for
resource ownership, whole-selection transports, declared prerequisites, accepted
native cache/report effects and the concrete Pyright and Lychee input limits.

## `run_checks`

Source: [`check_tools.py`](../../../mcp_server/tools/check_tools.py) and
[`CheckSelectionRequest`](../../../mcp_server/execution/check_selection.py).

The request requires `scope`: `configured`, `workspace`, `targets`, or `branch`.
Supply non-empty workspace-relative `targets` only when the scope is `targets`.
Optionally select either a configured `profile` or explicit non-empty `checks`; these
are mutually exclusive. `args` maps selected check IDs to native argument lists and
replaces that binding's configured defaults for the call. `timeout_seconds` overrides
the configured timeout when supplied. Omit unused optional fields rather than passing
null.

Example using a currently configured profile and target:
`{"scope":"targets","targets":["mcp_server/tools/check_tools.py"],"profile":"python_review"}`

The output includes requested scope and targets, selected profile, branch-removed targets
when relevant, ordered check results, `run_status`, `success`, and an optional
operation `error_code` with typed details. Each result records the selected check,
status, native evidence, adapter identity, and bounded process capture as applicable.
`run_status` describes check outcomes; it is distinct from operation success and must
be reviewed alongside result rows.

## `run_tests`

Source: [`run_tests_tool.py`](../../../mcp_server/tools/run_tests_tool.py) and
[`TestSelectionRequest`](../../../mcp_server/execution/test_service.py).

The request requires `scope`: `configured`, `workspace`, or `targets`. Supply
non-empty workspace-relative `targets` only for the targets scope. Optional `tests`
selects configured test IDs; omitting it uses the applicable configured selection.
`args` maps selected test IDs to native argument lists, and `timeout_seconds` may
override configured timing. The public request rejects extra fields and duplicate
selections.

Example: `{"scope":"configured"}`

The output reports requested scope/targets, selected test IDs, an ordered result row
for each selected test, `success`, and an optional operation `error_code` with typed
details. Rows preserve passed, failed, unavailable, and not-executed states with native
evidence and invocation facts where applicable. Read both the operation envelope and
individual test rows; selection/protocol failures and test failure are different facts.

## `apply_fixes`

Source: [`fix_tools.py`](../../../mcp_server/tools/fix_tools.py) and
[`FixSelectionRequest`](../../../mcp_server/execution/fix_service.py).

Fixing is explicitly target-scoped. The request requires `scope: "targets"`, non-empty
workspace-relative file `targets`, and non-empty configured `fixes`. Optional
`args` maps selected fix IDs to native argument lists, replacing configured defaults
for those bindings; optional `timeout_seconds` overrides the configured timeout.

Example: `{"scope":"targets","targets":["mcp_server/tools/check_tools.py"],"fixes":["python_format"]}`

Fixes run in the order selected. The operation stops when a selected fix does not pass or
cannot continue; result rows identify later steps as not executed. Earlier native changes
may already have happened, so the operation does not promise atomic rollback. Inspect
affected files and native evidence before deciding whether to recheck or recover. The
tool does not automatically run checks after fixes.

The output includes requested targets, selected fix IDs, ordered factual results,
`success`, and an optional operation `error_code` with typed details. Per-result status
and available adapter identity, capture, and evidence distinguish a completed negative
fix result from an operation-level failure.

## Configuration and policy

Workspace declarations own check profiles and bindings, test bindings and activation,
and fix bindings. Adapter packages own capability contracts, native invocation behavior,
and external-tool identity. Runtime settings for native tools remain the owner's
responsibility. Configuration selects admitted work; it does not install dependencies or
redefine native option semantics.

Workflow contracts determine when evidence is required. Use the narrowest appropriate
selection, keep tests distinct from checks, and treat fixes as authorized mutations on
explicit files. After a fix, review observed file changes and select a recheck based on
the outcome. No automatic fix/check choreography is implied.

## Results and resources

The normal text response is a bounded projection. The complete structured operation DTO
is available at its cache URI, with native output represented only to the extent the
operation's bounded evidence and capture models retain it. Read the cache when you need
omitted rows or fields. Do not parse Markdown back into structured evidence, and do not
treat the presence of a cache URI as a passing verdict.

An invocation-directory cleanup failure after an accepted adapter response preserves
that complete preceding response and its outcome as JSON evidence. A fix may already
have changed sources; inspect the preserved native result and affected files.
Cancellation, request rejection and preceding process failure retain their primary
state while public check/test/fix/content results expose the additional cleanup cause.
Unconfirmed process termination retains owned resources for recovery.

For paged resources, assemble contiguous Unicode-codepoint slices and verify stable
run/length/hash metadata and the complete UTF-8 SHA256 before parsing. Preserve durable
observations because caches are transient. The client deadline must allow invocation,
termination and result processing; raising only the native deadline cannot recover a
receipt after the client has expired.

## Related references

- [Presentation architecture](../presentation_architecture.md)
- [Quality and evidence standards](../../coding_standards/QUALITY_GATES.md)
- [MCP tools navigation](README.md)
