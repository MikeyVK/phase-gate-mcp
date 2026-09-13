# mcp_server/services/template_graph.py
# template=service version=5d5b489a created=2026-09-13T15:49Z updated=
"""Prepare a static Jinja dependency graph from an explicitly supplied suite."""

from collections.abc import Callable, Iterable
from pathlib import Path

from jinja2 import nodes


class TemplateGraphResolver:
    """Resolve literal Jinja dependencies before publishing a runtime catalog."""

    def __init__(self, suite_root: Path, parse: Callable[[str, str], nodes.Template]) -> None:
        self._suite_root = suite_root
        self._parse = parse

    def resolve(self, entrypoints: Iterable[tuple[str, str]]) -> object:
        """Prepare all declared roots atomically."""
        raise NotImplementedError("template_graph_preparation")
