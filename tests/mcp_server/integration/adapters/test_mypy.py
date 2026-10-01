"""Native Mypy/check-v1 conformance using isolated packages and workspaces."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import venv
from dataclasses import dataclass
from pathlib import Path
from shutil import copytree

import pytest
from jsonschema import Draft202012Validator
from pydantic import JsonValue, TypeAdapter

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.adapter_manifest import AdapterTrustConfig
from mcp_server.core.interfaces.execution import AdapterLaunch
from mcp_server.execution.catalog import AdapterCatalogLoader, FileAdapterPackageReader


@dataclass(frozen=True)
class MypyPackage:
    launch: AdapterLaunch
    root: Path
    workspace: Path
    schema: Draft202012Validator


@pytest.fixture
def mypy_package(tmp_path: Path, pytestconfig: pytest.Config) -> MypyPackage:
    root = tmp_path / "official packages" / "mypy"
    copytree(pytestconfig.rootpath / "mcp_server/bundled_adapters/mypy", root)
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / "pyproject.toml").write_bytes(
        (pytestconfig.rootpath / "pyproject.toml").read_bytes()
    )
    loader = ConfigLoader(tmp_path / "config", tmp_path / "templates")
    catalog = AdapterCatalogLoader(
        root.parent,
        tmp_path / "workspace adapters",
        AdapterTrustConfig(trusted_adapter_ids=()),
        read_manifest=loader.load_adapter_manifest,
        files=FileAdapterPackageReader(),
        resolve_program=lambda name: Path(sys.executable) if name == "python" else None,
        windows=os.name == "nt",
    ).load()
    binding = catalog.get_check("mypy", "types")
    assert binding.capability.inputs == ("selection",)
    assert binding.capability.requires_file is None
    schema_path = pytestconfig.rootpath / "mcp_server/execution/contracts/check_v1.schema.json"
    return MypyPackage(
        catalog.get_check("mypy", "types").launch,
        root,
        workspace,
        Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8"))),
    )


def native(
    workspace: Path,
    operation: str,
    targets: tuple[Path, ...],
    args: tuple[str, ...] = (),
) -> subprocess.CompletedProcess[bytes]:
    assert operation == "types"
    return subprocess.run(
        [sys.executable, "-m", "mypy", *args, *(str(path) for path in targets)],
        cwd=workspace,
        capture_output=True,
        timeout=30,
    )


def invoke(
    package: MypyPackage,
    operation: str,
    targets: tuple[Path, ...] = (),
    args: tuple[str, ...] = (),
    *,
    interpreter: Path | None = None,
    raw: bytes | None = None,
) -> tuple[int, dict[str, JsonValue]]:
    executable = interpreter if interpreter is not None else package.launch.executable
    assert executable is not None
    request = (
        raw
        if raw is not None
        else json.dumps(
            {
                "execution_context": {"scratch_directory": str(package.workspace.parent)},
                "operation": operation,
                "targets": [str(path) for path in targets],
                "args": list(args),
            }
        ).encode("utf-8")
    )
    completed = subprocess.run(
        [str(executable), *package.launch.args],
        input=request,
        cwd=package.workspace,
        capture_output=True,
        timeout=40,
    )
    assert not completed.stderr, completed.stderr.decode("utf-8", errors="replace")
    response: JsonValue = TypeAdapter(JsonValue).validate_json(completed.stdout)
    assert isinstance(response, dict)
    package.schema.validate(response)
    return completed.returncode, response


def evidence_text(response: dict[str, JsonValue]) -> str:
    evidence = response.get("evidence")
    if evidence is None:
        return ""
    assert isinstance(evidence, dict) and evidence["format"] == "text"
    data = evidence["data"]
    assert isinstance(data, str)
    return data


def decision(response: dict[str, JsonValue]) -> dict[str, JsonValue]:
    value = response["decision"]
    assert isinstance(value, dict)
    return value


def assert_native_evidence(
    response: dict[str, JsonValue],
    result: subprocess.CompletedProcess[bytes],
) -> None:
    evidence = evidence_text(response)
    for stream in (result.stdout, result.stderr):
        if stream:
            assert stream.decode("utf-8", errors="replace") in evidence
    assert response["coverage"] is None
    assert response["required_targets"] == []
    assert response["external_tools"] == [{"tool_id": "mypy", "version": "1.19.1"}]


@pytest.mark.parametrize(
    ("source", "args", "native_code", "adapter_code", "diagnostic"),
    [
        ("value: int = 1\n", ("--no-error-summary",), 0, 0, b""),
        (
            "def typed_add(a: int, b: int) -> int:\n    return a + b\n\n"
            'wrong_call: int = typed_add("hello", "world")\nreveal_type(wrong_call)\n',
            ("--show-column-numbers",),
            1,
            1,
            b"[arg-type]",
        ),
        ("value: int = 1\nreveal_type(value)\n", (), 0, 0, b"Revealed type"),
        ("def invalid(:\n    pass\n", (), 2, 1, b"syntax"),
        ('value: int = "bad"\n', ("--output=json",), 1, 1, b"Incompatible types"),
    ],
    ids=["clean", "type-errors-and-notes", "notes-only", "syntax-blocker", "json-output"],
)
def test_native_results_and_complete_evidence(
    mypy_package: MypyPackage,
    source: str,
    args: tuple[str, ...],
    native_code: int,
    adapter_code: int,
    diagnostic: bytes,
) -> None:
    package = mypy_package
    target = package.workspace / "sample with space.py"
    before = source.encode()
    target.write_bytes(before)
    direct = native(package.workspace, "types", (target,), args)
    assert direct.returncode == native_code
    combined = direct.stdout + direct.stderr
    assert diagnostic in combined
    if diagnostic == b"":
        assert combined == b""
    if diagnostic == b"[arg-type]":
        assert combined.count(b"[arg-type]") == 2
        assert b"sample with space.py:4:" in combined
        assert b"Revealed type" in combined
    code, response = invoke(package, "types", (target,), args)
    assert code == adapter_code
    assert decision(response)["status"] == ("passed" if code == 0 else "failed")
    if code == 1:
        assert isinstance(decision(response)["message"], str)
        assert decision(response)["message"]
        if args == ("--output=json",):
            assert "Incompatible types" in str(decision(response)["message"])
    assert_native_evidence(response, direct)
    assert target.read_bytes() == before
    assert (package.root / "requirements.txt").read_text().strip() == "mypy==1.19.1"


def test_configured_roots_and_explicit_tests_use_native_selection(
    mypy_package: MypyPackage,
) -> None:
    package = mypy_package
    app = package.workspace / "mcp_server"
    app.mkdir()
    (app / "__init__.py").write_text("", encoding="utf-8")
    (app / "clean.py").write_text("value: int = 1\n", encoding="utf-8")
    tests = package.workspace / "tests"
    tests.mkdir()
    (tests / "__init__.py").write_text("", encoding="utf-8")
    target = tests / "sample.py"
    target.write_text(
        'value: int = "bad"\n\ndef untyped(value):\n    return value\n',
        encoding="utf-8",
    )
    for targets, args, expected in (
        ((), (), 0),
        ((target,), (), 1),
        ((package.workspace,), (), 1),
        ((), ("--module", "tests.sample"), 1),
    ):
        direct = native(package.workspace, "types", targets, args)
        code, response = invoke(package, "types", targets, args)
        assert direct.returncode == code == expected
        assert b"no-untyped-def" not in direct.stdout + direct.stderr
        assert_native_evidence(response, direct)


def test_native_missing_import_policy_and_configuration_change(
    mypy_package: MypyPackage,
) -> None:
    package = mypy_package
    target = package.workspace / "imports.py"
    target.write_text("import missing_cy021_native_package\n", encoding="utf-8")
    direct = native(package.workspace, "types", (target,))
    assert direct.returncode == 1 and b"import-not-found" in direct.stdout
    code, response = invoke(package, "types", (target,))
    assert code == 1
    assert_native_evidence(response, direct)
    legacy = native(package.workspace, "types", (target,), ("--ignore-missing-imports",))
    assert legacy.returncode == 0
    config = package.workspace / "pyproject.toml"
    before = config.read_text(encoding="utf-8")
    assert "ignore_missing_imports = false" in before
    config.write_text(
        before.replace("ignore_missing_imports = false", "ignore_missing_imports = true"),
        encoding="utf-8",
    )
    direct = native(package.workspace, "types", (target,))
    code, response = invoke(package, "types", (target,))
    assert direct.returncode == code == 0
    assert_native_evidence(response, direct)


@pytest.mark.parametrize(
    "case", ["usage", "missing-target", "configuration", "native-usage", "plugin", "config-read"]
)
def test_native_inability_is_distinct_from_syntax_blockers(
    mypy_package: MypyPackage,
    case: str,
) -> None:
    package = mypy_package
    target = package.workspace / "sample.py"
    target.write_text("value: int = 1\n", encoding="utf-8")
    args: tuple[str, ...] = ()
    reason = "execution_error"
    if case == "usage":
        args = ("--unknown-cy021-option",)
        reason = "unsupported_input"
    elif case == "missing-target":
        target = package.workspace / "absent.py"
    elif case == "native-usage":
        args = ("--non-interactive",)
        reason = "unsupported_input"
    elif case == "plugin":
        (package.workspace / "fixture_plugin.py").write_text(
            '"""A module without a Mypy plugin entrypoint."""\n', encoding="utf-8"
        )
        (package.workspace / "pyproject.toml").write_text(
            '[tool.mypy]\nplugins = ["fixture_plugin.py"]\n', encoding="utf-8"
        )
        reason = "invalid_configuration"
    elif case == "config-read":
        directory = package.workspace / "config.toml"
        directory.mkdir()
        args = ("--config-file", str(directory))
    else:
        (package.workspace / "pyproject.toml").write_text(
            '[tool.mypy]\npython_version = "unterminated\n', encoding="utf-8"
        )
        reason = "invalid_configuration"
    direct = native(package.workspace, "types", (target,), args)
    assert direct.stderr
    if case not in {"configuration", "config-read"}:
        assert direct.returncode == 2
    code, response = invoke(package, "types", (target,), args)
    assert code == 3
    assert decision(response)["reason"] == reason
    if case == "config-read":
        assert "config.toml" in str(decision(response)["message"])
    else:
        assert direct.stderr.decode().replace("\r\n", "\n") in evidence_text(response).replace(
            "\r\n", "\n"
        )


@pytest.mark.parametrize(
    "args",
    [
        ("--command", "value = 1"),
        ("--shadow-file", "sample.py", "replacement.py"),
        ("--junit-x", "forbidden.xml"),
        ("--install-types",),
        ("\x00",),
    ],
)
def test_source_replacement_and_write_options_are_refused(
    mypy_package: MypyPackage,
    args: tuple[str, ...],
) -> None:
    package = mypy_package
    target = package.workspace / "sample.py"
    before = b"value: int = 1\n"
    target.write_bytes(before)
    (package.workspace / "replacement.py").write_text("value = 2\n", encoding="utf-8")
    targets: tuple[Path, ...] = (target,)
    if args[0] == "--command":
        (package.workspace / "pyproject.toml").write_text("[tool.mypy]\n", encoding="utf-8")
        targets = ()
        assert native(package.workspace, "types", targets, args).returncode == 0
    code, response = invoke(package, "types", targets, args)
    assert code == 3 and decision(response)["reason"] == "unsupported_input"
    assert not (package.workspace / "forbidden.xml").exists()
    assert target.read_bytes() == before


def test_response_file_report_is_refused_before_native_output_write(
    mypy_package: MypyPackage,
) -> None:
    package = mypy_package
    target = package.workspace / "sample.py"
    target.write_text("value: int = 1\n", encoding="utf-8")
    options = package.workspace / "options.txt"
    options.write_text("--junit-xml\nforbidden.xml\n", encoding="utf-8")
    args = ("@" + str(options),)
    direct = native(package.workspace, "types", (target,), args)
    report = package.workspace / "forbidden.xml"
    assert direct.returncode == 0 and report.exists()
    report.unlink()
    code, response = invoke(package, "types", (target,), args)
    assert code == 3 and decision(response)["reason"] == "unsupported_input"
    assert not report.exists()


@pytest.mark.parametrize("setting", ['junit_xml = "forbidden.xml"', "install_types = true"])
def test_native_configuration_cannot_enable_check_writes(
    mypy_package: MypyPackage,
    setting: str,
) -> None:
    package = mypy_package
    target = package.workspace / "sample.py"
    target.write_text("value: int = 1\n", encoding="utf-8")
    (package.workspace / "pyproject.toml").write_text(
        "[tool.mypy]\n" + setting + "\n", encoding="utf-8"
    )
    code, response = invoke(package, "types", (target,))
    assert code == 3 and decision(response)["reason"] == "unsupported_input"
    assert not (package.workspace / "forbidden.xml").exists()


def test_missing_dependency_is_observed_in_selected_interpreter(
    mypy_package: MypyPackage,
) -> None:
    package = mypy_package
    environment = package.root.parent / "without mypy"
    venv.EnvBuilder(with_pip=False).create(environment)
    interpreter = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    code, response = invoke(package, "types", interpreter=interpreter)
    assert code == 3
    assert decision(response)["reason"] == "dependency_unavailable"
    assert response["external_tools"] == [{"tool_id": "mypy", "version": None}]


def test_request_rejection_preserves_protocol_details(mypy_package: MypyPackage) -> None:
    for payload, location, reason in (
        (b"{", [], "invalid_value"),
        (b"[]", [], "wrong_type"),
        (
            json.dumps(
                {
                    "execution_context": {"scratch_directory": str(mypy_package.workspace.parent)},
                    "operation": [],
                    "targets": [],
                    "args": [],
                }
            ).encode(),
            ["operation"],
            "wrong_type",
        ),
        (
            json.dumps(
                {
                    "execution_context": {"scratch_directory": str(mypy_package.workspace.parent)},
                    "operation": "types",
                    "targets": [42],
                    "args": [],
                }
            ).encode(),
            ["targets", 0],
            "wrong_type",
        ),
    ):
        code, response = invoke(mypy_package, "types", raw=payload)
        assert code == 2
        assert response == {
            "reason": "invalid_request",
            "details": [{"location": location, "code": reason}],
        }


@pytest.mark.parametrize("args", [("--help",), ("-h",), ("--version",), ("-V",)])
def test_native_metadata_exit_cannot_be_passed_type_analysis(
    mypy_package: MypyPackage,
    args: tuple[str, ...],
) -> None:
    package = mypy_package
    target = package.workspace / "negative.py"
    before = b'value: int = "bad"\n'
    target.write_bytes(before)
    direct = native(package.workspace, "types", (target,), args)
    assert direct.returncode == 0 and direct.stdout
    code, response = invoke(package, "types", (target,), args)
    assert code == 3 and decision(response)["reason"] == "unsupported_input"
    assert direct.stdout.decode().replace("\r\n", "\n") in evidence_text(response).replace(
        "\r\n", "\n"
    )
    assert target.read_bytes() == before


def test_declared_version_mismatch_stops_before_native_parser(
    mypy_package: MypyPackage,
) -> None:
    package = mypy_package
    (package.root / "requirements.txt").write_text("mypy==0.0.0\n", encoding="utf-8")
    code, response = invoke(package, "types", args=("--help",))
    assert code == 3 and decision(response)["reason"] == "dependency_unavailable"
    assert response["external_tools"] == [{"tool_id": "mypy", "version": "1.19.1"}]
    assert "0.0.0" in str(decision(response)["message"])


def test_argument_file_preserves_oversized_cross_file_analysis(
    mypy_package: MypyPackage,
) -> None:
    package = mypy_package
    targets = tuple(package.workspace / f"member_{index:03d}.py" for index in range(350))
    for target in targets:
        target.write_text("value: int = 1\n", encoding="utf-8")
    targets[0].write_text("def typed(value: int) -> int:\n    return value\n", encoding="utf-8")
    targets[-1].write_text(
        'from member_000 import typed\nwrong = typed("late error")\n', encoding="utf-8"
    )
    decoy = package.workspace / "unselected.py"
    decoy.write_text('value: int = "unselected error"\n', encoding="utf-8")
    command = subprocess.list2cmdline([str(path) for path in targets])
    assert len(command.encode("utf-16-le")) // 2 > 32767
    small_code, small = invoke(package, "types", (targets[0], targets[-1]))
    assert small_code == 1 and b"arg-type" in evidence_text(small).encode()
    code, response = invoke(package, "types", targets)
    assert code == 1 and decision(response)["status"] == "failed"
    evidence = evidence_text(response)
    assert targets[-1].name in evidence and "[arg-type]" in evidence
    assert "checked 350 source files" in evidence
    assert decoy.name not in evidence


@pytest.mark.parametrize("token", ["", " ", "#literal", " literal "])
def test_pinned_mypy_argument_file_preserves_option_value(
    mypy_package: MypyPackage,
    token: str,
) -> None:
    package = mypy_package
    target = package.workspace / "literal Ω with spaces.py"
    target.write_text('value: int = "bad"\n', encoding="utf-8")
    args = ("--exclude", token)
    direct = native(package.workspace, "types", (target,), args)
    code, response = invoke(package, "types", (target,), args)
    assert code == direct.returncode == 1
    assert_native_evidence(response, direct)


@pytest.mark.parametrize("separator", ["\n", "\v", "\u2028", "\ud800"])
def test_unrepresentable_mypy_argument_file_input_is_refused(
    mypy_package: MypyPackage,
    separator: str,
) -> None:
    package = mypy_package
    target = package.workspace / "clean.py"
    target.write_text("value: int = 1\n", encoding="utf-8")
    code, response = invoke(
        package, "types", (target,), ("--exclude", "line" + separator + "break")
    )
    assert code == 3 and decision(response)["reason"] == "unsupported_input"
