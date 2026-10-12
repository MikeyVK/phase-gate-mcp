<!-- CHANGELOG.md -->
<!-- template=generic_doc version=43c84181 created=2026-07-22T17:47Z updated=2026-10-11 -->
# Changelog

All notable changes to Phase-Gate MCP Server are documented here, following
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

Release artifacts, tags and publication dates are recorded on
[GitHub Releases](https://github.com/MikeyVK/phase-gate-mcp/releases).
The release-preparation evidence records exact package verification and limitations.

## 3.0.0

The change boundary starts at the reconstructed 2.0.0 source revision
`ee32667ca95bf17ffb4ecd59062ef8cbed930e0b` and includes the merged v3 work through
[PR #499](https://github.com/MikeyVK/phase-gate-mcp/pull/499), plus the release
preparation in #500. Development-folder membership is not the release inventory.

### Breaking changes

- **Template suite and scaffolding:** Explicit packages combine manifests, context
  schemas, policies and shared Jinja tiers under `template_suite/`. Scaffold creation
  and existing-file editing have separate contracts. Rediscover admitted artifact IDs
  and context fields with the live tool schemas and `scaffold_schema`; removed aliases
  and old configuration shapes have no compatibility fallback
  ([#464](https://github.com/MikeyVK/phase-gate-mcp/pull/464)).
- **Authored context:** Full-document templates require `document_metadata` with status
  and a nonempty ordered revision history, including minimal contexts. Python package
  fields use explicit ASCII identifiers; module/class prose follows the selected
  package's schema. Tracking titles and labels belong to publication inputs rather than
  scaffold bodies ([#480](https://github.com/MikeyVK/phase-gate-mcp/pull/480),
  [#487](https://github.com/MikeyVK/phase-gate-mcp/pull/487)).
- **Native execution:** `run_checks`, `run_tests` and `apply_fixes` replace the old
  numbered quality routes. Migrate check/test/fix bindings and adapter declarations;
  interpret operation success alongside each native result. Branch checks require
  per-check `configured_targets` policies. They filter Git candidates before invocation;
  explicit-target calls retain native targeting semantics. Test execution has no
  branch scope ([#464](https://github.com/MikeyVK/phase-gate-mcp/pull/464),
  [#479](https://github.com/MikeyVK/phase-gate-mcp/pull/479),
  [#489](https://github.com/MikeyVK/phase-gate-mcp/pull/489)).
- **Planning mutation:** Initial save accepts ordered named cycles and complete phase
  blocks; the server derives totals and `C_#` / `D_#.#` references. Updates use explicit
  complete-block operations and explicit removal. A cycle with qualifying execution
  commits cannot be replaced, removed or renumbered. Planning admission is configured,
  cycle re-entry requires an explicit current-plan reference, and same-branch
  initialization refuses before overwriting planning
  ([#496](https://github.com/MikeyVK/phase-gate-mcp/pull/496)).
- **Discovery and Markdown:** Removed `search_documentation`; use host-native repository
  search and refresh client tool discovery. Lychee replaces the owned Markdown
  preflight/link implementation. The adapter no longer enforces an H1 rule
  ([#451](https://github.com/MikeyVK/phase-gate-mcp/pull/451),
  [#494](https://github.com/MikeyVK/phase-gate-mcp/pull/494)).

### Added and improved

- **Bundled artifact families:** YAML configuration, JSON Schema, ADR and arc42-based SAD
  packages extend the existing schema/Jinja composition. YAML/JSON output uses native
  parsing/schema checks; template identity can be read through the declared format route.
  ADR/SAD reuse the Markdown tiers
  ([#499](https://github.com/MikeyVK/phase-gate-mcp/pull/499)).
- **Recovery:** Rejected startup retains `health_check` and `restart_server`. Agents can
  diagnose from textual JSON, repair the owner-controlled cause and request restart.
  Restart acknowledgement alone does not establish healthy admission
  ([#488](https://github.com/MikeyVK/phase-gate-mcp/pull/488)).
- **Editing:** Proposed content, validation and persisted text share one LF representation.
  Change reporting reflects actual bytes; syntax feedback identifies candidate content.
  Shared scaffolds own headers/history, section joins and one terminal LF
  ([#497](https://github.com/MikeyVK/phase-gate-mcp/pull/497),
  [#490](https://github.com/MikeyVK/phase-gate-mcp/pull/490),
  [#480](https://github.com/MikeyVK/phase-gate-mcp/pull/480)).
- **Workflow and evidence:** Positive issue numbers are required for branch creation.
  Configured Chore supports compact maintenance work. Phase instructions, bounded
  presentation and Git push/upstream feedback were corrected; durable records retain
  invocation and outcome rather than relying solely on transient cache receipts
  ([#454](https://github.com/MikeyVK/phase-gate-mcp/pull/454),
  [#450](https://github.com/MikeyVK/phase-gate-mcp/pull/450),
  [#457](https://github.com/MikeyVK/phase-gate-mcp/pull/457),
  [#453](https://github.com/MikeyVK/phase-gate-mcp/pull/453),
  [#455](https://github.com/MikeyVK/phase-gate-mcp/pull/455),
  [#458](https://github.com/MikeyVK/phase-gate-mcp/pull/458)).
- **Distribution:** Canonical distributable agent sources and explicit nested/dotfile
  packaging support complete host assets. Release preparation aligns package versions,
  routes temporary issue/PR bodies to the ignored artifact directory and archives the
  previous development working set
  ([#447](https://github.com/MikeyVK/phase-gate-mcp/pull/447), #500).

### Owner migration and prerequisites

Installing the package, reconciling owner configuration, renewing the active template
suite/checkpoint and reconnecting the server/client are distinct steps. Existing roots
are not initialized in place; external roots are owner-controlled. Follow the
repository [workspace upgrade guide](https://github.com/MikeyVK/phase-gate-mcp/blob/main/docs/setup/workspace-upgrade.md) and
[release assets procedure](https://github.com/MikeyVK/phase-gate-mcp/blob/main/docs/reference/release-assets-procedure.md).

The shipped adapter declarations pin Ruff 0.15.6, Mypy 1.19.1, Pyright 1.1.408,
Lychee 0.24.2, Pytest 9.0.2 and its test dependencies, check-jsonschema 0.38.2 and
parser dependencies, Commitlint 21.2.2 with Node >=22.12.0, and TypeScript 6.0.3.
Provision applicable native tools separately; package installation and renewal do not
install them. See the [native adapter contract](https://github.com/MikeyVK/phase-gate-mcp/blob/main/docs/reference/execution-adapters.md)
and each adapter's declarations under `mcp_server/bundled_adapters/`.

### Limits

Native acceptance does not certify semantic use of every context field or preservation
of a template's structure after later edits. Template release review follows the
[existing maintenance guide](https://github.com/MikeyVK/phase-gate-mcp/blob/main/docs/development/schema-template-maintenance.md)
([#493](https://github.com/MikeyVK/phase-gate-mcp/pull/493)); active documentation links
were repaired ([#495](https://github.com/MikeyVK/phase-gate-mcp/pull/495)). Automatic
template-compliance enforcement is not included. Tool presentation and caches are bounded and caches are transient.
Read structured results when needed and retain durable evidence. Parked #121/#462
and automatic external rollout remain outside this release.

## 2.0.0 — Historical source boundary: 2026-07-22

Reconstructed from [PR #441](https://github.com/MikeyVK/phase-gate-mcp/pull/441),
revision `ee32667ca95bf17ffb4ecd59062ef8cbed930e0b`. This date identifies the
source integration; it is not a retrospective GitHub publication date.

### Added

- `pgmcp --upgrade` with timestamped backups, asset renewal and structured upgrade logs.
- Workspace `.version` validation and actionable init/upgrade advice.
- Four-operation `safe_edit_file` for existing files: replace, append, rewrite and
  pattern replacement, backed by atomic file writing.
- Degraded startup with health diagnostics on configuration failure.
- Dynamic state-file version tracking and preservation during upgrades.

### Changed and fixed

- Package release values align on 2.0.0; the bootstrapper delegates version validation.
- Template/schema configuration consolidates under the then-current `templates/` root.
- Force transitions use the explicit `human_approval_message` input.
- Upgrade preserves dynamic state and Git commit handling corrects dirty-worktree behavior.

Historical wheel/sdist reconstruction retains this revision's runtime and declared
assets. Its only packaging correction includes manifest-declared hidden assets. Reconstructed binaries must identify their build date/toolchain and
verification separately; they are not asserted to be original historical binaries.

## 1.0.0 — Historical source boundary: 2026-07-08

Reconstructed from [PR #426](https://github.com/MikeyVK/phase-gate-mcp/pull/426),
revision `3bfcef80fa97303d2b51738005b022edbcb0afbd`. The package name/version existed
earlier; this boundary completes standalone distribution. It supersedes the old
July 6 changelog date for this reconstructed release and does not invent a GitHub
publication date.

### Added

- Standalone Phase-Gate MCP package, `pgmcp` CLI, `--init` and `--version`.
- Manifest-driven asset assembly, installable wheel, host instructions and setup guides.
- Configured engineering workflows with Git/GitHub operations, project/phase tools,
  quality execution and Jinja scaffolding/schema discovery.
- Coordination, Implementation and independent QA agent roles.
- The `PGMCP_*` environment naming used by the standalone installation.

Historical wheel/sdist reconstruction retains this source and its declared assets,
with the same limited hidden-asset packaging correction as v2. Preparation does
not certify compatibility with every current dependency environment or rerun old
full suites. Final artifact evidence and actual publication remain separate.
