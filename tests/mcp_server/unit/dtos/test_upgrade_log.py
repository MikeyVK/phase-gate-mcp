# tests/mcp_server/unit/dtos/test_upgrade_log.py
"""Unit tests for UpgradeLogDTO value object."""

import pytest
from pydantic import ValidationError

from mcp_server.dtos.upgrade_log import UpgradeLogDTO


def test_upgrade_log_dto_creation_and_immutability() -> None:
    """Verify UpgradeLogDTO instantiation and frozen immutability."""
    dto = UpgradeLogDTO(
        timestamp="2026-07-22T18:00:00Z",
        from_version="1.0.0",
        to_version="2.0.0",
        backup_path="/tmp/.pgmcp_backup_20260722_180000",
        renewed_files=["templates/default.yaml"],
        preserved_files=["config/git.yaml"],
        status="success",
        details="Upgrade completed cleanly.",
    )
    assert dto.from_version == "1.0.0"
    assert dto.to_version == "2.0.0"
    assert dto.status == "success"

    with pytest.raises(ValidationError):
        # Attribute assignment must raise ValidationError / TypeError on frozen model
        dto.status = "failed"  # type: ignore[misc]


def test_upgrade_log_dto_forbid_extra() -> None:
    """Verify extra fields raise ValidationError due to extra='forbid'."""
    with pytest.raises(ValidationError):
        UpgradeLogDTO(
            timestamp="2026-07-22T18:00:00Z",
            from_version="1.0.0",
            to_version="2.0.0",
            backup_path="/tmp/backup",
            renewed_files=[],
            preserved_files=[],
            status="success",
            extra_field="invalid",  # type: ignore[call-arg]
        )


def test_upgrade_log_dto_status_literal_validation() -> None:
    """Verify status is restricted to 'success' or 'failed'."""
    with pytest.raises(ValidationError):
        UpgradeLogDTO(
            timestamp="2026-07-22T18:00:00Z",
            from_version="1.0.0",
            to_version="2.0.0",
            backup_path="/tmp/backup",
            renewed_files=[],
            preserved_files=[],
            status="invalid_status",  # type: ignore[arg-type]
        )
