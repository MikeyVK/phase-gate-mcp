# Mermaid Voorbeelddiagrammen — Best Practice

Drie concrete voorbeelden: max 7–9 nodes, geen nesting dieper dan 2 niveaus.

---

## Diagram 1 — System Context (C4 Level 1)

```mermaid
graph TD
    VSCode["VS Code\n(MCP Client)"]
    Proxy["MCP Proxy\n(dev only)"]
    Server["MCP Server\n(FastMCP)"]
    Git["Git / GitHub"]
    FS["Filesystem\n(.st3/ + workspace)"]

    VSCode -->|"stdio"| Proxy
    Proxy -->|"stdio"| Server
    Server -->|"read/write"| FS
    Server -->|"gh CLI"| Git
```

---

## Diagram 2 — Workflow State Subsystem (integratiekloof zichtbaar)

```mermaid
graph LR
    PSE["PhaseStateEngine"]
    SR["StateRepository"]
    PCR["PhaseContractResolver"]
    DC["DeliverableChecker"]

    PSE -->|"load / save"| SR
    PSE -.->|"niet ingedraad"| PCR
    PSE -->|"direct new"| DC

    style PCR fill:#f90,color:#000
    style DC  fill:#f90,color:#000
```

> Oranje = gebouwd maar niet correct gekoppeld (integratiekloof RC-2).

---

## Diagram 3 — Sequence: `transition_phase`

```mermaid
sequenceDiagram
    participant Client as VS Code
    participant Tool   as TransitionPhaseTool
    participant PSE    as PhaseStateEngine
    participant Repo   as StateRepository

    Client->>Tool: transition_phase(branch, to_phase)
    Tool->>PSE: transition(branch, to_phase)
    PSE->>Repo: load_state(branch)
    Repo-->>PSE: BranchState
    PSE->>PSE: validate_transition()
    PSE->>Repo: save_state(branch, new_state)
    PSE-->>Tool: TransitionResult
    Tool-->>Client: success / error
```
