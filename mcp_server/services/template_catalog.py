# mcp_server/services/template_catalog.py
# template=service version=5d5b489a created=2026-09-13T16:00Z updated=
"""Admit immutable template selections and render through explicitly injected consumers."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path

from pydantic import JsonValue

from mcp_server.config.schemas.template_suite import TemplateManifest, TemplatePolicy
from mcp_server.core.exceptions import MCPError
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, thaw_json
from mcp_server.services.template_graph import TemplateGraph


@dataclass(frozen=True)
class TemplatePackage:
    """One admitted public selection, independent of its physical directory name."""

    manifest: TemplateManifest
    version: str
    policy: TemplatePolicy
    schema: FrozenJsonObject
    renderer: str


@dataclass(frozen=True)
class TemplateCatalog:
    """One startup snapshot shared by introspection, validation and renderer selection."""

    packages: tuple[TemplatePackage, ...]
    graph: TemplateGraph

    def get(self, template_id: str) -> TemplatePackage:
        """Return the exact admitted package, without aliases or filesystem lookup."""
        for package in self.packages:
            if package.manifest.template_id == template_id:
                return package
        raise MCPError(
            "template_selection_unknown", code="ERR_CONFIG", params={"template_id": template_id}
        )


class TemplateCatalogLoader:
    """Join explicit package readers, policy validation and the prepared Jinja graph."""

    def __init__(
        self,
        suite_root: Path,
        *,
        read_manifest: Callable[[Path], TemplateManifest],
        read_version: Callable[[Path], str],
        read_policy: Callable[[Path], TemplatePolicy],
        read_schema: Callable[[Path], FrozenJsonObject],
        validate_policy: Callable[[TemplatePolicy], None],
        resolve_graph: Callable[[Iterable[tuple[str, str]]], TemplateGraph],
    ) -> None:
        if not suite_root.is_absolute():
            raise MCPError("absolute_suite_root_required", code="ERR_CONFIG")
        self._suite_root = suite_root.resolve()
        self._read_manifest = read_manifest
        self._read_version = read_version
        self._read_policy = read_policy
        self._read_schema = read_schema
        self._validate_policy = validate_policy
        self._resolve_graph = resolve_graph

    def load(self) -> TemplateCatalog:
        """Prepare every direct package before returning any catalog to consumers."""
        if (self._suite_root / "templates.yaml").exists():
            raise MCPError("duplicate_template_inventory", code="ERR_CONFIG")
        packages: list[TemplatePackage] = []
        identities: set[str] = set()
        for directory in sorted(self._suite_root.iterdir()):
            if not directory.is_dir():
                raise MCPError(
                    "template_package_directory_required",
                    code="ERR_CONFIG",
                    params={"package": directory.name},
                )
            if directory.name == "shared":
                if not directory.resolve(strict=True).is_relative_to(self._suite_root):
                    raise MCPError("template_package_escape", code="ERR_CONFIG")
                continue
            package = self._load_package(directory)
            identity = package.manifest.template_id
            if identity in identities:
                raise MCPError(
                    "template_identity_duplicate",
                    code="ERR_CONFIG",
                    params={"template_id": identity},
                )
            identities.add(identity)
            packages.append(package)
        if not packages:
            raise MCPError("template_catalog_empty", code="ERR_CONFIG")
        entries = tuple((package.manifest.template_id, package.renderer) for package in packages)
        graph = self._resolve_graph(entries)
        if {(root.template_id, root.template_name) for root in graph.roots} != set(entries):
            raise MCPError("template_renderer_selection_mismatch", code="ERR_CONFIG")
        return TemplateCatalog(
            tuple(sorted(packages, key=lambda item: item.manifest.template_id)), graph
        )

    def _load_package(self, directory: Path) -> TemplatePackage:
        resolved = directory.resolve(strict=True)
        if not resolved.is_relative_to(self._suite_root):
            raise MCPError(
                "template_package_escape", code="ERR_CONFIG", params={"package": directory.name}
            )
        members: dict[str, Path] = {}
        for name in (
            "manifest.yaml",
            ".version",
            "policy.yaml",
            "context.schema.json",
            "template.jinja2",
        ):
            path = directory / name
            if not path.is_file() or not path.resolve(strict=True).is_relative_to(resolved):
                raise MCPError(
                    "template_package_member_invalid",
                    code="ERR_CONFIG",
                    params={"package": directory.name, "member": name},
                )
            members[name] = path
        manifest = self._read_manifest(members["manifest.yaml"])
        version = self._read_version(members[".version"])
        policy = self._read_policy(members["policy.yaml"])
        self._validate_policy(policy)
        schema = self._read_schema(members["context.schema.json"])
        renderer = members["template.jinja2"].relative_to(self._suite_root).as_posix()
        return TemplatePackage(manifest, version, policy, schema, renderer)


class TemplateCatalogRenderer:
    """Consume one catalog snapshot through narrow validation and rendering callables."""

    def __init__(
        self,
        catalog: TemplateCatalog,
        *,
        validate_context: Callable[[FrozenJsonObject, object], FrozenJsonObject],
        render_context: Callable[[str, Mapping[str, JsonValue]], str],
    ) -> None:
        self._catalog = catalog
        self._validate_context = validate_context
        self._render_context = render_context

    def render(self, template_id: str, context: object, provenance: FrozenJsonObject) -> str:
        """Render validated caller content and a separately supplied server namespace."""
        package = self._catalog.get(template_id)
        content = self._validate_context(package.schema, context)
        return self._render_context(
            package.renderer, {"content": thaw_json(content), "provenance": thaw_json(provenance)}
        )
