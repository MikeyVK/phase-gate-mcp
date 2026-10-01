"""Installation checkpoint persistence and explicit bootstrap policy."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, ValidationError, model_validator

from mcp_server.config.schemas.installation import (
    InstallationState,
    TemplateCheckpoint,
)
from mcp_server.core.exceptions import MCPError
from mcp_server.services.template_components import ComponentState

BootstrapDisposition = Literal[
    "fresh",
    "candidate_equal",
    "trusted_prior",
    "persisted_evidence",
    "baseline_accepted",
    "checkpoint_required",
    "checkpoint_available",
]
JsonWriter = Callable[[Path, dict[str, object]], None]


class ValidatedSuiteEvidence(BaseModel):
    """Immutable complete component evidence from suite admission."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    shared: ComponentState
    packages: tuple[ComponentState, ...]

    @model_validator(mode="after")
    def validate_complete_components(self) -> ValidatedSuiteEvidence:
        if (
            self.shared.kind != "shared"
            or self.shared.component_id != "shared"
            or not self.shared.present
        ):
            raise ValueError("validated_suite_shared_required")
        if any(package.kind != "package" or not package.present for package in self.packages):
            raise ValueError("validated_suite_package_invalid")
        ids = [package.component_id for package in self.packages]
        if len(ids) != len(set(ids)):
            raise ValueError("validated_suite_package_duplicate")
        return self

    def to_checkpoint(self) -> TemplateCheckpoint:
        """Project complete admitted evidence to the closed checkpoint map."""

        if self.shared.fingerprint is None:
            raise ValueError("validated_suite_shared_fingerprint_required")
        packages: dict[str, str] = {}
        for package in sorted(self.packages, key=lambda item: item.component_id):
            if package.fingerprint is None:
                raise ValueError("validated_suite_package_fingerprint_required")
            packages[package.component_id] = package.fingerprint
        return TemplateCheckpoint(shared=self.shared.fingerprint, packages=packages)


Admission = Callable[[str], ValidatedSuiteEvidence]


class BootstrapResult(BaseModel):
    """Immutable bootstrap facts; no operation is performed by the DTO."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    disposition: BootstrapDisposition
    adopted: ValidatedSuiteEvidence | None = None
    checkpoint: TemplateCheckpoint | None = None
    actual_unchanged: bool = True


def read_installation_state(path: Path) -> InstallationState | None:
    """Read one closed installation document without a write-capable dependency."""

    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise TypeError("installation_document_object_required")
        return InstallationState.model_validate(payload, strict=True)
    except (OSError, ValueError, TypeError, ValidationError) as exc:
        raise MCPError(
            "installation_state_invalid",
            code="ERR_CONFIG",
            params={"path": str(path)},
        ) from exc


class InstallationStateRepository:
    """Read and explicitly publish one installation.json document."""

    def __init__(self, path: Path, *, writer: JsonWriter) -> None:
        self._path = path
        self._writer = writer

    def read(self) -> InstallationState | None:
        """Read the closed document; missing state means checkpoint-less."""

        return read_installation_state(self._path)

    def publish(self, state: InstallationState) -> None:
        """Publish a validated state through the injected atomic writer."""

        payload = state.model_dump(mode="json", exclude_none=True)
        self._writer(self._path, payload)

    def migrate_legacy_compatibility(self, legacy_path: Path) -> None:
        """Explicitly publish legacy compatibility once, without a checkpoint."""

        current = self.read()
        if current is not None:
            return
        version = self.read_legacy_compatibility(legacy_path)
        if version is None:
            raise MCPError("legacy_version_missing", code="ERR_CONFIG")
        state = InstallationState(pgmcp_version=version)
        self.publish(state)

    def read_legacy_compatibility(self, path: Path) -> str | None:
        """Read legacy PGMCP compatibility only when explicitly requested."""

        if not path.exists():
            return None
        try:
            value = path.read_text(encoding="utf-8-sig").strip()
        except OSError as exc:
            raise MCPError(
                "legacy_version_unreadable",
                code="ERR_CONFIG",
                params={"path": str(path)},
            ) from exc
        if not value:
            raise MCPError(
                "legacy_version_invalid",
                code="ERR_CONFIG",
                params={"path": str(path)},
            )
        return value


class BootstrapResolver:
    """Resolve checkpoint-less bootstrap from an injected admission boundary."""

    def __init__(self, *, admission: Admission) -> None:
        self._admission = admission

    def resolve(
        self,
        *,
        candidate_source: str | None = None,
        actual_source: str | None = None,
        trusted_prior_source: str | None = None,
        checkpoint: TemplateCheckpoint | None = None,
        managed: bool,
        fresh: bool = False,
        accept_baseline: bool = False,
        persisted_checkpoint: TemplateCheckpoint | None = None,
    ) -> BootstrapResult:
        """Classify fresh, trustworthy, explicit, or unresolved bootstrap."""

        if checkpoint is not None:
            return BootstrapResult(
                disposition="checkpoint_available",
                checkpoint=checkpoint,
            )
        if candidate_source is None:
            raise MCPError("candidate_evidence_required", code="ERR_CONFIG")
        candidate = self._admission(candidate_source)
        if actual_source is None:
            if not managed or not fresh:
                return BootstrapResult(disposition="checkpoint_required")
            return BootstrapResult(
                disposition="fresh",
                adopted=candidate,
                checkpoint=candidate.to_checkpoint(),
            )

        actual = self._admission(actual_source)
        if persisted_checkpoint is not None:
            if not managed or trusted_prior_source is None:
                return BootstrapResult(disposition="checkpoint_required")
            prior = self._admission(trusted_prior_source)
            if (
                prior.to_checkpoint() == actual.to_checkpoint()
                and actual.to_checkpoint() == persisted_checkpoint
            ):
                return BootstrapResult(
                    disposition="persisted_evidence",
                    adopted=prior,
                    checkpoint=prior.to_checkpoint(),
                )
            return BootstrapResult(disposition="checkpoint_required")
        if trusted_prior_source is not None:
            prior = self._admission(trusted_prior_source)
            return BootstrapResult(
                disposition="trusted_prior",
                adopted=prior,
                checkpoint=prior.to_checkpoint(),
            )
        if accept_baseline:
            return BootstrapResult(
                disposition="baseline_accepted",
                adopted=candidate,
                checkpoint=candidate.to_checkpoint(),
            )
        if managed and actual.to_checkpoint() == candidate.to_checkpoint():
            return BootstrapResult(
                disposition="candidate_equal",
                adopted=candidate,
                checkpoint=candidate.to_checkpoint(),
            )
        return BootstrapResult(disposition="checkpoint_required")
