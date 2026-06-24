<!-- docs\development\issue406\pr.md -->
<!-- template=pr version=93bb9b4e created=2026-06-24T17:41Z updated= -->
# Russian Doll Decorator Pipeline for exception mapping

Refactored the monolithic exception mapping and validation bridge in server.py into a decoupled Russian Doll decorator pipeline with CQRS cache segregation, linear transport orchestration, and graceful presentation fallbacks. Also documented cache run resource and validation schema URIs.
## Changes
- Introduced InputValidationDecorator, EnforcementDecorator, and ToolErrorHandlerDecorator in core/decorators/
- Extracted narrow interfaces: ITool, ICoreTool, IPresenter, IToolResponsePublisher, IToolResponseReader in core/interfaces/
- Refactored server.py to implement a clean linear 5-step orchestration flow in handle_call_tool
- Added CachePublication DTO and configured user-facing fallback warnings in presentation.yaml
- Documented cache run resource and validation schema URIs in ARCHITECTURE.md

## Testing
Ran full unit test suite (2150 passed) and integration test suite (259 passed). All quality gates passed with 10.00/10.
## Checklist

- [ ] Run quality gates successfully
- [ ] Verify all tests pass
- [ ] Document all URI schemes in ARCHITECTURE.md
- [ ] Prepare deferred work transfer

## ⚠️ Breaking Changes

None. All JSON-RPC API structures and error DTO shapes have been preserved.
## Deferred Work

- Presenter (text_presenter.py) hardcoded tool classification: tool display categories are hardcoded as string literals in Python.
- Presenter (text_presenter.py) startup template check: presentation.yaml templates are not validated against DTOs at startup.
- Cache (cache.py/response_cache.py) normalization & canonicalization: run_id parsing and normalization are duplicated.
- Bootstrapping (bootstrap.py) inline imports to bypass circular dependency: circular references bypass via local function imports.
- Enforcement (enforcement_runner.py) split concrete check logic: dispatching and rule enforcement are in the same class.
- Config Loader (loader.py) project structure validation & config root probing: validation is mixed with loading.
- Validation (validator.py) ignore presentation config check: startup validator does not check presentation configs.
- Physically delete empty/retired production & test files: tools/base.py and empty test files are not deleted yet.
- Test Suite bloat, setup duplication, fakes/fixtures: setup duplication and redundant unit tests for metadata.
## Related Documentation
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-1]**
- **[docs/development/issue406/validation.md][related-2]**
- **[docs/mcp_server/ARCHITECTURE.md][related-3]**

---

Closes: #406