"""Build one offline wheel and inspect it from a separate installed prefix."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from scripts.build_package import copy_assets, read_manifest


@dataclass(frozen=True)
class InstalledDistribution:
    wheel: Path
    root: Path
    workspace: Path
    python_executable: Path | None = None

    def python(
        self,
        code: str,
        *,
        arguments: tuple[str, ...] = (),
        input_text: str | None = None,
        cwd: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """Run with installed PGMCP ahead of provisioned third-party dependencies."""
        return subprocess.run(
            [
                str(self.python_executable)
                if self.python_executable is not None
                else sys.executable,
                "-I",
                "-c",
                "import sys; sys.path.insert(0, sys.argv.pop(1))\n" + code,
                str(self.root),
                *arguments,
            ],
            cwd=self.workspace if cwd is None else cwd,
            input=input_text,
            text=True,
            capture_output=True,
            timeout=90,
            env={**os.environ, "PYTHONNOUSERSITE": "1", "JITI_FS_CACHE": "0"},
            check=False,
        )


def build_installed_distribution(
    source: Path, temporary_root: Path, *, python_executable: Path | None = None
) -> InstalledDistribution:
    """Stage current sources, build without fetching, and install only that wheel."""
    if python_executable is not None:
        assert python_executable.is_absolute() and python_executable.is_file()
    runtime = str(python_executable) if python_executable is not None else sys.executable
    assert not temporary_root.resolve().is_relative_to(source.resolve())
    stage = temporary_root / "build"
    stage.mkdir(parents=True)
    shutil.copy2(source / "pyproject.toml", stage / "pyproject.toml")
    shutil.copytree(
        source / "mcp_server",
        stage / "mcp_server",
        ignore=shutil.ignore_patterns("assets", "__pycache__", "*.pyc"),
    )
    manifest = read_manifest(source / ".pgmcp/config/release_manifest.yaml")
    copy_assets(source, stage / "mcp_server/assets", manifest)
    wheels = temporary_root / "wheels"
    built = subprocess.run(
        [runtime, "-m", "build", "--wheel", "--no-isolation", "--outdir", str(wheels)],
        cwd=stage,
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
    assert built.returncode == 0, built.stdout + built.stderr
    artifacts = tuple(wheels.glob("*.whl"))
    assert len(artifacts) == 1
    installed = temporary_root / "installed"
    result = subprocess.run(
        [
            runtime,
            "-m",
            "pip",
            "install",
            "--no-index",
            "--no-deps",
            "--no-compile",
            "--target",
            str(installed),
            str(artifacts[0]),
        ],
        cwd=temporary_root,
        text=True,
        capture_output=True,
        timeout=90,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    workspace = temporary_root / "workspace"
    workspace.mkdir()
    return InstalledDistribution(artifacts[0], installed, workspace, python_executable)


CATALOG_PROBE = r"""
import json
import sys
from functools import partial
from pathlib import Path

import mcp_server
from jinja2 import Environment
from mcp_server.config.loader import ConfigLoader
from mcp_server.config.validator import ConfigValidator
from mcp_server.core.interfaces.template_catalog import freeze_json
from mcp_server.execution.catalog import AdapterCatalogLoader, FileAdapterPackageReader
from mcp_server.services.artifact_header_reader import ArtifactHeaderReader
from mcp_server.schemas.template_identity import ArtifactIdentity
from mcp_server.services.template_catalog import TemplateCatalogLoader, TemplateInputValidator
from mcp_server.services.template_contract_loader import TemplateContractLoader
from mcp_server.services.template_graph import TemplateGraphResolver

package = Path(mcp_server.__file__).resolve().parent
suite = package / "assets/template_suite"
config_root = package / "assets/config"
contracts = TemplateContractLoader(suite)
loader = ConfigLoader(config_root, suite, context_schema_reader=contracts.load_context_schema)
validator = ConfigValidator()
checks = loader.load_checks_config()
parser = Environment()
graph = TemplateGraphResolver(suite, parser.parse)
inputs = TemplateInputValidator(parser.parse, freeze_json(ArtifactIdentity.model_json_schema()))
catalog = TemplateCatalogLoader(
    suite,
    read_manifest=loader.load_template_manifest,
    read_version=loader.load_template_version,
    read_policy=loader.load_template_policy,
    read_schema=loader.load_template_context_schema,
    validate_policy=partial(
        validator.validate_template_policy,
        profiles=frozenset(name for name, _ in checks.profiles),
    ),
    resolve_graph=graph.resolve,
    validate_inputs=inputs.validate,
).load()
trust = loader.load_adapter_trust()
assert trust.trusted_adapter_ids == ()
adapters = AdapterCatalogLoader(
    package / "bundled_adapters", Path.cwd() / "workspace_adapters", trust,
    read_manifest=loader.load_adapter_manifest, files=FileAdapterPackageReader(),
    resolve_program=lambda _name: None, windows=sys.platform == "win32",
).load()
validator.validate_checks_config(
    checks, adapters,
    template_profiles=frozenset(item.policy.output_profile for item in catalog.packages),
)
validator.validate_tests_config(loader.load_tests_config(), adapters)
validator.validate_fixes_config(loader.load_fixes_config(), adapters)
bindings = adapters.checks + adapters.tests + adapters.fixes
assert all(item.launch.executable is None for item in bindings)
header = ArtifactHeaderReader().read(sys.argv[1])
origins = {
    name: str(Path(module.__file__).resolve())
    for name, module in sys.modules.items()
    if name.startswith("mcp_server") and getattr(module, "__file__", None)
}
assert all(Path(path).is_relative_to(package) for path in origins.values())
print(json.dumps({
    "package": str(package), "origins": origins,
    "templates": [item.manifest.template_id for item in catalog.packages],
    "adapters": sorted({item.identity.adapter_id for item in bindings}),
    "header": header.model_dump(mode="json"),
}))
"""


ENTRYPOINT_PROBE = r"""
import atexit
import json
import runpy
import sys
from pathlib import Path

prefix = Path(sys.path[0]).resolve()
entrypoint = prefix / sys.argv[1]
origin_report = Path(sys.argv[2])

def record_origins():
    origins = {
        name: str(Path(module.__file__).resolve())
        for name, module in sys.modules.items()
        if name.startswith("mcp_server") and getattr(module, "__file__", None)
    }
    assert all(Path(path).is_relative_to(prefix) for path in origins.values())
    origin_report.write_text(json.dumps(origins), encoding="utf-8")

atexit.register(record_origins)
runpy.run_path(str(entrypoint), run_name="__main__")
"""
