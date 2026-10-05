"""Observe the delivered unit-test family, including meaningful native Pytest execution."""

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
def delivered_unit_test(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredTemplate:
    source = pytestconfig.rootpath / ".pgmcp/template_suite"
    delivered = load_delivered_template(
        source_suite=source,
        source_package=source / "pytest_unit_test",
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "explicit suite",
        template_id="pytest_unit_test",
    )
    selected = delivered.catalog.get("pytest_unit_test")
    assert selected.policy.persistence == "workspace"
    assert dict(delivered.checks.profiles)[selected.policy.output_profile].checks == (
        "python_syntax",
    )
    return delivered


def parse_tests(output: str) -> ast.Module:
    tree = ast.parse(output)
    compile(tree, "<delivered-unit-tests>", "exec")
    return tree


def test_minimal_content_preserves_one_function_without_inferred_scaffolding(
    delivered_unit_test: DeliveredTemplate, syntax_package: SyntaxPackage, tmp_path: Path
) -> None:
    body = "result = sum([2, 3])\nassert result == 5"
    context: dict[str, JsonValue] = {
        "description": "Caller-owned arithmetic test",
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
    output = delivered_unit_test.renderer.render(
        "pytest_unit_test", context, delivered_unit_test.provenance
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
    assert header.provenance is not None and header.provenance.id == "pytest_unit_test"
    code, response = invoke(syntax_package, tmp_path, request(tmp_path / "test_output.py", output))
    assert code == 0 and response["decision"] == {"status": "passed"}
    assert not (tmp_path / "test_output.py").exists()


def test_explicit_fixtures_markers_and_assertions_execute_with_native_pytest(
    delivered_unit_test: DeliveredTemplate,
    native_case: NativeCase,
) -> None:
    context: dict[str, JsonValue] = {
        "description": "Explicit fixture composition and parameterized arithmetic",
        "imports": {"third_party": [{"kind": "import", "module": "pytest"}]},
        "markers": ['pytest.mark.usefixtures("base")'],
        "fixtures": [
            {
                "name": "base",
                "description": "Supply base",
                "async": False,
                "parameters": [],
                "return_type": "int",
                "body": "return 2",
                "decorator": "pytest.fixture",
            },
            {
                "name": "numbers",
                "description": "Compose values",
                "async": False,
                "parameters": [{"name": "base", "type": "int"}],
                "return_type": "list[int]",
                "body": "return [base, base + 1]",
                "decorator": "pytest.fixture",
                "scope": "function",
                "autouse": False,
            },
        ],
        "cases": [
            {
                "name": "test_total",
                "description": "Check composed values",
                "async": False,
                "parameters": [{"name": "numbers", "type": "list[int]"}],
                "body": "arranged = numbers\nobserved = sum(arranged)\nassert observed == 5",
            },
            {
                "name": "test_square",
                "description": "Check square",
                "async": False,
                "parameters": [
                    {"name": "value", "type": "int"},
                    {"name": "expected", "type": "int"},
                ],
                "markers": ['pytest.mark.parametrize("value, expected", [(2, 4), (3, 9)])'],
                "body": "assert value ** 2 == expected",
            },
        ],
    }
    before = deepcopy(context)
    output = delivered_unit_test.renderer.render(
        "pytest_unit_test", context, delivered_unit_test.provenance
    )
    tree = parse_tests(output)
    assert context == before
    functions = [item for item in tree.body if isinstance(item, ast.FunctionDef)]
    assert [item.name for item in functions] == ["base", "numbers", "test_total", "test_square"]
    assert isinstance(functions[0].decorator_list[0], ast.Attribute)
    configured_fixture = functions[1].decorator_list[0]
    assert isinstance(configured_fixture, ast.Call)
    assert {item.arg: ast.literal_eval(item.value) for item in configured_fixture.keywords} == {
        "scope": "function",
        "autouse": False,
    }
    assert [arg.arg for arg in functions[1].args.args] == ["base"]
    markers = [item for item in tree.body if isinstance(item, ast.Assign)]
    assert len(markers) == 1 and ast.unparse(markers[0].targets[0]) == "pytestmark"
    assert not any(isinstance(item, ast.ClassDef) for item in tree.body)
    native_case.source.write_text(output, encoding="utf-8")
    result = native(native_case, [str(native_case.source)], [])
    assert result.returncode == 0, result.stdout.decode(errors="replace")
    assert b"3 passed" in result.stdout


def test_class_async_fixture_and_case_content_remain_explicit(
    delivered_unit_test: DeliveredTemplate,
    syntax_package: SyntaxPackage,
    tmp_path: Path,
) -> None:
    fixture_body = "return await source.open()"
    async_body = "observed = await opened.read()\nassert observed == 7"
    context: dict[str, JsonValue] = {
        "description": 'Explicit "async" declarations 😀\nsecond line',
        "class_name": "TestExplicit",
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
    output = delivered_unit_test.renderer.render(
        "pytest_unit_test", context, delivered_unit_test.provenance
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
    delivered_unit_test: DeliveredTemplate,
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
        {**base, "class_name": blocked_composition},
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
            delivered_unit_test.renderer.render(
                "pytest_unit_test", context, delivered_unit_test.provenance
            )
    for content in (
        {**base, "fixtures": [], "markers": [], "imports": {}},
        {**base, "class_name": "TestCases"},
        {**base, "cases": [{**case, "parameters": [{"name": "self", "type": "object"}]}]},
    ):
        parse_tests(
            delivered_unit_test.renderer.render(
                "pytest_unit_test", content, delivered_unit_test.provenance
            )
        )


def test_invalid_native_body_remains_a_syntax_failure(
    delivered_unit_test: DeliveredTemplate,
    syntax_package: SyntaxPackage,
    tmp_path: Path,
) -> None:
    output = delivered_unit_test.renderer.render(
        "pytest_unit_test",
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
        delivered_unit_test.provenance,
    )
    code, response = invoke(syntax_package, tmp_path, request(tmp_path / "test_invalid.py", output))
    assert code == 1
    decision = response["decision"]
    assert isinstance(decision, dict) and decision["status"] == "failed"
    assert not (tmp_path / "test_invalid.py").exists()
