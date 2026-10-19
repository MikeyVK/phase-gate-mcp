<!-- template=reference -->
# Configuration and Template Loading

**Status:** DEFINITIVE  
**Version:** 1.2  
**Last Updated:** 2026-10-18

Runtime settings select roots, workspace declarations select policy, and template packages own artifact contracts. Existing typed models remain authoritative for their fields.

## Runtime settings

[Settings.from_env()](../../mcp_server/config/settings.py) reads server and logging settings from the optional PGMCP_CONFIG_PATH overlay and supported environment variables. GitHub identity is not a launcher setting. PGMCP_CONFIG_ROOT selects the configuration directory; PGMCP_TEMPLATE_ROOT independently selects the template suite. Without these overrides, both resolve under the configured server root.

## Workspace declarations

[ConfigLoader](../../mcp_server/config/loader.py) reads required complete bases from `config_root/defaults/<file>.yaml` and optional workspace differences from `config_root/<file>.yaml`. The selected root is self-contained: missing bases do not fall back to a repository or installed package. Loading does not write files, create backups or materialize effective configuration.

Normal proxy/server startup first reads the required [server policy](server-configuration.md#startup-admission-policy)
through this same loader: defaults/server.yaml plus optional root server.yaml. The proxy
injects its configured initialize deadline; the child reads only this policy before
bounded lock acquisition and keeps other source admission inside the lock. No separate
startup loader or timing fallback is involved. Policy edits require full proxy/child
relaunch; direct CLI --init/--upgrade dispatch remains outside ordinary startup admission.

The basis must be a complete valid document. After composition, the result must satisfy the same domain model and cross-config references. Present empty YAML, duplicate keys, nonmapping roots, unreadable sources and invalid schema versions are errors. An absent override inherits; `{}` changes nothing.

An explicit `config_path` selects exactly one complete file without companion lookup or commands. Package adapter/template declarations and check-schema JSON retain their standalone routes. Enforcement is optional: neither source means empty policy; an override without a basis must be a complete valid enforcement document. The release manifest is outside this composition route.

The unused operation-policy route is removed: `PolicyEngine`, `PolicyDecision`,
`OperationPolicy`, `OperationPoliciesConfig` and
`ConfigLoader.load_operation_policies_config()` are no longer supported Python
contracts. Direct importers must remove those dependencies; there are no aliases
or compatibility loaders. Startup does not read `config_root/policies.yaml` or
`config_root/defaults/policies.yaml`. After updating the server, workspace owners
may explicitly remove those obsolete files; PGMCP does not delete existing
workspace files automatically. Active tool admission remains configured through
`enforcement.yaml` and workflow contracts; template `policy.yaml` and check/test/fix
configuration retain their own responsibilities.

## Composition and identity

Native Pydantic Settings source composition performs recursive mapping additions and updates. Mapping keys supply authored object identity within their parent. Display names, dispatch types and selectors retain their payload meaning. Nested object collections are mappings; empty object collections use `{}`.

Ordinary value lists remain literal sequences. Dashes and brackets have identical semantics: an override replaces the whole list and retains its own order and duplicates. Scalars and explicit null replace values. Null does not delete a key.

A root checks.yaml override can change one inherited field:

```yaml
checks:
  python_lint:
    timeout_seconds: 90
```

The only deletion command is the exact singleton mapping `{$delete: true}` at an inherited mapping member or record field:

```yaml
checks:
  unwanted_check:
    $delete: true
```

The example requires unwanted_check to exist in the basis. Unknown targets, other command values, sibling payload fields and commands inside literal lists are rejected. Complete bases and standalone files reject commands. Final model validation still applies: a removed required field/reference fails; a removed optional field may receive its schema default.

Where object sequence matters, complete/new members require strict integer `order`. Partial updates inherit it; sibling ranks must be unique. Ascending rank determines execution or presentation independently of YAML placement. There is no automatic append, renumbering or ID-based ordering. Lookup-only catalogs need no artificial rank.

```yaml
# Fragment of an ordered action collection
first_guard:
  order: 10
  type: check_pr_status
second_guard:
  order: 20
  type: check_context_loaded
  exempt_tools:
    - force_phase_transition
    - force_cycle_transition
```

The composition extension interprets deletion only; existing config models own ordering/domain validation. Consumers receive resolved values without learning about layers or commands.

## GitHub configuration

defaults/github.yaml supplies neutral values. Root github.yaml supplies explicit owner, repo, optional project_number and an optional token alternative where host delivery is unavailable. Bootstrap prefers a nonempty GITHUB_TOKEN, then the configured token. Repository identity is never inferred from identity environment variables, remotes or the token holder. The launcher settings overlay has no github section.

Neutral integration settings permit startup/health. Existing token-based registration, selected-use failures and enforcement remain effective; an operation may still require a GitHub lookup.

## Quality bindings and initialization

Base check/test/fix acknowledgement values are null. The workspace declares configuration_choice after reviewing its native policy. Initialization copies supplied assets without resetting choices; it does not guarantee that arbitrary supplied assets are neutral. Unresolved choices permit startup but retain selected-use refusal and safe-edit report behavior. Follow the [quality setup guide](../setup/README.md#choose-the-workspace-quality-policy).

## Template packages and ownership

Packages own manifest, policy, context schema and templates. Use scaffold_schema before scaffold_artifact; package versions and fingerprints identify sources. Template-only renewal does not compose or migrate workspace configuration. Restart after changing startup-loaded sources.

This refactor supplies no new build/distribution/upgrade mechanism. Existing roots require deliberate owner reconciliation.

## Related references

- [Server configuration](server-configuration.md)
- [Scaffolding tools](tools/scaffolding.md)
- [Editing tools](tools/editing.md)
- [Quality tools](tools/quality.md)

## Version History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0 | 2026-10-16 | @imp documenter | Consolidate the implemented layered-source and composition contract. |
| 1.1 | 2026-10-16 | @imp documenter | Document removed operation-policy Python/config contracts, deliberate owner cleanup and preserved active admission for #506. |
| 1.2 | 2026-10-18 | @imp documenter | Place early startup policy in ordinary source composition and describe its relaunch boundary for #520. |
