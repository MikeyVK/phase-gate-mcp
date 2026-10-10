# tests\mcp_server\unit\config\test_contracts_loader.py
# template=unit_test version=3d15d309 created=2026-05-02T18:00Z updated=
"""
Unit tests for mcp_server.config.loader.

Unit tests for load_contracts_config (issue #271 C2)

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.config.loader, mcp_server.config.schemas.contracts_config]
@responsibilities:
    - Test load_contracts_config happy path, error paths, removed methods, 6-workflow roundtrip
    - Verify ContractsConfig roundtrip equality for all 6 production workflows
    - Verify _inject_terminal_phase and load_phase_contracts_config are removed
"""

# Standard library
import re
from dataclasses import dataclass
from pathlib import Path

# Third-party
import pytest
import yaml

# Project modules
from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.artifact_locations import ArtifactLocationsConfig
from mcp_server.config.schemas.contracts_config import (
    BranchLocalArtifact,
    ContractsConfig,
    MergePolicy,
    PhaseInstructionsSpec,
    WorkflowEntry,
    WorkflowPhaseEntry,
)
from mcp_server.core.exceptions import ConfigError
from mcp_server.core.interfaces.template_catalog import thaw_json
from mcp_server.core.operation_notes import NoteContext
from mcp_server.schemas.template_identity import ArtifactIdentity
from mcp_server.services.artifact_target_resolver import ArtifactTargetResolver
from mcp_server.services.scaffold_operation import ScaffoldOperation
from mcp_server.tools.scaffold_tool import ScaffoldArtifactTool
from mcp_server.utils.atomic_file_writer import CreateOnlyFileWriter
from mcp_server.utils.path_resolver import FileArtifactTargetPaths, resolve_temporary_paths
from tests.mcp_server.fixtures.delivered_templates import load_delivered_template
from tests.mcp_server.test_support import get_default_server_root
from tests.mcp_server.unit.execution.test_check_service import compose as compose_check_service

_STUB_INSTR_DICT: dict[str, str] = {
    "sub_role": "test-role",
    "phase_instructions": "Test instructions.",
    "handover_template": "Test handover.",
}
_STUB_INSTRUCTIONS = PhaseInstructionsSpec(
    sub_role="test-role",
    phase_instructions="Test instructions.",
    handover_template="Test handover.",
)

# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------


@pytest.fixture()
def config_dir(tmp_path: Path) -> Path:
    """Return a tmp .pgmcp/config directory."""
    d = tmp_path / get_default_server_root() / "config"
    d.mkdir(parents=True)
    return d


def _write_contracts(config_dir: Path, content: str) -> None:
    (config_dir / "contracts.yaml").write_text(content, encoding="utf-8")


_MINIMAL_YAML = """\
version: "1.0.0"
merge_policy:
  pr_allowed_phase: ready
  branch_local_artifacts: []
workflows:
  feature:
    phases:
      - name: research
        instructions:
          sub_role: test-role
          phase_instructions: Test instructions.
          handover_template: Test handover.
      - name: ready
        instructions:
          sub_role: test-role
          phase_instructions: Test instructions.
          handover_template: Test handover.
"""


def _make_loader_with_workflows(config_dir: Path, workflows: dict[str, object]) -> ConfigLoader:
    # Inject stub instructions into every phase that lacks them (field is required).
    enriched: dict[str, object] = {}
    for wf_name, wf_data in workflows.items():
        if isinstance(wf_data, dict) and "phases" in wf_data:
            phases = [
                {**p, "instructions": _STUB_INSTR_DICT}
                if isinstance(p, dict) and "instructions" not in p
                else p
                for p in wf_data["phases"]
            ]
            wf_data = {**wf_data, "phases": phases}
        enriched[wf_name] = wf_data
    content = yaml.dump(
        {
            "version": "1.0.0",
            "merge_policy": {
                "pr_allowed_phase": "ready",
                "branch_local_artifacts": [
                    {"path": f"{get_default_server_root()}/state.json", "reason": "branch-local"},
                ],
            },
            "workflows": enriched,
        },
        default_flow_style=False,
        allow_unicode=True,
    )
    _write_contracts(config_dir, content)
    return ConfigLoader(config_dir)


def _policy() -> MergePolicy:
    return MergePolicy(
        pr_allowed_phase="ready",
        branch_local_artifacts=[
            BranchLocalArtifact(
                path=f"{get_default_server_root()}/state.json", reason="branch-local"
            )
        ],
    )


def _wpe(name: str, **kwargs: object) -> WorkflowPhaseEntry:
    if "instructions" not in kwargs:
        kwargs["instructions"] = _STUB_INSTRUCTIONS
    return WorkflowPhaseEntry(name=name, **kwargs)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# load_contracts_config — happy path
# ---------------------------------------------------------------------------


class TestLoadContractsConfig:
    """Test load_contracts_config returns ContractsConfig on valid input."""

    def test_returns_contracts_config_instance(self, config_dir: Path) -> None:
        """load_contracts_config must return a ContractsConfig instance."""
        _write_contracts(config_dir, _MINIMAL_YAML)
        loader = ConfigLoader(config_dir)
        result = loader.load_contracts_config()
        assert isinstance(result, ContractsConfig)

    def test_feature_workflow_research_first_ready_last(self) -> None:
        """Real contracts.yaml: feature workflow has research first and ready last."""
        real = Path(__file__).parents[4] / get_default_server_root() / "config" / "contracts.yaml"
        if not real.exists():
            pytest.skip("contracts.yaml not yet created — passes after C2 GREEN")
        result = ConfigLoader(real.parent).load_contracts_config()
        phases = result.get_phases("feature")
        assert phases[0] == "research"
        assert phases[-1] == "ready"

    def test_real_chore_workflow_is_lightweight_and_non_cycle_based(self) -> None:
        """Real contracts.yaml exposes the approved five-phase chore contract."""
        real = Path(__file__).parents[4] / get_default_server_root() / "config" / "contracts.yaml"
        result = ConfigLoader(real.parent).load_contracts_config()

        assert result.get_phases("chore") == [
            "research",
            "implementation",
            "validation",
            "documentation",
            "ready",
        ]

        chore = result.workflows["chore"]
        research = chore.get_phase("research")
        implementation = chore.get_phase("implementation")

        assert research.exit_requires == []
        assert implementation.cycle_based is False
        assert implementation.subphases == []
        assert implementation.commit_type_map == {}
        assert "approved Research artifact" in implementation.instructions.phase_instructions
        assert "direct Chore / Research hand-over" in implementation.instructions.phase_instructions
        assert "when neither input exists" in implementation.instructions.phase_instructions

    def test_all_ready_contracts_are_exactly_equal(self) -> None:
        """Every workflow exposes one identical Ready instruction and hand-over."""

        real = Path(__file__).parents[4] / get_default_server_root() / "config" / "contracts.yaml"
        result = ConfigLoader(real.parent).load_contracts_config()
        ready_specs = [
            workflow.get_phase("ready").instructions for workflow in result.workflows.values()
        ]

        first = ready_specs[0]
        assert all(spec.phase_instructions == first.phase_instructions for spec in ready_specs)
        assert all(spec.handover_template == first.handover_template for spec in ready_specs)

    def test_ready_contract_retains_terminal_invariants(self) -> None:
        """The common Ready contract owns final evidence, transfer, and PR submission."""

        real = Path(__file__).parents[4] / get_default_server_root() / "config" / "contracts.yaml"
        result = ConfigLoader(real.parent).load_contracts_config()
        ready = result.workflows["feature"].get_phase("ready").instructions
        instructions = ready.phase_instructions
        handover = ready.handover_template or ""

        for marker in (
            "evidence",
            "deferred",
            "git_status",
            "git_diff_stat",
            "scaffold_artifact",
            "git_add_or_commit",
            "submit_pr",
        ):
            assert marker in instructions

        headings = (
            "#### Scope",
            "#### Deliverables",
            "#### Evidence",
            "#### Open Work",
            "#### Review Request",
        )
        positions = tuple(handover.index(heading) for heading in headings)
        assert positions == tuple(sorted(positions))
        assert "Review requested" in handover
        assert "human approval" not in instructions.lower()
        assert "merge_pr" not in instructions
        assert "selected workflow" in instructions
        assert "Validation evidence" not in instructions
        assert "Validation evidence" not in handover

    def test_real_contracts_preserve_global_instruction_invariants(self) -> None:
        """All effective contracts keep the approved structural instruction contract."""

        real = Path(__file__).parents[4] / get_default_server_root() / "config" / "contracts.yaml"
        result = ConfigLoader(real.parent).load_contracts_config()
        phases = [
            (workflow_name, phase)
            for workflow_name, workflow in result.workflows.items()
            for phase in workflow.phases
        ]

        assert len(phases) == 39

        headings = ("Scope", "Deliverables", "Evidence", "Open Work", "Review Request")
        prohibited = (
            "explore_subagent",
            "internal qa",
            "invoke the qa agent",
            "qa sub-agent",
            "return pass",
        )
        model_version = re.compile(r"\b(?:gpt|gemini|claude)[ -]?\d", re.IGNORECASE)

        for workflow_name, phase in phases:
            instructions = phase.instructions.phase_instructions
            handover = phase.instructions.handover_template or ""
            contract = f"{workflow_name}/{phase.name}"

            assert instructions.strip(), contract
            assert "get_work_context" not in instructions, contract
            assert handover.strip(), contract

            title = (
                "### Ready Hand-over"
                if phase.name == "ready"
                else f"### {workflow_name.title()} / {phase.name.title()} Hand-over"
            )
            assert handover.startswith(f"{title}\n"), contract

            canonical_headings = tuple(f"#### {heading}" for heading in headings)
            positions = tuple(handover.index(heading) for heading in canonical_headings)
            assert positions == tuple(sorted(positions)), contract
            assert "Review requested" in handover, contract

            effective_contract = f"{instructions}\n{handover}"
            lower_contract = effective_contract.lower()
            assert not any(marker in lower_contract for marker in prohibited), contract
            assert model_version.search(effective_contract) is None, contract

    def test_preimplementation_handovers_link_primary_review_inputs(self) -> None:
        """Research, Planning, and Design transfers expose clickable review inputs."""

        real = Path(__file__).parents[4] / get_default_server_root() / "config" / "contracts.yaml"
        result = ConfigLoader(real.parent).load_contracts_config()
        markdown_link = re.compile(r"\[[^\]\n]+\]\([^)\n]+\)")

        for workflow_name, workflow in result.workflows.items():
            for phase in workflow.phases:
                if phase.name not in {"research", "planning", "design"}:
                    continue

                handover = phase.instructions.handover_template or ""
                contract = f"{workflow_name}/{phase.name}"
                assert markdown_link.search(handover), contract
                assert not re.search(r"\([A-Za-z]:[\\/]", handover), contract

    def test_required_phase_artifacts_retain_scaffold_and_persistence(self) -> None:
        """Required Research, Planning, and Design artifacts remain executable."""

        real = Path(__file__).parents[4] / get_default_server_root() / "config" / "contracts.yaml"
        result = ConfigLoader(real.parent).load_contracts_config()
        artifact_ids = {"research-doc", "planning-doc", "design-doc"}
        schema_discovery_contracts = {
            ("docs", "planning"),
            ("epic", "research"),
            ("epic", "planning"),
            ("epic", "design"),
        }

        for workflow_name, workflow in result.workflows.items():
            for phase in workflow.phases:
                required_ids = {check.id for check in phase.exit_requires} & artifact_ids
                if not required_ids:
                    continue

                instructions = phase.instructions.phase_instructions
                contract = f"{workflow_name}/{phase.name}"
                assert "scaffold_artifact" in instructions, contract
                assert "git_add_or_commit" in instructions, contract
                if (workflow_name, phase.name) in schema_discovery_contracts:
                    assert "scaffold_schema" in instructions, contract

    def test_loaded_object_passes_model_validator(self, config_dir: Path) -> None:
        """Loaded object must satisfy the model_validator (last phase == pr_allowed_phase)."""
        _write_contracts(config_dir, _MINIMAL_YAML)
        result = ConfigLoader(config_dir).load_contracts_config()
        assert result.merge_policy.pr_allowed_phase == "ready"
        assert result.get_phases("feature")[-1] == "ready"


# ---------------------------------------------------------------------------
# load_contracts_config — error paths
# ---------------------------------------------------------------------------


class TestLoadContractsConfigErrors:
    def test_missing_file_raises_config_error(self, config_dir: Path) -> None:
        """ConfigError (not FileNotFoundError) must be raised when contracts.yaml absent."""
        with pytest.raises(ConfigError):
            ConfigLoader(config_dir).load_contracts_config()

    def test_yaml_parse_error_raises_config_error(self, config_dir: Path) -> None:
        """ConfigError must be raised on YAML parse error."""
        _write_contracts(config_dir, "merge_policy: [\ninvalid yaml")
        with pytest.raises(ConfigError):
            ConfigLoader(config_dir).load_contracts_config()


# ---------------------------------------------------------------------------
# Removed methods
# ---------------------------------------------------------------------------


class TestRemovedLoaderMethods:
    def test_inject_terminal_phase_does_not_exist(self) -> None:
        """_inject_terminal_phase must be removed from ConfigLoader."""
        assert not hasattr(ConfigLoader, "_inject_terminal_phase")

    def test_load_phase_contracts_config_does_not_exist(self) -> None:
        """load_phase_contracts_config must be removed from ConfigLoader."""
        assert not hasattr(ConfigLoader, "load_phase_contracts_config")


# ---------------------------------------------------------------------------
# Roundtrip tests — all 7 workflows
# ---------------------------------------------------------------------------


class TestContractsConfigRoundtrip:
    """YAML → ContractsConfig → hand-crafted object equality for all 6 workflows."""

    def test_feature_workflow_roundtrip(self, config_dir: Path) -> None:
        impl = {
            "name": "implementation",
            "cycle_based": True,
            "subphases": ["red", "green", "refactor"],
            "commit_type_map": {"red": "test", "green": "feat", "refactor": "refactor"},
        }
        loader = _make_loader_with_workflows(
            config_dir,
            {
                "feature": {
                    "phases": [
                        {"name": "research"},
                        {"name": "planning"},
                        {"name": "design"},
                        impl,
                        {"name": "validation"},
                        {"name": "documentation"},
                        {"name": "ready"},
                    ]
                }
            },
        )
        expected = ContractsConfig(
            merge_policy=_policy(),
            workflows={
                "feature": WorkflowEntry(
                    phases=[
                        _wpe("research"),
                        _wpe("planning"),
                        _wpe("design"),
                        _wpe(
                            "implementation",
                            cycle_based=True,
                            subphases=["red", "green", "refactor"],
                            commit_type_map={
                                "red": "test",
                                "green": "feat",
                                "refactor": "refactor",
                            },
                        ),
                        _wpe("validation"),
                        _wpe("documentation"),
                        _wpe("ready"),
                    ]
                )
            },
        )
        assert loader.load_contracts_config() == expected

    def test_bug_workflow_roundtrip(self, config_dir: Path) -> None:
        impl = {
            "name": "implementation",
            "cycle_based": True,
            "subphases": ["red", "green", "refactor"],
            "commit_type_map": {"red": "test", "green": "feat", "refactor": "refactor"},
        }
        loader = _make_loader_with_workflows(
            config_dir,
            {
                "bug": {
                    "phases": [
                        {"name": "research"},
                        {"name": "planning"},
                        {"name": "design"},
                        impl,
                        {"name": "validation"},
                        {"name": "documentation"},
                        {"name": "ready"},
                    ]
                }
            },
        )
        expected = ContractsConfig(
            merge_policy=_policy(),
            workflows={
                "bug": WorkflowEntry(
                    phases=[
                        _wpe("research"),
                        _wpe("planning"),
                        _wpe("design"),
                        _wpe(
                            "implementation",
                            cycle_based=True,
                            subphases=["red", "green", "refactor"],
                            commit_type_map={
                                "red": "test",
                                "green": "feat",
                                "refactor": "refactor",
                            },
                        ),
                        _wpe("validation"),
                        _wpe("documentation"),
                        _wpe("ready"),
                    ]
                )
            },
        )
        assert loader.load_contracts_config() == expected

    def test_hotfix_workflow_roundtrip(self, config_dir: Path) -> None:
        impl = {
            "name": "implementation",
            "cycle_based": True,
            "subphases": ["red", "green", "refactor"],
            "commit_type_map": {"red": "test", "green": "feat", "refactor": "refactor"},
        }
        loader = _make_loader_with_workflows(
            config_dir,
            {
                "hotfix": {
                    "phases": [
                        impl,
                        {"name": "validation"},
                        {"name": "documentation"},
                        {"name": "ready"},
                    ]
                }
            },
        )
        expected = ContractsConfig(
            merge_policy=_policy(),
            workflows={
                "hotfix": WorkflowEntry(
                    phases=[
                        _wpe(
                            "implementation",
                            cycle_based=True,
                            subphases=["red", "green", "refactor"],
                            commit_type_map={
                                "red": "test",
                                "green": "feat",
                                "refactor": "refactor",
                            },
                        ),
                        _wpe("validation"),
                        _wpe("documentation"),
                        _wpe("ready"),
                    ]
                )
            },
        )
        assert loader.load_contracts_config() == expected

    def test_refactor_workflow_roundtrip(self, config_dir: Path) -> None:
        impl = {
            "name": "implementation",
            "cycle_based": True,
            "subphases": ["red", "green", "refactor"],
            "commit_type_map": {"red": "test", "green": "feat", "refactor": "refactor"},
        }
        loader = _make_loader_with_workflows(
            config_dir,
            {
                "refactor": {
                    "phases": [
                        {"name": "research"},
                        {"name": "planning"},
                        impl,
                        {"name": "validation"},
                        {"name": "documentation"},
                        {"name": "ready"},
                    ]
                }
            },
        )
        expected = ContractsConfig(
            merge_policy=_policy(),
            workflows={
                "refactor": WorkflowEntry(
                    phases=[
                        _wpe("research"),
                        _wpe("planning"),
                        _wpe(
                            "implementation",
                            cycle_based=True,
                            subphases=["red", "green", "refactor"],
                            commit_type_map={
                                "red": "test",
                                "green": "feat",
                                "refactor": "refactor",
                            },
                        ),
                        _wpe("validation"),
                        _wpe("documentation"),
                        _wpe("ready"),
                    ]
                )
            },
        )
        assert loader.load_contracts_config() == expected

    def test_docs_workflow_roundtrip(self, config_dir: Path) -> None:
        loader = _make_loader_with_workflows(
            config_dir,
            {
                "docs": {
                    "phases": [
                        {"name": "planning"},
                        {"name": "documentation"},
                        {"name": "ready"},
                    ]
                }
            },
        )
        expected = ContractsConfig(
            merge_policy=_policy(),
            workflows={
                "docs": WorkflowEntry(
                    phases=[
                        _wpe("planning"),
                        _wpe("documentation"),
                        _wpe("ready"),
                    ]
                )
            },
        )
        assert loader.load_contracts_config() == expected

    def test_epic_workflow_roundtrip(self, config_dir: Path) -> None:
        loader = _make_loader_with_workflows(
            config_dir,
            {
                "epic": {
                    "phases": [
                        {"name": "research"},
                        {"name": "planning"},
                        {"name": "design"},
                        {"name": "coordination"},
                        {"name": "documentation"},
                        {"name": "ready"},
                    ]
                }
            },
        )
        expected = ContractsConfig(
            merge_policy=_policy(),
            workflows={
                "epic": WorkflowEntry(
                    phases=[
                        _wpe("research"),
                        _wpe("planning"),
                        _wpe("design"),
                        _wpe("coordination"),
                        _wpe("documentation"),
                        _wpe("ready"),
                    ]
                )
            },
        )
        assert loader.load_contracts_config() == expected

    def test_real_epic_workflow_uses_coordination_scoped_sub_roles(self) -> None:
        """Real contracts.yaml: epic workflow uses @co-scoped sub-role names."""
        real = Path(__file__).parents[4] / get_default_server_root() / "config" / "contracts.yaml"
        if not real.exists():
            pytest.skip("contracts.yaml not yet created — passes after C2 GREEN")

        result = ConfigLoader(real.parent).load_contracts_config()
        epic = result.workflows["epic"]

        assert [phase.instructions.sub_role for phase in epic.phases] == [
            "epic-researcher",
            "epic-planner",
            "epic-designer",
            "epic-coordinator",
            "epic-documenter",
            "epic-releaser",
        ]


class TestCY068DocflowE01:
    """CY068 / DOCFLOW-E01: workflow carriers, phase ordering, and instruction validation."""

    def test_nineteen_workflow_carriers_exist_and_preserve_phase_order(self) -> None:

        real = Path(__file__).parents[4] / get_default_server_root() / "config" / "contracts.yaml"
        loader = ConfigLoader(real.parent)
        config = loader.load_contracts_config()

        # Check that the 7 workflows exist
        assert set(config.workflows) == {
            "feature",
            "bug",
            "refactor",
            "chore",
            "epic",
            "docs",
            "hotfix",
        }

        # Verify nineteen carriers across the workflows
        carrier_phases = [
            ("feature", "research"),
            ("feature", "design"),
            ("feature", "planning"),
            ("feature", "validation"),
            ("bug", "research"),
            ("bug", "design"),
            ("bug", "planning"),
            ("bug", "validation"),
            ("refactor", "research"),
            ("refactor", "design"),
            ("refactor", "planning"),
            ("refactor", "validation"),
            ("chore", "research"),
            ("chore", "validation"),
            ("epic", "research"),
            ("epic", "design"),
            ("epic", "planning"),
            ("docs", "planning"),
            ("hotfix", "validation"),
        ]
        assert len(carrier_phases) == 19
        for wf_name, phase_name in carrier_phases:
            phase = config.workflows[wf_name].get_phase(phase_name)
            assert phase is not None
            assert phase.instructions.phase_instructions.strip()

    def test_live_v3_contracts_loading_and_docflow_e01(self) -> None:
        """DOCFLOW-E01: the live V3 workflow contract loads with its phase semantics."""
        real = Path(__file__).parents[4] / get_default_server_root() / "config" / "contracts.yaml"
        content = real.read_text(encoding="utf-8")
        assert "run_quality_gates" not in content
        assert "context=" not in content
        assert "files=[...]" not in content
        assert "cycles={...}" not in content
        assert "scaffold_schema" in content
        assert "safe_edit_file" in content
        assert "run_checks" in content

        config = ConfigLoader(real.parent).load_contracts_config()
        expected_phases = {
            "feature": [
                "research",
                "design",
                "planning",
                "implementation",
                "validation",
                "documentation",
                "ready",
            ],
            "bug": [
                "research",
                "design",
                "planning",
                "implementation",
                "validation",
                "documentation",
                "ready",
            ],
            "refactor": [
                "research",
                "design",
                "planning",
                "implementation",
                "validation",
                "documentation",
                "ready",
            ],
            "hotfix": ["implementation", "validation", "documentation", "ready"],
            "docs": ["planning", "documentation", "ready"],
            "chore": ["research", "implementation", "validation", "documentation", "ready"],
            "epic": ["research", "planning", "design", "coordination", "documentation", "ready"],
        }
        assert set(config.workflows) == set(expected_phases)
        for workflow_name, phase_names in expected_phases.items():
            phases = config.workflows[workflow_name].phases
            assert [phase.name for phase in phases] == phase_names
            for phase in phases:
                assert phase.instructions.phase_instructions.strip()
                assert phase.instructions.sub_role.strip()
                assert phase.instructions.handover_template
        assert config.merge_policy.pr_allowed_phase == "ready"

    @pytest.mark.asyncio
    async def test_nineteen_workflow_variants_satisfy_docflow_e02(self, tmp_path: Path) -> None:
        """DOCFLOW-E02: Schema-admitted carriers preserve the 19 workflow semantic meanings.

        All four physical carrier schemas/templates are exercised, with traceable assertions
        covering the union of the nineteen workflow meanings (DI-07 §7.2). The canonical V3
        route is exercised via the delivered catalog, schema admission against package schemas,
        renderer, and ScaffoldArtifactTool persistence. The schema-admitted scaffold preserves
        the complete semantic union supplied through existing carrier fields; final document
        organization and evidence expansion remain a safe_edit_file responsibility.
        """
        root = Path(__file__).parents[4]
        suite = root / ".pgmcp/template_suite"
        config_root = root / ".pgmcp/config"

        @dataclass(frozen=True)
        class WorkflowObligation:
            variant: str
            carrier: str
            obligations: str
            carrier_field: str
            sentinel: str

        obligations = [
            # Research carrier variants (DI-07 §7.2)
            WorkflowObligation(
                variant="Feature Research",
                carrier="research",
                obligations=(
                    "Evidence, affected consumers, alternatives/risks, "
                    "expected results and approved strategy"
                ),
                carrier_field="findings",
                sentinel="[SENTINEL-FEAT-RES:evidence-consumers-alternatives-risks-results]",
            ),
            WorkflowObligation(
                variant="Bug Research",
                carrier="research",
                obligations=(
                    "Reproduction/occurrence context, causal evidence, "
                    "correction boundary, expected results and strategy"
                ),
                carrier_field="problem_statement",
                sentinel="[SENTINEL-BUG-RES:repro-context-causal-evidence-boundary-strategy]",
            ),
            WorkflowObligation(
                variant="Refactor Research",
                carrier="research",
                obligations=(
                    "Responsibility/coupling problems, preservation invariants, "
                    "exclusions and strategy"
                ),
                carrier_field="scope_in",
                sentinel="[SENTINEL-REF-RES:coupling-problems-preservation-invariants-scope]",
            ),
            WorkflowObligation(
                variant="Chore Research",
                carrier="research",
                obligations=(
                    "Bounded objective, scope, consumers, risks and strategy; "
                    "persistence remains conditional"
                ),
                carrier_field="purpose",
                sentinel="[SENTINEL-CHORE-RES:bounded-objective-consumers-conditional-persistence]",
            ),
            WorkflowObligation(
                variant="Epic Research",
                carrier="research",
                obligations=(
                    "Workstream/consumer boundaries, assumptions, dependencies, "
                    "risks and shared strategy"
                ),
                carrier_field="background",
                sentinel="[SENTINEL-EPIC-RES:workstream-boundaries-assumptions-deps-risks]",
            ),
            # Design carrier variants (DI-07 §7.2)
            WorkflowObligation(
                variant="Feature Design",
                carrier="design",
                obligations=(
                    "Production responsibilities, interfaces, flow/failures, "
                    "alternatives, test design and migration"
                ),
                carrier_field="requirements_functional",
                sentinel="[SENTINEL-FEAT-DES:responsibilities-interfaces-failures-test-migration]",
            ),
            WorkflowObligation(
                variant="Bug Design",
                carrier="design",
                obligations=(
                    "Smallest causal correction, preserved behavior, failure behavior "
                    "and regression evidence design"
                ),
                carrier_field="problem_statement",
                sentinel="[SENTINEL-BUG-DES:smallest-causal-correction-preserved-regression-design]",
            ),
            WorkflowObligation(
                variant="Refactor Design",
                carrier="design",
                obligations=(
                    "Target responsibilities/interfaces, preservation, cutover/removals "
                    "and test architecture"
                ),
                carrier_field="key_decisions.rationale",
                sentinel="[SENTINEL-REF-DES:target-responsibilities-cutover-removals-test-arch]",
            ),
            WorkflowObligation(
                variant="Epic Design",
                carrier="design",
                obligations=(
                    "Cross-workstream interfaces, ownership, integration/failures "
                    "and shared evidence obligations"
                ),
                carrier_field="options",
                sentinel="[SENTINEL-EPIC-DES:cross-workstream-interfaces-integration-evidence]",
            ),
            # Planning carrier variants (DI-07 §7.2)
            WorkflowObligation(
                variant="Feature Planning",
                carrier="planning",
                obligations=(
                    "Dependency-ordered work, deliverables, verification and exit criteria"
                ),
                carrier_field="summary",
                sentinel="[SENTINEL-FEAT-PLAN:dependency-ordered-deliverables-exit-criteria]",
            ),
            WorkflowObligation(
                variant="Bug Planning",
                carrier="planning",
                obligations=("Reproduction/regression/correction obligations and exit evidence"),
                carrier_field="work_units.goal",
                sentinel="[SENTINEL-BUG-PLAN:repro-regression-correction-exit-evidence]",
            ),
            WorkflowObligation(
                variant="Refactor Planning",
                carrier="planning",
                obligations=(
                    "Responsibility moves, preservation/removal obligations, "
                    "dependencies and stop conditions"
                ),
                carrier_field="work_units.deliverables",
                sentinel="[SENTINEL-REF-PLAN:responsibility-moves-preservation-stop-conditions]",
            ),
            WorkflowObligation(
                variant="Docs Planning",
                carrier="planning",
                obligations=(
                    "Documentation scope/ownership, sources, deliverables, risks and "
                    "verification; no invented TDD cycles"
                ),
                carrier_field="dependencies",
                sentinel="[SENTINEL-DOCS-PLAN:docs-scope-sources-deliverables-no-invented-cycles]",
            ),
            WorkflowObligation(
                variant="Epic Planning",
                carrier="planning",
                obligations=(
                    "Child ownership, shared obligations/dependencies, acceptance "
                    "and stop conditions"
                ),
                carrier_field="milestones",
                sentinel="[SENTINEL-EPIC-PLAN:child-ownership-shared-obligations-acceptance]",
            ),
            # Validation Report carrier variants (DI-07 §7.2)
            WorkflowObligation(
                variant="Feature Validation",
                carrier="validation_report",
                obligations=(
                    "Observed requirement coverage, demonstration, failures, "
                    "caveats/risks and deferred work"
                ),
                carrier_field="scope",
                sentinel="[SENTINEL-FEAT-VAL:observed-requirement-coverage-demonstration-caveats]",
            ),
            WorkflowObligation(
                variant="Bug Validation",
                carrier="validation_report",
                obligations="Observed reproduction correction, regression and preserved behavior",
                carrier_field="scope",
                sentinel="[SENTINEL-BUG-VAL:observed-repro-correction-regression-preserved]",
            ),
            WorkflowObligation(
                variant="Refactor Validation",
                carrier="validation_report",
                obligations=(
                    "Observed structural completion/removal, invariants and "
                    "outstanding failures/caveats"
                ),
                carrier_field="scope",
                sentinel="[SENTINEL-REF-VAL:structural-completion-removal-invariants-caveats]",
            ),
            WorkflowObligation(
                variant="Hotfix Validation",
                carrier="validation_report",
                obligations="Correction, containment, preservation and operational risks/caveats",
                carrier_field="scope",
                sentinel="[SENTINEL-HOTFIX-VAL:correction-containment-preservation-operational]",
            ),
            WorkflowObligation(
                variant="Chore Validation",
                carrier="validation_report",
                obligations=(
                    "Bounded objective coverage and proportionate observed "
                    "evidence/risks/deferred work"
                ),
                carrier_field="scope",
                sentinel="[SENTINEL-CHORE-VAL:bounded-objective-proportionate-observed-evidence]",
            ),
        ]

        assert len(obligations) == 19
        assert len({item.sentinel for item in obligations}) == 19
        assert len({item.variant for item in obligations}) == 19

        sentinel_map = {ob.variant: ob.sentinel for ob in obligations}

        # 1. Research carrier (covers Feature, Bug, Refactor, Chore, Epic research semantics)
        research_context = {
            "title": "Representative Research Carrier",
            "document_metadata": {
                "status": "APPROVED",
                "revisions": [
                    {
                        "version": "1.0",
                        "date": "2026-09-17",
                        "author": "Template fixture",
                        "change": "Authored fixture revision.",
                    }
                ],
            },
            "problem_statement": (
                f"{sentinel_map['Bug Research']}\n"
                "Investigate responsibility and coupling problems, reproduction context, "
                "and workstream boundaries across affected workflows."
            ),
            "goals": [
                "Map affected code, config, tests, docs, and consumers across workstreams",
                "Formulate viable compatibility, migration, and containment strategies",
                "Identify preservation invariants, assumptions, dependencies, and risks",
            ],
            "purpose": (
                f"{sentinel_map['Chore Research']}\n"
                "Establish evidence-backed research covering Feature, Bug, Refactor, "
                "Chore, and Epic obligations."
            ),
            "scope_in": (
                f"{sentinel_map['Refactor Research']}\n"
                "Production seams, invariant preservation, alternatives, and strategy options"
            ),
            "scope_out": "Fix design, cycle sequencing, and child issue creation",
            "background": (
                f"{sentinel_map['Epic Research']}\n"
                "Causal evidence and architectural seams mapped across consumers and dependencies."
            ),
            "findings": (
                f"{sentinel_map['Feature Research']}\n"
                "Alternatives evaluated with comparative risk analysis; preservation invariants "
                "and Epic dependencies documented with causal evidence."
            ),
            "approved_strategy": (
                "Preserve supported contracts without breaking changes; clean-break where required"
            ),
            "expected_results": (
                "All existing caller contracts preserved; new behavior additive and verified"
            ),
            "prerequisites": ["docs/coding_standards/ARCHITECTURE_PRINCIPLES.md"],
            "questions": ["Are external consumers pinned to exact schema versions?"],
            "related_docs": [
                {
                    "label": "Workflow Design",
                    "target": "docs/development/issue460/design-workflow-documentation.md",
                }
            ],
        }

        # 2. Design carrier (covers Feature, Bug, Refactor, Epic design semantics)
        design_context = {
            "title": "Representative Design Carrier",
            "document_metadata": {
                "status": "APPROVED",
                "revisions": [
                    {
                        "version": "1.0",
                        "date": "2026-09-17",
                        "author": "Template fixture",
                        "change": "Authored fixture revision.",
                    }
                ],
            },
            "problem_statement": (
                f"{sentinel_map['Bug Design']}\n"
                "Technical design resolving root cause, public interfaces, and constraints."
            ),
            "requirements_functional": [
                (
                    f"{sentinel_map['Feature Design']}: "
                    "Target responsibilities, public interfaces, and data/control flow"
                ),
                "Failure behavior and cross-workstream integration obligations",
                "Smallest causal correction preserving existing behavior and cutover/removals",
            ],
            "requirements_nonfunctional": [
                "No runtime performance degradation; strict type-checking compliance",
                "Durable regression evidence design and test architecture",
            ],
            "decision": "Introduce narrow read-only interfaces and config-driven dispatch.",
            "rationale": "Enforces ISP and OCP principles as required by Architecture Contract.",
            "purpose": (
                "Comprehensive design covering Feature, Bug, Refactor, and Epic semantics."
            ),
            "scope_in": "Architecture, interfaces, data flow, failure behavior, and test design",
            "scope_out": "Cycle sequencing, production implementation code",
            "constraints": ["Backward compatibility for public tool parameters"],
            "options": [
                {
                    "name": "Config-driven dispatch with narrow read-only interfaces",
                    "description": (
                        f"{sentinel_map['Epic Design']}\n"
                        "Cross-workstream design with explicit failure behavior, "
                        "test architecture, and clean-break cutover."
                    ),
                    "pros": [
                        "Clear separation of concerns",
                        "Deterministic regression coverage",
                    ],
                    "cons": ["Requires careful sequencing across dependent components"],
                }
            ],
            "key_decisions": [
                {
                    "decision": (
                        "Smallest causal correction preserving behavior and cutover/removals"
                    ),
                    "rationale": (
                        f"{sentinel_map['Refactor Design']}\n"
                        "Enforces ISP and OCP principles without unnecessary breakage"
                    ),
                }
            ],
            "prerequisites": ["docs/coding_standards/ARCHITECTURE_PRINCIPLES.md"],
            "related_docs": [
                {
                    "label": "Workflow Design",
                    "target": "docs/development/issue460/design-workflow-documentation.md",
                }
            ],
        }

        # 3. Planning carrier (covers Feature, Bug, Refactor, Docs, Epic planning semantics)
        planning_context = {
            "title": "Representative Planning Carrier",
            "document_metadata": {
                "status": "APPROVED",
                "revisions": [
                    {
                        "version": "1.0",
                        "date": "2026-09-17",
                        "author": "Template fixture",
                        "change": "Authored fixture revision.",
                    }
                ],
            },
            "summary": (
                f"{sentinel_map['Feature Planning']}\n"
                "Decomposition of approved design into dependency-ordered work units, "
                "covering Feature, Bug, Refactor, Docs, and Epic obligations."
            ),
            "purpose": "Planning artifact expressing the full union of planning semantics.",
            "scope_in": (
                "Work unit breakdown, deliverables, verification, exit criteria, "
                "and stop conditions"
            ),
            "scope_out": "Premature implementation changes",
            "dependencies": [
                sentinel_map["Docs Planning"],
                "DI-07 §7.1 instruction alignment",
                "DI-03 template suite delivery",
                "Cross-workstream child issue tracking",
            ],
            "work_units": [
                {
                    "id": "CY068",
                    "name": "Workflow carriers and phase semantics",
                    "goal": (
                        f"{sentinel_map['Bug Planning']}: "
                        "Verify workflow carriers and phase semantics"
                    ),
                    "deliverables": [
                        {
                            "id": "DOCFLOW-E01",
                            "description": "Verify isolated contracts loading and hash integrity",
                        },
                        {
                            "id": "DOCFLOW-E02",
                            "description": (
                                f"{sentinel_map['Refactor Planning']}: "
                                "Reproduction, regression, correction, and preservation obligations"
                            ),
                        },
                    ],
                    "exit_criteria": (
                        "All 19 workflow semantic meanings preserved in rendered output"
                    ),
                    "dependencies": ["CY067"],
                    "stop_conditions": ["Preservation obligations satisfied"],
                }
            ],
            "risks": [
                {
                    "description": "Schema validation mismatch on optional context fields",
                    "mitigation": "Schema introspection and first-time-right payload verification",
                }
            ],
            "milestones": [
                (
                    f"{sentinel_map['Epic Planning']}: "
                    "M1: Document carrier semantics validated against public schemas"
                ),
                "M2: Exit criteria satisfied with objective proof",
            ],
            "prerequisites": ["docs/coding_standards/ARCHITECTURE_PRINCIPLES.md"],
            "related_docs": [
                {
                    "label": "Workflow Design",
                    "target": "docs/development/issue460/design-workflow-documentation.md",
                }
            ],
        }

        # 4. Validation Report carrier (covers Feature, Bug, Refactor, Hotfix, Chore)
        validation_scope_elements = [
            f"{sentinel_map['Feature Validation']}: Requirement coverage and demo",
            f"{sentinel_map['Bug Validation']}: Reproduction correction and regression prevention",
            f"{sentinel_map['Refactor Validation']}: Structural completion and invariant proof",
            f"{sentinel_map['Hotfix Validation']}: Correction, containment, and operational risks",
            f"{sentinel_map['Chore Validation']}: Bounded objective coverage and evidence",
        ]
        validation_context = {
            "title": "Representative Validation Carrier",
            "document_metadata": {
                "status": "APPROVED",
                "revisions": [
                    {
                        "version": "1.0",
                        "date": "2026-09-17",
                        "author": "Template fixture",
                        "change": "Authored fixture revision.",
                    }
                ],
            },
            "issue_number": 460,
            "cycle": "CY068",
            "validation_status": "PASS",
            "scope": "\n\n".join(validation_scope_elements),
        }

        carriers = {
            "research": research_context,
            "design": design_context,
            "planning": planning_context,
            "validation_report": validation_context,
        }

        rendered_outputs: dict[str, str] = {}

        for template_id, context in carriers.items():
            delivered = load_delivered_template(
                source_suite=suite,
                source_package=suite / template_id,
                config_root=config_root,
                destination=tmp_path / f"delivered_{template_id}",
                template_id=template_id,
            )

            # 1. Canonical V3 rendering via delivered catalog and renderer
            content = delivered.renderer.render(
                template_id,
                context,
                delivered.provenance,
            )
            rendered_outputs[template_id] = content

            # 2. Canonical V3 public scaffold tool execution
            run_root = tmp_path / f"run_{template_id}"
            run_root.mkdir(parents=True, exist_ok=True)
            profile = delivered.catalog.get(template_id).policy.output_profile
            checks, _, _ = compose_check_service(
                run_root,
                ("passed",),
                profile_id=profile,
            )
            locations = ArtifactLocationsConfig.model_validate(
                {"version": "2.0.0", "artifacts": {template_id: {"default_root": "outputs"}}}
            )
            resolver = ArtifactTargetResolver(
                paths=FileArtifactTargetPaths(run_root),
                temporary_artifacts_root=resolve_temporary_paths(
                    run_root / "server"
                ).artifacts_root,
                locations=locations,
            )
            identity = ArtifactIdentity.model_validate(thaw_json(delivered.provenance))
            operation = ScaffoldOperation(
                catalog=delivered.catalog,
                identities=(identity,),
                targets=resolver,
                render=delivered.renderer.render,
                checks=checks,
                creator=CreateOnlyFileWriter(),
                workspace_root=run_root,
            )
            tool = ScaffoldArtifactTool(operation=operation, catalog=delivered.catalog)
            assert tool.args_model is not None
            tool_input = tool.args_model(
                artifact_type=template_id,
                file_name=f"{template_id}.md",
                target_path="outputs",
                force_target=True,
                context=context,
                validation="report",
            )
            exec_result = await tool.execute(tool_input, NoteContext())
            assert exec_result.operation.success is True
            assert exec_result.operation.written is True
            saved_content = (run_root / f"outputs/{template_id}.md").read_text(encoding="utf-8")
            assert saved_content == content

        # Assert no Jinja template tags leaked into rendered output
        for carrier_name, content in rendered_outputs.items():
            assert "{{" not in content, f"Unrendered Jinja expression in {carrier_name}"
            assert "{%" not in content, f"Unrendered Jinja statement in {carrier_name}"

        # Assert all 19 workflow obligations survived into rendered Markdown
        for item in obligations:
            rendered = rendered_outputs[item.carrier]
            assert item.sentinel in rendered, (
                f"Obligation for '{item.variant}' ({item.carrier}.{item.carrier_field}) "
                f"was not preserved in rendered Markdown:\n{item.obligations}"
            )
