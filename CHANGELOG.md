<!-- CHANGELOG.md -->
<!-- template=generic_doc version=43c84181 created=2026-07-22T17:47Z updated=2026-07-22T17:52Z -->
# Changelog

All notable changes to Phase-Gate MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-07-22

### Added
- **Workspace Upgrade Command (`pgmcp --upgrade`)**: Automated workspace upgrade mechanism orchestrating fail-safe timestamped backups (`.pgmcp_backup_YYYYMMDD_HHMMSS/`), smart asset renewal, and structured audit logs (`.pgmcp/logs/upgrade_YYYYMMDD_HHMMSS.json`) (#428).
- **Workspace Version Validation Manager (`WorkspaceVersionValidator`)**: Decoupled manager enforcing `.version` file existence and runtime version parity with actionable CLI advice (`pgmcp --upgrade` / `pgmcp --init`) (#428).
- **Upgrade Log Telemetry (`UpgradeLogDTO`)**: Immutable frozen Pydantic model (`extra="forbid"`) capturing structured telemetry for workspace upgrades (#428).
- **Frictionless File Editing (`safe_edit_file`)**: 4-operation schema (`replace`, `append`, `rewrite`, `pattern_replace`) with `must_exist=True` governance and fuzzy-match `difflib` error suggestions (#433).
- **Atomic File Writing (`IAtomicFileWriter` & `AtomicFileWriter`)**: Safe atomic temp-swap file writer utility guaranteeing zero corrupted partial writes (#433).

### Changed
- **Version SSOT Parity**: Package release version synchronized to `2.0.0` across `pyproject.toml`, `.pgmcp/config/release_manifest.yaml`, and `mcp_server/config/settings.py` (#428).
- **Bootstrapper Decoupling**: Refactored `ServerBootstrapper._validate_version` to delegate version validation responsibilities to `WorkspaceVersionValidator` (#428).

### Fixed
- **Dynamic State Preservation**: Guaranteed preservation of dynamic runtime state files (`state.json`, `deliverables.json`, `template_registry.json`, `logs/`) during workspace upgrades (#428).

## [1.0.0] - 2026-07-06

### Added
- **Phase-Gate MCP Framework**: Core architecture supporting phase-gated software engineering workflows (`feature`, `bug`, `docs`, `refactor`, `hotfix`, `epic`, `custom`).
- **MCP Server Tools Registry**: 47 specialized tools covering Git operations, GitHub issues/PR management, template scaffolding, test execution, quality gate validation, and work context discovery.
- **Three-Agent Model Protocol**: Built-in instructions and boundary controls for Coordination (`@co`), Implementation (`@imp`), and QA (`@qa`) agents.
- **Quality Gates Engine**: Automated linting (Ruff), type checking (Pyright/Mypy), line length enforcement, and import checking.
- **Template Scaffolding Engine**: Jinja2-powered artifact scaffolding with strict metadata headers and schema validation (`scaffold_artifact`, `scaffold_schema`).
- **Release Assets Sync Pipeline**: Build script (`scripts/build_package.py`) driven by `.pgmcp/config/release_manifest.yaml` to bundle workspace assets into Python wheel distribution.
