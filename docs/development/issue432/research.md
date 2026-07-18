<!-- docs\development\issue432\research.md -->
<!-- template=research version=8b7bb3ab created=2026-07-18T17:49Z updated= -->
# Bug #432 Research: Graceful Server Initialization

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-07-18

---

## Problem Statement

Vulnerabilities in the MCP Server's startup sequence cause hard crashes on config validation errors. Crucially, the current sequence conflates actual server-related initialization issues with template vs. artifact (config) version mismatches. Template and artifact version mismatches have nothing to do with the server itself and only affect the template/artifact/scaffolding tools, yet they currently bring down the entire server and break the agent connection.

## Research Goals

- Identify root cause of hard crashes on config errors
- Determine architectural constraints for fixing the initialization sequence
- Propose a strategy for graceful error reporting via MCP protocol

---

## Background

This issue was originally discovered during the implementation of #429 and deferred for separate handling. The server uses `ConfigLoader` which raises `ConfigError` or `FileNotFoundError` on startup for invalid configurations or template mismatches. This correctly enforces the architectural 'Fail-Fast' principle at the domain layer. However, in `cli.py`, this exception is unhandled and causes a non-zero exit code process crash, terminating the `stdio` connection used by the MCP protocol. Because MCP relies on JSON-RPC over `stdio`, the agent experiences an unexpected EOF, perceives the tools as 'dead', and presents an unrecoverable initialization failure to the user.

---

## Findings

1. **Separation of Concerns (Server vs. Tools)**: Template and artifact version mismatches are strictly related to scaffolding tools. They should not block server bootstrap. The server must initialize successfully regardless of template mismatches, isolating the failure to the specific scaffolding tools that rely on those templates.
2. **Protocol Support for Server Errors**: For actual server configuration errors, the MCP specification (using JSON-RPC 2.0) allows returning a JSON-RPC error object during the `initialize` handshake, rather than returning a successful capability negotiation.
3. **Differentiation**: True server-binding or OS-level infrastructure issues should still fail-fast and crash the process. Domain-specific server configuration errors must be translated to MCP protocol errors. Template/artifact mismatches should simply be isolated to tool-level validation.
4. **Consumer Impact**: As confirmed, there are no CLI/CI consumers relying on the `exit code > 0` behavior, clearing the path to catch actual server config errors in the CLI and handle them gracefully for MCP clients.

---

## Approved Strategy

Clean break strategy with distinct handling paths:
1. **Template/Artifact Version Mismatches**: Decouple these from the global server bootstrap validation. The server must initialize normally even if templates mismatch. The mismatch must be handled locally by the scaffolding tools (e.g., returning a validation error when the specific tool is invoked).
2. **True Server-Related Config Errors**: Modify the CLI entrypoint to catch domain-level server `ConfigError`s. Translate these gracefully into an MCP JSON-RPC error response (or Degraded Server) so the agent UX is preserved.
3. **Infrastructure Errors**: True server infrastructure errors (e.g., failing to bind, OS faults) will continue to fail fast.
No separate `--stdio` flag is needed because no CLI/CI consumers rely on the non-zero exit code.

---

## Expected Results

1. Template/artifact version mismatches have zero impact on global server initialization; they only affect the specific scaffolding tools.
2. Actual server configuration errors do not cause a process crash, but instead return a diagnostic error message via the MCP protocol.
3. True infrastructure faults continue to fail-fast.

## Related Documentation

- **[docs/development/issue429/deferred_work_notice.md][related-1]**
- **Issue #429**

<!-- Link definitions -->
[related-1]: ../issue429/deferred_work_notice.md
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-18 | Agent | Initial draft |