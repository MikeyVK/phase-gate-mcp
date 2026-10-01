# Template Package Identity and Artifact Provenance

**Status:** DEFINITIVE  
**Last Updated:** 2026-09-24

This reference describes the current package identity and source provenance written into newly scaffolded artifacts. The old `TEMPLATE_METADATA` YAML block, regex-validation rules, per-file path headers, and manually maintained template registry are not part of the active suite contract.

## Package identity

A concrete package is selected by the stable `template_id` in its `manifest.yaml`. The package also declares its purpose and owns its caller schema, root template, policy, and authored `.version` release label. Shared generation sources contribute through the package's resolved dependency graph. The package ID comes from the manifest; the physical package-directory name is storage, not identity.

The resolved package fingerprint describes the selected package's admitted generation-source closure. The source suite fingerprint describes the currently supplied suite generation snapshot. Both are computed identities; neither is a path or a per-file version. The package release label is authored separately and is not inferred from either fingerprint.

## Persisted artifact record

Each newly scaffolded artifact carries one compact `pgmcp:v1` provenance record as a complete native comment on its first physical line. The record has exactly four fields:

| Field | Meaning |
|---|---|
| `id` | The selected package's manifest `template_id` |
| `pv` | The package's authored `.version` release label |
| `pf` | The 16-character resolved package fingerprint |
| `sf` | The 16-character source suite fingerprint |

The logical record has this form:

```text
pgmcp:v1 id=<template_id> pv=<package_version> pf=<package_fingerprint> sf=<suite_fingerprint>
```

The surrounding comment syntax follows the generated file's language. The record contains no absolute or workspace path, creation timestamp, update timestamp, per-file hash, or historical registry pointer.

## Meaning and limits

The package fingerprint captures the selected package's admitted manifest, resolved caller schema, root template, and transitively used shared generation sources. The suite fingerprint captures source context for the supplied suite generation. A change to either source identity affects newly scaffolded artifacts; existing artifacts are not silently rewritten or marked stale.

These values describe generation inputs. They are useful for identifying which package contract and suite generation produced an artifact, but do not prove authenticity, guarantee access to historical source files, or authorize writes. Suite renewal uses a separate installation checkpoint and operational component identities; those values never replace `pf` or `sf`.

The active suite is resolved from its configured `template_suite/` root when the server starts. Workspace owners retain control of their installed suite and explicit upgrade or recovery choices. Official package content is maintained and delivered by PGMCP. See [Scaffold Schema and Template Maintenance](../development/schema-template-maintenance.md) for package location and maintenance guidance.

## Related guidance

- [Template Library Usage](TEMPLATE_LIBRARY_USAGE.md) — discovery, valid scaffold basis, and normal refinement.
- [Scaffolding Tools](tools/scaffolding.md) — current public schema and scaffold behavior.
- [Template Package Resolution Design](../development/issue460/design-suite-resolution.md) — identity boundaries and computed fingerprint semantics.
