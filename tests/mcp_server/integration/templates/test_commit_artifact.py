"""Exercise delivered commit framing and native validation without publishing messages."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema.exceptions import ValidationError as ContextError
from pydantic import JsonValue

from mcp_server.core.interfaces.artifact_header_reader import HeaderReadStatus
from mcp_server.services.artifact_header_reader import ArtifactHeaderReader
from tests.mcp_server.fixtures.delivered_templates import DeliveredTemplate, load_delivered_template
from tests.mcp_server.integration.adapters.test_commitlint import (
    CommitlintPackage,
    commitlint_modules,
    commitlint_package,
    commitlint_runtime,
    evidence,
    invoke,
)

__all__ = ["commitlint_modules", "commitlint_package", "commitlint_runtime"]


@pytest.fixture
def commit_template(tmp_path: Path, pytestconfig: pytest.Config) -> DeliveredTemplate:
    suite = pytestconfig.rootpath / ".pgmcp/template_suite"
    delivered = load_delivered_template(
        source_suite=suite,
        source_package=suite / "commit",
        config_root=pytestconfig.rootpath / ".pgmcp/config",
        destination=tmp_path / "explicit suite",
        template_id="commit",
    )
    selected = delivered.catalog.get("commit")
    assert selected.policy.persistence == "workspace"
    assert dict(delivered.checks.profiles)[selected.policy.output_profile].checks == (
        "commit_message",
    )
    return delivered


def test_minimal_and_marker_only_commits_keep_explicit_intent(
    commit_template: DeliveredTemplate,
    commitlint_package: CommitlintPackage,
) -> None:
    base: dict[str, JsonValue] = {"type": "CuStOm_7", "subject": "Keep Caller Case"}
    ordinary = commit_template.renderer.render("commit", base, commit_template.provenance)
    assert ordinary.splitlines()[1] == f"{base['type']}: {base['subject']}"
    unchanged = commit_template.renderer.render(
        "commit", {**base, "breaking_change": False}, commit_template.provenance
    )
    assert unchanged == ordinary
    marker = commit_template.renderer.render(
        "commit", {**base, "breaking_change": True}, commit_template.provenance
    )
    assert marker.splitlines()[1] == f"{base['type']}!: {base['subject']}"
    code, response = invoke(commitlint_package, marker, ("--color=false", "--verbose"))
    assert code == 0 and response["decision"] == {"status": "passed"}


def test_commit_preserves_caller_fields_and_checks_full_saved_artifact(
    commit_template: DeliveredTemplate,
    commitlint_package: CommitlintPackage,
) -> None:
    context: dict[str, JsonValue] = {
        "type": "CuStOm",
        "scope": "Public-API",
        "subject": "Keep Case: (and punctuation)!",
        "breaking_change": True,
        "breaking_description": "Caller migration requirement.",
        "body": "First body paragraph.\nSecond line.\n\nAnother paragraph.",
        "refs": [460.0, 7],
        "footer": "Caller-footer: First line\nSecond footer line.",
    }
    before = deepcopy(context)
    output = commit_template.renderer.render("commit", context, commit_template.provenance)
    assert context == before
    header = ArtifactHeaderReader().read(output)
    assert header.status is HeaderReadStatus.RECOGNIZED
    assert header.provenance is not None and header.provenance.id == "commit"
    assert output.splitlines()[1] == (
        f"{context['type']}({context['scope']})!: {context['subject']}"
    )
    for key in ("body", "breaking_description", "footer"):
        value = context[key]
        assert isinstance(value, str) and value in output
    assert "BREAKING CHANGE: " + str(context["breaking_description"]) in output
    assert "Refs: #460, #7" in output and "#460.0" not in output
    assert output.index("First body") < output.index("BREAKING CHANGE:") < output.index("Refs:")
    assert output.index("Refs:") < output.index("Caller-footer:")
    code, response = invoke(commitlint_package, output, ("--color=false", "--verbose"))
    assert code == 0 and response["decision"] == {"status": "passed"}
    assert output.partition("\n")[2] in evidence(response)
    assert response["external_tools"] == [{"tool_id": "commitlint", "version": "21.2.2"}]
    assert not (commitlint_package.runtime.workspace / "commit.txt").exists()
    malformed = output.replace("pgmcp:v1", "pgmcp:v2", 1)
    assert ArtifactHeaderReader().read(malformed).provenance is None
    code, response = invoke(commitlint_package, malformed, ("--color=false", "--verbose"))
    assert code == 1 and response["decision"] == {"status": "failed"}


def test_explicit_empty_commit_options_preserve_plain_text_structure(
    commit_template: DeliveredTemplate,
) -> None:
    base: dict[str, JsonValue] = {"type": "Tune", "subject": "Subject"}
    absent = commit_template.renderer.render("commit", base, commit_template.provenance)
    explicit = {**base, "body": "", "footer": "", "refs": []}
    output = commit_template.renderer.render("commit", explicit, commit_template.provenance)
    assert output.splitlines()[1] == absent.splitlines()[1]
    assert output.count("\n") > absent.count("\n")
    assert "Refs:" in output and "#460" not in output


def test_commit_rejects_framing_breaks_and_invalid_breaking_or_reference_shapes(
    commit_template: DeliveredTemplate,
) -> None:
    base: dict[str, JsonValue] = {"type": "Tune", "subject": "Subject"}
    invalid: list[dict[str, JsonValue]] = [
        {"subject": "Missing type"},
        {**base, "type": ""},
        {**base, "type": "bad:type"},
        {**base, "type": "feat\n"},
        {**base, "subject": "Two\nlines"},
        {**base, "subject": ""},
        {**base, "scope": ""},
        {**base, "scope": "Nested(scope)"},
        {**base, "scope": "Two\rlines"},
        {**base, "refs": ["#460"]},
        {**base, "refs": [0]},
        {**base, "refs": [1.5]},
        {**base, "breaking_description": "Requires explicit true"},
        {**base, "breaking_change": False, "breaking_description": "Contradiction"},
        {**base, "breaking_change": True, "breaking_description": ""},
        {**base, "body": None},
        {**base, "message": "Legacy subject"},
    ]
    for context in invalid:
        with pytest.raises(ContextError):
            commit_template.renderer.render("commit", context, commit_template.provenance)
