"""Proposed-content requests and invocation-owned scratch lifecycle."""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path
from shutil import which
from uuid import uuid4

import pytest
from jsonschema import Draft202012Validator
from pydantic import TypeAdapter, ValidationError

from mcp_server.config.schemas.adapter_manifest import CheckCapability
from mcp_server.core.interfaces.execution import (
    AdapterBinding,
    AdapterLaunch,
    AdapterPackageIdentity,
    ContentScratchFiles,
    OwnedScratchFile,
    ScratchPreparationError,
)
from mcp_server.execution.content_input import (
    ContentInputPreparer,
    FileContentScratch,
    ScaffoldContentInput,
    ScaffoldContentRequest,
    ScaffoldFileRequest,
    ScaffoldTextRequest,
)
from mcp_server.execution.models import (
    AdapterCallFailure,
    AdapterCallFailureReason,
    InvocationCancelled,
    InvocationCompleted,
    InvocationFailed,
    ProcessCapture,
    StreamCapture,
    TerminationProblem,
)
from mcp_server.execution.process_runtime import AdapterProcessRuntime, AsyncioProcessBackend
from mcp_server.utils.path_resolver import resolve_temporary_paths
from tests.mcp_server.fixtures.adapter_process import (
    FixtureModel,
    ProcessResponse,
    response_contract,
)
from tests.mcp_server.fixtures.suite_roots import write_package_tree


def binding(requires_file: bool) -> AdapterBinding[CheckCapability]:
    """A resolved synthetic content check, independent of catalog discovery."""
    return AdapterBinding(
        identity=AdapterPackageIdentity("content_fixture", "1.0.0", "fixture_snapshot"),
        capability_id="echo",
        contract_version=1,
        launch=AdapterLaunch(None, ()),
        capability=CheckCapability(inputs=("content",), requires_file=requires_file),
    )


def test_direct_and_file_routes_preserve_complete_content_and_logical_target(
    tmp_path: Path,
) -> None:
    paths = resolve_temporary_paths(tmp_path / "server")
    preparer = ContentInputPreparer(
        FileContentScratch(paths.validation_root, fresh_id=lambda: uuid4().hex)
    )
    target = tmp_path / "missing parent" / "proposed.py"
    content = "hello 世界\r\nsecond\n"
    direct = preparer.prepare(binding(False), target_path=str(target), content=content, args=())
    assert isinstance(direct.request, ScaffoldTextRequest)
    assert direct.request.content == content
    assert direct.request.target_path == str(target)
    assert direct.scratch is None
    assert not paths.temp_root.exists()

    materialized = preparer.prepare(
        binding(True), target_path=str(target), content=content, args=("--literal",)
    )
    assert isinstance(materialized.request, ScaffoldFileRequest)
    assert materialized.scratch is not None
    physical = Path(materialized.request.input_path)
    assert physical.read_bytes() == content.encode("utf-8")
    assert physical.name == target.name
    assert physical.parent.parent == paths.validation_root
    assert materialized.request.target_path == str(target)
    assert materialized.request.args == ("--literal",)
    assert paths.artifacts_root == paths.temp_root / "artifacts"
    assert not paths.artifacts_root.exists()
    assert not target.parent.exists()
    FileContentScratch(paths.validation_root, fresh_id=lambda: uuid4().hex).remove(
        materialized.scratch
    )


def test_closed_immutable_models_agree_with_published_request_schema(
    tmp_path: Path, pytestconfig: pytest.Config
) -> None:
    inputs = TypeAdapter(ScaffoldContentInput)
    requests = TypeAdapter(ScaffoldContentRequest)
    assert "oneOf" in inputs.json_schema()
    assert "oneOf" in requests.json_schema()
    projected_requests = Draft202012Validator(requests.json_schema())
    projected_inputs = Draft202012Validator(inputs.json_schema())
    schema_path = pytestconfig.rootpath / "mcp_server/execution/contracts/check_v1.schema.json"
    validator = Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8")))
    paths = (
        str(tmp_path / "not created" / "item.py"),
        "/not-created/item.py",
        r"C:\not-created\item.py",
        r"\\host\share\item.py",
    )
    for target in paths:
        text = ScaffoldTextRequest(operation="echo", target_path=target, content="", args=())
        file = ScaffoldFileRequest(
            operation="echo", target_path=target, input_path=str(tmp_path / "absent.py"), args=()
        )
        for request in (text, file):
            validator.validate(request.model_dump(mode="json"))
            projected_requests.validate(request.model_dump(mode="json"))
            assert requests.validate_json(request.model_dump_json()) == request
        with pytest.raises(ValidationError, match="frozen"):
            text.content = "mutation"
    valid: dict[str, object] = {"target_path": paths[0], "content": ""}
    invalid = (
        {"target_path": paths[0]},
        {**valid, "input_path": paths[0]},
        {**valid, "unknown": True},
        {**valid, "content": None},
        {**valid, "content": 12},
        {**valid, "target_path": False},
        {**valid, "target_path": "relative.py"},
        {**valid, "target_path": "C:relative.py"},
        {**valid, "target_path": "/"},
        {**valid, "target_path": "C:\\"},
        {**valid, "target_path": "/bad\x00.py"},
        {**valid, "target_path": r"\\host\share"},
        {"target_path": paths[0], "input_path": r"\\host\share"},
    )
    for payload in invalid:
        with pytest.raises(ValidationError):
            inputs.validate_json(json.dumps(payload))
        assert not validator.is_valid({"operation": "echo", "args": [], **payload})
        assert not projected_inputs.is_valid(payload)
        assert not projected_requests.is_valid({"operation": "echo", "args": [], **payload})
    assert not (tmp_path / "not created").exists()


def test_repeated_concurrent_and_colliding_allocations_never_share_or_adopt(tmp_path: Path) -> None:
    paths = resolve_temporary_paths(tmp_path / "server")
    target = tmp_path / "untouched.py"
    target.write_bytes(b"original")
    provider = FileContentScratch(paths.validation_root, fresh_id=lambda: uuid4().hex)
    preparer = ContentInputPreparer(provider)

    def prepare_one(_: int) -> OwnedScratchFile:
        prepared = preparer.prepare(
            binding(True), target_path=str(target), content="same\n", args=()
        )
        assert prepared.scratch is not None
        return prepared.scratch

    sequential = [prepare_one(0), prepare_one(1)]
    with ThreadPoolExecutor(max_workers=4) as pool:
        parallel = list(pool.map(prepare_one, range(4)))
    allocations = sequential + parallel
    assert len({allocation.directory for allocation in allocations}) == 6
    existing = allocations[0]
    collision = FileContentScratch(paths.validation_root, fresh_id=lambda: existing.directory.name)
    with pytest.raises(ScratchPreparationError) as collision_failure:
        collision.create(target.name, b"must not overwrite")
    assert collision_failure.value.phase == "allocation"
    assert isinstance(collision_failure.value.__cause__, FileExistsError)
    assert existing.input_path.read_bytes() == b"same\n"
    assert target.read_bytes() == b"original"
    artifacts = write_package_tree(paths.artifacts_root, {"persisted.txt": b"keep"})
    for allocation in allocations:
        provider.remove(allocation)
    assert not any(paths.validation_root.iterdir())
    assert (artifacts / "persisted.txt").read_bytes() == b"keep"


def test_admission_failure_creates_no_scratch(tmp_path: Path) -> None:
    root = resolve_temporary_paths(tmp_path).validation_root
    preparer = ContentInputPreparer(FileContentScratch(root, fresh_id=lambda: uuid4().hex))
    selection = replace(binding(False), capability=CheckCapability(inputs=("selection",)))
    with pytest.raises(ValueError):
        preparer.prepare(selection, target_path=str(tmp_path / "item.py"), content="", args=())
    with pytest.raises(ValidationError):
        preparer.prepare(binding(True), target_path="relative.py", content="", args=())
    with pytest.raises(UnicodeEncodeError):
        preparer.prepare(
            binding(True), target_path=str(tmp_path / "item.py"), content="\ud800", args=()
        )
    assert not root.exists()


CONTENT_ADAPTER = r"""
const {readFileSync} = require('node:fs');
async function main() {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  const request = JSON.parse(Buffer.concat(chunks).toString('utf8'));
  const received = Object.hasOwn(request, 'content')
    ? request.content : readFileSync(request.input_path, 'utf8');
  const failed = request.args[0] === 'failed';
  const response = {
    decision: failed ? {status: 'failed', message: 'content rejected'} : {status: 'passed'},
    external_tools: [{tool_id: 'node', version: process.version}],
    evidence: {format: 'text', data: JSON.stringify({request, received})}
  };
  process.stdout.write(JSON.stringify(response));
  process.exitCode = failed ? 1 : 0;
}
main().catch(error => {process.stderr.write(String(error)); process.exitCode = 42;});
"""


class ContentEcho(FixtureModel):
    request: ScaffoldContentRequest
    received: str


class DeniedRemoval:
    """Inject a real deletion refusal at the owned filesystem boundary."""

    def __init__(self, files: ContentScratchFiles) -> None:
        self.files = files

    def create(self, basename: str, content: bytes) -> OwnedScratchFile:
        return self.files.create(basename, content)

    def remove(self, allocation: OwnedScratchFile) -> None:
        raise PermissionError(f"fixture denied removal: {allocation.directory}")


@pytest.mark.asyncio
@pytest.mark.slow
@pytest.mark.parametrize(
    "requires_file, mode, deny_cleanup",
    [
        (False, "passed", False),
        (True, "passed", True),
        (True, "failed", True),
        (True, "missing", False),
    ],
)
async def test_real_adapter_observes_input_and_cleanup_preserves_primary_result(
    tmp_path: Path, requires_file: bool, mode: str, deny_cleanup: bool
) -> None:
    node = which("node")
    assert node is not None, "Node is required for non-Python input boundary evidence"
    package = write_package_tree(tmp_path / "package", {"adapter.cjs": CONTENT_ADAPTER.encode()})
    workspace = write_package_tree(tmp_path / "workspace", {"proposed.py": b"original\n"})
    target = workspace / "proposed.py"
    paths = resolve_temporary_paths(tmp_path / "server")
    provider = FileContentScratch(paths.validation_root, fresh_id=lambda: uuid4().hex)
    preparer = ContentInputPreparer(DeniedRemoval(provider) if deny_cleanup else provider)
    content = "hello 世界\r\nnext\n" if requires_file else ""
    selected = replace(
        binding(requires_file),
        launch=AdapterLaunch(Path(node).resolve(), (str(package / "adapter.cjs"),)),
    )
    prepared = preparer.prepare(selected, target_path=str(target), content=content, args=(mode,))
    if mode == "missing":
        assert prepared.scratch is not None
        prepared.scratch.input_path.unlink()
    outcome = await AdapterProcessRuntime(AsyncioProcessBackend()).invoke(
        launch=selected.launch,
        workspace_root=workspace,
        request=prepared.request,
        response_contract=response_contract(),
        timeout_seconds=5,
    )
    if mode == "missing":
        assert isinstance(outcome, InvocationFailed)
        assert outcome.failure.reason is AdapterCallFailureReason.PROCESS_FAILED
    else:
        assert isinstance(outcome, InvocationCompleted)
        assert isinstance(outcome.response.root, ProcessResponse)
        assert outcome.response.root.decision.status == mode
        echo = ContentEcho.model_validate_json(outcome.response.root.evidence.data)
        assert echo.request == prepared.request
        assert echo.received == content
    original_outcome = outcome.model_dump_json()
    warning = preparer.cleanup(prepared, outcome)
    assert outcome.model_dump_json() == original_outcome
    assert target.read_bytes() == b"original\n"
    if deny_cleanup:
        assert warning is not None
        assert "fixture denied removal" in warning.message
        assert prepared.scratch is not None
        assert prepared.scratch.input_path.exists()
        provider.remove(prepared.scratch)
    else:
        assert warning is None
        if prepared.scratch is not None:
            assert not prepared.scratch.directory.exists()
        else:
            assert not paths.temp_root.exists()


@pytest.mark.parametrize("cancelled", [False, True])
@pytest.mark.parametrize("unconfirmed", [False, True])
def test_cleanup_uses_existing_termination_evidence(
    tmp_path: Path, cancelled: bool, unconfirmed: bool
) -> None:
    provider = FileContentScratch(
        resolve_temporary_paths(tmp_path).validation_root, fresh_id=lambda: uuid4().hex
    )
    preparer = ContentInputPreparer(provider)
    prepared = preparer.prepare(
        binding(True), target_path=str(tmp_path / "proposed.py"), content="pending", args=()
    )
    assert prepared.scratch is not None
    stream = StreamCapture(observed_bytes=0, head="", tail="", truncated=False)
    capture = ProcessCapture(exit_code=None if unconfirmed else 1, stdout=stream, stderr=stream)
    termination = TerminationProblem.UNCONFIRMED if unconfirmed else None
    outcome: InvocationFailed | InvocationCancelled
    if cancelled:
        outcome = InvocationCancelled(
            outcome="cancelled", termination_problem=termination, capture=capture
        )
    else:
        outcome = InvocationFailed(
            outcome="failed",
            failure=AdapterCallFailure(
                reason=AdapterCallFailureReason.TIMEOUT, message="execution deadline elapsed"
            ),
            termination_problem=termination,
            capture=capture,
        )
    snapshot = outcome.model_dump_json()
    preparer.cleanup(prepared, outcome)
    assert outcome.model_dump_json() == snapshot
    assert prepared.scratch.directory.exists() is unconfirmed
    if unconfirmed:
        provider.remove(prepared.scratch)


def test_partial_write_failure_keeps_primary_error_when_rollback_fails(tmp_path: Path) -> None:
    root = resolve_temporary_paths(tmp_path).validation_root
    primary = OSError("fixture disk full")

    def partial_write(path: Path, content: bytes) -> int:
        path.write_bytes(content[:2])
        raise primary

    def denied_remove(directory: Path) -> None:
        raise PermissionError(f"fixture rollback denied: {directory}")

    provider = FileContentScratch(
        root,
        fresh_id=lambda: "owned",
        write_bytes=partial_write,
        remove_tree=denied_remove,
    )
    with pytest.raises(ScratchPreparationError) as failure:
        provider.create("proposed.py", b"complete text")
    assert failure.value.phase == "write"
    assert failure.value.__cause__ is primary
    assert (root / "owned" / "proposed.py").read_bytes() == b"co"
    assert any("rollback" in note for note in getattr(primary, "__notes__", ()))
    FileContentScratch(root, fresh_id=lambda: uuid4().hex).remove(
        OwnedScratchFile(root / "owned", root / "owned" / "proposed.py")
    )
