"""Proposed-content requests and invocation-owned scratch lifecycle."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from mcp_server.config.schemas.adapter_manifest import CheckCapability
from mcp_server.core.interfaces.execution import (
    AdapterBinding,
    AdapterLaunch,
    AdapterPackageIdentity,
)
from mcp_server.execution.content_input import (
    ContentInputPreparer,
    FileContentScratch,
    ScaffoldFileRequest,
    ScaffoldTextRequest,
)
from mcp_server.utils.path_resolver import resolve_temporary_paths


def binding(requires_file: bool) -> AdapterBinding[CheckCapability]:
    """A resolved synthetic content check, independent of catalog discovery."""
    return AdapterBinding(
        identity=AdapterPackageIdentity("content_fixture", "1.0.0", "fixture_snapshot"),
        capability_id="echo",
        contract_version=1,
        launch=AdapterLaunch(None, ()),
        capability=CheckCapability(inputs=("content",), requires_file=requires_file),
    )


def test_direct_and_file_routes_preserve_complete_content_and_logical_target(tmp_path: Path) -> None:
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
