<!-- template=reference -->
# Configuration and Template Loading

The server separates runtime settings, workspace declarations, and template packages. Their public contracts are owned by the corresponding schemas and package manifests; this page explains how the pieces are selected without duplicating their fields.

## Runtime settings

[`Settings.from_env()`](../../mcp_server/config/settings.py) builds the server, logging, and GitHub settings. It accepts an optional YAML overlay from `PGMCP_CONFIG_PATH`; environment variables override the server fields (`PGMCP_SERVER_NAME`, `PGMCP_WORKSPACE_ROOT`, `PGMCP_SERVER_PROJECT_DIR`, `PGMCP_CONFIG_ROOT`, `PGMCP_TEMPLATE_ROOT`, `PGMCP_LOGS_DIR`), GitHub fields (`GITHUB_OWNER`, `GITHUB_REPO`, `GITHUB_PROJECT_NUMBER`, `GITHUB_TOKEN`), and `LOG_LEVEL`. The exact fields/defaults are defined in the settings models.

By default, the server root is `<workspace_root>/<server_root_dir>`; its config and template roots are `config` and `templates` beneath it. `PGMCP_CONFIG_ROOT` and `PGMCP_TEMPLATE_ROOT` provide explicit root overrides. Runtime settings do not replace workspace declarations.

## Workspace declarations

The current check, test, fix, adapter-trust, and artifact-location declarations are read by [`ConfigLoader`](../../mcp_server/config/loader.py) from the selected config root:

- `checks.yaml` → `ChecksConfig`
- `tests.yaml` → `TestsConfig`
- `fixes.yaml` → `FixesConfig`
- `adapters.yaml` → `AdapterTrustConfig`
- `artifacts.yaml` → `ArtifactLocationsConfig`

Their schemas live in [`mcp_server/config/schemas/`](../../mcp_server/config/schemas/). Check/test/fix rows select named adapter work; native tools and their arguments remain owned by the adapter registry and native executables. Config loading does not install or probe native dependencies.

## Template packages

Scaffolding uses the resolved template catalog. A package owns its manifest, policy, context schema, and template content; its schema is the authority for that package’s context fields. Use `scaffold_schema(artifact_type=...)` to retrieve the resolved schema, then pass a context to `scaffold_artifact`. The package version and fingerprint identify the resolved package in operation results. Do not maintain a second list of template IDs or context fields here.

## Ownership and failure boundaries

Configuration readers validate declarations against their typed schemas and report invalid or unreadable input as configuration errors. Workspace configuration selects work; it does not redefine tool input schemas, native executable behavior, or template package contracts. For exact tool arguments and result fields, see the relevant tool reference and its implementation/schema links.

## Related references

- [Server configuration](server-configuration.md)
- [Scaffolding tools](tools/scaffolding.md)
- [Editing tools](tools/editing.md)
- [Quality tools](tools/quality.md)
