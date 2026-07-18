<!-- docs\development\issue432\research.md -->
<!-- template=research version=8b7bb3ab created=2026-07-18T17:49Z updated= -->
# Bug #432 Research: Graceful Server Initialization

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-07-18

---

## Problem Statement

Vulnerabilities in the MCP Server's startup sequence cause hard crashes on config validation errors (like template/artifact mismatches), breaking the agent connection instead of gracefully reporting the error.

## Research Goals

- Identify root cause of hard crashes on config errors
- Determine architectural constraints for fixing the initialization sequence
- Propose a strategy for graceful error reporting via MCP protocol

---

## Background

The server uses `ConfigLoader` which raises `ConfigError` or `FileNotFoundError` on startup for invalid configurations or template mismatches. This correctly enforces the architectural 'Fail-Fast' principle at the domain layer. However, in `cli.py`, this exception is unhandled and causes a non-zero exit code process crash, terminating the `stdio` connection used by the MCP protocol. Because MCP relies on JSON-RPC over `stdio`, the agent experiences an unexpected EOF, perceives the tools as 'dead', and presents an unrecoverable initialization failure to the user.

---

## Findings

1. **Protocol Support**: The MCP specification uses JSON-RPC 2.0. When an initialization error occurs, the protocol allows returning a JSON-RPC error object (e.g. -32602 for Invalid Params, or standard JSON-RPC errors) during the `initialize` handshake, rather than returning a successful capability negotiation.
2. **Differentiation**: True server-binding or OS-level infrastructure issues should still fail-fast and crash the process, but domain-specific configuration errors must be translated to MCP protocol errors to preserve the agent client UX.
3. **Consumer Impact**: As confirmed, there are no CLI/CI consumers relying on the `exit code > 0` behavior, clearing the path to catch these errors in the CLI and handle them gracefully for MCP clients.

---

## Approved Strategy

Clean break for CLI exit codes: modify the CLI entrypoint to catch domain-level `ConfigError` and `FileNotFoundError`. Since no CLI/CI consumers rely on a non-zero exit code, we do not need a separate `--stdio` flag. Differentiate between these domain config errors (which must be gracefully translated into an MCP JSON-RPC error response or handled by a Degraded Server) and true server infrastructure errors (which should continue to fail fast).

---

## Expected Results

1. Domain configuration errors (e.g., template/artifact version mismatches, missing config files) do not cause a process crash.
2. The MCP agent receives a diagnostic error message via the protocol, allowing it to inform the user about the specific configuration issue rather than showing a 'dead server' state.

## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-18 | Agent | Initial draft |