# Code Style Guide

## Purpose

This guide collects practical Python style advice. Binding architecture rules live in
[ARCHITECTURE_PRINCIPLES.md](ARCHITECTURE_PRINCIPLES.md); typing guidance lives in
[TYPE_CHECKING_PLAYBOOK.md](TYPE_CHECKING_PLAYBOOK.md); configured quality and test
requirements live in [QUALITY_GATES.md](QUALITY_GATES.md). Follow the repository's
formatters, linters, schemas, and file-specific conventions where they apply.

## Formatting and readability

Prefer clear names, short focused functions, explicit types at public boundaries, and
simple control flow. Use the project's configured formatter and linter to settle whitespace,
imports, and line length. Treat editor settings and sample limits as conveniences, not as
independent policy.

When examples are needed, use project-local concepts and keep them smaller than the
behavior being explained:

```python
from pathlib import Path


def resolve_workspace(path: Path) -> Path:
    """Return the normalized workspace path."""
    return path.resolve()
```

## Imports

Keep imports at module scope when practical and group standard-library, third-party, and
project imports according to the configured lint rules. Follow the architecture contract
when a local import is needed to avoid a cycle, defer optional work, or keep a dependency
at its intended boundary; do not move such imports mechanically.

## Documentation

Use module, class, and function docstrings to explain purpose and non-obvious contracts.
Keep routine method descriptions concise. Add examples to a Pydantic schema when they
materially clarify its public contract; required fields, examples, mutability, and extra-field
policy are determined by that contract's owner, not by a universal DTO recipe.

## Types and data contracts

Use precise types at public boundaries. Prefer the owning Pydantic model or protocol when
the boundary has a defined schema; use ordinary Python types for local implementation
details when they communicate the contract clearly. Apply frozen value semantics where
the architecture or owning model requires immutability.

## Repository-specific conventions

- Keep comments focused on decisions or constraints that are not clear from the code.
- Avoid unrelated trade, market, or service-domain examples in this repository's guidance.
- Do not add generated file headers or metadata unless the relevant template or source
  contract requires them.
- Use the project quality and type-checking references for executable commands and gate
  policy.

## Related documentation

- [Architecture principles](ARCHITECTURE_PRINCIPLES.md)
- [Type-checking playbook](TYPE_CHECKING_PLAYBOOK.md)
- [Quality gates](QUALITY_GATES.md)
- [Coding standards index](README.md)
- [Architecture manual](../manuals/architecture.md)
