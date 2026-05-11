<!-- .st3\temp\issue_render.md -->
<!-- template=issue version=8dd42510 created=2026-04-24T12:34Z updated= -->
# Centralize .st3 config root via MCP setting — DUPLICATE van #260

## Problem
De MCP server gebruikt op veel plekken hardcoded '.st3/...' paden. Padmigratie is kostbaar en foutgevoelig.

## Expected Behavior

Één centrale configuratie-instelling die de config root bepaalt (default '.st3'). Alle config/state toegang via een gedeelde path-resolver.
## Actual Behavior

Duplicaat van #260 (Configureerbare MCP root directory: .st3 vervangen door instelbaar pad). Issue #260 is de bredere, correcte formulering: de scope omvat de volledige vervangbaarheid van de directorynaam, niet alleen centralisatie van config root. Gesloten ten gunste van #260.
## Context

Aangemaakt tijdens research voor issue #251. De bredere implicatie (distribueerbare MCP server zonder projectspecifieke directorynaam) is beter gecaptured in #260.
## Related Documentation
- **[https://github.com/MikeyVK/SimpleTraderV3/issues/260][related-1]**
