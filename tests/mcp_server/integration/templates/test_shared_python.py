"""Native syntax and values from delivered shared sources in isolated consumers."""

from __future__ import annotations

import ast
import json
import keyword
from pathlib import Path
from shutil import copytree
from types import MappingProxyType

import pytest
from jinja2 import DictLoader, Environment, StrictUndefined
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError as ContextError
from pydantic import JsonValue

from mcp_server.config.validator import ConfigValidator
from mcp_server.core.interfaces.artifact_header_reader import HeaderReadStatus
from mcp_server.core.interfaces.template_catalog import thaw_json
from mcp_server.services.artifact_header_reader import ArtifactHeaderReader
from mcp_server.services.template_contract_loader import DRAFT_2020_12, TemplateContractLoader
from mcp_server.services.template_engine import TemplateEngine, register_template_filters
from mcp_server.services.template_graph import TemplateGraphResolver
from tests.mcp_server.integration.adapters.test_typescript_syntax import (
    TypeScriptPackage,
    invoke,
    typescript_package,
)

__all__ = ["typescript_package"]


def render(tmp_path: Path, repo: Path, template: str, content: dict[str, JsonValue]) -> str:
    suite = tmp_path / "arbitrary-suite"
    if not suite.exists():
        copytree(repo / ".pgmcp/template_suite/shared", suite / "shared")
    package = suite / "consumer"
    package.mkdir(exist_ok=True)
    (package / "template.jinja2").write_text(template, encoding="utf-8")
    parser = Environment()
    register_template_filters(parser)
    graph = TemplateGraphResolver(suite, parser.parse).resolve(
        (("custom.consumer", "consumer/template.jinja2"),)
    )
    environment = Environment(
        loader=DictLoader(
            MappingProxyType(
                {source.name: source.content.decode("utf-8") for source in graph.sources}
            )
        ),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    return TemplateEngine(environment=environment).render_context(
        "consumer/template.jinja2",
        {
            "content": content,
            "provenance": {
                "id": "custom.consumer",
                "pv": "1.0.0",
                "pf": "a" * 16,
                "sf": "b" * 16,
            },
        },
    )


def test_python_base_composes_fixed_and_caller_imports(
    tmp_path: Path,
    pytestconfig: pytest.Config,
) -> None:
    output = render(
        tmp_path,
        pytestconfig.rootpath,
        '{% extends "shared/templates/bases/tier2_python.jinja2" %}\n'
        '{% block module_imports %}{{ imports.groups(content.imports, {"stdlib": ['
        '{"kind":"import","module":"sys"}]}) }}{% endblock %}\n'
        "{% block code %}VALUE = 1{% endblock %}",
        {
            "description": 'Multiline 😀\nQuotes """ and \\ stay data.',
            "imports": {
                "stdlib": [
                    {"kind": "import", "module": "os", "alias": "operating"},
                ],
                "third_party": [
                    {
                        "kind": "from",
                        "module": "pydantic",
                        "names": [{"name": "BaseModel", "alias": "Model"}],
                    }
                ],
                "project": [
                    {"kind": "from", "module": ".contracts", "names": [{"name": "Item"}]},
                    {"kind": "from", "module": "__future__", "names": [{"name": "annotations"}]},
                ],
            },
        },
    )
    tree = ast.parse(output)
    assert ast.get_docstring(tree, clean=False) == 'Multiline 😀\nQuotes """ and \\ stay data.'
    assert isinstance(tree.body[1], ast.ImportFrom) and tree.body[1].module == "__future__"
    statements = [
        ast.unparse(node) for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))
    ]
    assert statements == [
        "from __future__ import annotations",
        "import os as operating",
        "import sys",
        "from pydantic import BaseModel as Model",
        "from .contracts import Item",
    ]
    assert "# Standard library" in output and "# Third party" in output and "# Project" in output
    assert "logger" not in output and "created=" not in output
    provenance = ArtifactHeaderReader().read(output)
    assert provenance.status is HeaderReadStatus.RECOGNIZED
    assert provenance.provenance is not None and provenance.provenance.id == "custom.consumer"


def test_shared_schema_is_consumed_without_redeclaring_records(
    tmp_path: Path,
    pytestconfig: pytest.Config,
) -> None:
    suite = tmp_path / "suite"
    copytree(pytestconfig.rootpath / ".pgmcp/template_suite/shared", suite / "shared")
    package = suite / "consumer"
    package.mkdir()
    schema_path = package / "context.schema.json"
    schema_path.write_text(
        json.dumps(
            {
                "$schema": DRAFT_2020_12,
                "$ref": "../shared/definitions/python.schema.json#/$defs/Imports",
            }
        ),
        encoding="utf-8",
    )
    loaded = TemplateContractLoader(suite).load_context_schema(schema_path)
    validate = ConfigValidator().validate_template_context
    value = {
        "stdlib": [
            {"kind": "import", "module": "os", "alias": "operating"},
            {"kind": "from", "module": ".relative", "names": [{"name": "*"}]},
        ]
    }
    assert thaw_json(validate(loaded, value)) == value
    for rejected in (
        {"unknown": []},
        {"stdlib": None},
        {"stdlib": [{"kind": "import", "module": "os; pass"}]},
        {"project": [{"kind": "from", "module": ".x", "names": [{"name": "*", "alias": "x"}]}]},
        {"project": [{"kind": "from", "module": ".x", "names": [{"name": "*"}, {"name": "x"}]}]},
    ):
        with pytest.raises(ContextError):
            validate(loaded, rejected)
    for definition, accepted, rejected in (
        (
            "ModelField",
            {"name": "value", "type": "object", "description": "Value", "default": None},
            {
                "name": "value",
                "type": "object",
                "description": "Value",
                "default": None,
                "default_factory": "dict",
            },
        ),
        (
            "Parameter",
            {"name": "value", "type": "bool", "default": False},
            {"name": "value", "type": "list", "default": []},
        ),
        (
            "Signature",
            {
                "name": "read",
                "description": "Read",
                "async": False,
                "parameters": [],
                "return_type": "None",
            },
            {
                "name": "class",
                "description": "Read",
                "async": False,
                "parameters": [],
                "return_type": "None",
            },
        ),
        (
            "TestCase",
            {
                "name": "test_read",
                "description": "Read",
                "async": True,
                "parameters": [],
                "body": "await read()",
            },
            {
                "name": "test_read",
                "description": "Read",
                "async": True,
                "parameters": [],
                "body": " ",
            },
        ),
        (
            "Fixture",
            {
                "name": "value",
                "description": "Value",
                "async": False,
                "parameters": [],
                "return_type": "int",
                "body": "return 0",
                "decorator": "pytest.fixture",
                "autouse": False,
            },
            {
                "name": "value",
                "description": "Value",
                "async": False,
                "parameters": [],
                "return_type": "int",
                "body": "return 0",
                "decorator": "pytest.fixture",
                "autouse": None,
            },
        ),
    ):
        schema_path.write_text(
            json.dumps(
                {
                    "$schema": DRAFT_2020_12,
                    "$ref": f"../shared/definitions/python.schema.json#/$defs/{definition}",
                }
            ),
            encoding="utf-8",
        )
        selected = TemplateContractLoader(suite).load_context_schema(schema_path)
        assert thaw_json(validate(selected, accepted)) == accepted
        with pytest.raises(ContextError):
            validate(selected, rejected)

    schema_path.write_text(
        json.dumps(
            {
                "$schema": DRAFT_2020_12,
                "$ref": "../shared/definitions/python.schema.json#/$defs/Symbol",
            }
        ),
        encoding="utf-8",
    )
    symbol_schema = TemplateContractLoader(suite).load_context_schema(schema_path)
    # Native lexical facts, not a duplicated regex oracle.
    validator = Draft202012Validator(thaw_json(symbol_schema))
    for name in ("a²", "cafe\u0301", "plain_name", "class"):
        assert validator.is_valid(name) == (name.isidentifier() and not keyword.iskeyword(name))


@pytest.mark.parametrize("populated", [False, True])
def test_pydantic_literals_order_and_configuration_without_model_execution(
    tmp_path: Path,
    pytestconfig: pytest.Config,
    populated: bool,
) -> None:
    supplied = [False, 0, None, 'quotes 😀 " and \\', [False, {"zero": 0}], {"key": None}]
    fields: list[JsonValue] = []
    if populated:
        for index, value in enumerate(supplied):
            fields.append(
                {
                    "name": f"value_{index}",
                    "type": "object",
                    "description": f"Field {index}",
                    "default": value,
                }
            )
        fields.append(
            {
                "name": "factory",
                "type": "dict",
                "description": "Fresh mapping",
                "default_factory": "dict",
                "min_length": 0,
            }
        )
    output = render(
        tmp_path,
        pytestconfig.rootpath,
        '{% extends "shared/templates/bases/tier2_python.jinja2" %}\n'
        '{% import "shared/templates/patterns/python/pydantic.jinja2" as model %}\n'
        "{% block module_imports %}{{ imports.groups(content.imports | default({}), "
        '{"third_party": [{"kind":"from","module":"pydantic","names": ['
        '{"name":"BaseModel"},{"name":"ConfigDict"},{"name":"Field"}]}]}) }}{% endblock %}\n'
        "{% block code %}class Example(BaseModel):\n"
        "    {{ imports.documentation(content.description) }}\n"
        "    {{ model.model_config(content.frozen, content.examples) }}\n"
        "{{ model.fields(content.fields) | indent(4, true) }}\n"
        "{% endblock %}",
        {
            "description": "Example model",
            "fields": fields,
            "frozen": populated,
            "examples": [{"does_not_match_fields": [False, 0, None]}] if populated else [],
        },
    )
    tree = ast.parse(output)
    compile(tree, "<generated-model>", "exec")
    model_class = next(node for node in tree.body if isinstance(node, ast.ClassDef))
    assert model_class.name == "Example"
    config = next(node for node in model_class.body if isinstance(node, ast.Assign))
    assert isinstance(config.value, ast.Call)
    options = {item.arg: ast.literal_eval(item.value) for item in config.value.keywords}
    assert options["extra"] == "forbid" and options["frozen"] == populated
    assert ("json_schema_extra" in options) == populated
    emitted = [node for node in model_class.body if isinstance(node, ast.AnnAssign)]
    assert len(emitted) == len(fields)
    for index, (node, expected) in enumerate(zip(emitted, supplied, strict=False)):
        assert isinstance(node.target, ast.Name) and node.target.id == f"value_{index}"
        assert isinstance(node.value, ast.Call)
        values = {item.arg: ast.literal_eval(item.value) for item in node.value.keywords}
        assert values == {"default": expected, "description": f"Field {index}"}
    if populated:
        factory = emitted[-1].value
        assert isinstance(factory, ast.Call)
        reference = next(item.value for item in factory.keywords if item.arg == "default_factory")
        assert isinstance(reference, ast.Name) and reference.id == "dict"
    assert "validator" not in output and "getLogger" not in output


@pytest.mark.parametrize("protocol", [False, True])
def test_shared_signatures_keep_order_defaults_and_explicit_stub_behavior(
    tmp_path: Path,
    pytestconfig: pytest.Config,
    protocol: bool,
) -> None:
    output = render(
        tmp_path,
        pytestconfig.rootpath,
        '{% extends "shared/templates/bases/tier2_python.jinja2" %}\n'
        '{% import "shared/templates/patterns/python/signatures.jinja2" as signatures %}\n'
        "{% block code %}class Reader:\n"
        "{{ signatures.method(content.signature, content.stub) | indent(4, true) }}\n"
        "{% endblock %}",
        {
            "description": "Explicit method",
            "stub": "..." if protocol else "raise NotImplementedError",
            "signature": {
                "name": "read",
                "description": "Read supplied input.",
                "async": True,
                "parameters": [
                    {"name": "value", "type": "int"},
                    {"name": "enabled", "type": "bool", "default": False},
                    {"name": "label", "type": "str | None", "default": None},
                ],
                "return_type": "str",
            },
        },
    )
    tree = ast.parse(output)
    compile(tree, "<generated-signature>", "exec")
    cls = next(node for node in tree.body if isinstance(node, ast.ClassDef))
    method = cls.body[0]
    assert isinstance(method, ast.AsyncFunctionDef) and method.name == "read"
    assert [argument.arg for argument in method.args.args] == ["self", "value", "enabled", "label"]
    assert [ast.literal_eval(default) for default in method.args.defaults] == [False, None]
    assert ast.unparse(method.returns) == "str"
    assert isinstance(method.body[-1], ast.Expr if protocol else ast.Raise)
    assert len(method.body) == 2 and "import asyncio" not in output and "logger" not in output


def test_explicit_pytest_bodies_fixtures_and_markers_are_not_inferred(
    tmp_path: Path,
    pytestconfig: pytest.Config,
) -> None:
    output = render(
        tmp_path,
        pytestconfig.rootpath,
        '{% extends "shared/templates/bases/tier2_python.jinja2" %}\n'
        '{% import "shared/templates/patterns/testing/pytest.jinja2" as tests %}\n'
        "{% block code %}{{ tests.module_markers(content.markers) }}\n"
        "{{ tests.fixture(content.fixture) }}\n"
        "{{ tests.cases(content.cases, content.class_name) }}\n{% endblock %}",
        {
            "description": "Caller-owned testing",
            "imports": {"third_party": [{"kind": "import", "module": "pytest"}]},
            "markers": ["pytest.mark.integration"],
            "class_name": "TestReader",
            "fixture": {
                "name": "item",
                "description": "Produce item.",
                "async": False,
                "parameters": [],
                "return_type": "int",
                "body": "return 0",
                "decorator": "pytest.fixture",
                "autouse": False,
            },
            "cases": [
                {
                    "name": "test_read",
                    "description": "Await explicit reader.",
                    "async": True,
                    "parameters": [{"name": "item", "type": "int"}],
                    "body": "result = await read(item)\nassert result == item",
                    "markers": [],
                }
            ],
        },
    )
    tree = ast.parse(output)
    compile(tree, "<generated-pytest>", "exec")
    fixture = next(node for node in tree.body if isinstance(node, ast.FunctionDef))
    assert fixture.name == "item" and ast.get_docstring(fixture) == "Produce item."
    decorator = fixture.decorator_list[0]
    assert isinstance(decorator, ast.Call)
    assert ast.unparse(decorator.func) == "pytest.fixture"
    assert [(item.arg, ast.literal_eval(item.value)) for item in decorator.keywords] == [
        ("autouse", False)
    ]
    cls = next(node for node in tree.body if isinstance(node, ast.ClassDef))
    case = cls.body[0]
    assert isinstance(case, ast.AsyncFunctionDef) and not case.decorator_list
    assert [argument.arg for argument in case.args.args] == ["self", "item"]
    assert [ast.unparse(node) for node in case.body[1:]] == [
        "result = await read(item)",
        "assert result == item",
    ]
    assert "mark.asyncio" not in output and "import asyncio" not in output
    assert "tmp_path" not in output and "MagicMock" not in output and "TDD" not in output


def test_logging_is_explicit_and_quoted(
    tmp_path: Path,
    pytestconfig: pytest.Config,
) -> None:
    for index, selected in enumerate((None, {}, {"name": 'name " \\'})):
        output = render(
            tmp_path / str(index),
            pytestconfig.rootpath,
            '{% extends "shared/templates/bases/tier2_python.jinja2" %}\n'
            '{% import "shared/templates/patterns/python/logging.jinja2" as logging_pattern %}\n'
            '{% block module_imports %}{{ imports.groups({}, {"stdlib": '
            '[{"kind":"import","module":"logging"}]} if content.logging is defined else {}) }}'
            "{% endblock %}\n"
            "{% block code %}{% if content.logging is defined %}"
            "{{ logging_pattern.logger(content.logging) }}{% endif %}\nVALUE = 1{% endblock %}",
            {
                "description": "Explicit logging",
                **({"logging": selected} if selected is not None else {}),
            },
        )
        tree = ast.parse(output)
        assert ("import logging" in output) == (selected is not None)
        calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
        if selected is None:
            assert not calls
        elif not selected:
            assert isinstance(calls[0].args[0], ast.Name) and calls[0].args[0].id == "__name__"
        else:
            assert ast.literal_eval(calls[0].args[0]) == selected["name"]


def test_typescript_frame_preserves_native_imports_and_safe_documentation(
    tmp_path: Path,
    pytestconfig: pytest.Config,
    typescript_package: TypeScriptPackage,
) -> None:
    output = render(
        tmp_path / "rendered",
        pytestconfig.rootpath,
        '{% extends "shared/templates/bases/tier2_typescript.jinja2" %}\n'
        "{% block code %}export const value = 1;{% endblock %}",
        {
            "description": "Multiline 😀\nclose */ stays a comment.\tBackslash \\",
            "imports": ["import type { Item } from './contracts';"],
        },
    )
    assert "import type { Item } from './contracts';" in output
    assert output.count("*/") == 1
    code, response = invoke(
        typescript_package,
        typescript_package.workspace,
        {
            "operation": "syntax",
            "target_path": str(typescript_package.workspace / "example.ts"),
            "content": output,
            "args": [],
        },
    )
    assert code == 0 and response["decision"] == {"status": "passed"}
    provenance = ArtifactHeaderReader().read(output)
    assert provenance.status is HeaderReadStatus.RECOGNIZED
    assert provenance.provenance is not None and provenance.provenance.id == "custom.consumer"
