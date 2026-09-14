"""Observe unchanged rendering, check facts, and actual create-only filesystem outcomes."""

from __future__ import annotations

import os
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
        source_suite=suite, source_package=suite / "issue",
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "suite", template_id="issue",
    )


def operation(
    root: Path,
    delivered: DeliveredTemplate,
    outcomes: tuple[str, ...],
    *,
    render: Callable[[str, object, FrozenJsonObject], str] | None = None,
    write_scratch: Callable[[Path, bytes], int] | None = None,
) -> tuple[ScaffoldOperation, RecordingRuntime]:
    profile = delivered.catalog.get("issue").policy.output_profile
    checks, _, runtime = compose(
        root, outcomes, profile_id=profile,
        file_content=write_scratch is not None,
        write_bytes=write_scratch if write_scratch is not None else Path.write_bytes,
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
        catalog=delivered.catalog, identities=(identity,), targets=resolver,
        render=render if render is not None else delivered.renderer.render,
        checks=checks, creator=CreateOnlyFileWriter(), workspace_root=root,
    ), runtime


@pytest.mark.asyncio
@pytest.mark.parametrize("policy", ["enforce", "report"])
@pytest.mark.parametrize(
    ("outcomes", "status"),
    [(("passed",), "passed"), (("failed", "unavailable", "passed"), "failed"),
     (("unavailable",), "unavailable"), (("cancelled",), "not_executed")],
)
async def test_validation_policy_preserves_facts_and_exact_saved_bytes(
    tmp_path: Path, delivered: DeliveredTemplate,
    policy: Literal["enforce", "report"], outcomes: tuple[str, ...], status: str,
) -> None:
    service, runtime = operation(tmp_path, delivered, outcomes)
    context = {"problem": "Caller text\r\nwith a second line", "context": ""}
    original = deepcopy(context)
    filename = "MiXeD release.v2.md"
    result = await service.execute(
        artifact_type="issue", file_name=filename, context=context, validation=policy,
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
    for replacement in (
        {"written": not written}, {"error_details": {}}, {"unexpected": True}
    ):
        with pytest.raises(ValidationError):
            ScaffoldOperationOutput.model_validate({**payload, **replacement})


@pytest.mark.asyncio
@pytest.mark.parametrize("when", ["early", "late"])
async def test_collisions_preserve_competing_bytes_and_observed_validation(
    tmp_path: Path, delivered: DeliveredTemplate, monkeypatch: pytest.MonkeyPatch, when: str,
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
        artifact_type="issue", file_name=target.name, context={"problem": "Caller"},
        target_path="outputs", force_target=True, validation="report",
    )
    assert not result.success and not result.written
    assert result.error_code == "target_exists"
    assert target.read_bytes() == competing
    assert result.validation_status == ("not_executed" if when == "early" else "passed")
    assert len(runtime.requests) == (0 if when == "early" else 1)
    assert list(target.parent.iterdir()) == [target]


@pytest.mark.asyncio
@pytest.mark.parametrize("failure", ["context", "render"])
async def test_precheck_failures_do_not_invoke_or_create(
    tmp_path: Path, delivered: DeliveredTemplate, failure: str,
) -> None:
    def broken_render(
        template_id: str, context: object, provenance: FrozenJsonObject,
    ) -> str:
        raise TemplateRuntimeError("render boundary failed")

    service, runtime = operation(
        tmp_path, delivered, ("passed",),
        render=broken_render if failure == "render" else None,
    )
    context: object = {"problem": 42} if failure == "context" else {"problem": "Caller"}
    result = await service.execute(
        artifact_type="issue", file_name="result.md", context=context, validation="report",
    )
    assert result.error_code == ("context_invalid" if failure == "context" else "render_failed")
    assert result.validation_status == "not_executed" and result.checks == ()
    assert not result.written and not (tmp_path / "outputs" / "result.md").exists()
    assert runtime.requests == []


@pytest.mark.asyncio
async def test_partial_staging_failure_never_exposes_proposed_target(
    tmp_path: Path, delivered: DeliveredTemplate, monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, _ = operation(tmp_path, delivered, ("passed",))
    original_write = Path.write_bytes

    def partial_write(path: Path, content: bytes) -> int:
        original_write(path, content[:3])
        raise OSError("staging write interrupted")

    monkeypatch.setattr(Path, "write_bytes", partial_write)
    result = await service.execute(
        artifact_type="issue", file_name="result.md", context={"problem": "Caller"},
    )
    assert result.error_code == "persistence_failed"
    assert result.validation_status == "passed" and not result.written
    assert not (tmp_path / "outputs" / "result.md").exists()
    assert list((tmp_path / "outputs").iterdir()) == []


@pytest.mark.asyncio
async def test_preparation_failure_retains_its_stage_without_writing(
    tmp_path: Path, delivered: DeliveredTemplate,
) -> None:
    def failed_write(path: Path, content: bytes) -> int:
        raise PermissionError("scratch write refused")

    service, runtime = operation(tmp_path, delivered, ("passed",), write_scratch=failed_write)
    result = await service.execute(
        artifact_type="issue", file_name="result.md", context={"problem": "Caller"},
        validation="report",
    )
    assert result.error_code == "preparation_failed"
    assert result.error_details is not None
    assert result.error_details.model_dump()["reason"] == "validation_input_write_failed"
    assert result.error_details.model_dump()["path"] == "outputs/result.md"
    assert not result.written and runtime.requests == []
    assert not (tmp_path / "outputs" / "result.md").exists()


@pytest.mark.asyncio
@pytest.mark.parametrize("stop", ["invalid_request", "unconfirmed"])
async def test_operation_blockers_retain_prior_and_unstarted_checks(
    tmp_path: Path, delivered: DeliveredTemplate, stop: str,
) -> None:
    for policy in ("enforce", "report"):
        root = tmp_path / policy
        root.mkdir()
        service, runtime = operation(root, delivered, ("failed", stop, "passed"))
        result = await service.execute(
            artifact_type="issue", file_name="result.md", context={"problem": "Caller"},
            validation=policy,
        )
        assert result.error_code == (
            "adapter_request_rejected" if stop == "invalid_request" else "termination_unconfirmed"
        )
        assert result.validation_status == "failed"
        assert [row.status for row in result.checks] == [
            "failed", "not_executed" if stop == "invalid_request" else "unavailable", "not_executed"
        ]
        assert result.checks[-1].reason == "not_started"
        assert len(runtime.requests) == 2
        assert not result.written and not (root / "outputs" / "result.md").exists()


@pytest.mark.asyncio
async def test_postcommit_result_failure_does_not_undo_created_bytes(
    tmp_path: Path, delivered: DeliveredTemplate, monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, _ = operation(tmp_path, delivered, ("passed",))

    def fail_result(**fields: object) -> ScaffoldOperationOutput:
        assert fields["written"] is True
        raise RuntimeError("result delivery failed after creation")

    monkeypatch.setattr("mcp_server.services.scaffold_operation.ScaffoldOperationOutput", fail_result)
    context = {"problem": "Caller"}
    with pytest.raises(RuntimeError, match="result delivery failed after creation"):
        await service.execute(artifact_type="issue", file_name="result.md", context=context)
    assert (tmp_path / "outputs" / "result.md").read_bytes() == delivered.renderer.render(
        "issue", context, delivered.provenance
    ).encode("utf-8")
