<!-- docs\development\issue406\rest_gaps.md -->
<!-- template=generic_doc version=43c84181 created=2026-06-24T05:42Z updated= -->
# Remaining Gaps: Presentation Layer & DTO Refactoring

**Status:** APPROVED  
**Version:** 1.0.0  
**Last Updated:** 2026-06-24

---

## Purpose

To document the remaining architectural gaps identified during Issue #406 regarding text presentation and error DTO structures, outlining the approved design for future implementation sessions.

## Scope

**In Scope:**
Sanitization of BaseToolOutput, creation of BaseErrorOutput, status resolution updates in server.py and text_presenter.py, and declarative template mapping in presentation.yaml.

**Out of Scope:**
Implementation changes on the active branch (feature/406), which is being closed. These steps will be implemented in subsequent issues.

---

## Summary

This document records the design and implementation roadmap for resolving the backdoor in BaseToolOutput (error_message) and decoupling system errors from tool-level domain errors using the BaseErrorOutput hierarchy.

---

## Key Changes

- Remove error_message from BaseToolOutput to eliminate the Python-level text presentation backdoor.
- Introduce BaseErrorOutput (without success field) in error_outputs.py for all platform, decorator, and system errors.
- Update status resolution in server.py and text_presenter.py to check for BaseErrorOutput type (isinstance).
- Update presenter template selection to route system errors to global failures/templates and domain errors to tool-specific template_failures.
- Leverage generic core exception classes (PreflightError, ValidationError) carrying error_code and params instead of introducing custom exception classes.




## Related Documentation
- **[docs/coding_standards/ARCHITECTURE_PRINCIPLES.md][related-1]**
- **[docs/development/issue406/research_get_work_context_gaps.md][related-2]**

<!-- Link definitions -->

[related-1]: docs/coding_standards/ARCHITECTURE_PRINCIPLES.md
[related-2]: docs/development/issue406/research_get_work_context_gaps.md

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-24 | Agent | Initial draft |