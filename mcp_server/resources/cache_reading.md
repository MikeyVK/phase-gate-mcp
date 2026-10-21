# Reading cached tool results

Every normal response starts with bounded readable inline text. In structured mode,
use `data.operation` in the structured envelope when the client exposes it;
`presentation` contains the full rendered explanation before inline clipping.
Resource mode instead ends the inline text with a real
`pgmcp://cache/runs/<run_id>` locator for the complete canonical operation.
No complete JSON envelope is appended to text.

Available schema attachments are always separate native MCP embedded-resource content
blocks with URI, MIME type and full text. Structured `attachments` contains only
URI/MIME references to those blocks, without another body copy. A `schema://` identity
does not by itself promise a registered reader. The operation cache does not store
independent attachments or rendered presentation; existing schema fields owned by an
operation remain part of it.

A failed publication supplies no usable URI. Inspect the warning/outcome instead of
trying a fabricated resource. Structured operation data can remain complete after a
cache storage failure. A prior operation serialization failure is not retried.
Diagnostic excerpts are labelled potentially incomplete; they are not complete JSON
results. Compact processing recovery can reference an already-successful publication
without executing or publishing the operation again.

A published operation exceeding `global.cache_read_budget_chars` (default 6000 Unicode
codepoints) also gets paging advice when its URI is offered. This is a read-advice
threshold, not a client truncation guarantee. Mode selection and cache state are
process-local: use the same connected server that produced the reference.
For durable evidence, record the exact invocation, scope and observed outcome;
a run ID or cache URI alone is insufficient.

## Bounded reads

For large or truncated results, read the same URI with `?offset=0&limit=6000`.
Both parameters are required: offset is nonnegative and limit is 1–12000.
Offsets count Unicode codepoints, not UTF-8 bytes or JavaScript UTF-16 code units.

Each window contains `run_id`, `offset`, `total_chars`, `sha256`, `text` and
`next_offset`. Follow `next_offset` on the same base URI until it is null.
Require identical run ID, full-content hash and total length on every page,
and contiguous offsets. Join the text in order, verify its codepoint length and
UTF-8 SHA-256, then parse the complete JSON. Never parse an incomplete assembly.

If a window is truncated, retry that offset with a smaller limit. On cache loss
or changed hash, discard the partial assembly. Repeat only a safe read-only query
to obtain a fresh run and start again. Never replay a mutating or non-repeatable
producer to recover its cache: use an existing result/status query, or report
that the details are unavailable. Never combine pages from different runs.

The cache is transient. EOF permits an empty page; an offset beyond EOF fails.
Ordinary reads and windows use the same JSON representation.
