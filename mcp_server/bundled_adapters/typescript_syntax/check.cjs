"use strict";

// check/v1 adapter for one proposed TypeScript source; no emit or semantic checks.
const fs = require("node:fs");
const path = require("node:path");
const { createRequire } = require("node:module");
const { TextDecoder } = require("node:util");

const REQUEST_KEYS = ["operation", "target_path", "content", "args"];
const ABSOLUTE_PATH = /^(?:\/|[A-Za-z]:[\\/]|\\\\[^\\/]+[\\/][^\\/]+)[\s\S]*$/;
const UNC_ROOT = /^\\\\[^\\/]+[\\/][^\\/]+$/;
// Native project-root selection does not determine a proposed snapshot's validity.
const PROJECT_SELECTION_DIAGNOSTICS = new Set([18002, 18003]);

function invalid(location, code) {
  return { reason: "invalid_request", details: [{ location, code }] };
}

function validate(request) {
  if (request === null || typeof request !== "object" || Array.isArray(request)) {
    return invalid([], "wrong_type");
  }
  for (const key of Object.keys(request).sort()) {
    if (!REQUEST_KEYS.includes(key)) return invalid([key], "unknown_field");
  }
  for (const key of REQUEST_KEYS) {
    if (!Object.hasOwn(request, key)) return invalid([key], "missing_field");
  }
  if (typeof request.operation !== "string") return invalid(["operation"], "wrong_type");
  if (request.operation !== "syntax") return invalid(["operation"], "invalid_value");
  const target = request.target_path;
  if (typeof target !== "string") return invalid(["target_path"], "wrong_type");
  const lastComponent = target.split(/[\\/]/).filter(Boolean).at(-1);
  if (!target || target.includes("\0") || !ABSOLUTE_PATH.test(target) ||
      UNC_ROOT.test(target) || /[\\/]$/.test(target) ||
      lastComponent === "." || lastComponent === "..") {
    return invalid(["target_path"], "invalid_value");
  }
  if (typeof request.content !== "string") return invalid(["content"], "wrong_type");
  if (!Array.isArray(request.args)) return invalid(["args"], "wrong_type");
  for (const [index, arg] of request.args.entries()) {
    if (typeof arg !== "string") return invalid(["args", index], "wrong_type");
  }
  return null;
}

function response(decision, version, evidence = null) {
  const value = { decision, external_tools: [{ tool_id: "typescript", version }] };
  if (evidence !== null) value.evidence = evidence;
  return value;
}

function unavailable(reason, message, version = null, evidence = null) {
  return [response({ status: "unavailable", reason, message }, version, evidence), 3];
}

function formatDiagnostics(ts, diagnostics) {
  return { format: "text", data: ts.formatDiagnostics(diagnostics, {
    getCanonicalFileName: (name) => name,
    getCurrentDirectory: () => process.cwd(),
    getNewLine: () => ts.sys.newLine,
  }) };
}

function configuration(ts, target) {
  const configFile = ts.findConfigFile(path.dirname(target), ts.sys.fileExists);
  if (configFile === undefined) return { options: {}, errors: [] };
  const unrecoverable = [];
  const parsed = ts.getParsedCommandLineOfConfigFile(configFile, {}, {
    useCaseSensitiveFileNames: ts.sys.useCaseSensitiveFileNames,
    getCurrentDirectory: () => process.cwd(),
    fileExists: ts.sys.fileExists,
    readFile: ts.sys.readFile,
    readDirectory: ts.sys.readDirectory,
    onUnRecoverableConfigFileDiagnostic: (diagnostic) => unrecoverable.push(diagnostic),
  });
  const nativeErrors = parsed ? ts.getConfigFileParsingDiagnostics(parsed) : [];
  const errors = [...unrecoverable, ...nativeErrors].filter(
    (diagnostic) => !PROJECT_SELECTION_DIAGNOSTICS.has(diagnostic.code),
  );
  return { options: parsed?.options || {}, errors };
}

function syntacticDiagnostics(ts, target, content, options) {
  const canonical = (name) => {
    const absolute = path.resolve(name);
    return ts.sys.useCaseSensitiveFileNames ? absolute : absolute.toLowerCase();
  };
  const targetName = canonical(target);
  const isTarget = (name) => canonical(name) === targetName;
  const snapshot = ts.ScriptSnapshot.fromString(content);
  const host = {
    getCompilationSettings: () => options,
    getScriptFileNames: () => [target],
    getScriptVersion: () => "0",
    getScriptSnapshot: (name) => isTarget(name) ? snapshot : undefined,
    getCurrentDirectory: () => process.cwd(),
    getDefaultLibFileName: () => ts.getDefaultLibFilePath(options),
    useCaseSensitiveFileNames: () => ts.sys.useCaseSensitiveFileNames,
    fileExists: isTarget,
    readFile: (name) => isTarget(name) ? content : undefined,
    readDirectory: () => [],
  };
  // TypeScript's Syntactic service mode does not support getSyntacticDiagnostics.
  const service = ts.createLanguageService(host);
  try {
    return service.getSyntacticDiagnostics(target);
  } finally {
    service.dispose();
  }
}

function run(request) {
  const issue = validate(request);
  if (issue !== null) return [issue, 2];
  let ts;
  try {
    const workspaceRequire = createRequire(path.join(process.cwd(), "package.json"));
    ts = workspaceRequire("typescript");
  } catch (error) {
    return unavailable("dependency_unavailable",
      "TypeScript is unavailable from the workspace: " + error.message);
  }
  const version = ts.version;
  if (request.args.length) {
    return unavailable("unsupported_input",
      "TypeScript syntax checking does not support native options.", version);
  }
  try {
    const config = configuration(ts, request.target_path);
    if (config.errors.length) {
      return unavailable("invalid_configuration",
        ts.flattenDiagnosticMessageText(config.errors[0].messageText, "\n"),
        version, formatDiagnostics(ts, config.errors));
    }
    const diagnostics = syntacticDiagnostics(
      ts, request.target_path, request.content, config.options,
    );
    if (diagnostics.length) {
      return [response({
        status: "failed",
        message: ts.flattenDiagnosticMessageText(diagnostics[0].messageText, "\n"),
      }, version, formatDiagnostics(ts, diagnostics)), 1];
    }
    return [response({ status: "passed" }, version), 0];
  } catch (error) {
    return unavailable("execution_error", "TypeScript syntax check failed: " + error.message, version);
  }
}

let request;
let output;
try {
  request = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(fs.readFileSync(0)));
} catch {
  output = [invalid([], "invalid_value"), 2];
}
if (output === undefined) output = run(request);
process.stdout.write(JSON.stringify(output[0]) + "\n");
process.exitCode = output[1];
