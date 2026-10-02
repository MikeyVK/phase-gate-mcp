"use strict";

// Self-contained check/v1 entrypoint; dependencies resolve from the workspace.
const fs = require("node:fs");
const path = require("node:path");
const { spawnSync } = require("node:child_process");
const { createRequire } = require("node:module");
const { TextDecoder } = require("node:util");

const REQUEST_KEYS = ["operation", "targets", "args", "execution_context"];
const ABSOLUTE_PATH = /^(?:\/|[A-Za-z]:[\\/]|\\\\[^\\/]+[\\/][^\\/]+)[\s\S]*$/;

function invalid(location, code) {
  return { reason: "invalid_request", details: [{ location, code }] };
}

function validateExecutionContext(context) {
  if (context === null || typeof context !== "object" || Array.isArray(context)) {
    return invalid(["execution_context"], "wrong_type");
  }
  for (const key of Object.keys(context).sort()) {
    if (key !== "scratch_directory") return invalid(["execution_context", key], "unknown_field");
  }
  if (!Object.hasOwn(context, "scratch_directory")) {
    return invalid(["execution_context", "scratch_directory"], "missing_field");
  }
  const directory = context.scratch_directory;
  if (typeof directory !== "string") {
    return invalid(["execution_context", "scratch_directory"], "wrong_type");
  }
  if (!directory || directory.includes("\0") || !ABSOLUTE_PATH.test(directory)) {
    return invalid(["execution_context", "scratch_directory"], "invalid_value");
  }
  return null;
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
  const contextIssue = validateExecutionContext(request.execution_context);
  if (contextIssue !== null) return contextIssue;
  if (typeof request.operation !== "string") return invalid(["operation"], "wrong_type");
  if (request.operation !== "types") return invalid(["operation"], "invalid_value");
  if (!Array.isArray(request.targets)) return invalid(["targets"], "wrong_type");
  for (const [index, target] of request.targets.entries()) {
    if (typeof target !== "string") return invalid(["targets", index], "wrong_type");
    if (!target || target.includes("\0") || !ABSOLUTE_PATH.test(target)) {
      return invalid(["targets", index], "invalid_value");
    }
  }
  if (!Array.isArray(request.args)) return invalid(["args"], "wrong_type");
  for (const [index, arg] of request.args.entries()) {
    if (typeof arg !== "string") return invalid(["args", index], "wrong_type");
  }
  return null;
}

function response(decision, version, evidence) {
  const value = {
    decision,
    external_tools: [{ tool_id: "pyright", version }],
    coverage: null,
    required_targets: [],
  };
  if (evidence !== null) value.evidence = evidence;
  return value;
}

function unavailable(reason, message, version = null, evidence = null) {
  return [response({ status: "unavailable", reason, message }, version, evidence), 3];
}

function nativeEvidence(stdout, stderr) {
  const parts = [];
  if (stdout) parts.push("stdout:\n" + stdout);
  if (stderr) parts.push("stderr:\n" + stderr);
  return parts.length ? { format: "text", data: parts.join("\n") } : null;
}

function nativeMessage(stdout, stderr) {
  try {
    const parsed = JSON.parse(stdout);
    if (Array.isArray(parsed.generalDiagnostics)) {
      for (const severity of ["error", "warning"]) {
        const diagnostic = parsed.generalDiagnostics.find(
          (item) => item.severity === severity && typeof item.message === "string" &&
            item.message.trim(),
        );
        if (diagnostic) return diagnostic.message;
      }
    }
    return stderr.split(/\r?\n/).find((line) => line.trim()) ||
      "Pyright reported an unsuccessful check.";
  } catch {
    // Explicit native output modes remain text; no generic finding conversion.
  }
  const lines = (stderr + "\n" + stdout).split(/\r?\n/).filter((line) => line.trim());
  return lines.find((line) => / - (?:error|warning): /.test(line)) ||
    lines[0] || "Pyright reported a failure.";
}

function nativeOptionName(token) {
  const attached = token.match(/^(--\S+?)=(.*)/);
  if (attached) return attached[1];
  const long = token.match(/^--(\S+)/);
  return long ? "--" + long[1] : token;
}

// Project only Pyright 1.1.408's file-channel ownership, leaving native option
// validation and caller tokens to Pyright's bundled command-line-args parser.
function additionalFileInput(args) {
  const scalarOptions = new Set([
    "createstub", "level", "project", "pythonpath", "pythonplatform", "pythonversion",
    "threads", "typeshed-path", "typeshedpath", "venv-path", "venvpath", "verifytypes",
  ]);
  const booleanOptions = new Set([
    "dependencies", "help", "ignoreexternal", "lib", "outputjson", "skipunannotated",
    "stats", "verbose", "version", "warnings", "watch",
  ]);
  const aliases = { p: "project", t: "typeshedpath", v: "venvpath", h: "help", w: "watch" };
  const tokens = args.flatMap((arg) => /^-[^\d-]{2,}$/.test(arg) ?
    arg.slice(1).split("").map((letter) => "-" + letter) : [arg]);
  let pendingScalar = false;
  for (const token of tokens) {
    const attached = token.match(/^(--\S+?)=(.*)/);
    const short = token.match(/^-([^\d-])$/);
    const long = token.match(/^--(\S+)/);
    if (attached || short || long) {
      const name = short ? aliases[short[1]] : nativeOptionName(token).slice(2);
      if (name === "files") return token;
      if (scalarOptions.has(name)) {
        pendingScalar = !attached;
      } else if (booleanOptions.has(name) && !attached) {
        pendingScalar = false;
      } else {
        // Unknown options and boolean equals-values already fail natively.
        return null;
      }
    } else if (pendingScalar) {
      pendingScalar = false;
    } else {
      return token;
    }
  }
  return null;
}

function filenameInputIssue(targets) {
  for (const target of targets) {
    if (/[ \r\n]/.test(target) || target.trim() !== target ||
        Buffer.from(target, "utf8").toString("utf8") !== target) {
      return "Pyright stdin cannot represent this filename literally: " + JSON.stringify(target);
    }
  }
  return null;
}

function run(request) {
  const issue = validate(request);
  if (issue !== null) return [issue, 2];

  let entrypoint;
  let version;
  try {
    const workspaceRequire = createRequire(path.join(process.cwd(), "package.json"));
    entrypoint = workspaceRequire.resolve("pyright");
    const metadata = JSON.parse(
      fs.readFileSync(workspaceRequire.resolve("pyright/package.json"), "utf8"),
    );
    version = typeof metadata.version === "string" && metadata.version.trim() ?
      metadata.version : null;
  } catch (error) {
    return unavailable("dependency_unavailable",
      "Pyright is unavailable from the workspace: " + error.message);
  }

  let expectedVersion;
  try {
    const declaration = JSON.parse(fs.readFileSync(path.join(__dirname, "package.json"), "utf8"));
    expectedVersion = declaration.dependencies?.pyright;
    if (typeof expectedVersion !== "string" || !/^\d+\.\d+\.\d+$/.test(expectedVersion)) {
      throw new Error("The Pyright dependency must declare one exact supported version.");
    }
  } catch (error) {
    return unavailable("dependency_unavailable",
      "Pyright prerequisite declaration is unavailable: " + error.message, version);
  }
  if (version !== expectedVersion) {
    return unavailable("dependency_unavailable",
      "Pyright version mismatch: actual=" + (version ?? "unreadable") +
        ", expected=" + expectedVersion, version);
  }

  const alternateOperations = new Set([
    "--help", "-h", "--version", "--watch", "-w", "--verifytypes", "--createstub",
  ]);
  for (const arg of request.args) {
    if (arg.includes("\0") || arg === "-" || alternateOperations.has(nativeOptionName(arg)) ||
        (/^-[^\d-]{2,}$/.test(arg) && /[hw]/.test(arg.slice(1)))) {
      return unavailable("unsupported_input",
        "Pyright argument conflicts with the check contract: " + JSON.stringify(arg), version);
    }
  }

  const selected = request.targets.length > 0;
  if (selected) {
    const filenameIssue = filenameInputIssue(request.targets);
    if (filenameIssue !== null) return unavailable("unsupported_input", filenameIssue, version);
    const additionalInput = additionalFileInput(request.args);
    if (additionalInput !== null) {
      return unavailable("unsupported_input",
        "Pyright caller input conflicts with the selected filename channel: " +
          JSON.stringify(additionalInput), version);
    }
  }
  const nativeModes = new Set(["--outputjson", "--verbose", "--stats", "--dependencies"]);
  const explicitMode = request.args.some((arg) => nativeModes.has(nativeOptionName(arg)));
  const args = [
    entrypoint, ...(explicitMode ? [] : ["--outputjson"]),
    // Place the owned file marker before options so a dangling scalar cannot consume it.
    ...(selected ? ["-"] : []), ...request.args,
  ];
  let result;
  try {
    // The outer runtime owns the timeout, process tree and protocol output bound.
    result = spawnSync(process.execPath, args, {
      stdio: [selected ? "pipe" : "ignore", "pipe", "pipe"],
      input: selected ? Buffer.from(request.targets.join("\n"), "utf8") : undefined,
      maxBuffer: Infinity,
    });
  } catch (error) {
    return unavailable("execution_error", "Pyright launch failed: " + error.message, version);
  }
  const stdout = result.stdout ? result.stdout.toString("utf8") : "";
  const stderr = result.stderr ? result.stderr.toString("utf8") : "";
  const evidence = nativeEvidence(stdout, stderr);
  if (result.error || result.signal) {
    return unavailable("execution_error",
      "Pyright execution failed: " + (result.error?.message || result.signal), version, evidence);
  }

  if (result.status === 0) return [response({ status: "passed" }, version, evidence), 0];
  if (result.status === 1) {
    if (!stdout.trim() && !stderr.trim()) {
      return unavailable("invalid_result", "Pyright failed without native evidence.", version);
    }
    return [response({
      status: "failed", message: nativeMessage(stdout, stderr),
    }, version, evidence), 1];
  }
  // Pyright 1.1.408's native ExitStatus enum; never infer severity from exit codes.
  const reasons = { 2: "execution_error", 3: "invalid_configuration", 4: "unsupported_input" };
  return unavailable(reasons[result.status] || "execution_error",
    nativeMessage(stdout, stderr), version, evidence);
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
