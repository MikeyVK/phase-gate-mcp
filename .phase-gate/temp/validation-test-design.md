<!-- .st3\temp\validation-test-design.md -->
<!-- template=design version=5827e841 created=2026-05-08T13:23Z updated= -->
# Validation Test Design

**Status:** DRAFT  
**Version:** 1.0  
**Last Updated:** 2026-05-08

---

## 1. Context & Requirements

### 1.1. Problem Statement

Validate NoteContext propagation through scaffold chain.

### 1.2. Requirements

**Functional:**
- [ ] NoteContext passed to scaffolder
- [ ] BlockerNote produced on ValidationError

**Non-Functional:**
- [ ] Tool response contains notes

### 1.3. Constraints

None
---

## 2. Design Options
---

## 3. Chosen Design

**Decision:** Propagate NoteContext via scaffold() parameter

**Rationale:** Enables rich feedback in tool responses without breaking existing callers

### 3.1. Key Design Decisions

| Decision | Rationale |
|----------|-----------|

## Related Documentation
None
---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 |  | Agent | Initial draft |