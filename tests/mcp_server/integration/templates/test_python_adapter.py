"""Observe delivered portable adapters through public catalog and native syntax."""

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
def delivered_adapter(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredTemplate:
    source = pytestconfig.rootpath / ".pgmcp/template_suite"
    delivered = load_delivered_template(
        source_suite=source,
        source_package=source / "python_adapter",
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "explicit suite",
        template_id="python_adapter",
    )
    selected = delivered.catalog.get("python_adapter")
    assert selected.policy.persistence == "workspace"
    assert dict(delivered.checks.profiles)[selected.policy.output_profile].checks == (
        "python_syntax",
    )
    return delivered


def parse_adapter(output: str) -> tuple[ast.Module, ast.ClassDef]:
    tree = ast.parse(output)
    compile(tree, "<delivered-adapter>", "exec")
    classes = [item for item in tree.body if isinstance(item, ast.ClassDef)]
    assert len(classes) == 1
    return tree, classes[0]


def test_minimal_adapter_has_no_inferred_dependencies_or_operations(
    delivered_adapter: DeliveredTemplate, syntax_package: SyntaxPackage, tmp_path: Path
) -> None:
    context = {
        "class_name": "exact_adapter",
        "class_description": "Explicit adapter.",
        "module_description": "Explicit adapter.",
    }
    output = delivered_adapter.renderer.render(
        "python_adapter", context, delivered_adapter.provenance
    )
    tree, cls = parse_adapter(output)
    assert cls.name == "exact_adapter" and not cls.bases
    assert ast.get_docstring(tree) == ast.get_docstring(cls) == context["class_description"]
    assert len(tree.body) == 2 and len(cls.body) == 2
    assert isinstance(cls.body[-1], ast.Pass)
    header = ArtifactHeaderReader().read(output)
    assert header.status is HeaderReadStatus.RECOGNIZED
    assert header.provenance is not None and header.provenance.id == "python_adapter"
    code, response = invoke(syntax_package, tmp_path, request(tmp_path / "adapter.py", output))
    assert code == 0 and response["decision"] == {"status": "passed"}
    assert not (tmp_path / "adapter.py").exists()


def test_explicit_injection_bodies_bases_and_imports_are_preserved(
    delivered_adapter: DeliveredTemplate, syntax_package: SyntaxPackage, tmp_path: Path
) -> None:
    constructor_body = "self.client = client\nself.enabled = enabled"
    sync_body = "if value:\n    return self.client.convert(value)\nraise ValueError('empty input')"
    async_body = "return await self.client.fetch(label)"
    method: dict[str, JsonValue] = {
        "name": "__call__",
        "description": "Translate explicit input",
        "async": False,
        "parameters": [{"name": "value", "type": "int", "default": 0}],
        "return_type": "str",
        "body": sync_body,
    }
    context: dict[str, JsonValue] = {
        "class_name": "exact_adapter",
        "class_description": 'Adapter "description" 😀\nnext line',
        "module_description": "Separate module prose",
        "imports": {
            "stdlib": [{"kind": "import", "module": "collections", "alias": "col"}],
            "third_party": [
                {"kind": "from", "module": "absent_external", "names": [{"name": "Client"}]}
            ],
            "project": [
                {
                    "kind": "from",
                    "module": "absent_project",
                    "names": [{"name": "Boundary", "alias": "Base"}],
                }
            ],
        },
        "bases": ["Base"],
        "constructor": {
            "parameters": [
                {"name": "client", "type": "Client"},
                {"name": "enabled", "type": "bool", "default": False},
            ],
            "body": constructor_body,
        },
        "methods": [
            method,
            {
                "name": "fetch",
                "description": "Fetch result",
                "async": True,
                "parameters": [{"name": "label", "type": "str | None", "default": None}],
                "return_type": "str",
                "body": async_body,
            },
        ],
    }
    before = deepcopy(context)
    output = delivered_adapter.renderer.render(
        "python_adapter", context, delivered_adapter.provenance
    )
    tree, cls = parse_adapter(output)
    assert context == before
    assert ast.get_docstring(tree) == context["module_description"]
    assert ast.get_docstring(cls) == context["class_description"]
    assert [ast.unparse(base) for base in cls.bases] == ["Base"]
    assert [
        ast.unparse(item) for item in tree.body if isinstance(item, (ast.Import, ast.ImportFrom))
    ] == [
        "import collections as col",
        "from absent_external import Client",
        "from absent_project import Boundary as Base",
    ]
    assert len(tree.body) == 5
    methods = [
        item for item in cls.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    assert [item.name for item in methods] == ["__init__", "__call__", "fetch"]
    assert isinstance(methods[0], ast.FunctionDef) and isinstance(methods[1], ast.FunctionDef)
    assert isinstance(methods[2], ast.AsyncFunctionDef)
    assert [[arg.arg for arg in item.args.args] for item in methods] == [
        ["self", "client", "enabled"],
        ["self", "value"],
        ["self", "label"],
    ]
    assert [[ast.literal_eval(value) for value in item.args.defaults] for item in methods] == [
        [False],
        [0],
        [None],
    ]
    assert [ast.unparse(item.returns) for item in methods] == ["None", "str", "str"]
    for item, body, has_doc in zip(
        methods, [constructor_body, sync_body, async_body], [False, True, True], strict=True
    ):
        assert not item.decorator_list
        actual = ast.Module(body=item.body[1:] if has_doc else item.body, type_ignores=[])
        assert ast.dump(actual) == ast.dump(ast.parse(body))
    assert [ast.get_docstring(item) for item in methods[1:]] == [
        "Translate explicit input",
        "Fetch result",
    ]
    code, response = invoke(syntax_package, tmp_path, request(tmp_path / "explicit.py", output))
    assert code == 0 and response["decision"] == {"status": "passed"}
    assert not (tmp_path / "explicit.py").exists()


def test_logging_is_explicit_and_joins_caller_imports(
    delivered_adapter: DeliveredTemplate, syntax_package: SyntaxPackage, tmp_path: Path
) -> None:
    records: tuple[dict[str, JsonValue], ...] = ({}, {"name": 'caller."logger"'})
    for record in records:
        context: dict[str, JsonValue] = {
            "class_name": "LoggedAdapter",
            "class_description": "Opt-in logger",
            "module_description": "Opt-in logger",
            "logging": record,
            "imports": {"stdlib": [{"kind": "import", "module": "logging"}]},
            "methods": [],
            "bases": [],
        }
        output = delivered_adapter.renderer.render(
            "python_adapter", context, delivered_adapter.provenance
        )
        tree, cls = parse_adapter(output)
        assert isinstance(cls.body[-1], ast.Pass)
        statements = [ast.unparse(item) for item in tree.body if isinstance(item, ast.Import)]
        assert statements == ["import logging"]
        assignments = [item for item in tree.body if isinstance(item, ast.Assign)]
        assert len(assignments) == 1 and ast.unparse(assignments[0].targets[0]) == "logger"
        call = assignments[0].value
        assert isinstance(call, ast.Call) and ast.unparse(call.func) == "logging.getLogger"
        assert len(call.args) == 1 and not call.keywords
        if record:
            assert ast.literal_eval(call.args[0]) == record["name"]
        else:
            assert isinstance(call.args[0], ast.Name) and call.args[0].id == "__name__"
        code, response = invoke(syntax_package, tmp_path, request(tmp_path / "logged.py", output))
        assert code == 0 and response["decision"] == {"status": "passed"}
    assert not (tmp_path / "logged.py").exists()


def test_context_rejects_hidden_fields_self_and_conflicting_constructor(
    delivered_adapter: DeliveredTemplate,
) -> None:
    base: dict[str, JsonValue] = {
        "class_name": "Example",
        "class_description": "Explicit adapter",
        "module_description": "Explicit adapter",
    }
    method: dict[str, JsonValue] = {
        "name": "read",
        "description": "Read",
        "async": False,
        "parameters": [],
        "return_type": "None",
        "body": "return None",
    }
    constructor: dict[str, JsonValue] = {"parameters": [], "body": "self.client = None"}
    invalid: list[dict[str, JsonValue]] = [
        {"class_name": "Example", "module_description": "Explicit adapter"},
        {**base, "strategy_cache": True},
        {**base, "boundary_description": "Duplicate field"},
        {**base, "methods": None},
        {**base, "constructor": {**constructor, "name": "create"}},
        {**base, "logging": None},
        {**base, "logging": {"expression": "__name__"}},
        {**base, "logging": {"name": ""}},
        {**base, "methods": [{**method, "body": " \n\t"}]},
        {**base, "methods": [{**method, "async": "false"}]},
        {**base, "methods": [{**method, "decorators": []}]},
    ]
    for spelling in ("self", "ｓｅｌｆ"):
        parameter = {"name": spelling, "type": "object"}
        invalid.extend(
            [
                {**base, "methods": [{**method, "parameters": [parameter]}]},
                {**base, "constructor": {**constructor, "parameters": [parameter]}},
            ]
        )
    for spelling in ("__init__", "_＿ｉｎｉｔ__"):
        observed = ast.parse(f"def {spelling}(self): pass").body[0]
        assert isinstance(observed, ast.FunctionDef) and observed.name == "__init__"
        invalid.append(
            {**base, "constructor": constructor, "methods": [{**method, "name": spelling}]}
        )
    for context in invalid:
        with pytest.raises(ContextError):
            delivered_adapter.renderer.render(
                "python_adapter", context, delivered_adapter.provenance
            )
    for content in (
        {**base, "constructor": constructor},
        {**base, "methods": [{**method, "name": "__init__"}]},
        {**base, "methods": [], "bases": [], "imports": {}},
    ):
        parse_adapter(
            delivered_adapter.renderer.render(
                "python_adapter", content, delivered_adapter.provenance
            )
        )


def test_invalid_native_body_is_rejected_by_the_syntax_check(
    delivered_adapter: DeliveredTemplate, syntax_package: SyntaxPackage, tmp_path: Path
) -> None:
    output = delivered_adapter.renderer.render(
        "python_adapter",
        {
            "class_name": "InvalidBody",
            "class_description": "Native body syntax",
            "module_description": "Native body syntax",
            "constructor": {"parameters": [], "body": "if True"},
        },
        delivered_adapter.provenance,
    )
    code, response = invoke(syntax_package, tmp_path, request(tmp_path / "invalid.py", output))
    assert code == 1
    decision = response["decision"]
    assert isinstance(decision, dict) and decision["status"] == "failed"
    assert not (tmp_path / "invalid.py").exists()

