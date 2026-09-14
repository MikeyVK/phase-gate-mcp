"""Behavioral activation and process recovery evidence."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import pytest

from mcp_server.config.schemas.installation import InstallationState
from mcp_server.core.exceptions import MCPError
from mcp_server.services.installation_state import InstallationStateRepository
from mcp_server.services.template_activation import (
    ActivationFiles,
    TemplateActivationService,
    UpgradeLock,
)
from mcp_server.services.template_proposal import SuiteSnapshot
from mcp_server.utils.atomic_json_writer import AtomicJsonWriter
from tests.mcp_server.fixtures.suite_roots import write_package_tree
from tests.mcp_server.test_support import make_template_suite_admission

FP_CLOCK = datetime(2026, 9, 14, 12, 0, tzinfo=UTC)


@dataclass(frozen=True)
class ActivationCase:
    root: Path
    server: Path
    config: Path
    official_adapters: Path
    workspace_adapters: Path
    actual: Path
    candidate: Path
    proposal: Path


def _package_files(
    body: bytes,
    *,
    package_id: str = "demo",
    version: str = "1.0.0",
) -> dict[str, bytes]:
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "properties": {"value": {"type": "integer"}},
        "required": ["value"],
    }
    directory = package_id
    return {
        "shared/templates/base.jinja2": b"shared",
        f"{directory}/manifest.yaml": (
            f"template_id: {package_id}\npurpose: Activation test\n".encode()
        ),
        f"{directory}/.version": f"{version}\n".encode(),
        f"{directory}/policy.yaml": b"output_profile: text\npersistence: workspace\n",
        f"{directory}/context.schema.json": json.dumps(schema).encode(),
        f"{directory}/template.jinja2": body,
    }


def _write_config(case: ActivationCase) -> None:
    write_package_tree(
        case.config,
        {
            "adapters.yaml": b"trusted_adapter_ids: []\n",
            "checks.yaml": (
                b"checks:\n"
                b"  syntax:\n"
                b"    adapter_id: python_syntax\n"
                b"    capability: syntax\n"
                b"    timeout_seconds: 30\n"
                b"    default_args: []\n"
                b"profiles: {text: {checks: [syntax]}}\n"
                b"profiles_by_extension: {}\n"
                b"run_checks: {}\n"
            ),
        },
    )
    write_package_tree(
        case.official_adapters / "syntax",
        {
            "manifest.yaml": (
                b"adapter_id: python_syntax\nversion: 1.0.0\nfiles: [check.py]\n"
                b"roles:\n  check:\n    contract_version: 1\n"
                b"    entrypoint: {executable: unavailable_native, args: []}\n"
                b"    capabilities:\n"
                b"      syntax: {inputs: [content, selection], requires_file: false}\n"
            ),
            "check.py": (
                b"raise RuntimeError('activation admission must not execute native tools')\n"
            ),
        },
    )


@pytest.fixture
def activation_case(tmp_path: Path) -> ActivationCase:
    case = ActivationCase(
        root=tmp_path,
        server=tmp_path / ".pgmcp",
        config=tmp_path / "config",
        official_adapters=tmp_path / "official-adapters",
        workspace_adapters=tmp_path / "workspace-adapters",
        actual=tmp_path / ".pgmcp" / "template_suite",
        candidate=tmp_path / ".pgmcp" / "upgrade",
        proposal=tmp_path / "proposal",
    )
    case.server.mkdir()
    case.config.mkdir()
    case.official_adapters.mkdir()
    case.workspace_adapters.mkdir()
    _write_config(case)
    return case


def _admit(case: ActivationCase) -> Callable[[Path], SuiteSnapshot]:
    return make_template_suite_admission(
        case.config,
        official_adapter_root=case.official_adapters,
        workspace_adapter_root=case.workspace_adapters,
    )


def _publish_initial_state(case: ActivationCase, snapshot: SuiteSnapshot) -> None:
    repository = InstallationStateRepository(
        case.server / "installation.json",
        writer=AtomicJsonWriter().write_json,
    )
    repository.publish(
        InstallationState(
            pgmcp_version="3.0.0",
            template_checkpoint=snapshot.evidence.to_checkpoint(),
        )
    )


def _service(
    case: ActivationCase,
    *,
    json_writer: Callable[[Path, dict[str, object]], None] | None = None,
    move: Callable[[Path, Path], None] = os.replace,
) -> TemplateActivationService:
    writer = json_writer or AtomicJsonWriter().write_json
    repository = InstallationStateRepository(case.server / "installation.json", writer=writer)
    files = ActivationFiles(
        case.server,
        json_writer=writer,
        move=move,
        read_installation=repository.read,
    )
    assert files.paths.actual == case.server / "template_suite"
    assert files.paths.candidate == case.server / "upgrade"
    assert files.paths.next == case.server / "template_suite.next"
    assert files.paths.previous == case.server / "template_suite.previous"
    assert files.paths.installation == case.server / "installation.json"
    assert files.paths.record == case.server / "template_upgrade.json"
    assert files.paths.lock == case.server / "template_upgrade.lock"
    return TemplateActivationService(
        files,
        UpgradeLock(files.paths.lock),
        admit=_admit(case),
        clock=lambda: FP_CLOCK,
    )


def _tree_bytes(root: Path) -> dict[str, bytes]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def _prepare_transition(
    case: ActivationCase,
    *,
    actual_body: bytes = b"actual",
    candidate_body: bytes = b"candidate",
    proposal_body: bytes = b"candidate",
    proposal_version: str = "2.0.0",
) -> tuple[SuiteSnapshot, SuiteSnapshot]:
    write_package_tree(case.actual, _package_files(actual_body))
    write_package_tree(case.candidate, _package_files(candidate_body, version="2.0.0"))
    write_package_tree(case.proposal, _package_files(proposal_body, version=proposal_version))
    actual = _admit(case)(case.actual)
    _publish_initial_state(case, actual)
    candidate = _admit(case)(case.candidate)
    return actual, candidate


def _pause_after_boundary(
    stage: str,
    ready: Path,
    resume: Path,
    current: str,
) -> None:
    if stage != current:
        return
    ready.touch()
    deadline = time.monotonic() + 60
    while not resume.exists():
        if time.monotonic() >= deadline:
            raise TimeoutError(f"activation test did not resume at {stage}")
        time.sleep(0.02)


def _child_activation(
    server_root: str,
    config_root: str,
    official_adapter_root: str,
    workspace_adapter_root: str,
    proposal_root: str,
    stage: str,
    ready_path: str,
    resume_path: str,
    error_path: str | None = None,
) -> None:
    case = ActivationCase(
        root=Path(server_root).parent,
        server=Path(server_root),
        config=Path(config_root),
        official_adapters=Path(official_adapter_root),
        workspace_adapters=Path(workspace_adapter_root),
        actual=Path(server_root) / "template_suite",
        candidate=Path(server_root) / "upgrade",
        proposal=Path(proposal_root),
    )
    real_writer = AtomicJsonWriter().write_json
    ready = Path(ready_path)
    resume = Path(resume_path)

    def writer(path: Path, payload: dict[str, object]) -> None:
        real_writer(path, payload)
        if path == case.server / "template_upgrade.json":
            _pause_after_boundary(stage, ready, resume, "record")
        elif path == case.server / "installation.json":
            _pause_after_boundary(stage, ready, resume, "installation")

    def move(source: Path, target: Path) -> None:
        os.replace(source, target)
        if target == case.server / "template_suite.previous":
            _pause_after_boundary(stage, ready, resume, "actual_to_previous")
        elif target == case.server / "template_suite":
            _pause_after_boundary(stage, ready, resume, "next_to_actual")

    try:
        service = _service(case, json_writer=writer, move=move)
        service.activate(case.proposal, pgmcp_version="3.0.0")
    except BaseException as exc:
        if error_path is not None:
            Path(error_path).write_text(repr(exc), encoding="utf-8")
        raise


def _child_recover(
    server_root: str,
    config_root: str,
    official_adapter_root: str,
    workspace_adapter_root: str,
    report_path: str | None = None,
) -> None:
    case = ActivationCase(
        root=Path(server_root).parent,
        server=Path(server_root),
        config=Path(config_root),
        official_adapters=Path(official_adapter_root),
        workspace_adapters=Path(workspace_adapter_root),
        actual=Path(server_root) / "template_suite",
        candidate=Path(server_root) / "upgrade",
        proposal=Path(server_root).parent / "proposal",
    )
    try:
        _service(case).recover()
    except MCPError as exc:
        if report_path is not None:
            Path(report_path).write_text(
                json.dumps({"code": exc.code, "message": str(exc)}),
                encoding="utf-8",
            )
        raise
    else:
        if report_path is not None:
            Path(report_path).write_text(json.dumps({"recovered": True}), encoding="utf-8")


def _child_lock_probe(
    server_root: str,
    config_root: str,
    official_adapter_root: str,
    workspace_adapter_root: str,
    proposal_root: str,
    report_path: str,
) -> None:
    case = ActivationCase(
        root=Path(server_root).parent,
        server=Path(server_root),
        config=Path(config_root),
        official_adapters=Path(official_adapter_root),
        workspace_adapters=Path(workspace_adapter_root),
        actual=Path(server_root) / "template_suite",
        candidate=Path(server_root) / "upgrade",
        proposal=Path(proposal_root),
    )
    try:
        _service(case).activate(case.proposal, pgmcp_version="3.0.0")
    except MCPError as exc:
        Path(report_path).write_text(
            json.dumps({"code": exc.code, "message": str(exc)}),
            encoding="utf-8",
        )
    except BaseException as exc:
        Path(report_path).write_text(
            json.dumps({"exception": repr(exc)}),
            encoding="utf-8",
        )
        raise
    else:
        Path(report_path).write_text(json.dumps({"activated": True}), encoding="utf-8")


def _child_code(target: str) -> str:
    return (
        "import sys; "
        "from tests.mcp_server.integration.test_template_activation import "
        f"{target}; "
        f"{target}(*sys.argv[1:])"
    )


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _start_child(target: str, *args: str) -> subprocess.Popen[str]:
    return subprocess.Popen(
        [sys.executable, "-c", _child_code(target), *args],
        cwd=_repo_root(),
        text=True,
    )


def _wait_for_file(path: Path, timeout: float = 15) -> bool:
    deadline = time.monotonic() + timeout
    while not path.exists() and time.monotonic() < deadline:
        time.sleep(0.02)
    return path.exists()


def _terminate(process: subprocess.Popen[str]) -> None:
    if process.poll() is None:
        process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)
    assert process.poll() is not None


def _recover_in_fresh_process(
    case: ActivationCase,
    report_path: Path | None = None,
) -> subprocess.Popen[str]:
    args = [
        str(case.server),
        str(case.config),
        str(case.official_adapters),
        str(case.workspace_adapters),
    ]
    if report_path is not None:
        args.append(str(report_path))
    process = _start_child("_child_recover", *args)
    process.wait(timeout=20)
    return process


def test_fresh_activation_publishes_coherent_pair(activation_case: ActivationCase) -> None:
    case = activation_case
    write_package_tree(case.candidate, _package_files(b"candidate", version="2.0.0"))
    write_package_tree(case.proposal, _package_files(b"candidate", version="2.0.0"))
    expected = _admit(case)(case.candidate)

    service = _service(case)
    service.activate(case.proposal, pgmcp_version="3.0.0", fresh=True)

    installed = _admit(case)(case.actual)
    state = InstallationStateRepository(
        case.server / "installation.json",
        writer=AtomicJsonWriter().write_json,
    ).read()
    assert installed.evidence.to_checkpoint() == expected.evidence.to_checkpoint()
    assert state is not None
    assert state.template_checkpoint == expected.evidence.to_checkpoint()
    assert state.pgmcp_version == "3.0.0"
    assert not (case.server / "template_upgrade.json").exists()
    assert not (case.server / "template_suite.next").exists()
    assert not (case.server / "template_suite.previous").exists()
    assert not case.candidate.exists()
    assert service.last_result is not None
    assert service.last_result.outcome == "activated"


def test_forced_activation_keeps_verified_backup(activation_case: ActivationCase) -> None:
    case = activation_case
    actual, candidate = _prepare_transition(case)
    prior_tree = _tree_bytes(case.actual)
    prior_installation = (case.server / "installation.json").read_bytes()

    service = _service(case)
    collision = case.server.parent / (
        f".pgmcp_template_backup_{FP_CLOCK.strftime('%Y%m%dT%H%M%S%fZ')}"
    )
    collision.mkdir()
    with pytest.raises(FileExistsError):
        service.activate(case.proposal, pgmcp_version="3.0.0", force=True)
    assert _tree_bytes(case.actual) == prior_tree
    assert (case.server / "installation.json").read_bytes() == prior_installation
    assert not (case.server / "template_upgrade.json").exists()
    assert not (case.server / "template_suite.next").exists()
    collision.rmdir()
    service.activate(case.proposal, pgmcp_version="3.0.0", force=True)

    assert _tree_bytes(case.actual) == _tree_bytes(case.proposal)
    state = InstallationStateRepository(
        case.server / "installation.json",
        writer=AtomicJsonWriter().write_json,
    ).read()
    assert state is not None
    assert state.template_checkpoint == candidate.evidence.to_checkpoint()
    result = service.last_result
    assert result is not None
    assert result.outcome == "activated"
    assert result.backup_path is not None
    backup = result.backup_path
    assert backup.is_dir()
    assert backup.parent == case.server.parent
    assert _tree_bytes(backup / "template_suite") == prior_tree
    assert (backup / "installation.json").read_bytes() == prior_installation
    assert actual.evidence.to_checkpoint() != candidate.evidence.to_checkpoint()


def test_local_content_retains_adopted_checkpoint(activation_case: ActivationCase) -> None:
    case = activation_case
    baseline_root = case.root / "baseline"
    write_package_tree(baseline_root, _package_files(b"baseline"))
    write_package_tree(case.actual, _package_files(b"local customization"))
    write_package_tree(case.candidate, _package_files(b"upstream update", version="2.0.0"))
    write_package_tree(case.proposal, _package_files(b"local customization"))
    baseline = _admit(case)(baseline_root)
    _publish_initial_state(case, baseline)
    adopted_state = InstallationStateRepository(
        case.server / "installation.json",
        writer=AtomicJsonWriter().write_json,
    ).read()
    assert adopted_state is not None

    service = _service(case)
    service.activate(case.proposal, pgmcp_version="3.0.0")

    current = InstallationStateRepository(
        case.server / "installation.json",
        writer=AtomicJsonWriter().write_json,
    ).read()
    assert current == adopted_state, (
        f"adopted={adopted_state.model_dump(mode='json')} "
        f"current={None if current is None else current.model_dump(mode='json')}"
    )
    assert _tree_bytes(case.actual) == _tree_bytes(case.proposal)
    assert case.candidate.exists()
    assert service.last_result is not None
    assert service.last_result.candidate_retained is True


@pytest.mark.parametrize(
    "stage",
    ["record", "actual_to_previous", "next_to_actual", "installation"],
)
def test_interruption_recovers_pair_in_fresh_process(
    activation_case: ActivationCase,
    stage: str,
) -> None:
    case = activation_case
    _, candidate = _prepare_transition(case)
    prior_tree = _tree_bytes(case.actual)
    prior_installation = (case.server / "installation.json").read_bytes()
    target_tree = _tree_bytes(case.proposal)
    target_state = InstallationState(
        pgmcp_version="3.0.0",
        template_checkpoint=candidate.evidence.to_checkpoint(),
    )

    ready = case.root / f"activation-child-{stage}.ready"
    resume = case.root / f"activation-child-{stage}.resume"
    error_path = case.root / f"activation-child-{stage}.error"
    process = _start_child(
        "_child_activation",
        str(case.server),
        str(case.config),
        str(case.official_adapters),
        str(case.workspace_adapters),
        str(case.proposal),
        stage,
        str(ready),
        str(resume),
        str(error_path),
    )
    try:
        assert _wait_for_file(ready, 8), (
            f"child did not reach activation boundary {stage}; "
            f"returncode={process.poll()} "
            f"error={error_path.read_text(encoding='utf-8') if error_path.exists() else 'none'}"
        )
        _terminate(process)
    finally:
        resume.touch()
        if process.poll() is None:
            _terminate(process)

    recovery = _recover_in_fresh_process(case)
    assert recovery.returncode == 0

    if stage == "installation":
        assert _tree_bytes(case.actual) == target_tree
        state = InstallationStateRepository(
            case.server / "installation.json",
            writer=AtomicJsonWriter().write_json,
        ).read()
        assert state == target_state
    else:
        assert _tree_bytes(case.actual) == prior_tree
        assert (case.server / "installation.json").read_bytes() == prior_installation


def test_unknown_recovery_state_is_preserved(activation_case: ActivationCase) -> None:
    case = activation_case
    _prepare_transition(case)
    ready = case.root / "unknown-child.ready"
    resume = case.root / "unknown-child.resume"
    error_path = case.root / "unknown-child.error"
    process = _start_child(
        "_child_activation",
        str(case.server),
        str(case.config),
        str(case.official_adapters),
        str(case.workspace_adapters),
        str(case.proposal),
        "actual_to_previous",
        str(ready),
        str(resume),
        str(error_path),
    )
    try:
        assert _wait_for_file(ready, 8), (
            f"child did not reach unknown-state boundary; returncode={process.poll()} "
            f"error={error_path.read_text(encoding='utf-8') if error_path.exists() else 'none'}"
        )
        _terminate(process)
    finally:
        resume.touch()
        if process.poll() is None:
            _terminate(process)

    write_package_tree(case.actual, {"unknown.txt": b"unknown durable state"})
    before = {
        "actual": _tree_bytes(case.actual),
        "previous": _tree_bytes(case.server / "template_suite.previous"),
        "record": (case.server / "template_upgrade.json").read_bytes(),
        "installation": (case.server / "installation.json").read_bytes(),
    }
    report = case.root / "unknown-recovery.json"
    recovery = _start_child(
        "_child_recover",
        str(case.server),
        str(case.config),
        str(case.official_adapters),
        str(case.workspace_adapters),
        str(report),
    )
    recovery.wait(timeout=20)
    assert recovery.returncode != 0
    assert _tree_bytes(case.actual) == before["actual"]
    assert _tree_bytes(case.server / "template_suite.previous") == before["previous"]
    assert (case.server / "template_upgrade.json").read_bytes() == before["record"]
    assert (case.server / "installation.json").read_bytes() == before["installation"]


def test_cross_process_activation_lock_excludes_second_activation(
    activation_case: ActivationCase,
) -> None:
    case = activation_case
    _prepare_transition(case)
    ready = case.root / "lock-child.ready"
    resume = case.root / "lock-child.resume"
    error_path = case.root / "lock-child.error"
    first = _start_child(
        "_child_activation",
        str(case.server),
        str(case.config),
        str(case.official_adapters),
        str(case.workspace_adapters),
        str(case.proposal),
        "record",
        str(ready),
        str(resume),
        str(error_path),
    )
    second_report = case.root / "second-lock.json"
    try:
        assert _wait_for_file(ready, 8), (
            f"child did not reach lock boundary; returncode={first.poll()} "
            f"error={error_path.read_text(encoding='utf-8') if error_path.exists() else 'none'}"
        )
        second = _start_child(
            "_child_lock_probe",
            str(case.server),
            str(case.config),
            str(case.official_adapters),
            str(case.workspace_adapters),
            str(case.proposal),
            str(second_report),
        )
        second.wait(timeout=15)
        report = json.loads(second_report.read_text(encoding="utf-8"))
        if (report.get("code"), report.get("message")) != ("ERR_CONFIG", "template_upgrade_locked"):
            pytest.fail(f"second activation report={report}; first_returncode={first.poll()}")
    finally:
        resume.touch()
        _terminate(first)
