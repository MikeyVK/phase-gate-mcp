<!-- docs\development\issue406\pr.md -->
<!-- template=pr version=93bb9b4e created=2026-06-20T09:17Z updated= -->
# feature: Russian Doll Decorator Pipeline for exception mapping

Refactored the MCP server tool execution flow using a clean separation of concerns. Monolithic validation and exception routing is replaced by a modular Russian Doll decorator chain, with segregated cache persistence and graceful text presentation fallbacks.
## Changes
Decomposed monolithic exception mapping and validation bridge into modular Russian Doll decorator pipeline. Introduced core interfaces (ITool, ICoreTool, IPresenter, IToolResponseCache) and decorators (InputValidationDecorator, EnforcementDecorator, ToolErrorHandlerDecorator). Cleaned up transport layer (server.py). Retired legacy decorators.

## Testing
Ran full test suite (2896 passed, 5 skipped, 2 xfailed, 1 xpassed) and verified all quality gates pass completely (10.00/10 on Ruff format, lint, imports, line length, and Pyright type-checking).
## Checklist

- [ ] All unit and integration tests pass successfully
- [ ] Ruff formatting, linting, imports, and line lengths pass cleanly
- [ ] Pyright type-checking passes with 0 violations
- [ ] Legacy decorators and base tool definitions retired
- [ ] Documentation updated to reflect new subsystems

## Related Documentation
- **[docs/development/issue406/validation.md][related-1]**
- **[docs/mcp_server/ARCHITECTURE.md][related-2]**

---

Closes: #406