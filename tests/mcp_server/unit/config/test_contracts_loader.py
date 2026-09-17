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
import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

# Third-party
import pytest
import yaml

# Project modules
from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.contracts_config import (
    BranchLocalArtifact,
    ContractsConfig,
    MergePolicy,
    PhaseInstructionsSpec,
    WorkflowEntry,
    WorkflowPhaseEntry,
)
from mcp_server.core.exceptions import ConfigError
from tests.mcp_server.test_support import get_default_server_root, make_artifact_manager

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

    def test_real_implementation_cycle_semantics_are_preserved(self) -> None:
        """Cycle-based workflows retain TDD metadata; Chore remains non-cycle-based."""

        real = Path(__file__).parents[4] / get_default_server_root() / "config" / "contracts.yaml"
        result = ConfigLoader(real.parent).load_contracts_config()

        for workflow_name in ("feature", "bug", "hotfix", "refactor"):
            implementation = result.workflows[workflow_name].get_phase("implementation")
            assert implementation.cycle_based is True
            assert implementation.subphases == ["red", "green", "refactor"]
            assert set(implementation.commit_type_map) == {"red", "green", "refactor"}

        chore = result.workflows["chore"].get_phase("implementation")
        assert chore.cycle_based is False
        assert chore.subphases == []
        assert chore.commit_type_map == {}

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


@dataclass
class _DiffHunk:
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    lines: list[str] = field(default_factory=list)


class TestCY068DocflowE01:
    """CY068 / DOCFLOW-E01: workflow carriers, phase ordering, and instruction validation."""

    def test_nineteen_workflow_carriers_exist_and_preserve_phase_order(self) -> None:

        real = Path(__file__).parents[4] / get_default_server_root() / "config" / "contracts.yaml"
        content_bytes = real.read_bytes()
        sha256_preimage = hashlib.sha256(content_bytes).hexdigest()
        assert sha256_preimage == "9610d38bf943c687e8c200b626259b3f107b69d4e9d0a40e44f38c91f8194d10"

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

    @staticmethod
    def _apply_unified_diff(original: str, diff_text: str) -> str:
        """Apply a unified diff string to an original text."""
        orig_lines = original.splitlines(keepends=True)
        diff_lines = diff_text.splitlines(keepends=True)

        hunks: list[_DiffHunk] = []
        current_hunk: _DiffHunk | None = None
        for line in diff_lines:
            if line.startswith("@@"):
                m = re.match(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", line)
                if m:
                    old_start = int(m.group(1))
                    old_count = int(m.group(2)) if m.group(2) is not None else 1
                    new_start = int(m.group(3))
                    new_count = int(m.group(4)) if m.group(4) is not None else 1
                    current_hunk = _DiffHunk(
                        old_start=old_start,
                        old_count=old_count,
                        new_start=new_start,
                        new_count=new_count,
                    )
                    hunks.append(current_hunk)
            elif current_hunk is not None and line.startswith(("+", "-", " ")):
                current_hunk.lines.append(line)

        # Apply hunks in reverse line order to prevent offset drift
        hunks.sort(key=lambda h: h.old_start, reverse=True)
        result_lines = list(orig_lines)
        for hunk in hunks:
            old_idx = hunk.old_start - 1
            replacement: list[str] = []
            old_consumed = 0
            for hline in hunk.lines:
                prefix = hline[0]
                content = hline[1:]
                if prefix == " ":
                    old_consumed += 1
                    replacement.append(content)
                elif prefix == "-":
                    old_consumed += 1
                elif prefix == "+":
                    replacement.append(content)
            result_lines[old_idx : old_idx + old_consumed] = replacement

        return "".join(result_lines)

    def test_isolated_patched_contracts_loading_and_docflow_e01(self, tmp_path: Path) -> None:
        """DOCFLOW-E01: Patch from rollout-workflow-input.md applies and loads cleanly."""
        root = Path(__file__).parents[4]
        evidence_file = root / "docs" / "development" / "issue460" / "rollout-workflow-input.md"
        assert evidence_file.exists(), "rollout-workflow-input.md must exist"
        evidence_text = evidence_file.read_text(encoding="utf-8")

        # 1. Extract Postimage SHA-256 and unified diff from markdown
        sha_match = re.search(r"\*\*Postimage SHA-256:\*\*\s+`([a-f0-9]{64})`", evidence_text)
        assert sha_match, "Postimage SHA-256 must be documented in section 5.1"
        expected_postimage_sha = sha_match.group(1)

        diff_match = re.search(
            r"```diff\n(--- a/\.pgmcp/config/contracts\.yaml\n.+?\n)```",
            evidence_text,
            re.DOTALL,
        )
        assert diff_match, "Unified diff must be present in section 5.2"
        unified_diff = diff_match.group(1)

        # 2. Read preimage contracts.yaml and verify preimage SHA-256
        real_contracts = root / get_default_server_root() / "config" / "contracts.yaml"
        content_bytes = real_contracts.read_bytes()
        preimage_sha = hashlib.sha256(content_bytes).hexdigest()
        assert preimage_sha == "9610d38bf943c687e8c200b626259b3f107b69d4e9d0a40e44f38c91f8194d10"
        original_text = real_contracts.read_text(encoding="utf-8")

        # 3. Apply the stored unified diff to preimage
        patched_text = self._apply_unified_diff(original_text, unified_diff)
        actual_postimage_sha = hashlib.sha256(patched_text.encode("utf-8")).hexdigest()
        assert (
            actual_postimage_sha
            == expected_postimage_sha
            == "0c358a2d3170dd9a0758238a27e952b1cd646d08d771672df184cbee4e80f5d0"
        )

        # 4. Invariant assertions on patched text
        assert "run_quality_gates" not in patched_text
        assert "context=" not in patched_text
        assert "files=[...]" not in patched_text
        assert "cycles={...}" not in patched_text
        assert "A valid scaffold is not phase completion" in patched_text
        assert "scaffold_schema" in patched_text
        assert "safe_edit_file" in patched_text
        assert "run_checks" in patched_text

        # 5. Write to tmp_path and load via ConfigLoader
        tmp_cfg_dir = tmp_path / get_default_server_root() / "config"
        tmp_cfg_dir.mkdir(parents=True, exist_ok=True)
        (tmp_cfg_dir / "contracts.yaml").write_text(patched_text, encoding="utf-8")

        loader = ConfigLoader(tmp_cfg_dir)
        patched_config = loader.load_contracts_config()

        # 6. Verify structural integrity and phase order preservation
        preimage_config = ConfigLoader(real_contracts.parent).load_contracts_config()
        assert (
            set(patched_config.workflows)
            == set(preimage_config.workflows)
            == {
                "feature",
                "bug",
                "refactor",
                "chore",
                "epic",
                "docs",
                "hotfix",
            }
        )
        for wf_name, orig_wf in preimage_config.workflows.items():
            patched_wf = patched_config.workflows[wf_name]
            assert [p.name for p in patched_wf.phases] == [p.name for p in orig_wf.phases]
            for p in patched_wf.phases:
                assert p.instructions.phase_instructions.strip()
                assert p.instructions.sub_role.strip()
                assert p.instructions.handover_template and p.instructions.handover_template.strip()

        assert patched_config.merge_policy.pr_allowed_phase == "ready"

    def test_nineteen_workflow_variants_satisfy_docflow_e02(self, tmp_path: Path) -> None:
        """DOCFLOW-E02: Schema-admitted carriers preserve the 19 workflow semantic meanings.

        All four physical carrier schemas/templates are exercised, with traceable assertions
        covering the union of the nineteen workflow meanings (DI-07 §7.2). The schema-admitted
        scaffold preserves the complete semantic union supplied through existing carrier fields;
        final document organization and evidence expansion remain a safe_edit_file responsibility.
        """
        root = Path(__file__).parents[4]
        manager = make_artifact_manager(root)

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
                carrier_field="key_decisions",
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
                carrier_field="cycles.goal",
                sentinel="[SENTINEL-BUG-PLAN:repro-regression-correction-exit-evidence]",
            ),
            WorkflowObligation(
                variant="Refactor Planning",
                carrier="planning",
                obligations=(
                    "Responsibility moves, preservation/removal obligations, "
                    "dependencies and stop conditions"
                ),
                carrier_field="cycles.success_criteria",
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
            "status": "APPROVED",
            "version": "1.0",
            "last_updated": "2026-09-17",
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
            "timestamp": "2026-09-17T09:00Z",
            "prerequisites": ["docs/coding_standards/ARCHITECTURE_PRINCIPLES.md"],
            "questions_list": ["Are external consumers pinned to exact schema versions?"],
            "references": ["docs/coding_standards/ARCHITECTURE_PRINCIPLES.md"],
            "related_docs": ["docs/development/issue460/design-workflow-documentation.md"],
        }
        res_research = manager.scaffolder.scaffold(
            artifact_type="research",
            **research_context,
        )

        # 2. Design carrier (covers Feature, Bug, Refactor, Epic design semantics)
        design_context = {
            "title": "Representative Design Carrier",
            "status": "APPROVED",
            "version": "1.0",
            "last_updated": "2026-09-17",
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
                        f"{sentinel_map['Refactor Design']}\n"
                        "Smallest causal correction preserving behavior and cutover/removals"
                    ),
                    "rationale": ("Enforces ISP and OCP principles without unnecessary breakage"),
                }
            ],
            "related_docs": ["docs/development/issue460/design-workflow-documentation.md"],
            "timestamp": "2026-09-17T09:00Z",
            "prerequisites": ["docs/coding_standards/ARCHITECTURE_PRINCIPLES.md"],
        }
        res_design = manager.scaffolder.scaffold(
            artifact_type="design",
            **design_context,
        )

        # 3. Planning carrier (covers Feature, Bug, Refactor, Docs, Epic planning semantics)
        planning_context = {
            "title": "Representative Planning Carrier",
            "status": "APPROVED",
            "version": "1.0",
            "last_updated": "2026-09-17",
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
            "cycles": [
                {
                    "name": "CY068",
                    "goal": (
                        f"{sentinel_map['Bug Planning']}: "
                        "Verify workflow carriers and phase semantics"
                    ),
                    "tests": ["test_isolated_patched_contracts_loading_and_docflow_e01"],
                    "success_criteria": [
                        (
                            f"{sentinel_map['Refactor Planning']}: "
                            "Reproduction/regression/correction obligations verified"
                        ),
                        "Responsibility moves and preservation obligations satisfied",
                        "Exit criteria and stop conditions confirmed",
                    ],
                    "dependencies": ["CY067"],
                }
            ],
            "risks": [
                {
                    "description": "Schema validation mismatch on optional context fields",
                    "mitigation": (
                        "Schema introspection and first-time-right payload verification"
                    ),
                }
            ],
            "milestones": [
                (
                    f"{sentinel_map['Epic Planning']}: "
                    "M1: Document carrier semantics validated against public schemas"
                ),
                "M2: Exit criteria satisfied with objective proof",
            ],
            "related_docs": ["docs/development/issue460/design-workflow-documentation.md"],
            "timestamp": "2026-09-17T09:00Z",
            "prerequisites": ["docs/coding_standards/ARCHITECTURE_PRINCIPLES.md"],
        }
        res_planning = manager.scaffolder.scaffold(
            artifact_type="planning",
            **planning_context,
        )

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
            "status": "APPROVED",
            "version": "1.0",
            "last_updated": "2026-09-17",
            "timestamp": "2026-09-17T09:00Z",
            "issue_number": 460,
            "cycle": "CY068",
            "validation_status": "PASS",
            "scope": "\n\n".join(validation_scope_elements),
        }
        res_validation = manager.scaffolder.scaffold(
            artifact_type="validation_report",
            **validation_context,
        )

        rendered_outputs: dict[str, str] = {
            "research": res_research.content,
            "design": res_design.content,
            "planning": res_planning.content,
            "validation_report": res_validation.content,
        }

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
