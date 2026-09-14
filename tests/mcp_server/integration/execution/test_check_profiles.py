"""Real admitted adapter execution through recomposed configuration profiles."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.adapter_manifest import AdapterTrustConfig
from mcp_server.config.schemas.checks_config import ChecksConfig
from mcp_server.execution.catalog import AdapterCatalogLoader, FileAdapterPackageReader
from mcp_server.execution.check_service import CheckService
from mcp_server.execution.content_input import ContentInputPreparer, FileContentScratch
from mcp_server.execution.models import InvocationCompleted
from mcp_server.execution.process_runtime import AdapterProcessRuntime, AsyncioProcessBackend


@pytest.mark.asyncio
async def test_renamed_recomposed_profile_uses_declared_native_capabilities(
    tmp_path: Path, pytestconfig: pytest.Config,
) -> None:
    loader = ConfigLoader(pytestconfig.rootpath / ".pgmcp/config", pytestconfig.rootpath / ".pgmcp/templates")
    catalog = AdapterCatalogLoader(
        pytestconfig.rootpath / "mcp_server/bundled_adapters", tmp_path / "adapters",
        AdapterTrustConfig(trusted_adapter_ids=()), read_manifest=loader.load_adapter_manifest,
        files=FileAdapterPackageReader(),
        resolve_program=lambda name: Path(sys.executable) if name == "python" else None,
        windows=sys.platform == "win32",
    ).load()
    initial = loader.load_checks_config()
    assert len(initial.checks) == 10
    assert initial.run_checks.default_profile == "python_review"
    assert initial.profile_for_filename("body.MD") == "markdown_body"
    data = initial.model_dump(mode="json")
    data["profiles"]["owner_named"] = {"checks": ["markdown_body", "python_syntax"]}
    data["profiles_by_extension"][".custom"] = "owner_named"
    config = ChecksConfig.model_validate(data)
    assert config.profile_for_filename("candidate.custom") == "owner_named"
    service = CheckService(
        config, catalog, AdapterProcessRuntime(AsyncioProcessBackend()),
        ContentInputPreparer(FileContentScratch(tmp_path / "scratch", fresh_id=lambda: "one")), tmp_path,
    )
    target = tmp_path / "candidate.custom"
    for content, expected in (("value = 1\n", "passed"), ("value = (\n", "failed")):
        result = await service.run_content("owner_named", target_path=str(target), content=content)
        assert [row.check_id for row in result.results] == ["markdown_body", "python_syntax"]
        assert result.stop_reason is None
        outcomes = [row.invocation for row in result.results]
        assert all(isinstance(outcome, InvocationCompleted) for outcome in outcomes)
        assert [outcome.response.root.decision.status for outcome in outcomes] == ["passed", expected]
        assert outcomes[1].response.root.external_tools[0].version == sys.version.split()[0]
    assert not target.exists()
