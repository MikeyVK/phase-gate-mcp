# tests/mcp_server/unit/services/test_template_graph.py
# template=unit_test version=8825c0bb created=2026-09-13T15:49Z updated=
"""Prove graph admission and rendering using independently authored template trees."""

from __future__ import annotations

import os
import subprocess
from dataclasses import FrozenInstanceError

import pytest
from jinja2 import DictLoader, Environment, StrictUndefined

from mcp_server.core.exceptions import MCPError
from mcp_server.services.template_graph import TemplateGraphResolver
from tests.mcp_server.fixtures.suite_roots import SuiteRoots, write_package_tree


class TestTemplateGraph:
    def test_complete_static_graph_retains_inheritance_imports_and_includes(
        self, suite_roots: SuiteRoots, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        files = {
            "opaque/template.jinja2": b'{% extends "shared/templates/bases/leaf.jinja2" %}'
            b'{% import "shared/templates/patterns/macros.jinja2" as m %}'
            b'{% from "shared/templates/patterns/macros.jinja2" import word %}'
            b"{% block body %}{{ m.word(value) }}|{{ word(value) }}"
            b'{% include "shared/templates/patterns/tail.jinja2" %}{% endblock %}',
            "shared/templates/bases/leaf.jinja2": (
                b'{% extends "shared/templates/bases/root.jinja2" %}'
            ),
            "shared/templates/bases/root.jinja2": b"BEGIN[{% block body %}{% endblock %}]END",
            "shared/templates/patterns/macros.jinja2": (
                b"{% macro word(x) %}<{{ x }}>{% endmacro %}"
            ),
            "shared/templates/patterns/tail.jinja2": b"!",
            "shared/templates/unused.jinja2": b"Unused",
            "another/template.jinja2": b"Independent",
        }
        write_package_tree(suite_roots.templates, files)
        parser = Environment(undefined=StrictUndefined)
        resolver = TemplateGraphResolver(suite_roots.templates, parser.parse)
        monkeypatch.chdir(suite_roots.temp)
        graph = resolver.resolve(
            [
                ("unrelated.public-id", "opaque/template.jinja2"),
                ("other.id", "another/template.jinja2"),
            ]
        )
        assert {edge.kind for edge in graph.edges} == {
            "extends",
            "include",
            "import",
            "from_import",
        }
        assert {source.name for source in graph.sources} == set(files) - {
            "shared/templates/unused.jinja2"
        }
        assert {root.template_id for root in graph.roots} == {"unrelated.public-id", "other.id"}
        root = next(item for item in graph.roots if item.template_id == "unrelated.public-id")
        assert root.template_name == "opaque/template.jinja2"
        assert set(root.closure) == set(files) - {
            "shared/templates/unused.jinja2",
            "another/template.jinja2",
        }
        source_map = {source.name: source.content.decode("utf-8-sig") for source in graph.sources}
        snapshot_renderer = Environment(loader=DictLoader(source_map), undefined=StrictUndefined)
        assert (
            snapshot_renderer.get_template(root.template_name).render(value="ok")
            == "BEGIN[<ok>|<ok>!]END"
        )
        write_package_tree(suite_roots.templates, {"opaque/template.jinja2": b"Changed"})
        assert (
            snapshot_renderer.get_template(root.template_name).render(value="ok")
            == "BEGIN[<ok>|<ok>!]END"
        )
        with pytest.raises(FrozenInstanceError):
            graph.roots = ()

    @pytest.mark.parametrize(
        ("source", "code"),
        [
            ("{% include variable %}", "template_dependency_dynamic"),
            ("{% extends parent %}", "template_dependency_dynamic"),
            ("{% import module as m %}", "template_dependency_dynamic"),
            ("{% from module import word %}", "template_dependency_dynamic"),
            ('{% include ["one.jinja2", "two.jinja2"] %}', "template_dependency_ambiguous"),
            (
                '{% include "shared/templates/missing.jinja2" ignore missing %}',
                "template_dependency_optional",
            ),
            (
                '{% extends "shared/templates/one.jinja2" %}'
                '{% extends "shared/templates/two.jinja2" %}',
                "template_renderer_ambiguous",
            ),
            ('{% include "shared/templates/missing.jinja2" %}', "template_source_unavailable"),
            ('{% include "../escape.jinja2" %}', "template_path_invalid"),
            ('{% include "/absolute.jinja2" %}', "template_path_invalid"),
            ('{% include "other/template.jinja2" %}', "template_dependency_direction"),
            ("{% if %}", "template_syntax_invalid"),
        ],
    )
    def test_invalid_graphs_fail_with_logical_diagnostics(
        self, suite_roots: SuiteRoots, source: str, code: str
    ) -> None:
        write_package_tree(
            suite_roots.templates,
            {
                "pkg/template.jinja2": source.encode(),
                "other/template.jinja2": b"Other",
            },
        )
        resolver = TemplateGraphResolver(suite_roots.templates, Environment().parse)
        with pytest.raises(MCPError) as caught:
            resolver.resolve([("arbitrary-id", "pkg/template.jinja2")])
        assert caught.value.message == code
        assert str(suite_roots.templates) not in str(caught.value.params)
        assert "template" in caught.value.params

    def test_shared_to_package_and_cycles_are_rejected(self, suite_roots: SuiteRoots) -> None:
        files = {
            "pkg/template.jinja2": b'{% include "shared/templates/part.jinja2" %}',
            "shared/templates/part.jinja2": b'{% include "pkg/template.jinja2" %}',
        }
        write_package_tree(suite_roots.templates, files)
        resolver = TemplateGraphResolver(suite_roots.templates, Environment().parse)
        with pytest.raises(MCPError, match="template_dependency_direction"):
            resolver.resolve([("any-id", "pkg/template.jinja2")])
        write_package_tree(
            suite_roots.templates,
            {
                "shared/templates/part.jinja2": b'{% include "shared/templates/loop.jinja2" %}',
                "shared/templates/loop.jinja2": b'{% include "shared/templates/part.jinja2" %}',
            },
        )
        with pytest.raises(MCPError, match="template_dependency_cycle"):
            resolver.resolve([("any-id", "pkg/template.jinja2")])

    @pytest.mark.parametrize(
        "roots",
        [
            [("same", "pkg/template.jinja2"), ("same", "other/template.jinja2")],
            [("one", "pkg/template.jinja2"), ("two", "pkg/template.jinja2")],
            [("shared-choice", "shared/templates/base.jinja2")],
            [("wrong-entry", "pkg/other.jinja2")],
        ],
    )
    def test_duplicate_and_invalid_entrypoints_fail(
        self, suite_roots: SuiteRoots, roots: list[tuple[str, str]]
    ) -> None:
        write_package_tree(
            suite_roots.templates,
            {
                "pkg/template.jinja2": b"One",
                "other/template.jinja2": b"Two",
                "shared/templates/base.jinja2": b"Shared",
                "pkg/other.jinja2": b"Private",
            },
        )
        with pytest.raises(MCPError):
            TemplateGraphResolver(suite_roots.templates, Environment().parse).resolve(roots)

    def test_escaping_directory_alias_is_rejected(self, suite_roots: SuiteRoots) -> None:
        write_package_tree(
            suite_roots.templates,
            {
                "pkg/template.jinja2": b'{% include "pkg/linked/hidden.jinja2" %}',
            },
        )
        write_package_tree(suite_roots.temp, {"hidden.jinja2": b"Must not be read"})
        link = suite_roots.templates / "pkg/linked"
        if os.name == "nt":
            subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(link), str(suite_roots.temp)],
                check=True,
                capture_output=True,
            )
        else:
            link.symlink_to(suite_roots.temp, target_is_directory=True)
        with pytest.raises(MCPError, match="template_path_escape"):
            TemplateGraphResolver(suite_roots.templates, Environment().parse).resolve(
                [("any-id", "pkg/template.jinja2")]
            )

    def test_comments_and_raw_blocks_do_not_declare_dependencies(
        self, suite_roots: SuiteRoots
    ) -> None:
        source = b'{# {% include "missing1" %} #}{% raw %}{% include "missing2" %}{% endraw %}'
        write_package_tree(suite_roots.templates, {"pkg/template.jinja2": source})
        graph = TemplateGraphResolver(suite_roots.templates, Environment().parse).resolve(
            [("custom", "pkg/template.jinja2")]
        )
        assert graph.edges == ()
        assert graph.sources[0].content == source
