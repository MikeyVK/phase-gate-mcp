"""Observe the delivered plain class through real catalog and native Python syntax."""

from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema.exceptions import ValidationError as ContextError
from pydantic import JsonValue

from mcp_server.core.interfaces.artifact_header_reader import HeaderReadStatus
from mcp_server.services.artifact_header_reader import ArtifactHeaderReader
from tests.mcp_server.fixtures.delivered_templates import DeliveredTemplate, load_delivered_template
from tests.mcp_server.integration.adapters.test_python_syntax import (
    SyntaxPackage,
    invoke,
    request,
    syntax_package,
)

__all__ = ["syntax_package"]


@pytest.fixture
def delivered_class(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredTemplate:
    source = pytestconfig.rootpath / ".pgmcp/template_suite"
    delivered = load_delivered_template(
        source_suite=source,
        source_package=source / "python_class",
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "explicit suite",
        template_id="python_class",
    )
    selected = delivered.catalog.get("python_class")
    assert selected.policy.persistence == "workspace"
    assert dict(delivered.checks.profiles)[selected.policy.output_profile].checks == (
        "python_syntax",
    )
    return delivered


def parse_class(output: str) -> tuple[ast.Module, ast.ClassDef]:
    tree = ast.parse(output)
    compile(tree, "<delivered-class>", "exec")
    classes = [item for item in tree.body if isinstance(item, ast.ClassDef)]
    assert len(classes) == 1
    return tree, classes[0]


def test_empty_class_keeps_identity_documentation_and_no_hidden_behavior(
    delivered_class: DeliveredTemplate, syntax_package: SyntaxPackage, tmp_path: Path
) -> None:
    context = {
        "class_name": "exact_name",
        "class_description": "Explicit empty class.",
        "module_description": "Explicit empty class.",
    }
    output = delivered_class.renderer.render("python_class", context, delivered_class.provenance)
    tree, cls = parse_class(output)
    assert cls.name == "exact_name" and cls.bases == []
    assert ast.get_docstring(tree) == ast.get_docstring(cls) == context["class_description"]
    assert len(cls.body) == 2 and isinstance(cls.body[-1], ast.Pass)
    assert not any(isinstance(item, (ast.Import, ast.ImportFrom)) for item in tree.body)
    header = ArtifactHeaderReader().read(output)
    assert header.status is HeaderReadStatus.RECOGNIZED
    assert header.provenance is not None and header.provenance.id == "python_class"
    code, response = invoke(syntax_package, tmp_path, request(tmp_path / "class.py", output))
    assert code == 0 and response["decision"] == {"status": "passed"}
    assert not (tmp_path / "class.py").exists()


def test_explicit_bases_imports_and_ordered_sync_async_signatures(
    delivered_class: DeliveredTemplate, syntax_package: SyntaxPackage, tmp_path: Path
) -> None:
    context: dict[str, JsonValue] = {
        "class_name": "exact_reader",
        "class_description": 'Class "description" 😀\nnext line',
        "module_description": "Separate module prose",
        "imports": {
            "project": [
                {
                    "kind": "from",
                    "module": "absent_dependency",
                    "names": [{"name": "BaseA"}, {"name": "BaseB", "alias": "SecondBase"}],
                },
            ]
        },
        "bases": ["BaseA", "SecondBase"],
        "methods": [
            {
                "name": "read",
                "description": "Read input",
                "async": False,
                "parameters": [
                    {"name": "value", "type": "int"},
                    {"name": "enabled", "type": "bool", "default": False},
                    {"name": "offset", "type": "int", "default": 0},
                ],
                "return_type": "str",
            },
            {
                "name": "fetch",
                "description": "Fetch input",
                "async": True,
                "parameters": [
                    {"name": "label", "type": "str | None", "default": None},
                ],
                "return_type": "str | None",
            },
        ],
    }
    before = deepcopy(context)
    output = delivered_class.renderer.render("python_class", context, delivered_class.provenance)
    tree, cls = parse_class(output)
    assert context == before
    assert cls.name == "exact_reader" and [ast.unparse(base) for base in cls.bases] == [
        "BaseA",
        "SecondBase",
    ]
    assert ast.get_docstring(tree) == context["module_description"]
    assert ast.get_docstring(cls) == context["class_description"]
    imports = [item for item in tree.body if isinstance(item, ast.ImportFrom)]
    assert len(imports) == 1 and imports[0].module == "absent_dependency"
    assert [(item.name, item.asname) for item in imports[0].names] == [
        ("BaseA", None),
        ("BaseB", "SecondBase"),
    ]
    methods = [
        item for item in cls.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    assert [item.name for item in methods] == ["read", "fetch"]
    assert isinstance(methods[0], ast.FunctionDef)
    assert isinstance(methods[1], ast.AsyncFunctionDef)
    assert [arg.arg for arg in methods[0].args.args] == ["self", "value", "enabled", "offset"]
    assert [ast.literal_eval(value) for value in methods[0].args.defaults] == [False, 0]
    assert [arg.arg for arg in methods[1].args.args] == ["self", "label"]
    assert [ast.literal_eval(value) for value in methods[1].args.defaults] == [None]
    assert [ast.unparse(item.returns) for item in methods] == ["str", "str | None"]
    assert [ast.get_docstring(item) for item in methods] == ["Read input", "Fetch input"]
    for method in methods:
        assert not method.decorator_list and len(method.body) == 2
        stub = method.body[-1]
        assert isinstance(stub, ast.Raise)
        assert isinstance(stub.exc, ast.Name) and stub.exc.id == "NotImplementedError"
    code, response = invoke(syntax_package, tmp_path, request(tmp_path / "reader.py", output))
    assert code == 0 and response["decision"] == {"status": "passed"}
    assert not (tmp_path / "reader.py").exists()


def test_class_context_rejects_unsupported_bodies_and_reserved_insertion_names(
    delivered_class: DeliveredTemplate,
) -> None:
    base: dict[str, JsonValue] = {
        "class_name": "Example",
        "class_description": "Explicit class",
        "module_description": "Explicit class",
    }
    method: dict[str, JsonValue] = {
        "name": "read",
        "description": "Read input",
        "async": False,
        "parameters": [],
        "return_type": "None",
    }
    invalid: list[dict[str, JsonValue]] = [
        {"class_name": "Example", "module_description": "Explicit class"},
        {**base, "class_description": ""},
        {**base, "class_name": "class"},
        {**base, "service_type": "query"},
        {**base, "logging": {}},
        {**base, "constructor": {"parameters": [], "body": "pass"}},
        {**base, "methods": None},
        {**base, "methods": [{**method, "body": "return None"}]},
        {**base, "methods": [{**method, "decorators": []}]},
        {**base, "methods": [{**method, "async": "false"}]},
        {
            **base,
            "methods": [
                {**method, "parameters": [{"name": "value", "type": "list", "default": []}]}
            ],
        },
    ]
    for spelling, canonical in (("self", "self"), ("ｓｅｌｆ", "self")):
        parsed = ast.parse(f"{spelling} = None").body[0]
        assert isinstance(parsed, ast.Assign)
        assert isinstance(parsed.targets[0], ast.Name) and parsed.targets[0].id == canonical
        invalid.append(
            {**base, "methods": [{**method, "parameters": [{"name": spelling, "type": "object"}]}]}
        )
    for name in ("__init__", "__call__", "_＿init__"):
        invalid.append({**base, "methods": [{**method, "name": name}]})
    for context in invalid:
        with pytest.raises(ContextError):
            delivered_class.renderer.render("python_class", context, delivered_class.provenance)
    output = delivered_class.renderer.render(
        "python_class",
        {**base, "methods": [], "bases": [], "imports": {}},
        delivered_class.provenance,
    )
    _, cls = parse_class(output)
    assert isinstance(cls.body[-1], ast.Pass)


def test_invalid_native_parameter_order_remains_a_syntax_failure(
    delivered_class: DeliveredTemplate, syntax_package: SyntaxPackage, tmp_path: Path
) -> None:
    output = delivered_class.renderer.render(
        "python_class",
        {
            "class_name": "InvalidOrder",
            "class_description": "Native signature syntax",
            "module_description": "Native signature syntax",
            "methods": [
                {
                    "name": "read",
                    "description": "Read",
                    "async": False,
                    "parameters": [
                        {"name": "first", "type": "int", "default": 0},
                        {"name": "second", "type": "int"},
                    ],
                    "return_type": "None",
                }
            ],
        },
        delivered_class.provenance,
    )
    code, response = invoke(syntax_package, tmp_path, request(tmp_path / "invalid.py", output))
    assert code == 1
    decision = response["decision"]
    assert isinstance(decision, dict) and decision["status"] == "failed"
    assert not (tmp_path / "invalid.py").exists()

