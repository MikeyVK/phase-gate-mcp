"""
Unit tests for label tool integration with LabelConfig.

Tests validation hooks in CreateLabelTool, AddLabelsTool, and DetectLabelDriftTool.

@layer: Tests (Unit)
@dependencies: [pytest, mcp_server.tools.label_tools, mcp_server.config.label_config]
"""

# Standard library
from pathlib import Path
from unittest.mock import Mock

# Third-party
import pytest
from pydantic import ValidationError

# Local
from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas import LabelConfig
from mcp_server.config.schemas.label_config import validate_phase_label
from mcp_server.config.schemas.workphases import PhaseDefinition
from mcp_server.core.exceptions import ExecutionError
from mcp_server.core.operation_notes import NoteContext
from mcp_server.schemas import WorkphasesConfig
from mcp_server.schemas.tool_outputs import CreateLabelOutput, LabelOperationOutput
from mcp_server.tools.label_tools import (
    AddLabelsInput,
    AddLabelsTool,
    CreateLabelInput,
    CreateLabelTool,
    DetectLabelDriftInput,
    DetectLabelDriftTool,
)


# Test Helper
class _MockLabel:  # pylint: disable=too-few-public-methods
    """Mock label object for testing (avoids Mock.name conflict)."""

    def __init__(self, name: str, color: str, description: str = "") -> None:
        self.name = name
        self.color = color
        self.description = description


_PGMCP_CONFIG = Path(__file__).resolve().parents[4] / ".phase-gate" / "config"


def _load_label_config(tmp_path: Path, yaml_content: str) -> LabelConfig:
    yaml_file = tmp_path / "labels.yaml"
    yaml_file.write_text(yaml_content)
    return ConfigLoader(_PGMCP_CONFIG).load_label_config(config_path=yaml_file)


class TestCreateLabelToolValidation:
    """Tests for CreateLabelTool validation hooks."""

    @pytest.mark.asyncio
    async def test_create_label_validates_name_pattern(self) -> None:
        """Invalid label name pattern is rejected at schema validation level (Pydantic)."""
        with pytest.raises(ValidationError, match="string_pattern_mismatch"):
            CreateLabelInput(name="invalid-name", color="FF0000")

    @pytest.mark.asyncio
    async def test_create_label_rejects_hash_prefix(self) -> None:
        """Color with # prefix is rejected at schema validation level (Pydantic)."""
        with pytest.raises(ValidationError, match="string_pattern_mismatch"):
            CreateLabelInput(name="type:bug", color="#FF0000")

    @pytest.mark.asyncio
    async def test_create_label_valid_succeeds(self, tmp_path: Path) -> None:
        """CreateLabelTool creates label with valid name and color."""
        yaml_content = """version: "1.0"
labels:
  - name: "type:feature"
    color: "1D76DB"
"""
        label_config = _load_label_config(tmp_path, yaml_content)

        mock_manager = Mock()
        mock_manager.create_label = Mock(return_value=_MockLabel(name="type:bug", color="FF0000"))

        tool = CreateLabelTool(
            manager=mock_manager,
            label_config=label_config,
            workphases_config=Mock(),
        )
        params = CreateLabelInput(name="type:bug", color="FF0000")

        result = await tool.execute(params, NoteContext())
        assert isinstance(result, CreateLabelOutput)
        assert result.label_name == "type:bug"
        assert result.color == "FF0000"
        mock_manager.create_label.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_label_freeform_exception_allowed(self) -> None:
        """Freeform label names are rejected at schema validation level (Pydantic).

        The CreateLabelInput.name pattern enforces 'category:value' format.
        Freeform exceptions configured in labels.yaml cannot bypass this boundary.
        """
        with pytest.raises(ValidationError, match="string_pattern_mismatch"):
            CreateLabelInput(name="good first issue", color="7057FF")


class TestAddLabelsToolValidation:
    """Tests for AddLabelsTool validation hooks."""

    @pytest.mark.asyncio
    async def test_add_labels_validates_existence(self, tmp_path: Path) -> None:
        """AddLabelsTool rejects undefined labels (strict enforcement)."""
        yaml_content = """version: "1.0"
labels:
  - name: "type:feature"
    color: "1D76DB"
"""
        label_config = _load_label_config(tmp_path, yaml_content)

        tool = AddLabelsTool(manager=Mock(), label_config=label_config, workphases_config=Mock())
        params = AddLabelsInput(issue_number=1, labels=["undefined-label"])

        with pytest.raises(ExecutionError, match="Labels not valid per labels.yaml"):
            await tool.execute(params, NoteContext())

    @pytest.mark.asyncio
    async def test_add_labels_all_valid_succeeds(self, tmp_path: Path) -> None:
        """AddLabelsTool adds all labels when all are valid."""
        yaml_content = """version: "1.0"
labels:
  - name: "type:feature"
    color: "1D76DB"
  - name: "priority:high"
    color: "D93F0B"
"""
        label_config = _load_label_config(tmp_path, yaml_content)

        mock_manager = Mock()
        tool = AddLabelsTool(
            manager=mock_manager,
            label_config=label_config,
            workphases_config=Mock(),
        )
        params = AddLabelsInput(issue_number=1, labels=["type:feature", "priority:high"])

        result = await tool.execute(params, NoteContext())
        assert isinstance(result, LabelOperationOutput)
        assert result.issue_number == 1
        assert result.labels == ["type:feature", "priority:high"]
        mock_manager.add_labels.assert_called_once_with(1, ["type:feature", "priority:high"])

    @pytest.mark.asyncio
    async def test_add_labels_partial_invalid_rejects_all(self, tmp_path: Path) -> None:
        """AddLabelsTool rejects entire operation if ANY label is undefined."""
        yaml_content = """version: "1.0"
labels:
  - name: "type:feature"
    color: "1D76DB"
"""
        label_config = _load_label_config(tmp_path, yaml_content)

        mock_manager = Mock()
        tool = AddLabelsTool(
            manager=mock_manager,
            label_config=label_config,
            workphases_config=Mock(),
        )
        params = AddLabelsInput(issue_number=1, labels=["type:feature", "undefined"])

        with pytest.raises(ExecutionError, match="Labels not valid per labels.yaml"):
            await tool.execute(params, NoteContext())
        mock_manager.add_labels.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_labels_freeform_allowed(self, tmp_path: Path) -> None:
        """AddLabelsTool accepts freeform exceptions."""
        yaml_content = """version: "1.0"
freeform_exceptions:
  - "good first issue"
labels:
  - name: "type:feature"
    color: "1D76DB"
  - name: "good first issue"
    color: "7057FF"
"""
        label_config = _load_label_config(tmp_path, yaml_content)

        mock_manager = Mock()
        tool = AddLabelsTool(
            manager=mock_manager,
            label_config=label_config,
            workphases_config=Mock(),
        )
        params = AddLabelsInput(issue_number=1, labels=["good first issue"])

        result = await tool.execute(params, NoteContext())
        assert isinstance(result, LabelOperationOutput)
        assert result.issue_number == 1
        assert result.labels == ["good first issue"]

    @pytest.mark.asyncio
    async def test_add_labels_accepts_dynamic_pattern_label(self, tmp_path: Path) -> None:
        """AddLabelsTool accepts labels matching label_patterns (e.g. parent:302)."""
        yaml_content = """version: "1.0"
label_patterns:
  - pattern: "^parent:\\\\d+$"
    description: "Parent issue reference"
    color: "EDEDED"
    example: "parent:91"
labels:
  - name: "type:feature"
    color: "1D76DB"
"""
        label_config = _load_label_config(tmp_path, yaml_content)
        mock_manager = Mock()
        tool = AddLabelsTool(
            manager=mock_manager,
            label_config=label_config,
            workphases_config=Mock(),
        )
        params = AddLabelsInput(issue_number=1, labels=["parent:302"])

        result = await tool.execute(params, NoteContext())

        assert isinstance(result, LabelOperationOutput)
        assert result.issue_number == 1
        assert result.labels == ["parent:302"]
        mock_manager.add_labels.assert_called_once_with(1, ["parent:302"])


class TestDetectLabelDriftTool:
    """Tests for DetectLabelDriftTool (read-only drift detection)."""

    @pytest.mark.asyncio
    async def test_drift_detection_github_has_extra_labels(self, tmp_path: Path) -> None:
        """DetectLabelDriftTool detects labels in GitHub not in YAML."""
        yaml_content = """version: "1.0"
labels:
  - name: "type:feature"
    color: "1D76DB"
"""
        label_config = _load_label_config(tmp_path, yaml_content)

        mock_manager = Mock()
        mock_manager.list_labels = Mock(
            return_value=[
                _MockLabel(name="type:feature", color="1D76DB", description=""),
                _MockLabel(name="custom-label", color="FF0000", description=""),
            ]
        )

        tool = DetectLabelDriftTool(manager=mock_manager, label_config=label_config)
        params = DetectLabelDriftInput()

        result = await tool.execute(params, NoteContext())
        result_text = result.content[0]["text"]
        assert "drift detected" in result_text.lower()
        assert "GitHub-only labels" in result_text
        assert "custom-label" in result_text

    @pytest.mark.asyncio
    async def test_drift_detection_yaml_has_extra_labels(self, tmp_path: Path) -> None:
        """DetectLabelDriftTool detects labels in YAML not in GitHub."""
        yaml_content = """version: "1.0"
labels:
  - name: "type:feature"
    color: "1D76DB"
  - name: "type:new"
    color: "FF0000"
"""
        label_config = _load_label_config(tmp_path, yaml_content)

        mock_manager = Mock()
        mock_manager.list_labels = Mock(
            return_value=[_MockLabel(name="type:feature", color="1D76DB", description="")]
        )

        tool = DetectLabelDriftTool(manager=mock_manager, label_config=label_config)
        params = DetectLabelDriftInput()

        result = await tool.execute(params, NoteContext())
        result_text = result.content[0]["text"]
        assert "drift detected" in result_text.lower()
        assert "YAML-only labels" in result_text
        assert "type:new" in result_text

    @pytest.mark.asyncio
    async def test_drift_detection_color_mismatch(self, tmp_path: Path) -> None:
        """DetectLabelDriftTool detects color differences."""
        yaml_content = """version: "1.0"
labels:
  - name: "type:feature"
    color: "1D76DB"
"""
        label_config = _load_label_config(tmp_path, yaml_content)

        # Create mock label with attributes (not Mock object)
        class MockLabel:
            def __init__(self, name: str, color: str, description: str) -> None:
                self.name = name
                self.color = color
                self.description = description

        mock_manager = Mock()
        mock_manager.list_labels = Mock(
            return_value=[MockLabel(name="type:feature", color="FF0000", description="")]
        )

        tool = DetectLabelDriftTool(manager=mock_manager, label_config=label_config)
        params = DetectLabelDriftInput()

        result = await tool.execute(params, NoteContext())
        result_text = result.content[0]["text"]
        assert "drift detected" in result_text.lower()
        assert "Color mismatches" in result_text
        assert "1D76DB" in result_text
        assert "FF0000" in result_text

    @pytest.mark.asyncio
    async def test_drift_detection_description_mismatch(self, tmp_path: Path) -> None:
        """DetectLabelDriftTool detects description differences."""
        yaml_content = """version: "1.0"
labels:
  - name: "type:feature"
    color: "1D76DB"
    description: "YAML description"
"""
        label_config = _load_label_config(tmp_path, yaml_content)

        mock_manager = Mock()
        mock_manager.list_labels = Mock(
            return_value=[
                _MockLabel(
                    name="type:feature",
                    color="1D76DB",
                    description="GitHub description",
                )
            ]
        )

        tool = DetectLabelDriftTool(manager=mock_manager, label_config=label_config)
        params = DetectLabelDriftInput()

        result = await tool.execute(params, NoteContext())
        result_text = result.content[0]["text"]
        assert "drift detected" in result_text.lower()
        assert "Description mismatches" in result_text

    @pytest.mark.asyncio
    async def test_drift_detection_no_drift(self, tmp_path: Path) -> None:
        """DetectLabelDriftTool reports no drift when aligned."""
        yaml_content = """version: "1.0"
labels:
  - name: "type:feature"
    color: "1D76DB"
    description: "Test"
"""
        label_config = _load_label_config(tmp_path, yaml_content)

        mock_manager = Mock()
        mock_manager.list_labels = Mock(
            return_value=[_MockLabel(name="type:feature", color="1D76DB", description="Test")]
        )

        tool = DetectLabelDriftTool(manager=mock_manager, label_config=label_config)
        params = DetectLabelDriftInput()

        result = await tool.execute(params, NoteContext())
        result_text = result.content[0]["text"]
        assert "no drift detected" in result_text.lower()
        assert "aligned" in result_text.lower()

    @pytest.mark.asyncio
    async def test_drift_detection_returns_structured_report(self, tmp_path: Path) -> None:
        """DetectLabelDriftTool returns structured drift report."""
        yaml_content = """version: "1.0"
labels:
  - name: "type:feature"
    color: "1D76DB"
"""
        label_config = _load_label_config(tmp_path, yaml_content)

        mock_manager = Mock()
        mock_manager.list_labels = Mock(
            return_value=[
                _MockLabel(name="type:feature", color="FF0000", description=""),  # Color mismatch
                _MockLabel(name="github-only", color="000000", description=""),  # GitHub only
            ]
        )

        tool = DetectLabelDriftTool(manager=mock_manager, label_config=label_config)
        params = DetectLabelDriftInput()

        result = await tool.execute(params, NoteContext())
        result_text = result.content[0]["text"]
        # Should contain multiple drift types
        assert "GitHub-only labels" in result_text
        assert "Color mismatches" in result_text
        assert "github-only" in result_text

    @pytest.mark.asyncio
    async def test_drift_detection_handles_github_api_error(self, tmp_path: Path) -> None:
        """DetectLabelDriftTool handles GitHub API errors gracefully."""
        yaml_content = """version: "1.0"
labels:
  - name: "type:feature"
    color: "1D76DB"
"""
        label_config = _load_label_config(tmp_path, yaml_content)

        mock_manager = Mock()
        mock_manager.list_labels = Mock(side_effect=Exception("API Error"))

        tool = DetectLabelDriftTool(manager=mock_manager, label_config=label_config)
        params = DetectLabelDriftInput()

        result = await tool.execute(params, NoteContext())
        assert "Error loading labels" in result.content[0]["text"]

    @pytest.mark.asyncio
    async def test_drift_detection_pattern_labels_not_reported_as_drift(
        self, tmp_path: Path
    ) -> None:
        """DetectLabelDriftTool does NOT flag GitHub labels matching label_patterns as drift."""
        yaml_content = """version: "1.0"
label_patterns:
  - pattern: "^parent:\\\\d+$"
    description: "Parent issue reference"
    color: "EDEDED"
    example: "parent:91"
labels:
  - name: "type:feature"
    color: "1D76DB"
"""
        label_config = _load_label_config(tmp_path, yaml_content)

        mock_manager = Mock()
        mock_manager.list_labels = Mock(
            return_value=[
                _MockLabel(name="type:feature", color="1D76DB", description=""),
                _MockLabel(name="parent:302", color="EDEDED", description=""),
            ]
        )

        tool = DetectLabelDriftTool(manager=mock_manager, label_config=label_config)
        params = DetectLabelDriftInput()

        result = await tool.execute(params, NoteContext())
        result_text = result.content[0]["text"]

        assert "parent:302" not in result_text
        assert "no drift detected" in result_text.lower()


@pytest.fixture
def workphases_config() -> WorkphasesConfig:
    """Minimal WorkphasesConfig fixture with standard phases."""
    return WorkphasesConfig(
        version="1.0",
        phases={
            "research": PhaseDefinition(display_name="Research"),
            "planning": PhaseDefinition(display_name="Planning"),
            "implementation": PhaseDefinition(display_name="Implementation"),
            "ready": PhaseDefinition(display_name="Ready", terminal=True),
        },
    )


# ─── validate_phase_label() unit tests ─────────────────────────────────────────────


class TestValidatePhaseLabelFunction:
    """Unit tests for the validate_phase_label() free function."""

    def test_non_phase_label_is_always_valid(self, workphases_config: WorkphasesConfig) -> None:
        is_valid, _ = validate_phase_label("type:feature", workphases_config)
        assert is_valid

    def test_known_phase_is_valid(self, workphases_config: WorkphasesConfig) -> None:
        is_valid, msg = validate_phase_label("phase:implementation", workphases_config)
        assert is_valid
        assert msg == ""

    def test_unknown_phase_is_invalid(self, workphases_config: WorkphasesConfig) -> None:
        is_valid, msg = validate_phase_label("phase:unicorn", workphases_config)
        assert not is_valid
        assert "unicorn" in msg
        assert "Valid phases" in msg

    def test_subphase_is_invalid(self, workphases_config: WorkphasesConfig) -> None:
        """Subphases like 'red', 'green', 'refactor' are not valid issue labels."""
        is_valid, msg = validate_phase_label("phase:red", workphases_config)
        assert not is_valid
        assert "red" in msg

    def test_stale_integration_phase_is_invalid(self, workphases_config: WorkphasesConfig) -> None:
        is_valid, _ = validate_phase_label("phase:integration", workphases_config)
        assert not is_valid


# ─── AddLabelsTool phase:* semantic check ───────────────────────────────────────────────


class TestAddLabelsToolPhaseValidation:
    """AddLabelsTool rejects phase:* labels for unknown workphases."""

    @pytest.mark.asyncio
    async def test_add_labels_rejects_unknown_phase(
        self, tmp_path: Path, workphases_config: WorkphasesConfig
    ) -> None:
        """AddLabelsTool rejects phase labels not in workphases.yaml."""
        yaml_content = """version: "1.0"
label_patterns:
  - pattern: "^phase:[a-z][a-z0-9-]*$"
    description: "Workflow phase label"
    color: "C5DEF5"
    example: "phase:research"
labels: []
"""
        label_config = _load_label_config(tmp_path, yaml_content)
        mock_manager = Mock()
        tool = AddLabelsTool(
            manager=mock_manager, label_config=label_config, workphases_config=workphases_config
        )
        params = AddLabelsInput(issue_number=1, labels=["phase:unicorn"])

        with pytest.raises(ExecutionError, match="unknown workphase"):
            await tool.execute(params, NoteContext())
        mock_manager.add_labels.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_labels_accepts_known_phase(
        self, tmp_path: Path, workphases_config: WorkphasesConfig
    ) -> None:
        """AddLabelsTool accepts phase:implementation as a valid phase label."""
        yaml_content = """version: "1.0"
label_patterns:
  - pattern: "^phase:[a-z][a-z0-9-]*$"
    description: "Workflow phase label"
    color: "C5DEF5"
    example: "phase:research"
labels: []
"""
        label_config = _load_label_config(tmp_path, yaml_content)
        mock_manager = Mock()
        tool = AddLabelsTool(
            manager=mock_manager, label_config=label_config, workphases_config=workphases_config
        )
        params = AddLabelsInput(issue_number=1, labels=["phase:implementation"])

        result = await tool.execute(params, NoteContext())

        assert isinstance(result, LabelOperationOutput)
        assert result.issue_number == 1
        assert result.labels == ["phase:implementation"]
