# Testing

This testing structure is aligned with the HR Management System reference project:

- `backend/tests/` — automated acceptance, recovery, regression, reliability, and system tests.
- `frontend/src/test/` — frontend test location (documented; no JS runner currently configured).
- `testing/e2e/` — end-to-end workflow guidance.
- `testing/performance/load/` — load testing.
- `testing/performance/stress/` — stress testing.
- `testing/documentation/` — accessibility, compatibility, usability, exploratory, security, performance and test-matrix documentation.

Existing app-level tests remain in their original locations to preserve the currently verified Django test suite.
