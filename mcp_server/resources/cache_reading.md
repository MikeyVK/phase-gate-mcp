# Reading cached tool results

Read `pgmcp://cache/runs/<run_id>` for the complete JSON operation. Tool responses
always retain this link. Only results exceeding the configured
`global.cache_read_budget_chars` (default 6000 Unicode codepoints) also link here.
This is a conservative read budget, not a claim about every client's truncation limit.

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
