"""A synthetic Node adapter package for real process-boundary evidence."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, RootModel

from mcp_server.config.loader import ConfigLoader
from mcp_server.config.schemas.adapter_manifest import AdapterTrustConfig, CheckCapability
from mcp_server.core.interfaces.execution import AdapterBinding
from mcp_server.execution.catalog import (
    AdapterCatalog,
    AdapterCatalogLoader,
    FileAdapterPackageReader,
)
from mcp_server.execution.models import AdapterExitCode, InvocationCompleted
from mcp_server.execution.protocol import (
    AdapterExecutionContext,
    AdapterRequestContract,
    AdapterResponseContract,
)
from tests.mcp_server.fixtures.suite_roots import write_package_tree

NODE_ADAPTER = r"""
const {readFileSync, writeFileSync} = require('node:fs');
const write = (stream, data) => new Promise((resolve, reject) =>
  stream.write(data, error => error ? reject(error) : resolve()));
async function main() {
  if (process.argv.includes('--duplex')) {
    const diagnostics = Buffer.alloc(256 * 1024 + 31, 'x');
    diagnostics.write('HEAD\n');
    diagnostics.write('€', 128 * 1024 - 1);
    diagnostics.write('TAIL✓', diagnostics.length - Buffer.byteLength('TAIL✓'));
    await write(process.stderr, diagnostics);
  }
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  const request = JSON.parse(Buffer.concat(chunks).toString('utf8'));
  const mode = request.args[0];
  const codes = {passed: 0, failed: 1, invalid_request: 2, unavailable: 3};
  const status = mode === 'failed_detail' ? 'failed'
    : Object.hasOwn(codes, mode) ? mode : 'passed';
  if (mode === 'write_selected') {
    writeFileSync(request.targets[0], 'fixture applied repair\n');
  }
  const decisions = {
    passed: {status: 'passed'},
    failed: {status: 'failed', message: 'fixture rejected content'},
    unavailable: {status: 'unavailable', reason: 'dependency_unavailable',
                  message: 'fixture dependency unavailable'}
  };
  const echo = {request, cwd: process.cwd(), argv: process.argv.slice(2),
                dependency: readFileSync(__dirname + '/dependency.txt', 'utf8')};
  const response = status === 'invalid_request'
    ? {reason: 'invalid_request', details: [{location: ['operation'], code: 'invalid_value'}]}
    : {decision: decisions[status], external_tools: [{tool_id: 'node', version: process.version}],
       evidence: {format: 'text', data: JSON.stringify(echo)}};
  if (status !== 'invalid_request' && request.operation === 'echo' && request.targets) {
    response.coverage = null;
    response.required_targets = [];
  }
  if (mode === 'failed_detail') {
    echo.dependency = 'native diagnostic:' + 'x'.repeat(300000) + ':late diagnostic sentinel';
    response.evidence.data = JSON.stringify(echo);
  }
  let text = JSON.stringify(response);
  if (mode === 'malformed' || mode === 'crash') text = '{broken';
  if (mode === 'logs') text = 'not protocol\n' + text;
  if (mode === 'multiple') text += text;
  if (mode === 'unknown_field') text = JSON.stringify({...response, extra: true});
  if (mode === 'empty') text = '';
  if (mode === 'exact' || mode === 'oversize') {
    text += ' '.repeat(8 * 1024 * 1024 - Buffer.byteLength(text));
    if (mode === 'oversize') text += ' ';
  }
  process.exitCode = mode === 'crash' ? 42 : mode === 'mismatch' ? 1 : codes[status];
  await write(process.stdout, text);
  if (mode === 'oversize') setInterval(() => {}, 1000);
}
main().catch(error => {process.stderr.write(String(error)); process.exitCode = 42;});
"""

MANIFEST = """adapter_id: process_fixture
version: 1.2.3
files: [adapter.cjs, dependency.txt]
roles:
  check:
    contract_version: 1
    entrypoint:
      executable: node
      args: [{package_file: adapter.cjs}, "", "a b; literal"]
    capabilities:
      echo: {inputs: [content, selection], requires_file: false, configured_targets: fixture}
  test:
    contract_version: 1
    entrypoint:
      executable: node
      args: [{package_file: adapter.cjs}]
    capabilities:
      suite: {}
  fix:
    contract_version: 1
    entrypoint:
      executable: node
      args: [{package_file: adapter.cjs}]
    capabilities:
      repair:
        addresses: [{adapter_id: process_fixture, capability: echo}]
"""


class FixtureModel(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")


class ProcessRequest(FixtureModel):
    operation: Literal["echo"]
    target_path: str
    content: str
    args: tuple[str, ...]


class ProcessWireRequest(ProcessRequest):
    """Complete adapter input with explicit PGMCP-owned invocation context."""

    execution_context: AdapterExecutionContext


def request_contract() -> AdapterRequestContract[ProcessRequest]:
    """Encode fixture operation intent through the current wire request."""
    return AdapterRequestContract(ProcessWireRequest)


class Passed(FixtureModel):
    status: Literal["passed"]


class Failed(FixtureModel):
    status: Literal["failed"]
    message: str


class Unavailable(FixtureModel):
    status: Literal["unavailable"]
    reason: Literal["dependency_unavailable"]
    message: str


class ExternalTool(FixtureModel):
    tool_id: Literal["node"]
    version: str | None


class NativeText(FixtureModel):
    format: Literal["text"]
    data: str


class ProcessResponse(FixtureModel):
    decision: Passed | Failed | Unavailable
    external_tools: tuple[ExternalTool, ...]
    evidence: NativeText


class RequestIssue(FixtureModel):
    location: tuple[str, ...]
    code: Literal["invalid_value"]


class InvalidRequest(FixtureModel):
    reason: Literal["invalid_request"]
    details: tuple[RequestIssue, ...]


class FixtureResponse(RootModel[ProcessResponse | InvalidRequest]):
    model_config = ConfigDict(frozen=True, strict=True)


class EchoEvidence(FixtureModel):
    request: ProcessWireRequest
    cwd: str
    argv: tuple[str, ...]
    dependency: str


def expected_exit(response: FixtureResponse) -> AdapterExitCode:
    if isinstance(response.root, InvalidRequest):
        return AdapterExitCode.INVALID_REQUEST
    return {
        "passed": AdapterExitCode.SUCCESS,
        "failed": AdapterExitCode.NEGATIVE_RESULT,
        "unavailable": AdapterExitCode.UNAVAILABLE,
    }[response.root.decision.status]


def response_contract() -> AdapterResponseContract[FixtureResponse]:
    return AdapterResponseContract(
        response_type=FixtureResponse,
        completed_type=InvocationCompleted[FixtureResponse],
        expected_exit=expected_exit,
    )


@dataclass(frozen=True)
class ProcessFixture:
    """Explicit admitted package and workspace selected by test composition."""

    binding: AdapterBinding[CheckCapability]
    package: Path
    workspace: Path
    catalog: AdapterCatalog


def create_process_fixture(root: Path, node: Path) -> ProcessFixture:
    package = write_package_tree(
        root / "official" / "package with spaces",
        {
            "manifest.yaml": MANIFEST.encode(),
            "adapter.cjs": NODE_ADAPTER.encode(),
            "dependency.txt": b"declared package contribution\n",
        },
    )
    workspace = root / "logical workspace"
    workspace.mkdir()
    config = ConfigLoader(root / "config", root / "templates")
    catalog = AdapterCatalogLoader(
        root / "official",
        root / "workspace-adapters",
        AdapterTrustConfig(trusted_adapter_ids=()),
        read_manifest=config.load_adapter_manifest,
        files=FileAdapterPackageReader(),
        resolve_program=lambda name: node if name == "node" else None,
        windows=os.name == "nt",
    ).load()
    return ProcessFixture(catalog.get_check("process_fixture", "echo"), package, workspace, catalog)
