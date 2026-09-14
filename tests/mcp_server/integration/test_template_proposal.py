"""CY065 integration proof for candidate staging and complete proposals."""

from __future__ import annotations

import shutil
from collections.abc import Callable
from pathlib import Path

import pytest
from jinja2 import Environment
from mcp_server.config.loader import ConfigLoader
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.exceptions import MCPError
from mcp_server.core.interfaces.template_catalog import freeze_json
from mcp_server.services.artifact_identity import GenerationPackage, GenerationSource
from mcp_server.services.installation_state import ValidatedSuiteEvidence
from mcp_server.services.template_catalog import (
    TemplateCatalog,
    TemplateCatalogLoader,
    TemplateInputValidator,
)
from mcp_server.services.template_components import ComponentKey, component_fingerprints
from mcp_server.services.template_contract_loader import TemplateContractLoader
from mcp_server.services.template_graph import TemplateGraphResolver
from mcp_server.services.template_proposal import (
    SuiteSnapshot,
    TemplateProposalService,
)
from mcp_server.services.template_renewal import analyze_components
from tests.mcp_server.fixtures.suite_roots import write_package_tree

_CONFIG = """checks:
  fixture_check:
    adapter_id: fixture
    capability: check
    timeout_seconds: 1
    default_args: []
profiles:
  text:
    checks: [fixture_check]
profiles_by_extension: {}
run_checks: {}
"""



def _write_suite(root: Path, *, template: bytes, shared: dict[str, bytes]) -> None:
    files = {
        "alpha/manifest.yaml": b"template_id: alpha\npurpose: Alpha\n",
        "alpha/.version": b"1.0.0\n",
        "alpha/policy.yaml": b"output_profile: text\npersistence: workspace\n",
        "alpha/context.schema.json": (
            b'{"$schema":"https://json-schema.org/draft/2020-12/schema",'
            b'"type":"object"}'
        ),
        "alpha/template.jinja2": template,
        **{f"shared/{name}": value for name, value in shared.items()},
    }
    write_package_tree(root, files)



def _admitter(config_root: Path) -> Callable[[Path], SuiteSnapshot]:
    def admit(root: Path) -> SuiteSnapshot:
        parser = Environment()
        contracts = TemplateContractLoader(root)
        loader = ConfigLoader(
            config_root,
            root,
            context_schema_reader=contracts.load_context_schema,
        )
        validator = ConfigValidator()
        checks = loader.load_checks_config()
        graph = TemplateGraphResolver(root, parser.parse)
        inputs = TemplateInputValidator(
            parser.parse,
            freeze_json({"type": "object"}),
        )
        catalog = TemplateCatalogLoader(
            root,
            read_manifest=loader.load_template_manifest,
            read_version=loader.load_template_version,
            read_policy=loader.load_template_policy,
            read_schema=loader.load_template_context_schema,
            validate_policy=lambda policy: validator.validate_template_policy(
                policy,
                frozenset(name for name, _ in checks.profiles),
            ),
            resolve_graph=graph.resolve,
            validate_inputs=inputs.validate,
        ).load()
        packages = tuple(
            GenerationPackage(
                manifest=package.manifest,
                version=package.version,
                directory=package.renderer.split("/", 1)[0],
            )
            for package in catalog.packages
        )
        sources = tuple(
            GenerationSource(
                path=path.relative_to(root).as_posix(),
                content=path.read_bytes(),
            )
            for path in sorted(root.rglob("*"))
            if path.is_file()
        )
        states = component_fingerprints(packages, sources)
        return SuiteSnapshot(
            catalog=catalog,
            packages=packages,
            sources=sources,
            evidence=ValidatedSuiteEvidence(shared=states[0], packages=states[1:]),
        )

    return admit



@pytest.fixture
def proposal_fixture(tmp_path: Path) -> tuple[TemplateProposalService, Path, Path, Path]:
    config = tmp_path / "config"
    config.mkdir()
    (config / "checks.yaml").write_text(_CONFIG, encoding="utf-8")
    actual = tmp_path / "actual"
    candidate = tmp_path / "candidate"
    adopted = tmp_path / "adopted"
    _write_suite(
        actual,
        template=b'{% extends "shared/templates/base.jinja2" %}',
        shared={"templates/base.jinja2": b"actual\n"},
    )
    _write_suite(
        candidate,
        template=b'{% extends "shared/templates/extra.jinja2" %}',
        shared={
            "templates/base.jinja2": b"candidate\n",
            "templates/extra.jinja2": b"extra\n",
        },
    )
    _write_suite(
        adopted,
        template=b'{% extends "shared/templates/base.jinja2" %}',
        shared={"templates/base.jinja2": b"adopted\n"},
    )
    service = TemplateProposalService(
        admit_suite=_admitter(config),
        candidate_root=tmp_path / "upgrade",
        proposal_root=tmp_path / "proposal",
    )
    return service, actual, candidate, adopted


class TestTemplateProposal:
    def test_valid_candidate_is_staged_and_superseded(
        self,
        proposal_fixture: tuple[TemplateProposalService, Path, Path, Path],
        tmp_path: Path,
    ) -> None:
        service, actual, candidate, _ = proposal_fixture
        service.stage_candidate(actual)
        service.stage_candidate(candidate)
        staged = tmp_path / "upgrade"
        assert (staged / "alpha/template.jinja2").read_bytes() == (
            candidate / "alpha/template.jinja2"
        ).read_bytes()
        assert not (staged / "candidate/template_suite").exists()
        assert service.admit(staged).evidence == service.admit(candidate).evidence

    def test_invalid_candidate_preserves_existing_stage(
        self,
        proposal_fixture: tuple[TemplateProposalService, Path, Path, Path],
        tmp_path: Path,
    ) -> None:
        service, actual, candidate, _ = proposal_fixture
        service.stage_candidate(actual)
        before = {
            path.relative_to(tmp_path / "upgrade").as_posix(): path.read_bytes()
            for path in (tmp_path / "upgrade").rglob("*")
            if path.is_file()
        }
        (candidate / "alpha/policy.yaml").write_text(
            "output_profile: missing_profile\npersistence: workspace\n",
            encoding="utf-8",
        )
        with pytest.raises(MCPError, match="candidate_invalid"):
            service.stage_candidate(candidate)
        after = {
            path.relative_to(tmp_path / "upgrade").as_posix(): path.read_bytes()
            for path in (tmp_path / "upgrade").rglob("*")
            if path.is_file()
        }
        assert after == before

    def test_invalid_proposal_preserves_actual_and_candidate(
        self,
        proposal_fixture: tuple[TemplateProposalService, Path, Path, Path],
        tmp_path: Path,
    ) -> None:
        service, actual, candidate, adopted = proposal_fixture
        service.stage_candidate(candidate)
        before_actual = {
            path.relative_to(actual).as_posix(): path.read_bytes()
            for path in actual.rglob("*")
            if path.is_file()
        }
        analysis = analyze_components(
            _states(service.admit(adopted).evidence),
            _states(service.admit(actual).evidence),
            _states(service.admit(candidate).evidence),
        )
        with pytest.raises(MCPError, match="proposal_invalid"):
            service.materialize_proposal(actual, candidate, analysis)
        assert _files(actual) == before_actual
        assert _files(tmp_path / "upgrade") == _files(candidate)
        assert not (tmp_path / "proposal/alpha").exists()

    def test_missing_profile_reports_template_profile_and_sources(
        self,
        proposal_fixture: tuple[TemplateProposalService, Path, Path, Path],
    ) -> None:
        service, _, candidate, _ = proposal_fixture
        (candidate / "alpha/policy.yaml").write_text(
            "output_profile: missing_profile\npersistence: workspace\n",
            encoding="utf-8",
        )
        with pytest.raises(MCPError) as raised:
            service.stage_candidate(candidate)
        assert raised.value.params["template_id"] == "alpha"
        assert raised.value.params["output_profile"] == "missing_profile"
        assert raised.value.params["policy_source"] == "alpha/policy.yaml"
        assert raised.value.params["config_source"].endswith("checks.yaml")

    def test_native_absence_is_not_probed(
        self,
        proposal_fixture: tuple[TemplateProposalService, Path, Path, Path],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        service, _, candidate, _ = proposal_fixture
        probes: list[str] = []
        monkeypatch.setattr(shutil, "which", lambda name: probes.append(name) or None)
        admitted = service.admit(candidate)
        assert admitted.evidence.packages
        assert probes == []



def _states(evidence: ValidatedSuiteEvidence) -> dict[ComponentKey, object]:
    return {
        state.key: state
        for state in (evidence.shared, *evidence.packages)
    }



def _files(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }
