# Type Checking Playbook

## Purpose

This document standardizes how we resolve typing issues so that **all agents** (and humans) apply the **same** fixes in the **same order**.

**Goals:**
- Keep CI/PR gates strict and consistent.
- Avoid “random” workarounds (casts vs disables vs global config changes).
- Prefer durable type fixes over silencing.

---

## Non‑Negotiables

1. **No global disables** to “make the checker shut up”.
   - Do not relax `mypy` strictness globally.
   - Do not mass-disable Pyright diagnostics in `pyrightconfig.json` unless explicitly approved as a project policy.

2. **No blind casting of untrusted data.**
   - Never `cast(...)` external input (events, JSON, dict payloads) without a runtime check or validation first.

3. **If you must ignore, ignore precisely.**
   - Prefer error-code specific ignores.
   - Add a short rationale and a concrete reassessment trigger.

---

## Resolution Order (Mandatory)

When a typing issue appears, follow this sequence:

### 1) Fix the types at the source
- Add missing annotations (parameters and return types).
- Tighten `Any` where possible; raw unknown values start as `object`.
- Annotate stored `Literal` attributes and diagnosed collection/default factories at their owner.
- A container guard proves only its actual check: `dict[object, object]` does not certify string keys or JSON values.
- Prefer concrete types (e.g., `Mapping[str, str]`, `Sequence[int]`) over `Any`.

### 2) Narrow types using runtime checks
Use narrowing before using `cast` or ignores.

**Patterns:**
- `assert x is not None`
- `if x is None: ...`
- `isinstance(x, SomeType)`
- `match` on tagged unions / Literals

Example:
```python
value = dto.optional_field
assert value is not None  # narrows Optional[T] -> T
use(value)
```

### 3) Improve the model/type design
Prefer structural fixes that reduce future friction.

**Common tools:**
- `TypedDict` for dict-shaped payloads
- `Protocol` for dependency injection / interfaces
- `Literal` for constrained strings
- `NewType` for typed IDs
- `@overload` for factories/helpers

### 4) Contain dynamic edges (boundaries)
At system boundaries, convert “dynamic” input to typed objects once.

**Preferred boundary patterns:**
- Parse/validate into a Pydantic model (DTO) at the boundary.
- Convert to a typed dataclass/model and pass that through the core.
- Core and prepared tool inputs are model-only. `args_model` returns a `BaseModel` subclass; no-argument tools use an explicit empty model with unknown-key rejection, rather than a `None` admission route.
- Use supported callable/protocol parameters for partially typed native operations. Keep runtime guards, native error distinctions, opaque mapping keys and intentional variance; do not coerce or add admission policy just to silence `Unknown`.

### 5) Targeted ignore (last resort)
Only after 1–4 are not feasible.

**Mypy:**
```python
something()  # type: ignore[call-arg]  # rationale: third-party stub mismatch
```

**Pyright/Pylance:**
```python
x = something()  # pyright: ignore[reportGeneralTypeIssues]  # rationale: known false positive
```

Rules:
- Ignore **one line** or the smallest possible block.
- Always include a short rationale.
- Never use bare `# type: ignore` unless there is no error code available.

### 6) Casting (very last)
Use `cast(...)` only when:
- you have an invariant the type checker cannot prove, and
- you can defend it with a runtime check, validation, or documented guarantee.

Example:
```python
from typing import cast

assert isinstance(x, str)
value = cast(str, x)
```

---

## Standard Workarounds (Approved)

### A) Pydantic declarations

Check the actual field annotation, generic bindings, supported stubs and native checker plugin before choosing a workaround. Keep ordinary typed field access. Reflective `getattr` or `str(...)` solely to silence a diagnosis can hide an invalid value or change its meaning; neither proves the declared type. A verified library limitation may need a precise exception with runtime/schema evidence and a reassessment trigger.

### B) Optional fields
Prefer narrowing:
```python
value = dto.optional_field
assert value is not None
assert value.startswith("ABC")
```

### C) Generics and library limitations

Preserve deliberate covariance or invariance. Generic syntax conversion is appropriate only when the complete declaration retains its variance, construction, validation and schema behavior. Do not infer equivalence from a toy generic example. Use a precise source-local exception for a demonstrated checker/library limitation, and reassess it when the supported implementation can satisfy the same complete contract. Annotate only diagnosed factories; fresh default values remain a runtime invariant.

### D) Third-party missing/incorrect stubs
Prefer:
- installing typed stub packages (e.g., `types-PyYAML`) if available, or
- adding small local stubs in the repo when needed.

Only if unavoidable, use targeted ignore(s) with rationale.

### E) `reportPrivateUsage` in tests — never suppress without justification

`reportPrivateUsage` in test code is **almost always a test design smell**, not a false positive.

**Decision tree:**

1. Can the behaviour be observed via the public interface?
   - Yes → **Rewrite the test.** Do not suppress.
   - No → Is the private access a true test-infrastructure necessity? (e.g., injecting a test double into an attribute with no public setter or factory)
     - Yes → Add `# pyright: ignore[reportPrivateUsage]` **with a rationale comment**.
     - No → Inspect actual callers and registrations. Remove dead code only with source evidence; lack of a public setter does not prove that a private method is unreachable.

**Forbidden:**
```python
# ❌ suppression without rationale — not acceptable
runner._handle_merge_readiness(action, ctx, tmp_path)  # pyright: ignore[reportPrivateUsage]

# ❌ attribute inspection instead of observing behaviour
assert runner._merge_readiness_context is ctx  # pyright: ignore[reportPrivateUsage]
```

**Accepted (only with rationale):**
```python
# ✅ test-double injection, no public setter exists — documented
tool._settings = mock_settings  # pyright: ignore[reportPrivateUsage]  # inject test double: no public setter

# ✅ OR avoid the suppression entirely by using a factory/constructor that accepts the dependency
tool = MyTool(settings=mock_settings)  # preferred
```

See also: [ARCHITECTURE_PRINCIPLES.md §14 — Test via Public API](ARCHITECTURE_PRINCIPLES.md).

---

## Native selection and evidence

The configured strict type gate covers production sources; explicit test-file diagnosis does not create a whole-test Mypy/Pyright acceptance gate. Tests still use ordinary annotations and precise necessary fixture/interface/invalid-input exceptions instead of blanket ANN/ARG or untyped-definition exemptions. Workflow scope and timing remain governed by [Quality and Evidence Standards](QUALITY_GATES.md).

Restore native defaults by removing unjustified overrides; this does not mean enabling every optional diagnostic. For static sensitivity, verify both clean positive cases and intended negative codes under the actual effective policy. Confirm that the checker analyzed the requested files: hidden temporary paths can otherwise produce a misleading zero-file result. Keep temporary diagnostic probes separate from durable behavior tests, without dependency-version or legacy-format test matrices.

## What Agents Should Do (Short Checklist)

- Apply fixes in the **Resolution Order** above.
- Prefer `assert` / `isinstance` narrowing over `cast`.
- If ignoring: use **error-code specific** ignores + a brief reason.
- Avoid global config changes to silence issues.
