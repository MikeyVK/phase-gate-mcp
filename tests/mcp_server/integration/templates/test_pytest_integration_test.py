"""Observe the delivered integration-test family, including meaningful native Pytest execution."""

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
from tests.mcp_server.integration.adapters.test_pytest import NativeCase, native, native_case
from tests.mcp_server.integration.adapters.test_python_syntax import (
    SyntaxPackage,
    invoke,
    request,
    syntax_package,
)

__all__ = ["native_case", "syntax_package"]


@pytest.fixture
def delivered_integration_test(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredTemplate:
    source = pytestconfig.rootpath / ".pgmcp/template_suite"
    delivered = load_delivered_template(
        source_suite=source,
        source_package=source / "pytest_integration_test",
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "explicit suite",
        template_id="pytest_integration_test",
    )
    selected = delivered.catalog.get("pytest_integration_test")
    assert selected.policy.persistence == "workspace"
    assert dict(delivered.checks.profiles)[selected.policy.output_profile].checks == (
        "python_syntax",
    )
    return delivered


def parse_tests(output: str) -> ast.Module:
    tree = ast.parse(output)
    compile(tree, "<delivered-integration-tests>", "exec")
    return tree


def test_minimal_content_preserves_one_function_without_inferred_scaffolding(
    delivered_integration_test: DeliveredTemplate, syntax_package: SyntaxPackage, tmp_path: Path
) -> None:
    body = "result = sum([2, 3])\nassert result == 5"
    context: dict[str, JsonValue] = {
        "description": "Caller-owned component test",
        "cases": [
            {
                "name": "test_total",
                "description": "Check sum",
                "async": False,
                "parameters": [],
                "body": body,
            }
        ],
    }
    output = delivered_integration_test.renderer.render(
        "pytest_integration_test", context, delivered_integration_test.provenance
    )
    tree = parse_tests(output)
    assert ast.get_docstring(tree) == context["description"] and len(tree.body) == 2
    function = tree.body[1]
    assert isinstance(function, ast.FunctionDef) and function.name == "test_total"
    assert not function.args.args and not function.decorator_list
    assert ast.unparse(function.returns) == "None"
    assert ast.get_docstring(function) == "Check sum"
    assert ast.dump(ast.Module(body=function.body[1:], type_ignores=[])) == ast.dump(
        ast.parse(body)
    )
    header = ArtifactHeaderReader().read(output)
    assert header.status is HeaderReadStatus.RECOGNIZED
    assert header.provenance is not None and header.provenance.id == "pytest_integration_test"
    code, response = invoke(syntax_package, tmp_path, request(tmp_path / "test_output.py", output))
    assert code == 0 and response["decision"] == {"status": "passed"}
    assert not (tmp_path / "test_output.py").exists()


def test_explicit_json_and_filesystem_components_execute_with_native_pytest(
    delivered_integration_test: DeliveredTemplate,
    native_case: NativeCase,
) -> None:
    context: dict[str, JsonValue] = {
        "description": "Explicit JSON serialization and filesystem collaboration",
        "imports": {
            "stdlib": [
                {"kind": "import", "module": "json"},
                {"kind": "from", "module": "pathlib", "names": [{"name": "Path"}]},
            ],
            "third_party": [{"kind": "import", "module": "pytest"}],
        },
        "markers": ['pytest.mark.usefixtures("payload")'],
        "fixtures": [
            {
                "name": "payload",
                "description": "Supply content",
                "async": False,
                "parameters": [],
                "return_type": "dict[str, object]",
                "body": 'return {"value": 7, "enabled": False}',
                "decorator": "pytest.fixture",
            },
            {
                "name": "stored",
                "description": "Serialize to explicit fixture storage",
                "async": False,
                "parameters": [
                    {"name": "tmp_path", "type": "Path"},
                    {"name": "payload", "type": "dict[str, object]"},
                ],
                "return_type": "Path",
                "body": (
                    'destination = tmp_path / "payload.json"\n'
                    'destination.write_text(json.dumps(payload), encoding="utf-8")\n'
                    "return destination"
                ),
                "decorator": "pytest.fixture",
                "scope": "function",
                "autouse": False,
            },
        ],
        "cases": [
            {
                "name": "test_round_trip",
                "description": "Read serialized content",
                "async": False,
                "parameters": [
                    {"name": "stored", "type": "Path"},
                    {"name": "payload", "type": "dict[str, object]"},
                ],
                "body": (
                    'observed = json.loads(stored.read_text(encoding="utf-8"))\n'
                    "assert observed == payload\n"
                    'assert observed["enabled"] is False'
                ),
            },
            {
                "name": "test_selected_field",
                "description": "Check stored fields",
                "async": False,
                "parameters": [
                    {"name": "stored", "type": "Path"},
                    {"name": "field", "type": "str"},
                    {"name": "expected", "type": "object"},
                ],
                "markers": [
                    'pytest.mark.parametrize("field, expected", [("value", 7), ("enabled", False)])'
                ],
                "body": (
                    'loaded = json.loads(stored.read_text(encoding="utf-8"))\n'
                    "assert loaded[field] == expected"
                ),
            },
        ],
    }
    before = deepcopy(context)
    output = delivered_integration_test.renderer.render(
        "pytest_integration_test", context, delivered_integration_test.provenance
    )
    tree = parse_tests(output)
    assert context == before
    functions = [item for item in tree.body if isinstance(item, ast.FunctionDef)]
    assert [item.name for item in functions] == [
        "payload",
        "stored",
        "test_round_trip",
        "test_selected_field",
    ]
    assert isinstance(functions[0].decorator_list[0], ast.Attribute)
    configured_fixture = functions[1].decorator_list[0]
    assert isinstance(configured_fixture, ast.Call)
    assert {item.arg: ast.literal_eval(item.value) for item in configured_fixture.keywords} == {
        "scope": "function",
        "autouse": False,
    }
    assert [arg.arg for arg in functions[1].args.args] == ["tmp_path", "payload"]
    assert [
        ast.unparse(item) for item in tree.body if isinstance(item, (ast.Import, ast.ImportFrom))
    ] == ["from pathlib import Path", "import json", "import pytest"]
    markers = [item for item in tree.body if isinstance(item, ast.Assign)]
    assert len(markers) == 1 and ast.unparse(markers[0].targets[0]) == "pytestmark"
    assert not any(isinstance(item, ast.ClassDef) for item in tree.body)
    native_case.source.write_text(output, encoding="utf-8")
    # The full eight-worker suite can exceed 45 seconds during nested Pytest startup.
    # Keep a finite budget for this rendered-template operation without weakening assertions.
    result = native(native_case, [str(native_case.source)], [], timeout_seconds=120)
    assert result.returncode == 0, result.stdout.decode(errors="replace")
    assert b"3 passed" in result.stdout


def test_class_async_fixture_and_case_content_remain_explicit(
    delivered_integration_test: DeliveredTemplate,
    syntax_package: SyntaxPackage,
    tmp_path: Path,
) -> None:
    fixture_body = "return await source.open()"
    async_body = "observed = await opened.read()\nassert observed == 7"
    context: dict[str, JsonValue] = {
        "description": 'Explicit "async" declarations 😀\nsecond line',
        "class_name": "ＴestExplicit",
        "imports": {
            "stdlib": [{"kind": "import", "module": "collections", "alias": "col"}],
            "third_party": [
                {"kind": "import", "module": "pytest"},
                {"kind": "import", "module": "pytest_asyncio", "alias": "aio"},
            ],
            "project": [{"kind": "from", "module": "absent_project", "names": [{"name": "Port"}]}],
        },
        "fixtures": [
            {
                "name": "opened",
                "description": "Open explicit dependency",
                "async": True,
                "parameters": [{"name": "source", "type": "Port"}],
                "return_type": "Port",
                "body": fixture_body,
                "decorator": "aio.fixture",
                "scope": "module",
                "autouse": False,
            }
        ],
        "markers": [],
        "cases": [
            {
                "name": "test_defaults",
                "description": "Keep scalar defaults",
                "async": False,
                "parameters": [
                    {"name": "offset", "type": "int", "default": 0},
                    {"name": "enabled", "type": "bool", "default": False},
                    {"name": "label", "type": "str | None", "default": None},
                ],
                "body": "assert offset == 0 and enabled is False and label is None",
                "markers": [],
            },
            {
                "name": "test_read",
                "description": "Read asynchronously",
                "async": True,
                "parameters": [{"name": "opened", "type": "Port"}],
                "body": async_body,
                "markers": ["pytest.mark.asyncio"],
            },
        ],
    }
    before = deepcopy(context)
    output = delivered_integration_test.renderer.render(
        "pytest_integration_test", context, delivered_integration_test.provenance
    )
    tree = parse_tests(output)
    assert context == before and ast.get_docstring(tree) == context["description"]
    assert [
        ast.unparse(item) for item in tree.body if isinstance(item, (ast.Import, ast.ImportFrom))
    ] == [
        "import collections as col",
        "import pytest",
        "import pytest_asyncio as aio",
        "from absent_project import Port",
    ]
    fixtures = [item for item in tree.body if isinstance(item, ast.AsyncFunctionDef)]
    assert len(fixtures) == 1 and fixtures[0].name == "opened"
    assert [arg.arg for arg in fixtures[0].args.args] == ["source"]
    decorator = fixtures[0].decorator_list[0]
    assert isinstance(decorator, ast.Call) and ast.unparse(decorator.func) == "aio.fixture"
    assert {item.arg: ast.literal_eval(item.value) for item in decorator.keywords} == {
        "scope": "module",
        "autouse": False,
    }
    assert ast.dump(ast.Module(body=fixtures[0].body[1:], type_ignores=[])) == ast.dump(
        ast.parse(fixture_body)
    )
    classes = [item for item in tree.body if isinstance(item, ast.ClassDef)]
    assert len(classes) == 1 and classes[0].name == "TestExplicit"
    functions = classes[0].body
    assert len(functions) == 2
    first, second = functions
    assert isinstance(first, ast.FunctionDef) and isinstance(second, ast.AsyncFunctionDef)
    assert [first.name, second.name] == ["test_defaults", "test_read"]
    assert [arg.arg for arg in first.args.args] == ["self", "offset", "enabled", "label"]
    assert [ast.literal_eval(item) for item in first.args.defaults] == [0, False, None]
    assert [arg.arg for arg in second.args.args] == ["self", "opened"]
    assert not first.decorator_list
    assert [ast.unparse(item) for item in second.decorator_list] == ["pytest.mark.asyncio"]
    assert ast.dump(ast.Module(body=second.body[1:], type_ignores=[])) == ast.dump(
        ast.parse(async_body)
    )
    assert not any(isinstance(item, ast.Assign) for item in tree.body)
    code, response = invoke(syntax_package, tmp_path, request(tmp_path / "test_async.py", output))
    assert code == 0 and response["decision"] == {"status": "passed"}
    assert not (tmp_path / "test_async.py").exists()


def test_context_requires_real_cases_and_rejects_hidden_or_reserved_fields(
    delivered_integration_test: DeliveredTemplate,
) -> None:
    case: dict[str, JsonValue] = {
        "name": "test_value",
        "description": "Check",
        "async": False,
        "parameters": [],
        "body": "assert 2 + 3 == 5",
    }
    fixture: dict[str, JsonValue] = {
        "name": "value",
        "description": "Supply",
        "async": False,
        "parameters": [],
        "return_type": "int",
        "body": "return 2",
        "decorator": "pytest.fixture",
    }
    base: dict[str, JsonValue] = {"description": "Caller cases", "cases": [case]}
    noncollectable = "Test\u0307Cases"
    blocked_composition = "Test\u0300\u0307Cases"
    invalid: list[dict[str, JsonValue]] = [
        {"description": "Missing cases"},
        {**base, "cases": []},
        {**base, "cases": None},
        {**base, "description": ""},
        {**base, "module_description": "Unsupported"},
        {**base, "layer": "Tests"},
        {**base, "class_name": "Examples"},
        {**base, "class_name": noncollectable},
        {**base, "class_name": None},
        {**base, "cases": [{**case, "name": "check_value"}]},
        {**base, "cases": [{**case, "body": " \n\t"}]},
        {**base, "cases": [{**case, "arrange": "value = 2"}]},
        {**base, "cases": [{**case, "async": "false"}]},
        {**base, "fixtures": None},
        {**base, "fixtures": [{**fixture, "scope": "thread"}]},
        {**base, "fixtures": [{**fixture, "autouse": "false"}]},
        {**base, "fixtures": [{**fixture, "decorator": "factory()"}]},
        {**base, "markers": None},
    ]
    for spelling in ("self", "ｓｅｌｆ"):
        invalid.append(
            {
                **base,
                "class_name": "TestExplicit",
                "cases": [{**case, "parameters": [{"name": spelling, "type": "object"}]}],
            }
        )
    for context in invalid:
        with pytest.raises(ContextError):
            delivered_integration_test.renderer.render(
                "pytest_integration_test", context, delivered_integration_test.provenance
            )
    for content in (
        {**base, "fixtures": [], "markers": [], "imports": {}},
        {**base, "class_name": blocked_composition},
        {**base, "cases": [{**case, "parameters": [{"name": "self", "type": "object"}]}]},
    ):
        parse_tests(
            delivered_integration_test.renderer.render(
                "pytest_integration_test", content, delivered_integration_test.provenance
            )
        )


def test_invalid_native_body_remains_a_syntax_failure(
    delivered_integration_test: DeliveredTemplate,
    syntax_package: SyntaxPackage,
    tmp_path: Path,
) -> None:
    output = delivered_integration_test.renderer.render(
        "pytest_integration_test",
        {
            "description": "Native body syntax",
            "cases": [
                {
                    "name": "test_invalid",
                    "description": "Invalid",
                    "async": False,
                    "parameters": [],
                    "body": "if True",
                }
            ],
        },
        delivered_integration_test.provenance,
    )
    code, response = invoke(syntax_package, tmp_path, request(tmp_path / "test_invalid.py", output))
    assert code == 1
    decision = response["decision"]
    assert isinstance(decision, dict) and decision["status"] == "failed"
    assert not (tmp_path / "test_invalid.py").exists()
