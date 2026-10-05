"""Native syntax and values from delivered shared sources in isolated consumers."""

from __future__ import annotations

import ast
import json
import keyword
from copy import deepcopy
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
from tests.mcp_server.fixtures.delivered_templates import load_delivered_template
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
        "{% block module_documentation %}{{ imports.documentation(content.description) }}"
        "{% endblock %}\n"
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
    for name in (
        "_",
        "_private9",
        "A9",
        "plain_name",
        "match",
        "case",
        "type",
        "",
        "9name",
        "a-b",
        "a.b",
        "name ",
        " name",
        "name\n",
        "name\r",
        "name\nsuffix",
        "a²",
        "café",
        "cafe\u0301",
        "Ｆｏｏ",
        "K",
        "雪",
        "𐐀",
        *keyword.kwlist,
    ):
        assert validator.is_valid(name) == (
            name.isascii() and name.isidentifier() and not keyword.iskeyword(name)
        ), name


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
        "{% block module_documentation %}{{ imports.documentation(content.description) }}"
        "{% endblock %}\n"
        '{% import "shared/templates/patterns/python/pydantic.jinja2" as model %}\n'
        "{% block module_imports %}{{ imports.groups(content.imports | default({}), "
        '{"third_party": [{"kind":"from","module":"pydantic","names": ['
        '{"name":"BaseModel"},{"name":"ConfigDict"},{"name":"Field"}]}]}) }}{% endblock %}\n'
        "{% block code %}class Example(BaseModel):\n"
        "    {{ imports.documentation(content.description) }}\n"
        "{{ imports.indented(model.model_config(content.frozen, content.examples), 4) }}\n"
        "{{ imports.indented(model.fields(content.fields), 4) }}\n"
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
        "{% block module_documentation %}{{ imports.documentation(content.description) }}"
        "{% endblock %}\n"
        '{% import "shared/templates/patterns/python/signatures.jinja2" as signatures %}\n'
        "{% block code %}class Reader:\n"
        "{{ imports.indented(signatures.method(content.signature, content.stub), 4) }}\n"
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
        "{% block module_documentation %}{{ imports.documentation(content.description) }}"
        "{% endblock %}\n"
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
            "{% block module_documentation %}{{ imports.documentation(content.description) }}"
            "{% endblock %}\n"
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
        "{% block module_documentation %}/**\n{{ content.description "
        "| text_block "
        "| replace('\\\\', '\\\\\\\\') "
        "| replace('*/', '*\\\\/') "
        "| replace('\\r', '\\\\r') "
        "| replace('\\t', '\\\\t') "
        "| replace('\\x00', '\\\\0') "
        "| indent(' * ', true) }}\n */{% endblock %}\n"
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


@pytest.mark.parametrize(
    "definition, accepted, rejected",
    [
        (
            "DottedSymbol",
            ["module", "_pkg.mod_9", "match.case.type"],
            [
                "",
                ".pkg",
                "pkg.",
                "pkg..mod",
                "pkg.class",
                "class.pkg",
                "pkg.雪",
                "café.pkg",
                "pkg\n",
                "pkg.mod\nsuffix",
            ],
        ),
        (
            "ImportedName",
            [{"name": "_Name9", "alias": "local_9"}],
            [{"name": "雪"}, {"name": "Item", "alias": "café"}, {"name": "class"}, {"name": "*"}],
        ),
        (
            "FromImport",
            [
                {"kind": "from", "module": module, "names": [{"name": "Item", "alias": "Local9"}]}
                for module in (".", "...", ".pkg", "..pkg.mod_9", "pkg.mod")
            ]
            + [{"kind": "from", "module": ".pkg", "names": [{"name": "*"}]}],
            [
                {"kind": "from", "module": module, "names": [{"name": "Item"}]}
                for module in (
                    "",
                    ".pkg.",
                    "pkg..mod",
                    ".class.mod",
                    "..pkg.class",
                    ".雪",
                    ".pkg\n",
                )
            ]
            + [
                {"kind": "from", "module": "pkg", "names": [{"name": "Item", "alias": "雪"}]},
                {"kind": "from", "module": "pkg", "names": [{"name": "café"}]},
                {"kind": "from", "module": "pkg", "names": [{"name": "*", "alias": "all_items"}]},
                {"kind": "from", "module": "pkg", "names": [{"name": "*"}, {"name": "Item"}]},
            ],
        ),
        (
            "ImportStatement",
            [{"kind": "import", "module": "_pkg.mod9", "alias": "_local9"}],
            [
                {"kind": "import", "module": ".relative"},
                {"kind": "import", "module": "pkg.雪"},
                {"kind": "import", "module": "pkg", "alias": "Ｆｏｏ"},
                {"kind": "import", "module": "pkg.class"},
            ],
        ),
        (
            "ModelField",
            [
                {
                    "name": name,
                    "type": "list[雪]",
                    "description": "café 雪",
                    "default": {"雪": ["café", "🌍"]},
                }
                for name in ("value_9", "model_dump_custom", "ConfigDict", "BaseModel")
            ]
            + [
                {
                    "name": "value",
                    "type": "object",
                    "description": "café",
                    "default_factory": "_pkg.factory9",
                }
            ],
            [
                {"name": name, "type": "str", "description": "Value"}
                for name in (
                    "_private",
                    "model_config",
                    "Config",
                    "Field",
                    "model_dump",
                    "model_dump_json",
                    "model_validate",
                    "model_validate_json",
                    "model_validate_strings",
                    "value_雪",
                    "Ｆｉｅｌｄ",
                    "Conﬁg",
                )
            ]
            + [
                {"name": "value", "type": "object", "description": "Value", "default_factory": name}
                for name in ("pkg.雪", "factory()", "pkg.class", ".factory", "factory\n")
            ],
        ),
        (
            "InstanceParameter",
            [{"name": "self_9", "type": "雪", "default": "café"}],
            [{"name": name, "type": "object"} for name in ("self", "ｓｅｌｆ", "雪", "value\n")],
        ),
        (
            "Signature",
            [
                {
                    "name": "read_9",
                    "description": "café 雪",
                    "async": False,
                    "parameters": [{"name": "_value9", "type": "雪", "default": "🌍"}],
                    "return_type": "list[雪]",
                }
            ],
            [
                {
                    "name": name,
                    "description": "Read",
                    "async": False,
                    "parameters": [],
                    "return_type": "None",
                }
                for name in ("read_雪", "class", "read\n")
            ]
            + [
                {
                    "name": "read",
                    "description": "Read",
                    "async": False,
                    "parameters": [{"name": "雪", "type": "object"}],
                    "return_type": "None",
                }
            ],
        ),
        (
            "NonConstructorMethod",
            [
                {
                    "name": "__call__",
                    "description": "café",
                    "async": False,
                    "parameters": [],
                    "return_type": "str",
                    "body": "雪 = 'café'\nreturn 雪",
                }
            ],
            [
                {
                    "name": name,
                    "description": "Read",
                    "async": False,
                    "parameters": [],
                    "return_type": "None",
                    "body": "pass",
                }
                for name in ("__init__", "_＿ｉｎｉｔ__", "read_雪")
            ],
        ),
        (
            "TestCase",
            [
                {
                    "name": "test_value_9",
                    "description": "café",
                    "async": False,
                    "parameters": [],
                    "body": "雪 = '🌍'\nassert 雪 == '🌍'",
                    "markers": ["pytest.mark.reason('café')"],
                }
            ],
            [
                {
                    "name": name,
                    "description": "Check",
                    "async": False,
                    "parameters": [],
                    "body": "assert True",
                }
                for name in ("check_value", "test_雪", "test_value\n")
            ],
        ),
        (
            "PytestClassName",
            ["Test", "Test_9", "Testcase"],
            ["testCase", "Examples", "Test雪", "ＴｅｓｔCases", "Test\u0300\u0307Cases", "Test\n"],
        ),
        (
            "Fixture",
            [
                {
                    "name": "_value9",
                    "description": "café",
                    "async": False,
                    "parameters": [],
                    "return_type": "雪",
                    "body": "return '🌍'",
                    "decorator": "_pkg.fixture9",
                }
            ],
            [
                {
                    "name": name,
                    "description": "Value",
                    "async": False,
                    "parameters": [],
                    "return_type": "str",
                    "body": "return ''",
                    "decorator": "pytest.fixture",
                }
                for name in ("雪", "value\n")
            ]
            + [
                {
                    "name": "value",
                    "description": "Value",
                    "async": False,
                    "parameters": [],
                    "return_type": "str",
                    "body": "return ''",
                    "decorator": name,
                }
                for name in ("pkg.雪", "pytest.class", "factory()")
            ],
        ),
        ("Text", ["café 雪 🌍"], [""]),
        ("Prose", ["", "café 雪 🌍"], []),
        ("TypeText", ["list[雪]", "Annotated[str, 'café']"], [""]),
        ("Body", ["雪 = '🌍'\nreturn 雪"], [" \n\t"]),
        ("JSONScalar", ["café 雪 🌍", None, False, 0], [[]]),
    ],
)
def test_shared_ascii_contracts(
    tmp_path: Path,
    pytestconfig: pytest.Config,
    definition: str,
    accepted: list[JsonValue],
    rejected: list[JsonValue],
) -> None:
    suite = tmp_path / "suite"
    copytree(pytestconfig.rootpath / ".pgmcp/template_suite/shared", suite / "shared")
    consumer = suite / "consumer"
    consumer.mkdir()
    schema_path = consumer / "context.schema.json"
    schema_path.write_text(
        json.dumps(
            {
                "$schema": DRAFT_2020_12,
                "$ref": f"../shared/definitions/python.schema.json#/$defs/{definition}",
            }
        ),
        encoding="utf-8",
    )
    schema = TemplateContractLoader(suite).load_context_schema(schema_path)
    validator = Draft202012Validator(thaw_json(schema))
    for value in accepted:
        validator.validate(value)
    for value in rejected:
        assert not validator.is_valid(value), (definition, value)


@pytest.mark.parametrize(
    "template_id, context",
    [
        (
            "python_class",
            {
                "class_name": "_Reader9",
                "class_description": "café 雪",
                "module_description": "🌍 café",
                "bases": ["雪"],
                "methods": [
                    {
                        "name": "_read9",
                        "description": "café",
                        "async": False,
                        "parameters": [{"name": "_value9", "type": "雪", "default": "🌍"}],
                        "return_type": "list[雪]",
                    }
                ],
            },
        ),
        (
            "python_protocol",
            {
                "class_name": "_Reader9",
                "class_description": "café 雪",
                "module_description": "🌍 café",
                "bases": ["雪"],
                "methods": [
                    {
                        "name": "_read9",
                        "description": "café",
                        "async": False,
                        "parameters": [{"name": "_value9", "type": "雪", "default": "🌍"}],
                        "return_type": "list[雪]",
                    }
                ],
            },
        ),
        (
            "python_adapter",
            {
                "class_name": "_Reader9",
                "class_description": "café 雪",
                "module_description": "🌍 café",
                "methods": [
                    {
                        "name": "_read9",
                        "description": "café",
                        "async": False,
                        "parameters": [{"name": "_value9", "type": "雪", "default": "🌍"}],
                        "return_type": "str",
                        "body": "雪 = '🌍'\nreturn 雪",
                    }
                ],
            },
        ),
        (
            "python_worker",
            {
                "class_name": "_Reader9",
                "class_description": "café 雪",
                "module_description": "🌍 café",
                "logging": {"name": "café 雪"},
                "operation": {
                    "name": "_read9",
                    "description": "café",
                    "async": False,
                    "parameters": [{"name": "_value9", "type": "雪", "default": "🌍"}],
                    "return_type": "str",
                    "body": "雪 = '🌍'\nreturn 雪",
                },
            },
        ),
        (
            "python_pydantic_dto",
            {
                "class_name": "_Reader9",
                "class_description": "café 雪",
                "module_description": "🌍 café",
                "fields": [
                    {"name": "value_9", "type": "str", "description": "café 雪", "default": "🌍"}
                ],
                "examples": [{"value_9": "🌍", "雪": "café"}],
            },
        ),
        (
            "python_pydantic_config",
            {
                "frozen": True,
                "examples": [{"value_9": "🌍", "雪": "café"}],
                "class_name": "_Reader9",
                "class_description": "café 雪",
                "module_description": "🌍 café",
                "fields": [
                    {"name": "value_9", "type": "str", "description": "café 雪", "default": "🌍"}
                ],
            },
        ),
        (
            "pytest_unit_test",
            {
                "class_name": "TestASCII9",
                "description": "🌍 café 雪",
                "cases": [
                    {
                        "name": "test_value9",
                        "description": "café",
                        "async": False,
                        "parameters": [],
                        "body": "雪 = '🌍'\nassert 雪 == '🌍'",
                    }
                ],
                "fixtures": [
                    {
                        "name": "_value9",
                        "description": "café",
                        "async": False,
                        "parameters": [],
                        "return_type": "雪",
                        "body": "return '🌍'",
                        "decorator": "pytest.fixture",
                    }
                ],
            },
        ),
        (
            "pytest_integration_test",
            {
                "class_name": "TestASCII9",
                "description": "🌍 café 雪",
                "cases": [
                    {
                        "name": "test_value9",
                        "description": "café",
                        "async": False,
                        "parameters": [],
                        "body": "雪 = '🌍'\nassert 雪 == '🌍'",
                    }
                ],
                "fixtures": [
                    {
                        "name": "_value9",
                        "description": "café",
                        "async": False,
                        "parameters": [],
                        "return_type": "雪",
                        "body": "return '🌍'",
                        "decorator": "pytest.fixture",
                    }
                ],
            },
        ),
    ],
)
def test_shipped_python_ascii(
    tmp_path: Path,
    pytestconfig: pytest.Config,
    template_id: str,
    context: dict[str, JsonValue],
) -> None:
    suite = pytestconfig.rootpath / ".pgmcp/template_suite"
    delivered = load_delivered_template(
        source_suite=suite,
        source_package=suite / template_id,
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "isolated suite",
        template_id=template_id,
    )
    supplied = deepcopy(context)
    supplied["imports"] = {
        "project": [
            {
                "kind": "from",
                "module": "..pkg.mod_9",
                "names": [{"name": "Item9", "alias": "_Local9"}],
            },
        ]
    }
    before = deepcopy(supplied)
    output = delivered.renderer.render(template_id, supplied, delivered.provenance)
    tree = ast.parse(output)
    compile(tree, "<ascii-contract>", "exec")
    assert supplied == before
    assert ast.get_docstring(tree, clean=False) == context.get(
        "module_description", context.get("description")
    )
    assert "café" in output and "雪" in output and "🌍" in output
    declaration = next(node for node in tree.body if isinstance(node, ast.ClassDef))
    assert declaration.name == context["class_name"]
    for spelling in ("café", "Ｆｏｏ", "Name\u0301", "雪", "𐐀", "Valid\n"):
        with pytest.raises(ContextError):
            delivered.renderer.render(
                template_id, {**supplied, "class_name": spelling}, delivered.provenance
            )
    for statement in (
        {"kind": "import", "module": "pkg.雪"},
        {"kind": "import", "module": "pkg", "alias": "café"},
        {"kind": "from", "module": ".pkg", "names": [{"name": "雪"}]},
    ):
        with pytest.raises(ContextError):
            delivered.renderer.render(
                template_id,
                {**supplied, "imports": {"project": [statement]}},
                delivered.provenance,
            )


@pytest.mark.parametrize(
    "template_id",
    [
        "python_class",
        "python_protocol",
        "python_adapter",
        "python_worker",
        "python_pydantic_dto",
        "python_pydantic_config",
        "pytest_unit_test",
        "pytest_integration_test",
    ],
)
def test_shipped_python_ascii_schema_payload_is_bounded(
    pytestconfig: pytest.Config,
    template_id: str,
) -> None:
    suite = pytestconfig.rootpath / ".pgmcp/template_suite"
    schema = TemplateContractLoader(suite).load_context_schema(
        suite / template_id / "context.schema.json"
    )
    # Same JSON resource spelling as discovery; Python len counts Unicode codepoints.
    payload = json.dumps(thaw_json(schema), ensure_ascii=False)
    assert len(payload) < 25_000, (template_id, len(payload))
