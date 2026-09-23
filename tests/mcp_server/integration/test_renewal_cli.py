"""Public renewal CLI behavior through the real composition root."""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from io import StringIO
from pathlib import Path

import pytest

from mcp_server.cli_renewal import RenewalCli, build_default_operation
from mcp_server.config.settings import ServerSettings, Settings
from mcp_server.services.installation_state import InstallationStateRepository
from mcp_server.services.template_activation import (
    ActivationFiles,
    TemplateActivationService,
    UpgradeLock,
)
from mcp_server.services.template_renewal import RenewalResult, TemplateRenewalService
from mcp_server.utils.atomic_json_writer import AtomicJsonWriter
from tests.mcp_server.test_support import make_template_suite_admission


@dataclass(frozen=True)
class RenewalCase:
    workspace: Path
    server: Path
    config: Path
    source: Path
    actual: Path
    candidate: Path
    external_actual: Path


def _copy_suite(source: Path, target: Path) -> Path:
    target.mkdir(parents=True)
    for component in ("issue", "shared"):
        shutil.copytree(source / component, target / component)
    return target


def _append(path: Path, marker: bytes) -> None:
    path.write_bytes(path.read_bytes() + marker)


@pytest.fixture
def renewal_case(tmp_path: Path, pytestconfig: pytest.Config) -> RenewalCase:
    repository = pytestconfig.rootpath
    source = _copy_suite(
        repository / ".pgmcp" / "template_suite",
        tmp_path / "release-v1" / "template_suite",
    )
    config = tmp_path / "config"
    config.mkdir()
    for name in ("checks.yaml", "adapters.yaml"):
        shutil.copy2(repository / ".pgmcp" / "config" / name, config / name)
    server = tmp_path / ".pgmcp"
    server.mkdir()
    return RenewalCase(
        workspace=tmp_path,
        server=server,
        config=config,
        source=source,
        actual=server / "template_suite",
        candidate=server / "upgrade",
        external_actual=tmp_path / "external-template-suite",
    )


def _settings(case: RenewalCase, *, external: bool = False) -> Settings:
    return Settings(
        server=ServerSettings(
            workspace_root=str(case.workspace),
            config_root=str(case.config),
            template_root=str(case.external_actual) if external else None,
        )
    )


def _run(
    case: RenewalCase,
    *args: str,
    supplied: Path | None = None,
    external: bool = False,
) -> tuple[int, str, str, TemplateRenewalService]:
    operation = build_default_operation(
        _settings(case, external=external),
        supplied_candidate_root=supplied,
    )
    stdout = StringIO()
    stderr = StringIO()
    code = RenewalCli(
        operation=operation,
        stdout=stdout,
        stderr=stderr,
    ).run(["--upgrade", *args])
    return code, stdout.getvalue(), stderr.getvalue(), operation


def _stage(case: RenewalCase, source: Path) -> None:
    shutil.copytree(source, case.candidate)


def _result(operation: TemplateRenewalService) -> RenewalResult:
    result = getattr(operation, "last_result", None)
    assert isinstance(result, RenewalResult)
    return result


def _tree_bytes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def test_modifiers_are_mutually_exclusive_on_real_operation(renewal_case: RenewalCase) -> None:
    code, _out, err, operation = _run(
        renewal_case,
        "--accept-template-baseline",
        "--force-template-upgrade",
        supplied=renewal_case.source,
    )

    assert code == 2
    assert getattr(operation, "last_result", None) is None
    assert "not allowed" in err


def test_fresh_install_then_normal_upstream_upgrade(renewal_case: RenewalCase) -> None:
    code, _out, _err, operation = _run(
        renewal_case,
        supplied=renewal_case.source,
    )

    assert code == 0
    assert _result(operation).outcome == "fresh_installed"
    installed_before = _tree_bytes(renewal_case.actual)

    upgraded = _copy_suite(
        renewal_case.source,
        renewal_case.workspace / "release-v2" / "template_suite",
    )
    _append(upgraded / "issue" / "template.jinja2", b"\n{# upstream-v2 #}\n")
    code, _out, _err, operation = _run(renewal_case, supplied=upgraded)

    assert code == 0
    assert _result(operation).outcome == "activated"
    assert _tree_bytes(renewal_case.actual) != installed_before
    assert b"upstream-v2" in (renewal_case.actual / "issue" / "template.jinja2").read_bytes()


def test_checkpointless_baseline_publishes_checkpoint_without_copying(
    renewal_case: RenewalCase,
) -> None:
    _copy_suite(renewal_case.source, renewal_case.actual)
    before = _tree_bytes(renewal_case.actual)
    staged = _copy_suite(
        renewal_case.source,
        renewal_case.workspace / "release-baseline" / "template_suite",
    )
    _append(staged / "issue" / "template.jinja2", b"\n{# candidate-baseline #}\n")
    _stage(renewal_case, staged)

    code, _out, _err, operation = _run(
        renewal_case,
        "--accept-template-baseline",
    )

    assert code == 0
    assert _result(operation).outcome == "baseline_established"
    assert _tree_bytes(renewal_case.actual) == before
    assert not renewal_case.candidate.exists()
    assert (renewal_case.server / "installation.json").is_file()


def test_checkpointless_external_root_requires_action_and_rejects_force(
    renewal_case: RenewalCase,
) -> None:
    _copy_suite(renewal_case.source, renewal_case.external_actual)
    before = _tree_bytes(renewal_case.external_actual)
    candidate = _copy_suite(
        renewal_case.source,
        renewal_case.workspace / "release-external" / "template_suite",
    )
    _append(candidate / "issue" / "template.jinja2", b"\n{# external-candidate #}\n")
    _stage(renewal_case, candidate)

    code, out, err, operation = _run(renewal_case, external=True, supplied=renewal_case.source)
    assert code == 2
    assert _result(operation).outcome == "checkpoint_required"
    assert _tree_bytes(renewal_case.external_actual) == before
    assert "baseline" in out.lower()

    code, out, err, operation = _run(
        renewal_case,
        "--force-template-upgrade",
        external=True,
    )
    assert code == 1
    assert _result(operation).failure_code == "external_root_force_forbidden"
    assert "external" in (out + err).lower()
    assert _tree_bytes(renewal_case.external_actual) == before


def test_checkpointless_force_keeps_verified_backup_bytes(renewal_case: RenewalCase) -> None:
    _copy_suite(renewal_case.source, renewal_case.actual)
    before = _tree_bytes(renewal_case.actual)
    staged = _copy_suite(
        renewal_case.source,
        renewal_case.workspace / "release-force" / "template_suite",
    )
    _append(staged / "issue" / "template.jinja2", b"\n{# forced-v2 #}\n")
    _stage(renewal_case, staged)

    code, _out, _err, operation = _run(
        renewal_case,
        "--force-template-upgrade",
    )

    assert code == 0
    result = _result(operation)
    assert result.outcome == "forced_candidate_installed"
    assert result.backup_path is not None
    assert _tree_bytes(result.backup_path / "template_suite") == before
    assert not renewal_case.candidate.exists()


def test_conflict_resolution_uses_persisted_checkpoint_and_keeps_remaining_conflict(
    renewal_case: RenewalCase,
) -> None:
    code, _out, _err, operation = _run(renewal_case, supplied=renewal_case.source)
    assert code == 0
    assert _result(operation).outcome == "fresh_installed"

    _append(renewal_case.actual / "issue" / "template.jinja2", b"\n{# local-issue #}\n")
    _append(
        renewal_case.actual / "shared" / "templates" / "bases" / "tier2_markdown_tracking.jinja2",
        b"\n{# local-shared #}\n",
    )
    before = _tree_bytes(renewal_case.actual)
    upgraded = _copy_suite(
        renewal_case.source,
        renewal_case.workspace / "release-conflict" / "template_suite",
    )
    _append(upgraded / "issue" / "template.jinja2", b"\n{# upstream-issue #}\n")
    _append(
        upgraded / "shared" / "templates" / "bases" / "tier2_markdown_tracking.jinja2",
        b"\n{# upstream-shared #}\n",
    )

    code, _out, _err, operation = _run(renewal_case, supplied=upgraded)
    assert code == 2
    result = _result(operation)
    assert result.outcome == "activated_with_conflicts"
    assert _tree_bytes(renewal_case.actual) == before
    assert renewal_case.candidate.exists()

    code, out, err, operation = _run(renewal_case, "--resolve-template", "issue")
    assert code == 2
    result = _result(operation)
    assert result.outcome == "reconciliation_completed"
    assert "shared" in (out + err).lower()
    assert _tree_bytes(renewal_case.actual) == before
    assert renewal_case.candidate.exists()

    code, _out, _err, operation = _run(renewal_case, "--resolve-template", "shared")
    assert code == 0
    assert _result(operation).outcome == "reconciliation_completed"
    assert not renewal_case.candidate.exists()
    assert _tree_bytes(renewal_case.actual) == before


def test_busy_and_invalid_profile_are_actionable(renewal_case: RenewalCase) -> None:
    _copy_suite(renewal_case.source, renewal_case.actual)
    _stage(renewal_case, renewal_case.source)
    holder = UpgradeLock(renewal_case.server / "template_upgrade.lock")
    holder.acquire()
    try:
        code, out, err, operation = _run(renewal_case)
    finally:
        holder.release()

    assert code == 2
    assert _result(operation).outcome == "upgrade_busy"
    assert "template_upgrade_locked" in (out + err)

    invalid = _copy_suite(
        renewal_case.source,
        renewal_case.workspace / "release-invalid" / "template_suite",
    )
    _append(invalid / "issue" / "policy.yaml", b"\noutput_profile: missing_profile\n")
    code, out, err, operation = _run(renewal_case, supplied=invalid)
    assert code == 1
    result = _result(operation)
    assert result.outcome == "candidate_invalid"
    rendered = (out + err).lower()
    assert "issue" in rendered
    assert "missing_profile" in rendered
    assert "checks.yaml" in rendered


def test_completed_recovery_without_changes_omits_restart(
    renewal_case: RenewalCase,
    pytestconfig: pytest.Config,
) -> None:
    case = renewal_case
    code, _out, _err, _operation = _run(case, supplied=case.source)
    assert code == 0
    before = _tree_bytes(case.actual)
    before_installation = (case.server / "installation.json").read_bytes()
    _stage(case, case.source)
    writer = AtomicJsonWriter().write_json
    repository = InstallationStateRepository(case.server / "installation.json", writer=writer)

    def publish_then_interrupt(path: Path, payload: dict[str, object]) -> None:
        writer(path, payload)
        if path == case.server / "installation.json":
            raise OSError("simulated_interruption_after_publication")

    files = ActivationFiles(
        case.server,
        json_writer=publish_then_interrupt,
        move=os.replace,
        read_installation=repository.read,
    )
    activation = TemplateActivationService(
        files,
        UpgradeLock(files.paths.lock),
        admit=make_template_suite_admission(
            case.config,
            official_adapter_root=pytestconfig.rootpath / "mcp_server" / "bundled_adapters",
            workspace_adapter_root=case.server / "workspace_adapters",
        ),
        clock=lambda: datetime.now(UTC),
    )
    with pytest.raises(OSError, match="simulated_interruption_after_publication"):
        activation.activate(case.candidate, pgmcp_version=_settings(case).server.version)
    assert files.paths.record.exists()

    code, out, _err, operation = _run(case)
    assert code == 0
    result = _result(operation)
    assert result.actual_changed is False
    assert result.checkpoint_effect == "unchanged"
    assert "Restart any running" not in out
    assert _tree_bytes(case.actual) == before
    assert (case.server / "installation.json").read_bytes() == before_installation
    assert not files.paths.record.exists()


def test_first_legacy_upgrade_requires_owner_migration(renewal_case: RenewalCase) -> None:
    """Existing legacy bytes require a staged decision and verified force backup."""
    legacy_root = renewal_case.server / "templates"
    legacy_root.mkdir()
    legacy_file = legacy_root / "owner-customization.txt"
    empty_dir = legacy_root / "empty-owner-directory"
    empty_dir.mkdir()
    original = b"owner customization must survive migration\n"
    legacy_file.write_bytes(original)
    (renewal_case.server / ".version").write_text("2.0.0\n", encoding="utf-8")

    code, _out, _err, operation = _run(renewal_case, supplied=renewal_case.source)
    assert code == 2
    assert _result(operation).outcome == "checkpoint_required"
    assert legacy_file.read_bytes() == original
    assert not renewal_case.actual.exists()
    assert not (renewal_case.server / "installation.json").exists()

    code, out, err, operation = _run(renewal_case, "--force-template-upgrade")
    result = _result(operation)
    assert code == 0, out + err
    assert result.outcome == "forced_candidate_installed"
    assert result.backup_path is not None
    assert any(
        path.read_bytes() == original
        for path in result.backup_path.rglob("owner-customization.txt")
    )
    assert (result.backup_path / "legacy" / "templates" / empty_dir.name).is_dir()
    assert legacy_file.read_bytes() == original
    assert renewal_case.actual.is_dir()
    assert (renewal_case.server / "installation.json").is_file()
