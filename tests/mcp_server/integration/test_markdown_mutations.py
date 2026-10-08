# pgmcp:v1 id=pytest_integration_test pv=1.0.0 pf=70EjvGU6LK1YPSz3 sf=5--KpGf2wHUv2qAj

"Native Markdown mutation decisions, intended-location resolution and isolated persistence."

# Standard library
import os
import sys
from pathlib import Path
from typing import Literal

# Third party
import pytest
from pydantic import JsonValue

# Project
from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.adapter_manifest import AdapterTrustConfig
from mcp_server.config.schemas.artifact_locations import ArtifactLocationsConfig
from mcp_server.core.interfaces.template_catalog import thaw_json
from mcp_server.execution.catalog import AdapterCatalogLoader, FileAdapterPackageReader
from mcp_server.execution.check_service import CheckService
from mcp_server.execution.content_input import ContentInputPreparer, FileContentScratch
from mcp_server.execution.invocation_scratch import FileInvocationScratch
from mcp_server.execution.process_runtime import AdapterProcessRuntime, AsyncioProcessBackend
from mcp_server.schemas.template_identity import ArtifactIdentity
from mcp_server.services.artifact_header_reader import ArtifactHeaderReader
from mcp_server.services.artifact_target_resolver import ArtifactTargetResolver
from mcp_server.services.edit_construction import (
    RewriteOperation,
    construct_edit_proposal,
    select_profile,
)
from mcp_server.services.edit_operation import EditOperation
from mcp_server.services.scaffold_operation import ScaffoldOperation
from mcp_server.utils.atomic_file_writer import (
    CheckedFileWriter,
    CreateOnlyFileWriter,
    OriginalFileReader,
)
from mcp_server.utils.path_resolver import FileArtifactTargetPaths, resolve_temporary_paths
from tests.mcp_server.fixtures.delivered_templates import load_delivered_template
from tests.mcp_server.integration.adapters.test_lychee import LycheeRuntime, lychee_runtime

__all__ = ["lychee_runtime"]


@pytest.fixture
def markdown_environment(
    lychee_runtime: LycheeRuntime,
    tmp_path: Path,
    pytestconfig: pytest.Config,
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[Path, CheckService]:
    "Use delivered bindings and actual native execution in an isolated workspace."
    root = lychee_runtime.workspace
    monkeypatch.setenv(
        "PATH", str(lychee_runtime.executable.parent) + os.pathsep + os.environ.get("PATH", "")
    )
    loader = ConfigLoader(
        pytestconfig.rootpath / ".pgmcp/config", pytestconfig.rootpath / ".pgmcp/template_suite"
    )
    catalog = AdapterCatalogLoader(
        pytestconfig.rootpath / "mcp_server/bundled_adapters",
        tmp_path / "workspace adapters",
        AdapterTrustConfig(trusted_adapter_ids=()),
        read_manifest=loader.load_adapter_manifest,
        files=FileAdapterPackageReader(),
        resolve_program=lambda name: Path(sys.executable) if name == "python" else None,
        windows=os.name == "nt",
    ).load()
    checks = CheckService(
        loader.load_checks_config(),
        catalog,
        AdapterProcessRuntime(AsyncioProcessBackend(), FileInvocationScratch(root / "invocations")),
        ContentInputPreparer(FileContentScratch(root / "snapshots", fresh_id=lambda: "proposal")),
        root,
    )
    (root / "docs").mkdir()
    (root / "docs" / "neighbor (source).md").write_text("## Existing\n", encoding="utf-8")
    return root, checks


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("broken", "policy"), [(False, "enforce"), (True, "enforce"), (True, "report")]
)
async def test_scaffold_native_link_policy(
    markdown_environment: tuple[Path, CheckService],
    tmp_path: Path,
    pytestconfig: pytest.Config,
    broken: bool,
    policy: Literal["enforce", "report"],
) -> None:
    "Validate the delivered document/body route before create-only persistence."
    root, checks = markdown_environment
    template_id = "generic_doc" if not broken else "issue"
    suite = pytestconfig.rootpath / ".pgmcp/template_suite"
    delivered = load_delivered_template(
        source_suite=suite,
        source_package=suite / template_id,
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "suite",
        template_id=template_id,
    )
    target = root / "docs" / "guide.md"
    neighbor = target.with_name("neighbor (source).md")
    neighbor_before = neighbor.read_bytes()
    links = (
        "## Existing\n\n[Neighbor](<neighbor (source).md#existing>)\n"
        "[Self](<guide.md#existing>)\n[TOC](<#existing>)\n"
    )
    links += "[Reference][one]\n\n[one]: <neighbor (source).md#existing>\n"
    if broken:
        links += "[Missing](<missing.md>)\n[Missing anchor](<#absent>)\n"

    context: dict[str, JsonValue]
    if template_id == "generic_doc":
        context = {
            "title": "Guide",
            "purpose": "Exercise native mutation behavior.",
            "summary": links,
            "document_metadata": {
                "status": "Fixture",
                "revisions": [
                    {
                        "version": "0.1",
                        "date": "2026-10-08",
                        "author": "Fixture",
                        "change": "Native behavior witness.",
                    }
                ],
            },
        }
    else:
        context = {"problem": links}
    locations = ArtifactLocationsConfig.model_validate(
        {"version": "2.0.0", "artifacts": {template_id: {"default_root": "docs"}}}
    )
    service = ScaffoldOperation(
        catalog=delivered.catalog,
        identities=(ArtifactIdentity.model_validate(thaw_json(delivered.provenance)),),
        targets=ArtifactTargetResolver(
            paths=FileArtifactTargetPaths(root),
            temporary_artifacts_root=resolve_temporary_paths(root / "server").artifacts_root,
            locations=locations,
        ),
        render=delivered.renderer.render,
        checks=checks,
        creator=CreateOnlyFileWriter(),
        workspace_root=root,
    )
    result = await service.execute(
        artifact_type=template_id,
        file_name=target.name,
        context=context,
        validation=policy,
    )
    expected_status = "failed" if broken else "passed"
    expected_write = not broken or policy == "report"
    assert result.validation_status == expected_status
    assert result.written is expected_write and result.success is expected_write
    assert len(result.checks) == 1
    observation = result.checks[0]
    assert observation.status == expected_status
    assert observation.invocation is not None
    assert observation.invocation.external_tools is not None
    assert [(tool.tool_id, tool.version) for tool in observation.invocation.external_tools] == [
        ("lychee", "0.24.2")
    ]
    if broken:
        assert observation.evidence is not None
        assert observation.evidence.format == "json"
    assert neighbor.read_bytes() == neighbor_before
    assert not list((root / "snapshots").iterdir())
    assert not list((root / "invocations").iterdir())
    assert target.exists() is expected_write
    if expected_write:
        assert target.read_bytes() == delivered.renderer.render(
            template_id, context, delivered.provenance
        ).encode("utf-8")
    else:
        assert result.error_code == "validation_blocked"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("broken", "policy"), [(False, "enforce"), (True, "enforce"), (True, "report")]
)
async def test_edit_native_link_policy(
    markdown_environment: tuple[Path, CheckService],
    tmp_path: Path,
    pytestconfig: pytest.Config,
    broken: bool,
    policy: Literal["enforce", "report"],
) -> None:
    "Validate new self/neighbor content via metadata or extension before replacement."
    root, checks = markdown_environment
    template_id = "generic_doc" if not broken else "issue"
    suite = pytestconfig.rootpath / ".pgmcp/template_suite"
    delivered = load_delivered_template(
        source_suite=suite,
        source_package=suite / template_id,
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "suite",
        template_id=template_id,
    )
    target = root / "docs" / "guide.md"
    neighbor = target.with_name("neighbor (source).md")
    neighbor_before = neighbor.read_bytes()
    links = "## Existing\n\n[Neighbor](<neighbor (source).md#existing>)\n[Self](<guide.md#existing>)\n[TOC](<#existing>)\n"
    links += "[Reference][one]\n\n[one]: <neighbor (source).md#existing>\n"
    if broken:
        links += "[Missing](<missing.md>)\n[Missing anchor](<#absent>)\n"

    header = f"<!-- pgmcp:v1 id={template_id} pv=1.0.0 pf={'a' * 16} sf={'b' * 16} -->\n"
    use_header = not broken or policy == "report"
    original = ((header if use_header else "") + "## Old\n").encode("utf-8")
    target.write_bytes(original)
    proposal = (header if use_header else "") + links
    template_profiles = {
        item.manifest.template_id: item.policy.output_profile for item in delivered.catalog.packages
    }
    service = EditOperation(
        paths=FileArtifactTargetPaths(root),
        reader=OriginalFileReader(),
        writer=CheckedFileWriter(),
        select=lambda original, filename, explicit: select_profile(
            original,
            filename,
            explicit_template_id=explicit,
            header_reader=ArtifactHeaderReader(),
            template_profiles=template_profiles,
            extension_profile_for_filename=delivered.checks.match_for_filename,
        ),
        construct=construct_edit_proposal,
        checks=checks,
    )
    result = await service.execute(
        path="docs/guide.md", operation=RewriteOperation(content=proposal), validation=policy
    )
    expected_status = "failed" if broken else "passed"
    expected_write = not broken or policy == "report"
    assert result.validation_status == expected_status
    assert result.written is expected_write and result.success is expected_write
    assert len(result.checks) == 1
    observation = result.checks[0]
    assert observation.status == expected_status
    assert observation.invocation is not None
    assert observation.invocation.external_tools is not None
    assert [(tool.tool_id, tool.version) for tool in observation.invocation.external_tools] == [
        ("lychee", "0.24.2")
    ]
    if broken:
        assert observation.evidence is not None
        assert observation.evidence.format == "json"
    assert neighbor.read_bytes() == neighbor_before
    assert not list((root / "snapshots").iterdir())
    assert not list((root / "invocations").iterdir())
    assert result.selected_source == ("metadata" if use_header else "extension")
    assert target.read_bytes() == (proposal.encode("utf-8") if expected_write else original)
    if not expected_write:
        assert result.error_code == "validation_blocked"
