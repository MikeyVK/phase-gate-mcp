<!-- C:\temp\pgmcp\temp\issue460-design-workshops-20260910\10-distribution-integration.md -->
<!-- template=design version=5827e841 created=2026-09-10T09:24Z updated= -->
# W10 — Deliver one coherent release without reopening renewal

**Status:** HUMAN-APPROVED — W10 locally closed on 2026-09-12; canonical DI-06 §§7.6–7.7 owns the decisions; combined independent QA pending  
**Owner:** DI-06; upstream DI-01/02/03 and DI-05 official package declarations  
**Decision nucleus:** Keep the decided renewal state machine; finish asset inclusion, first-V3 migration and external-owner boundaries.

## 1. Purpose and authority

The suite design is not delivered if manifests/schemas disappear from the wheel or startup selects a different root. This workshop is an integration closure, not another upgrade strategy workshop.

## 2. Scope and exclusions

Release manifest, package-data inclusion, root wiring, initial V3 rollout and owner migration evidence. No adapter auto-upgrade, cross-repository migration, native dependency installer, compatibility matrix or artifact rewriting.

## 3. Binding inputs

[Distribution Design D-DIST-01–24](C:/temp/pgmcp/docs/development/issue460/design-distribution.md), F-10/I-17/I-18/E-21/E-22. [release_manifest.yaml](C:/temp/pgmcp/.pgmcp/config/release_manifest.yaml), [build_package.py](C:/temp/pgmcp/scripts/build_package.py), [pyproject.toml package discovery/data](C:/temp/pgmcp/pyproject.toml:36).

## 4. Proposed integration decisions

| ID | Proposal |
|---|---|
| W10-A | Approved: template_suite remains workspace assets; bundled_adapters remains outside assets |
| W10-B | Approved: mcp_server/bundled_adapters versus resolved_server_root/workspace_adapters |
| W10-C | Verify the built wheel as the consumer artifact, not only source directories |
| W10-D | First V3 migration remains checkpoint_required unless an approved explicit route applies |

## 5. Responsibilities and boundaries

Release build copies declared authoring sources into assets and packages them. Startup resolves configured roots. Template renewal owns only the managed template suite/checkpoint pair. Adapter catalog reads official installed assets plus trusted workspace packages; it does not let template renewal install or trust code.

## 6. Options and rationale

A single template/adapters upgrade tree would blur trust and merge responsibilities. Relying on a broad assets glob without inspecting the wheel can miss generation errors. Choose distinct mappings and consumer-level package tests; do not add another release registry.

## 7. Detailed design

### Source-grounded workshop clarification — 2026-09-11

W09 is human-approved, independently unreviewed. W10–W12 proceed before the combined
review by explicit human direction; the naming/location refinement and configuration integration are now consolidated in DI-05 D30 / DI-06 D25–26.

The current build manifest maps `.pgmcp/templates` to `assets/templates`.
`scripts/build_package.py:copy_assets` copies declared directories, while
`pyproject.toml` includes `mcp_server*` and `assets/**/*`. These are distribution
mechanisms, not proof that the final wheel contains each required package file.
`mcp_server/cli.py:main` currently copies the complete assets directory during init;
`WorkspaceUpgrader.renew_workspace_assets` likewise walks every packaged asset and
preserves existing configuration YAML by location. Under the previous same-name
adapter_suite proposal, placing official adapters in assets would have copied them into
the workspace extension store and created duplicate IDs. The approved separated roots
avoid this route entirely.

| Family | Authoring source | Installed distribution | Workspace destination and owner |
|---|---|---|---|
| Template suite | `.pgmcp/template_suite/` | `mcp_server/assets/template_suite/` | Managed resolved template root; DI-06 coherent suite/checkpoint operations, never generic per-file renewal |
| Official adapters | `mcp_server/bundled_adapters/` | `mcp_server/bundled_adapters/` | None: loaded from the server installation; never copied into the workspace extension store |
| Workspace adapters | Owner's resolved server root `workspace_adapters/` | Not collected into official assets by the release build | Remain owner-controlled; explicit trust and duplicate-ID rules from DI-05 |
| PGMCP configuration | `.pgmcp/config/` | `mcp_server/assets/config/` | Resolved config root; fresh-install defaults, existing configuration requires the approved migration/owner decisions |
| Native tool configuration | Workspace `pyproject.toml`, `pyrightconfig.json`, and other native files | Dependency/setup instructions as applicable, not a second settings authority | Workspace owner; no blanket overwrite or automatic native-dependency installation |

The release manifest remains the workspace-asset mapping authority; pyproject package
discovery/data inclusion ships bundled adapters directly. Build and
workspace delivery are separate operations: an asset's presence in the wheel does not
grant permission to install it into a workspace. Reuse the existing release mechanism;
do not create a second package registry, adapter updater or trusted-ID inventory.
DI-06 owns explicit delivery routing; DI-05 owns catalog admission and trust.

W09's self-hosting native settings are changes to this repository's own native config,
not permission to impose its Mypy file selection or Pyright platform settings on every
consumer workspace. Fresh role bindings/profile defaults can be shipped as PGMCP
configuration; native tool dependencies remain an explicit owner installation task.

Concrete missing-profile case: a candidate Python template uses `python_preflight`,
but the owner's effective `checks.yaml` has no such profile. The new template suite
must not activate against that configuration. Report the missing template/profile
relationship; the owner can inspect the shipped configuration and reconcile the
workspace configuration explicitly, then rerun `--upgrade`. Do not insert a profile,
replace the owner's file, execute the check, or manufacture availability. Existing
suite/checkpoint content remains unchanged while this admission failure persists.
The `.pgmcp/upgrade` tree remains template-only, not a catch-all config staging area.

Built-artifact evidence must include package `.version`, `policy.yaml`, JSON schemas,
Jinja files, adapter manifests/scripts and declared dependency contributions. Exercise
resource loading from an installed wheel outside the source checkout. In particular,
the commit adapter must resolve the shared header-reader implementation from the
installed distribution; no source-checkout import fallback or copied parser is allowed.
Wheel inspection proves delivery, not native dependency availability or adapter behavior.
Current `test_build_package.py` covers cleanup, manifest reading and missing sources;
it does not establish these installed-consumer guarantees. DI-08 receives the reusable
built-artifact fixture need; DI-06 retains the assertions and behavior ownership.

### Asset topology proposal

- Template authoring source: approved .pgmcp/template_suite; packaged target assets/template_suite.
- Official adapter authoring and installed location: mcp_server/bundled_adapters/, outside assets; no authoring-copy stage.
- Workspace adapter extension source: resolved_server_root/workspace_adapters, never the same implicit authoring/discovery source as official installed packages.
- Config assets contain the final role configs, approved adapters.yaml trust policy, artifact locations and presentation/workflow configuration. Managed V3 installation supplies trusted_adapter_ids: []; future config migration must preserve explicit owner trust rather than silently reset or broaden it.
- docs/agents remains source-first host instruction content, copied through existing release mapping.

The approved bundled_adapters/workspace_adapters separation prevents self-hosting from discovering official packages twice and keeps server-owned packages out of workspace asset copying. It does not change the approved template_suite topology.

Each declared package file, including manifest, schemas and dependency contributions, must survive authoring→wheel→installation; only workspace asset material passes through assets. Validate duplicate IDs and contained package references on installed material. Tests inspect wheel members and installed-resource resolution without relying on current working directory.

### Startup and upgrade seams already decided

- One actual template root; candidate .pgmcp/upgrade is non-authoritative.
- installation.json holds compatibility plus one optional template checkpoint with required shared and manifest-ID-keyed packages.
- Actual/adopted/candidate component comparison is unchanged.
- Full off-root proposal validation precedes recoverable complete-tree activation.
- Upgrade/startup share the decided lock; running server keeps its immutable old catalog.
- Actual content change yields CLI restart hint; checkpoint-only reconciliation does not pretend templates were reloaded.
- --upgrade remains the entrypoint; modifiers --accept-template-baseline, --resolve-template and --force-template-upgrade retain their approved mutual exclusion and semantics.
- Force requires verified timestamped backup outside active .pgmcp; no backup pruning/index is added.
- CLI exit codes remain 0 complete, 2 safe/action-required, 1 failure. No new MCP renewal result resource.

### Cross-config validation

Candidate template validation requires final manifest IDs and resolvable content-capable output profiles. It must use the intended effective config snapshot, not whichever live server object happens to exist. DI-06 receives a narrow SuiteAdmission interface plus explicit profile reader. It does not own adapter dependency readiness or execute validators during package admission.

A new candidate referencing a missing profile cannot activate. Shipping new role configuration is a separate release/config migration concern; do not solve this by silently overwriting workspace-native or customized PGMCP config. Installation/upgrade must expose the unresolved config requirement as actionable evidence.

### W10 config decision — approved 2026-09-12; canonical DI-06 §7.7

| Situation | Proposed behavior |
|---|---|
| New managed workspace, no existing configuration at its resolved config root | Supply V3 PGMCP defaults, including an empty workspace trust list; validate the initial suite against that effective configuration before activation |
| Existing workspace with valid V3 configuration | Read that actual configuration; do not replace customized profiles, binding defaults or trust with the shipped examples |
| Existing V2 configuration requires clean-break migration | Identify obsolete/missing configuration contracts and refer to the shipped V3 defaults and DI-07 migration instructions; owner/agent performs the explicit migration; no alias or automatic translation of native rules |
| New candidate references a profile absent from effective config | Admission fails before active suite/checkpoint mutation; report template_id, profile ID and config-relative source; use the existing candidate-invalid result, not a new upgrade state |
| Profile and adapter declarations resolve, but a native dependency is absent | Do not run dependency probes or validation tools during renewal; retain DI-05's configured discovery and on-use unavailable/error behavior |

An overridden config root remains authoritative; no fallback to packaged defaults merely
to pass candidate admission. For fresh install, an already populated external config root
must not be overwritten or mistaken for an empty one. Forced template replacement grants
no config overwrite authority and does not bypass suite/profile admission.

Shipped defaults remain inspectable in the installed assets/config directory. They are
reference material for an existing workspace, not a second runtime configuration layer.
The owner may reconcile configuration and rerun --upgrade; no separate config candidate
directory, config fingerprint ledger or config merge engine is introduced. All changed
configuration is loaded afresh for admission, not borrowed from the running server's old
catalog. The ordinary server-restart requirement still applies to adopting new runtime
configuration; template-renewal outcomes must not claim a running server was reloaded.

### First-V3 and external roots

No released V3 suite/checkpoint currently exists. Do not fabricate fingerprints, derive adopted components from V2 template_registry or equate missing new directory with fresh workspace. Preserve legacy actual, stage validated V3 candidate, return checkpoint_required. The owner chooses an approved explicit migration path.

External roots never acquire overwrite authority from equality. Owner-provided trusted prior V3 suite or explicit candidate acknowledgement can establish comparison basis, not permission to overwrite external content. The two-machine/four-workspace deployment context is evidence scope, not authorization for this task to touch those machines.

### Existing state and historical removals

.version contributes only its compatibility value during explicit migration; afterward normal startup reads installation.json only. Historical YAML bases remain recoverable by exact Git removal reference. Generic artifacts do not reintroduce S1mpleTrader-specific patterns; migration there remains owner workspace work.

## 8. Integration counterexamples

Valid source tree but missing wheel JSON schemas → distribution failure. Renamed package directory but same manifest ID → identity unchanged. Official adapter duplicated under workspace source → duplicate admission error, not precedence. New template profile absent → no activation. External root equals candidate → still no automatic overwrite. Reconciliation updates checkpoint only → no false actual_changed/restart claim.

## 9. Compatibility, migration and removal

Remove old per-file paired-asset renewal and normal .version/template_registry readers only under their decided cutover. Update settings resolved_template_root to template_suite and remove old root assumptions in setup/tests/docs. No dual-read fallback or stale assets retained for convenience. Do not delete unrelated user files as “package cleanup.”

## 10. Evidence

Built-wheel content tests; installed path resolution; config/root overrides; complete candidate validation; fresh vs existing V2 bootstrap; external safety; every activation interruption/recovery state; restart-stable running catalog; conditional restart hint; exact backup contents/path. Existing DI-06 state table remains the detailed acceptance authority.

## 11. Review points

Adapter authoring/location and associated delivery evidence are approved in DI-06 §7.6. Candidate/profile config integration is now approved in DI-06 §7.7. Review the canonical document with the remaining packages; this temporary file is navigation only. Do not reopen three-way merge logic or interpret package SemVer as compatibility.

## 12. Planning consequences

Packaging, config migration, renewal activation and owner deployment evidence are distinct deliverables. F-10 activation and F-20 fix application must not share a cycle. No actual deployment or cycles here.

## 13. Traceability

DI-06/F-10/E-21/E-22; DI-03 final IDs/removals; DI-05 distribution/pyproject consumer; DI-07 setup guidance; XC-02 old assets and readers.

## 14. Related documentation and history

Next: [W11 workflow/documentation](C:/temp/pgmcp/temp/issue460-design-workshops-20260910/11-workflow-documentation.md).  
0.1, 2026-09-10: temporary integration proposal over unchanged D-DIST decisions.
