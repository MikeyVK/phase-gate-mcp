# mcp_server/services/template_catalog.py
# template=service version=5d5b489a created=2026-09-13T16:00Z updated=
"""Admit immutable template selections and render through explicitly injected consumers."""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path

from jinja2 import meta, nodes
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
        validate_inputs: Callable[[TemplatePackage, TemplateGraph], None],
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
        self._validate_inputs = validate_inputs

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
        for package in packages:
            self._validate_inputs(package, graph)
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


# Paths contain literal member names/indices; None denotes a computed item selection.
InputPath = tuple[str | int | None, ...]


@dataclass(frozen=True)
class _InputRead:
    path: InputPath
    line: int
    unbound: bool = False


class TemplateInputValidator:
    """Check static input declarations against prepared schemas without rendering.

    This is declaration linkage, not a proof of all control-flow/optional-value behavior.
    Computed accesses and macro arguments retain their containing schema; concrete
    renderer conformance tests own their value-dependent behavior.
    """

    def __init__(
        self,
        parse: Callable[[str, str], nodes.Template],
        provenance_schema: FrozenJsonObject,
    ) -> None:
        self._parse = parse
        self._provenance_schema = provenance_schema

    def validate(self, package: TemplatePackage, graph: TemplateGraph) -> None:
        """Check each reachable source against the selected package's input contract."""
        root = next(
            item for item in graph.roots if item.template_id == package.manifest.template_id
        )
        trees = {
            source.name: self._parse(source.content.decode("utf-8-sig"), source.name)
            for source in graph.sources
            if source.name in root.closure
        }
        schemas = {
            "content": thaw_json(package.schema),
            "provenance": thaw_json(self._provenance_schema),
        }

        def inherited(
            name: str, incoming: Mapping[str, InputPath | None]
        ) -> dict[str, InputPath | None]:
            available = dict(incoming)
            for edge in graph.edges:
                if edge.source == name and edge.kind == "extends":
                    available = inherited(edge.target, available)
                    _export_bindings(trees[edge.target].body, available)
            return available

        def visit(name: str, incoming: Mapping[str, InputPath | None]) -> None:
            tree = trees[name]
            module_bindings = inherited(name, incoming)
            _export_bindings(tree.body, module_bindings)
            external_names = meta.find_undeclared_variables(tree)

            parents: list[tuple[str, Mapping[str, InputPath | None]]] = []

            def dependency(node: nodes.Node, visible: Mapping[str, InputPath | None]) -> None:
                if not isinstance(
                    node, (nodes.Extends, nodes.Include, nodes.Import, nodes.FromImport)
                ):
                    return
                target = node.template
                if not isinstance(target, nodes.Const) or not isinstance(target.value, str):
                    raise MCPError("template_dependency_dynamic", code="ERR_CONFIG")
                if isinstance(node, nodes.Extends):
                    # Jinja renders a parent after the child's module statements.
                    parents.append((target.value, visible))
                else:
                    visit(target.value, visible if node.with_context else {})

            for read in _input_reads(tree, dict(incoming), dependency, module_bindings):
                namespace, *members = read.path
                if not isinstance(namespace, str):
                    continue
                if read.unbound:
                    if namespace in external_names:
                        raise _input_error(package, name, namespace, read.line)
                    continue
                if not _declares_path(schemas[namespace], tuple(members)):
                    display = ".".join("*" if part is None else str(part) for part in read.path)
                    raise _input_error(package, name, display, read.line)
            for parent_name, visible in parents:
                visit(parent_name, visible)

        visit(root.template_name, {key: (key,) for key in schemas})


def _input_error(package: TemplatePackage, source: str, field: str, line: int) -> MCPError:
    return MCPError(
        "template_input_undeclared",
        code="ERR_CONFIG",
        params={
            "template_id": package.manifest.template_id,
            "template": source,
            "field": field,
            "line": line,
        },
    )


def _reference(node: nodes.Node, bindings: Mapping[str, InputPath | None]) -> InputPath | None:
    if isinstance(node, nodes.Name):
        return bindings.get(node.name)
    if isinstance(node, (nodes.Getattr, nodes.Getitem)):
        parent = _reference(node.node, bindings)
        if parent is None:
            return None
        if isinstance(node, nodes.Getattr):
            return (*parent, node.attr)
        key = node.arg.value if isinstance(node.arg, nodes.Const) else None
        return (*parent, key if isinstance(key, (str, int)) else None)
    return None


def _bind(
    target: nodes.Node, value: InputPath | None, bindings: dict[str, InputPath | None]
) -> None:
    if isinstance(target, nodes.Name):
        bindings[target.name] = value
    else:
        for child in target.iter_child_nodes():
            _bind(child, None, bindings)


def _export_bindings(
    statements: Iterable[nodes.Node], bindings: dict[str, InputPath | None]
) -> None:
    """Collect ancestor module bindings, excluding block/loop/with/macro-local stores."""
    for node in statements:
        if isinstance(node, nodes.Macro):
            bindings[node.name] = None
        elif isinstance(node, nodes.Assign):
            _bind(node.target, _reference(node.node, bindings), bindings)
        elif isinstance(node, nodes.AssignBlock):
            _bind(node.target, None, bindings)
        elif isinstance(node, nodes.Import):
            bindings[node.target] = None
        elif isinstance(node, nodes.FromImport):
            for name in node.names:
                bindings[name[1] if isinstance(name, tuple) else name] = None
        elif isinstance(node, nodes.If):
            _export_bindings((*node.body, *node.elif_, *node.else_), bindings)


def _input_reads(
    node: nodes.Node,
    bindings: dict[str, InputPath | None],
    visit_dependency: Callable[[nodes.Node, Mapping[str, InputPath | None]], None],
    module_bindings: Mapping[str, InputPath | None],
) -> Iterable[_InputRead]:
    """Follow static namespace/alias reads while respecting Jinja lexical bindings."""
    reference = _reference(node, bindings)
    if reference is not None:
        yield _InputRead(reference, node.lineno)
    elif isinstance(node, nodes.Name) and node.ctx == "load" and node.name not in bindings:
        yield _InputRead((node.name,), node.lineno, unbound=True)
    if isinstance(node, (nodes.Extends, nodes.Include, nodes.Import, nodes.FromImport)):
        visit_dependency(node, bindings)
        if isinstance(node, nodes.Import):
            bindings[node.target] = None
        elif isinstance(node, nodes.FromImport):
            for name in node.names:
                bindings[name[1] if isinstance(name, tuple) else name] = None
        return
    if isinstance(node, (nodes.Macro, nodes.CallBlock)):
        if isinstance(node, nodes.Macro):
            bindings[node.name] = None
        else:
            yield from _input_reads(node.call, bindings, visit_dependency, module_bindings)
        local = {**bindings, "caller": None, "varargs": None, "kwargs": None}
        for argument in node.args:
            _bind(argument, None, local)
        for value in node.defaults:
            yield from _input_reads(value, local, visit_dependency, module_bindings)
        for child in node.body:
            yield from _input_reads(child, local, visit_dependency, module_bindings)
        return
    if isinstance(node, nodes.For):
        yield from _input_reads(node.iter, bindings, visit_dependency, module_bindings)
        local = dict(bindings)
        local["loop"] = None
        iterable = _reference(node.iter, bindings)
        _bind(node.target, (*iterable, None) if iterable is not None else None, local)
        for child in node.body:
            yield from _input_reads(child, local, visit_dependency, module_bindings)
        if node.test is not None:
            yield from _input_reads(node.test, local, visit_dependency, module_bindings)
        for child in node.else_:
            yield from _input_reads(child, dict(bindings), visit_dependency, module_bindings)
        return
    if isinstance(node, nodes.With):
        local = dict(bindings)
        for target, value in zip(node.targets, node.values, strict=True):
            yield from _input_reads(value, bindings, visit_dependency, module_bindings)
            _bind(target, _reference(value, bindings), local)
        for child in node.body:
            yield from _input_reads(child, local, visit_dependency, module_bindings)
        return
    if isinstance(node, (nodes.AssignBlock, nodes.FilterBlock)):
        local = dict(bindings)
        for child in node.body:
            yield from _input_reads(child, local, visit_dependency, module_bindings)
        if node.filter is not None:
            yield from _input_reads(node.filter, local, visit_dependency, module_bindings)
        if isinstance(node, nodes.AssignBlock):
            _bind(node.target, None, bindings)
        return
    if isinstance(node, nodes.Assign):
        yield from _input_reads(node.node, bindings, visit_dependency, module_bindings)
        _bind(node.target, _reference(node.node, bindings), bindings)
        return
    if isinstance(node, nodes.Call) and isinstance(node.node, nodes.Getattr):
        # A mapping method is not a schema property. Literal get() keys are reads.
        receiver = node.node.node
        parent = _reference(receiver, bindings)
        if parent is not None and node.node.attr == "get" and node.args:
            key = node.args[0]
            if isinstance(key, nodes.Const) and isinstance(key.value, str):
                yield _InputRead((*parent, key.value), node.lineno)
        yield from _input_reads(receiver, bindings, visit_dependency, module_bindings)
        for child in node.iter_child_nodes(exclude=("node",)):
            yield from _input_reads(child, bindings, visit_dependency, module_bindings)
        return
    if isinstance(node, nodes.Block):
        local = {**module_bindings, **bindings} if node.scoped else dict(module_bindings)
    else:
        local = dict(bindings) if isinstance(node, nodes.Scope) else bindings
    for child in node.iter_child_nodes():
        yield from _input_reads(child, local, visit_dependency, module_bindings)


def _declares_path(schema: JsonValue, path: InputPath) -> bool:
    """Find declarations in schema positions, retaining composed object boundaries.

    This does not evaluate assertions, flatten schemas or materialize defaults.
    """
    if not path:
        return True
    if isinstance(schema, bool):
        return schema
    if not isinstance(schema, dict):
        return False
    key, *rest = path
    candidates: list[JsonValue] = []
    properties = schema.get("properties", {})
    if isinstance(properties, dict):
        candidates.extend(value for name, value in properties.items() if key is None or name == key)
    patterns = schema.get("patternProperties", {})
    if isinstance(patterns, dict):
        candidates.extend(
            value
            for pattern, value in patterns.items()
            if key is None or isinstance(key, str) and re.search(pattern, key)
        )
    if (key is None or not candidates) and "additionalProperties" in schema:
        candidates.append(schema["additionalProperties"])
    if isinstance(key, int) or key is None:
        prefix = schema.get("prefixItems", [])
        if isinstance(prefix, list):
            candidates.extend(
                value for index, value in enumerate(prefix) if key is None or index == key
            )
            if "items" in schema and (key is None or key >= len(prefix)):
                candidates.append(schema["items"])
    if any(
        _declares_path(candidate, tuple(rest)) for candidate in candidates if candidate is not False
    ):
        return True
    for keyword in ("allOf", "anyOf", "oneOf"):
        branches = schema.get(keyword)
        if isinstance(branches, list) and any(_declares_path(branch, path) for branch in branches):
            return True
    for keyword in ("then", "else", "dependentSchemas"):
        branch = schema.get(keyword)
        if keyword == "dependentSchemas" and isinstance(branch, dict):
            if any(_declares_path(value, path) for value in branch.values()):
                return True
        elif isinstance(branch, (dict, bool)) and _declares_path(branch, path):
            return True
    return not schema
