"""Preserve pure edit semantics and original-text profile selection."""

from __future__ import annotations

import pytest

from mcp_server.config.schemas.checks_config import ChecksConfig
from mcp_server.services.artifact_header_reader import ArtifactHeaderReader
from mcp_server.services.edit_construction import (
    AppendOperation,
    EditConstructionError,
    EditOperation,
    PatternReplaceOperation,
    ReplaceOperation,
    RewriteOperation,
    construct_edit,
    select_profile,
)


@pytest.fixture
def checks() -> ChecksConfig:
    return ChecksConfig.model_validate(
        {
            "configured_targets": {},
            "checks": {
                "syntax": {
                    "adapter_id": "syntax",
                    "capability": "check",
                    "timeout_seconds": 10,
                    "default_args": [],
                }
            },
            "profiles": {
                name: {"checks": ["syntax"]} for name in ("general", "declaration", "notes")
            },
            "profiles_by_extension": {".ts": "general", ".D.TS": "declaration"},
            "run_checks": {},
        }
    )


def test_operations_preserve_exact_matching_newlines_and_unchanged_text() -> None:
    cases: tuple[tuple[str, EditOperation, str], ...] = (
        ("x x", ReplaceOperation(target_content="x", replacement="y"), "y x"),
        (
            "x\r\nx\r\nx",
            ReplaceOperation(target_content="x", replacement="y", search_window=(2, 2)),
            "x\r\ny\r\nx",
        ),
        ("x", ReplaceOperation(target_content="x", replacement="x"), "x"),
        ("x", RewriteOperation(content="x"), "x"),
        ("old", RewriteOperation(content="new\r\n"), "new\r\n"),
        ("", AppendOperation(content="tail"), "tail\n"),
        ("x", AppendOperation(content="tail\n"), "x\ntail\n"),
        ("x\n", AppendOperation(content="tail"), "x\ntail\n"),
        ("x x", AppendOperation(content="a", anchor="x", position="before"), "a\nx x"),
        ("x\r\nx", AppendOperation(content="a\n\n", anchor="x"), "x\na\r\nx"),
        ("a1 a2", PatternReplaceOperation(pattern=r"a\d", replacement="b"), "b b"),
        (
            r"a\b a\b",
            PatternReplaceOperation(pattern=r"a\b", replacement=r"c\d", regex=False),
            r"c\d c\d",
        ),
        ("ab", PatternReplaceOperation(pattern="", replacement="X", regex=False), "XaXbX"),
        ("ab", PatternReplaceOperation(pattern=r"(?=b)", replacement="X"), "aXb"),
        ("body", PatternReplaceOperation(pattern="missing", replacement="x"), "body"),
        ("body", PatternReplaceOperation(pattern="missing", replacement="x", regex=False), "body"),
    )
    for original, operation, expected in cases:
        assert construct_edit(original, operation) == expected, operation


@pytest.mark.parametrize(
    ("operation", "reason"),
    [
        (
            ReplaceOperation(target_content="alpha", replacement="x", search_window=(12, 12)),
            "missing_match",
        ),
        (AppendOperation(content="x", anchor="alphaa"), "missing_anchor"),
        (PatternReplaceOperation(pattern="[", replacement="x"), "invalid_pattern"),
        (
            PatternReplaceOperation(pattern="absent", replacement=r"\g<missing>"),
            "invalid_replacement",
        ),
        (
            PatternReplaceOperation(pattern="alpha", replacement=r"\g<missing>"),
            "invalid_replacement",
        ),
    ],
)
def test_construction_failures_retain_typed_bounded_source_facts(
    operation: EditOperation,
    reason: str,
) -> None:
    original = "\n".join(["alpha", "alphas", "alphabet"] + ["body"] * 9)
    with pytest.raises(EditConstructionError) as caught:
        construct_edit(original, operation)
    details = caught.value.details
    assert details.reason == reason and details.message
    if reason in ("missing_match", "missing_anchor"):
        assert details.suggestions and len(details.suggestions) <= 3
        assert [(line.line_number, line.text) for line in details.context] == list(
            enumerate(original.splitlines()[:10], 1)
        )
    else:
        assert details.suggestions == ()
        assert details.context == ()


def header(template_id: str) -> str:
    return f"// pgmcp:v1 id={template_id} pv=0.1.0 pf={'c' * 16} sf={'d' * 16}\n"


def test_selection_uses_configured_suffix_and_original_metadata(checks: ChecksConfig) -> None:
    profiles = {"source_notes": "notes", "release_notes": "general"}
    cases = (
        (
            header("source_notes"),
            "release_notes",
            "orders.d.ts",
            ("input", "general", "release_notes", None, None),
        ),
        (
            header("source_notes"),
            None,
            "orders.d.ts",
            ("metadata", "notes", "source_notes", None, None),
        ),
        ("body\n", None, "orders.d.ts", ("extension", "declaration", None, ".D.TS", "absent")),
        (
            "// pgmcp: malformed\n",
            None,
            "orders.d.ts",
            ("extension", "declaration", None, ".D.TS", "invalid"),
        ),
        (
            header("retired_notes"),
            None,
            "orders.d.ts",
            ("extension", "declaration", None, ".D.TS", "unknown_template"),
        ),
        (
            "\n" + header("source_notes"),
            None,
            "orders.d.ts",
            ("extension", "declaration", None, ".D.TS", "absent"),
        ),
        ("body\n", None, "README", ("none", None, None, None, "absent")),
    )
    for original, explicit, filename, expected in cases:
        selected = select_profile(
            original,
            filename,
            explicit_template_id=explicit,
            header_reader=ArtifactHeaderReader(),
            template_profiles=profiles,
            extension_profile_for_filename=checks.match_for_filename,
        )
        assert (
            selected.selected_source,
            selected.profile_id,
            selected.template_id,
            selected.extension,
            selected.selection_reason,
        ) == expected

    original = header("source_notes") + "body"
    selected = select_profile(
        original,
        "orders.ts",
        explicit_template_id=None,
        header_reader=ArtifactHeaderReader(),
        template_profiles=profiles,
        extension_profile_for_filename=checks.match_for_filename,
    )
    proposed = construct_edit(original, RewriteOperation(content=header("release_notes")))
    assert proposed == header("release_notes") and selected.profile_id == "notes"
    with pytest.raises(ValueError, match="unknown_template"):
        select_profile(
            original,
            "orders.ts",
            explicit_template_id="retired_notes",
            header_reader=ArtifactHeaderReader(),
            template_profiles=profiles,
            extension_profile_for_filename=checks.match_for_filename,
        )
