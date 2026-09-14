"""Observe unchanged rendering, check facts, and actual create-only filesystem outcomes."""

from __future__ import annotations

import json
import os
import shutil
from collections.abc import Callable
from copy import deepcopy
from pathlib import Path
from typing import Literal

import pytest
from jinja2 import TemplateRuntimeError
from pydantic import ValidationError

from mcp_server.config.schemas.artifact_locations import ArtifactLocationsConfig
from mcp_server.core.interfaces.template_catalog import FrozenJsonObject, thaw_json
from mcp_server.schemas.mutation_outputs import ScaffoldOperationOutput
from mcp_server.services.artifact_identity import ArtifactIdentity
from mcp_server.services.artifact_target_resolver import ArtifactTargetResolver
from mcp_server.services.scaffold_operation import ScaffoldOperation
from mcp_server.utils.atomic_file_writer import CreateOnlyFileWriter
from mcp_server.utils.path_resolver import FileArtifactTargetPaths, resolve_temporary_paths
from tests.mcp_server.fixtures.delivered_templates import DeliveredTemplate, load_delivered_template
from tests.mcp_server.unit.execution.test_check_service import RecordingRuntime, compose


@pytest.fixture
def delivered(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredTemplate:
    suite = pytestconfig.rootpath / ".pgmcp/template_suite"
    return load_delivered_template(
        source_suite=suite,
        source_package=suite / "issue",
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "suite",
        template_id="issue",
    )


def operation(
    root: Path,
    delivered: DeliveredTemplate,
    outcomes: tuple[str, ...],
    *,
    render: Callable[[str, object, FrozenJsonObject], str] | None = None,
    write_scratch: Callable[[Path, bytes], int] | None = None,
    remove_scratch: Callable[[Path], None] = shutil.rmtree,
) -> tuple[ScaffoldOperation, RecordingRuntime]:
    profile = delivered.catalog.get("issue").policy.output_profile
    checks, _, runtime = compose(
        root,
        outcomes,
        profile_id=profile,
        file_content=write_scratch is not None,
        write_bytes=write_scratch if write_scratch is not None else Path.write_bytes,
        remove_tree=remove_scratch,
    )
    locations = ArtifactLocationsConfig.model_validate(
        {"version": "2.0.0", "artifacts": {"issue": {"default_root": "outputs"}}}
    )
    resolver = ArtifactTargetResolver(
        paths=FileArtifactTargetPaths(root),
        temporary_artifacts_root=resolve_temporary_paths(root / "server").artifacts_root,
        locations=locations,
    )
    identity = ArtifactIdentity.model_validate(thaw_json(delivered.provenance))
    return ScaffoldOperation(
        catalog=delivered.catalog,
        identities=(identity,),
        targets=resolver,
        render=render if render is not None else delivered.renderer.render,
        checks=checks,
        creator=CreateOnlyFileWriter(),
        workspace_root=root,
    ), runtime


@pytest.mark.asyncio
@pytest.mark.parametrize("policy", ["enforce", "report"])
@pytest.mark.parametrize(
    ("outcomes", "status"),
    [
        (("passed",), "passed"),
        (("failed", "unavailable", "passed"), "failed"),
        (("unavailable",), "unavailable"),
        (("cancelled",), "not_executed"),
    ],
)
async def test_validation_policy_preserves_facts_and_exact_saved_bytes(
    tmp_path: Path,
    delivered: DeliveredTemplate,
    policy: Literal["enforce", "report"],
    outcomes: tuple[str, ...],
    status: str,
) -> None:
    service, runtime = operation(tmp_path, delivered, outcomes)
    context = {"problem": "Caller text\r\nwith a second line", "context": ""}
    original = deepcopy(context)
    filename = "MiXeD release.v2.md"
    result = await service.execute(
        artifact_type="issue",
        file_name=filename,
        context=context,
        validation=policy,
    )
    written = status == "passed" or (policy == "report" and status in {"failed", "unavailable"})
    assert (result.success, result.written) == (written, written)
    assert result.validation_policy == policy
    assert result.validation_status == status
    assert result.output_path == f"outputs/{filename}"
    assert context == original
    assert len(runtime.requests) == len(outcomes)
    assert [row.check_id for row in result.checks] == [
        f"check_{index}" for index in range(len(outcomes))
    ]
    assert all(row.args_source == "configured" for row in result.checks)
    assert result.checks[0].effective_args == ("check_0",)
    assert result.checks[0].invocation is not None
    assert result.output_path is not None
    target = tmp_path / result.output_path
    if written:
        expected = delivered.renderer.render("issue", context, delivered.provenance)
        assert target.read_bytes() == expected.encode("utf-8")
        assert result.error_code is None and result.error_details is None
    else:
        assert not target.exists()
        assert result.error_code in {"validation_blocked", "operation_interrupted"}
    if len(outcomes) == 3:
        assert [row.status for row in result.checks] == ["failed", "unavailable", "passed"]
        assert result.checks[0].message == "Native observation"
        assert result.checks[0].evidence is not None
    payload = result.model_dump(mode="json")
    assert "error_details" in payload and "profile_id" in payload
    if policy == "enforce" and status == "passed":
        assert ScaffoldOperationOutput.model_validate_json(json.dumps(payload)) == result
        missing_arguments = deepcopy(payload)
        missing_arguments["checks"][0].update(args_source=None, effective_args=None)
        with pytest.raises(ValidationError, match="attempt_argument_facts_required"):
            ScaffoldOperationOutput.model_validate_json(json.dumps(missing_arguments))
        for replacement in ({"written": not written}, {"error_details": {}}, {"unexpected": True}):
            with pytest.raises(ValidationError):
                ScaffoldOperationOutput.model_validate_json(json.dumps({**payload, **replacement}))


@pytest.mark.asyncio
@pytest.mark.parametrize("when", ["early", "late"])
async def test_collisions_preserve_competing_bytes_and_observed_validation(
    tmp_path: Path,
    delivered: DeliveredTemplate,
    monkeypatch: pytest.MonkeyPatch,
    when: str,
) -> None:
    service, runtime = operation(tmp_path, delivered, ("passed",))
    target = tmp_path / "outputs" / "result.md"
    competing = b"Concurrent caller bytes\r\n"
    if when == "early":
        target.parent.mkdir()
        target.write_bytes(competing)
    else:
        original_link = os.link

        def competing_link(source: Path, destination: Path) -> None:
            destination.write_bytes(competing)
            original_link(source, destination)

        monkeypatch.setattr("mcp_server.utils.atomic_file_writer.os.link", competing_link)
    result = await service.execute(
        artifact_type="issue",
        file_name=target.name,
        context={"problem": "Caller"},
        target_path="outputs",
        force_target=True,
        validation="report",
    )
    assert not result.success and not result.written
    assert result.error_code == "target_exists"
    assert result.output_path == "outputs/result.md"
    assert result.error_details is not None
    assert result.error_details.model_dump()["path"] == "outputs/result.md"
    assert target.read_bytes() == competing
    assert result.validation_status == ("not_executed" if when == "early" else "passed")
    assert len(runtime.requests) == (0 if when == "early" else 1)
    assert list(target.parent.iterdir()) == [target]


@pytest.mark.asyncio
@pytest.mark.parametrize("failure", ["context", "render"])
async def test_precheck_failures_do_not_invoke_or_create(
    tmp_path: Path,
    delivered: DeliveredTemplate,
    failure: str,
) -> None:
    def broken_render(
        _template_id: str,
        _context: object,
        _provenance: FrozenJsonObject,
    ) -> str:
        raise TemplateRuntimeError("render boundary failed")

    service, runtime = operation(
        tmp_path,
        delivered,
        ("passed",),
        render=broken_render if failure == "render" else None,
    )
    context: object = {"problem": 42} if failure == "context" else {"problem": "Caller"}
    result = await service.execute(
        artifact_type="issue",
        file_name="result.md",
        context=context,
        validation="report",
    )
    assert result.error_code == ("context_invalid" if failure == "context" else "render_failed")
    assert result.validation_status == "not_executed" and result.checks == ()
    assert not result.written and not (tmp_path / "outputs" / "result.md").exists()
    assert runtime.requests == []


@pytest.mark.asyncio
@pytest.mark.parametrize("fault", ["write", "write_cleanup", "cleanup", "acquisition"])
async def test_staging_failures_keep_write_and_cleanup_facts_separate(
    tmp_path: Path,
    delivered: DeliveredTemplate,
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
) -> None:
    service, _ = operation(tmp_path, delivered, ("passed",))
    original_open, original_write, original_unlink = os.open, os.write, Path.unlink
    staged: list[Path] = []
    owned: set[int] = set()
    foreign = b"Other writer owns these bytes"

    def stage_open(path: Path, flags: int, mode: int = 0o777) -> int:
        staged.append(Path(path))
        if fault == "acquisition":
            Path(path).write_bytes(foreign)
        descriptor = original_open(path, flags, mode)
        owned.add(descriptor)
        return descriptor

    def stage_write(descriptor: int, content: bytes) -> int:
        assert descriptor in owned
        if fault in ("write", "write_cleanup"):
            original_write(descriptor, content[:3])
            raise OSError("staging write interrupted")
        return original_write(descriptor, content)

    def stage_unlink(path: Path, *, missing_ok: bool = False) -> None:
        if fault in ("write_cleanup", "cleanup") and path in staged:
            raise PermissionError("staging cleanup refused")
        original_unlink(path, missing_ok=missing_ok)

    monkeypatch.setattr(os, "open", stage_open)
    monkeypatch.setattr(os, "write", stage_write)
    monkeypatch.setattr(Path, "unlink", stage_unlink)
    context = {"problem": "Caller"}
    result = await service.execute(
        artifact_type="issue",
        file_name="result.md",
        context=context,
    )
    target = tmp_path / "outputs" / "result.md"
    assert result.validation_status == "passed"
    assert result.written == (fault == "cleanup")
    assert result.success == result.written
    assert result.error_code == (None if result.written else "persistence_failed")
    if result.written:
        assert target.read_bytes() == delivered.renderer.render(
            "issue", context, delivered.provenance
        ).encode("utf-8")
    else:
        assert not target.exists()
    if fault == "acquisition":
        assert staged[0].read_bytes() == foreign
        assert result.housekeeping == () and owned == set()
    elif fault == "write":
        assert result.housekeeping == ()
        assert not staged[0].exists()
    else:
        assert staged[0].exists()
        assert result.housekeeping[0].purpose == "write_staging"
        assert result.housekeeping[0].path == staged[0].relative_to(tmp_path).as_posix()


@pytest.mark.asyncio
async def test_preparation_failure_retains_its_stage_without_writing(
    tmp_path: Path,
    delivered: DeliveredTemplate,
) -> None:
    def failed_write(_path: Path, _content: bytes) -> int:
        raise PermissionError("scratch write refused")

    def failed_cleanup(_path: Path) -> None:
        raise PermissionError("scratch cleanup refused")

    service, runtime = operation(
        tmp_path,
        delivered,
        ("passed",),
        write_scratch=failed_write,
        remove_scratch=failed_cleanup,
    )
    result = await service.execute(
        artifact_type="issue",
        file_name="result.md",
        context={"problem": "Caller"},
        validation="report",
    )
    assert result.error_code == "preparation_failed"
    assert result.error_details is not None
    assert result.error_details.model_dump()["reason"] == "validation_input_write_failed"
    assert result.error_details.model_dump()["path"] == "outputs/result.md"
    assert not result.written and runtime.requests == []
    assert result.checks[0].invocation is None
    assert result.checks[0].housekeeping[0].purpose == "validation_input"
    assert result.checks[0].housekeeping[0].path == "scratch/one"
    assert (tmp_path / "scratch" / "one").is_dir()
    assert not (tmp_path / "outputs" / "result.md").exists()


@pytest.mark.asyncio
@pytest.mark.parametrize("stop", ["invalid_request", "unconfirmed"])
async def test_operation_blockers_retain_prior_and_unstarted_checks(
    tmp_path: Path,
    delivered: DeliveredTemplate,
    stop: str,
) -> None:
    policies: tuple[Literal["enforce", "report"], ...] = ("enforce", "report")
    for policy in policies:
        root = tmp_path / policy
        root.mkdir()
        service, runtime = operation(root, delivered, ("failed", stop, "passed"))
        result = await service.execute(
            artifact_type="issue",
            file_name="result.md",
            context={"problem": "Caller"},
            validation=policy,
        )
        assert result.error_code == (
            "adapter_request_rejected" if stop == "invalid_request" else "termination_unconfirmed"
        )
        assert result.validation_status == "failed"
        assert [row.status for row in result.checks] == [
            "failed",
            "not_executed" if stop == "invalid_request" else "unavailable",
            "not_executed",
        ]
        assert result.checks[-1].reason == "not_started"
        assert len(runtime.requests) == 2
        assert not result.written and not (root / "outputs" / "result.md").exists()


@pytest.mark.asyncio
async def test_postcommit_result_failure_does_not_undo_created_bytes(
    tmp_path: Path,
    delivered: DeliveredTemplate,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, _ = operation(tmp_path, delivered, ("passed",))

    def fail_result(**fields: object) -> ScaffoldOperationOutput:
        assert fields["written"] is True
        raise RuntimeError("result delivery failed after creation")

    monkeypatch.setattr(
        "mcp_server.services.scaffold_operation.ScaffoldOperationOutput", fail_result
    )
    context = {"problem": "Caller"}
    with pytest.raises(RuntimeError, match="result delivery failed after creation"):
        await service.execute(artifact_type="issue", file_name="result.md", context=context)
    assert (tmp_path / "outputs" / "result.md").read_bytes() == delivered.renderer.render(
        "issue", context, delivered.provenance
    ).encode("utf-8")
