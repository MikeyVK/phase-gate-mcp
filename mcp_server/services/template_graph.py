# mcp_server/services/template_graph.py
# template=service version=5d5b489a created=2026-09-13T15:49Z updated=
"""Prepare a static Jinja dependency graph from an explicitly supplied suite."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Literal, TypeAlias

from jinja2 import TemplateSyntaxError, nodes

from mcp_server.core.exceptions import MCPError

EdgeKind: TypeAlias = Literal["extends", "include", "import", "from_import"]
DependencyNode: TypeAlias = nodes.Extends | nodes.Include | nodes.Import | nodes.FromImport
_EDGE_KINDS: dict[type[DependencyNode], EdgeKind] = {
    nodes.Extends: "extends",
    nodes.Include: "include",
    nodes.Import: "import",
    nodes.FromImport: "from_import",
}


@dataclass(frozen=True)
class TemplateSource:
    """Exact admitted source bytes at a logical suite-relative name."""

    name: str
    content: bytes


@dataclass(frozen=True)
class TemplateEdge:
    """One parser-derived dependency, including its kind and source location."""

    source: str
    target: str
    kind: EdgeKind
    line: int


@dataclass(frozen=True)
class TemplateRoot:
    """A public manifest identity and its complete isolated source closure."""

    template_id: str
    template_name: str
    closure: tuple[str, ...]


@dataclass(frozen=True)
class TemplateGraph:
    """One immutable preparation result; consumers perform no filesystem lookup."""

    roots: tuple[TemplateRoot, ...]
    sources: tuple[TemplateSource, ...]
    edges: tuple[TemplateEdge, ...]


class TemplateGraphResolver:
    """Resolve literal dependencies using Jinja's default loader-root name semantics.

    The composition root supplies the parser. Preparation never invokes a renderer,
    executes an import or probes caller values. Private paths and shared/templates
    are admitted; suite metadata and shared schema definitions are not render sources.
    """

    def __init__(self, suite_root: Path, parse: Callable[[str, str], nodes.Template]) -> None:
        if not suite_root.is_absolute():
            raise _error("absolute_suite_root_required", "")
        self._suite_root = suite_root.resolve()
        self._parse = parse

    def resolve(self, entrypoints: Iterable[tuple[str, str]]) -> TemplateGraph:
        """Prepare every declared concrete entrypoint atomically and deterministically."""
        entries = tuple(entrypoints)
        self._validate_roots(entries)
        sources: dict[str, TemplateSource] = {}
        closures: dict[str, frozenset[str]] = {}
        edges: list[TemplateEdge] = []
        active: set[str] = set()

        def visit(name: str) -> frozenset[str]:
            if name in active:
                raise _error("template_dependency_cycle", name)
            if name in closures:
                return closures[name]
            active.add(name)
            try:
                path = self._path(name)
                content = path.read_bytes()
                tree = self._parse(content.decode("utf-8-sig"), name)
            except (OSError, UnicodeError) as exc:
                raise _error("template_source_unavailable", name) from exc
            except TemplateSyntaxError as exc:
                raise _error("template_syntax_invalid", name, line=exc.lineno) from exc
            sources[name] = TemplateSource(name, content)
            closure = {name}
            for edge in _dependencies(tree, name):
                self._validate_edge(edge)
                edges.append(edge)
                closure.update(visit(edge.target))
            active.remove(name)
            closures[name] = frozenset(closure)
            return closures[name]

        roots = tuple(
            TemplateRoot(template_id, name, tuple(sorted(visit(name))))
            for template_id, name in sorted(entries)
        )
        return TemplateGraph(
            roots,
            tuple(sources[name] for name in sorted(sources)),
            tuple(sorted(edges, key=lambda edge: (edge.source, edge.line, edge.kind, edge.target))),
        )

    def _validate_roots(self, entries: tuple[tuple[str, str], ...]) -> None:
        identities: set[str] = set()
        paths: set[Path] = set()
        for template_id, name in entries:
            parts = PurePosixPath(name).parts
            if len(parts) != 2 or parts[0] == "shared" or parts[-1] != "template.jinja2":
                raise _error("template_entrypoint_invalid", name)
            path = self._path(name)
            if template_id in identities or path in paths:
                raise _error("template_entrypoint_duplicate", name)
            identities.add(template_id)
            paths.add(path)

    def _path(self, name: str) -> Path:
        logical = PurePosixPath(name)
        if (
            not name
            or logical.is_absolute()
            or ".." in logical.parts
            or "\\" in name
            or ":" in name
            or "\x00" in name
        ):
            raise _error("template_path_invalid", name)
        self._owner(name)
        path = (self._suite_root / logical).resolve()
        if not path.is_relative_to(self._suite_root):
            raise _error("template_path_escape", name)
        if self._owner(path.relative_to(self._suite_root).as_posix()) != self._owner(name):
            raise _error("template_path_escape", name)
        return path

    @staticmethod
    def _owner(name: str) -> str:
        parts = PurePosixPath(name).parts
        if len(parts) < 2:
            raise _error("template_path_invalid", name)
        if parts[0] == "shared" and (len(parts) < 3 or parts[1] != "templates"):
            raise _error("template_path_invalid", name)
        if not name.endswith(".jinja2"):
            raise _error("template_path_invalid", name)
        return parts[0]

    def _validate_edge(self, edge: TemplateEdge) -> None:
        self._path(edge.target)
        source_owner = self._owner(edge.source)
        target_owner = self._owner(edge.target)
        if target_owner != source_owner and target_owner != "shared":
            raise _error(
                "template_dependency_direction", edge.source, target=edge.target, line=edge.line
            )


def _dependencies(tree: nodes.Template, source: str) -> tuple[TemplateEdge, ...]:
    dependencies = tuple(tree.find_all(tuple(_EDGE_KINDS)))
    if sum(isinstance(node, nodes.Extends) for node in dependencies) > 1:
        raise _error("template_renderer_ambiguous", source)
    result: list[TemplateEdge] = []
    for node in dependencies:
        if isinstance(node, nodes.Include) and node.ignore_missing:
            raise _error("template_dependency_optional", source, line=node.lineno)
        expression = node.template
        if isinstance(expression, (nodes.List, nodes.Tuple)):
            raise _error("template_dependency_ambiguous", source, line=node.lineno)
        if not isinstance(expression, nodes.Const) or not isinstance(expression.value, str):
            raise _error("template_dependency_dynamic", source, line=node.lineno)
        result.append(TemplateEdge(source, expression.value, _EDGE_KINDS[type(node)], node.lineno))
    return tuple(result)


def _error(
    key: str, template: str, *, target: str | None = None, line: int | None = None
) -> MCPError:
    return MCPError(
        key, code="ERR_CONFIG", params={"template": template, "target": target, "line": line}
    )
