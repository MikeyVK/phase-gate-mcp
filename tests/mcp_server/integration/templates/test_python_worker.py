"""Observe portable worker operations through the delivered catalog and native syntax."""

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
def delivered_worker(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredTemplate:
    source = pytestconfig.rootpath / ".pgmcp/template_suite"
    delivered = load_delivered_template(
        source_suite=source,
        source_package=source / "python_worker",
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "explicit suite",
        template_id="python_worker",
    )
    selected = delivered.catalog.get("python_worker")
    assert selected.policy.persistence == "workspace"
    assert dict(delivered.checks.profiles)[selected.policy.output_profile].checks == (
        "python_syntax",
    )
    return delivered


def parse_worker(output: str) -> tuple[ast.Module, ast.ClassDef]:
    tree = ast.parse(output)
    compile(tree, "<delivered-worker>", "exec")
    classes = [item for item in tree.body if isinstance(item, ast.ClassDef)]
    assert len(classes) == 1
    return tree, classes[0]


@pytest.mark.parametrize("asynchronous", [False, True])
def test_minimal_worker_preserves_the_single_supplied_operation(
    delivered_worker: DeliveredTemplate,
    syntax_package: SyntaxPackage,
    tmp_path: Path,
    asynchronous: bool,
) -> None:
    context: dict[str, JsonValue] = {
        "class_name": "exact_worker",
        "description": "Explicit worker",
        "operation": {
            "name": "process_value",
            "description": "Process one value",
            "async": asynchronous,
            "parameters": [{"name": "value", "type": "int"}],
            "return_type": "int",
            "body": "return value + 1",
        },
    }
    output = delivered_worker.renderer.render("python_worker", context, delivered_worker.provenance)
    tree, cls = parse_worker(output)
    assert len(tree.body) == 2 and len(cls.body) == 2
    assert cls.name == "exact_worker" and not cls.bases
    assert ast.get_docstring(tree) == ast.get_docstring(cls) == context["description"]
    operation = cls.body[1]
    expected_kind = ast.AsyncFunctionDef if asynchronous else ast.FunctionDef
    assert isinstance(operation, expected_kind)
    assert operation.name == "process_value" and not operation.decorator_list
    assert [arg.arg for arg in operation.args.args] == ["self", "value"]
    assert ast.unparse(operation.returns) == "int"
    assert ast.dump(ast.Module(body=operation.body[1:], type_ignores=[])) == ast.dump(
        ast.parse("return value + 1")
    )
    header = ArtifactHeaderReader().read(output)
    assert header.status is HeaderReadStatus.RECOGNIZED
    assert header.provenance is not None and header.provenance.id == "python_worker"
    code, response = invoke(syntax_package, tmp_path, request(tmp_path / "worker.py", output))
    assert code == 0 and response["decision"] == {"status": "passed"}
    assert not (tmp_path / "worker.py").exists()


def test_explicit_injection_imports_logging_and_nested_body_are_preserved(
    delivered_worker: DeliveredTemplate,
    syntax_package: SyntaxPackage,
    tmp_path: Path,
) -> None:
    constructor_body = "self.client = client"
    operation_body = (
        "if enabled:\n"
        "    logger.debug(label)\n"
        "    return await self.client.fetch(offset)\n"
        "raise ValueError('disabled')"
    )
    records: tuple[dict[str, JsonValue], ...] = ({}, {"name": 'caller."worker"'})
    for record in records:
        context: dict[str, JsonValue] = {
            "class_name": "PortableWorker",
            "description": 'Worker "description" 😀\nnext line',
            "module_description": "Separate module prose",
            "imports": {
                "stdlib": [{"kind": "import", "module": "logging"}],
                "third_party": [
                    {
                        "kind": "from",
                        "module": "absent_external",
                        "names": [{"name": "Client", "alias": "Injected"}],
                    }
                ],
                "project": [
                    {"kind": "from", "module": "absent_project", "names": [{"name": "Result"}]}
                ],
            },
            "logging": record,
            "constructor": {
                "parameters": [{"name": "client", "type": "Injected"}],
                "body": constructor_body,
            },
            "operation": {
                "name": "__call__",
                "description": "Process explicit input",
                "async": True,
                "parameters": [
                    {"name": "offset", "type": "int", "default": 0},
                    {"name": "enabled", "type": "bool", "default": False},
                    {"name": "label", "type": "str | None", "default": None},
                ],
                "return_type": "Result",
                "body": operation_body,
            },
        }
        before = deepcopy(context)
        output = delivered_worker.renderer.render(
            "python_worker", context, delivered_worker.provenance
        )
        tree, cls = parse_worker(output)
        assert context == before
        assert ast.get_docstring(tree) == context["module_description"]
        assert ast.get_docstring(cls) == context["description"]
        assert not cls.bases
        statements = [
            ast.unparse(item)
            for item in tree.body
            if isinstance(item, (ast.Import, ast.ImportFrom))
        ]
        assert statements == [
            "import logging",
            "from absent_external import Client as Injected",
            "from absent_project import Result",
        ]
        assert all(
            label in output for label in ("# Standard library", "# Third party", "# Project")
        )
        methods = [
            item for item in cls.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        assert [item.name for item in methods] == ["__init__", "__call__"]
        assert isinstance(methods[0], ast.FunctionDef) and isinstance(
            methods[1], ast.AsyncFunctionDef
        )
        assert [[arg.arg for arg in item.args.args] for item in methods] == [
            ["self", "client"],
            ["self", "offset", "enabled", "label"],
        ]
        assert [ast.literal_eval(item) for item in methods[1].args.defaults] == [0, False, None]
        assert [ast.unparse(item.returns) for item in methods] == ["None", "Result"]
        assert ast.get_docstring(methods[1]) == "Process explicit input"
        for method, body, has_doc in zip(
            methods, [constructor_body, operation_body], [False, True], strict=True
        ):
            assert not method.decorator_list
            actual = ast.Module(body=method.body[1:] if has_doc else method.body, type_ignores=[])
            assert ast.dump(actual) == ast.dump(ast.parse(body))
        assignments = [item for item in tree.body if isinstance(item, ast.Assign)]
        assert len(assignments) == 1 and ast.unparse(assignments[0].targets[0]) == "logger"
        call = assignments[0].value
        assert isinstance(call, ast.Call) and ast.unparse(call.func) == "logging.getLogger"
        assert len(call.args) == 1 and not call.keywords
        if record:
            assert ast.literal_eval(call.args[0]) == record["name"]
        else:
            assert isinstance(call.args[0], ast.Name) and call.args[0].id == "__name__"
        code, response = invoke(syntax_package, tmp_path, request(tmp_path / "explicit.py", output))
        assert code == 0 and response["decision"] == {"status": "passed"}
    assert not (tmp_path / "explicit.py").exists()


def test_context_requires_one_operation_and_rejects_hidden_lifecycle_or_conflicts(
    delivered_worker: DeliveredTemplate,
) -> None:
    operation: dict[str, JsonValue] = {
        "name": "process",
        "description": "Process",
        "async": False,
        "parameters": [],
        "return_type": "None",
        "body": "return None",
    }
    base: dict[str, JsonValue] = {
        "class_name": "Worker",
        "description": "Explicit worker",
        "operation": operation,
    }
    constructor: dict[str, JsonValue] = {"parameters": [], "body": "self.client = None"}
    invalid: list[dict[str, JsonValue]] = [
        {"class_name": "Worker", "description": "Missing operation"},
        {**base, "operation": None},
        {**base, "operation": {**operation, "body": " \n\t"}},
        {**base, "operation": {**operation, "async": "false"}},
        {**base, "operation": {**operation, "decorators": []}},
        {**base, "methods": []},
        {**base, "bases": []},
        {**base, "worker_scope": "strategy"},
        {**base, "strategy_cache": True},
        {**base, "constructor": {**constructor, "name": "create"}},
        {**base, "logging": None},
        {**base, "logging": {"expression": "__name__"}},
        {**base, "logging": {"name": ""}},
    ]
    for spelling in ("self", "ｓｅｌｆ"):
        parameter = {"name": spelling, "type": "object"}
        invalid.extend(
            [
                {**base, "operation": {**operation, "parameters": [parameter]}},
                {**base, "constructor": {**constructor, "parameters": [parameter]}},
            ]
        )
    for spelling in ("__init__", "_＿ｉｎｉｔ__"):
        invalid.append(
            {**base, "constructor": constructor, "operation": {**operation, "name": spelling}}
        )
    for context in invalid:
        with pytest.raises(ContextError):
            delivered_worker.renderer.render("python_worker", context, delivered_worker.provenance)
    for content in (
        {**base, "constructor": constructor},
        {**base, "operation": {**operation, "name": "__init__"}},
        {**base, "imports": {}},
    ):
        parse_worker(
            delivered_worker.renderer.render("python_worker", content, delivered_worker.provenance)
        )


def test_invalid_native_operation_body_remains_a_syntax_failure(
    delivered_worker: DeliveredTemplate, syntax_package: SyntaxPackage, tmp_path: Path
) -> None:
    output = delivered_worker.renderer.render(
        "python_worker",
        {
            "class_name": "InvalidBody",
            "description": "Native body syntax",
            "operation": {
                "name": "process",
                "description": "Process",
                "async": False,
                "parameters": [],
                "return_type": "None",
                "body": "if True",
            },
        },
        delivered_worker.provenance,
    )
    code, response = invoke(syntax_package, tmp_path, request(tmp_path / "invalid.py", output))
    assert code == 1
    decision = response["decision"]
    assert isinstance(decision, dict) and decision["status"] == "failed"
    assert not (tmp_path / "invalid.py").exists()
