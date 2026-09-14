"""Native syntax and values from delivered shared sources in isolated consumers."""

from __future__ import annotations

import ast
from pathlib import Path
from shutil import copytree
from types import MappingProxyType

import pytest
from jinja2 import DictLoader, Environment, StrictUndefined
from pydantic import JsonValue

from mcp_server.services.template_engine import TemplateEngine
from mcp_server.services.template_graph import TemplateGraphResolver


def render(
    tmp_path: Path, repo: Path, template: str, content: dict[str, JsonValue]
) -> str:
    suite = tmp_path / "arbitrary-suite"
    if not suite.exists():
        copytree(repo / ".pgmcp/template_suite/shared", suite / "shared")
    package = suite / "consumer"
    package.mkdir(exist_ok=True)
    (package / "template.jinja2").write_text(template, encoding="utf-8")
    parser = Environment()
    graph = TemplateGraphResolver(suite, parser.parse).resolve(
        (("custom.consumer", "consumer/template.jinja2"),)
    )
    environment = Environment(
        loader=DictLoader(MappingProxyType({
            source.name: source.content.decode("utf-8") for source in graph.sources
        })),
        undefined=StrictUndefined, keep_trailing_newline=True,
    )
    return TemplateEngine(environment=environment).render_context(
        "consumer/template.jinja2",
        {"content": content, "provenance": {
            "id": "custom.consumer", "pv": "1.0.0", "pf": "a" * 16, "sf": "b" * 16,
        }},
    )


def test_python_base_composes_fixed_and_caller_imports(
    tmp_path: Path, pytestconfig: pytest.Config,
) -> None:
    output = render(
        tmp_path, pytestconfig.rootpath,
        '{% extends "shared/templates/bases/tier2_python.jinja2" %}\n'
        '{% block module_imports %}{{ imports.groups(content.imports, {"stdlib": ['
        '{"kind":"import","module":"sys"}]}) }}{% endblock %}\n'
        '{% block code %}VALUE = 1{% endblock %}',
        {"description": 'Multiline\nQuotes """ and \\ stay data.',
         "imports": {
             "stdlib": [
                 {"kind": "import", "module": "os", "alias": "operating"},
                 {"kind": "from", "module": "__future__", "names": [{"name": "annotations"}]},
             ],
             "third_party": [{"kind": "from", "module": "pydantic",
                              "names": [{"name": "BaseModel", "alias": "Model"}]}],
             "project": [{"kind": "from", "module": ".contracts", "names": [{"name": "Item"}]}],
         }},
    )
    tree = ast.parse(output)
    assert ast.get_docstring(tree, clean=False) == 'Multiline\nQuotes """ and \\ stay data.'
    assert isinstance(tree.body[1], ast.ImportFrom) and tree.body[1].module == "__future__"
    statements = [ast.unparse(node) for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
    assert statements == [
        "from __future__ import annotations", "import os as operating", "import sys",
        "from pydantic import BaseModel as Model", "from .contracts import Item",
    ]
    assert "# Standard library" in output and "# Third party" in output and "# Project" in output
    assert "logger" not in output and "created=" not in output
