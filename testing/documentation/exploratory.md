# Exploratory Testing Charter

## Automated exploratory regression

`testing/e2e/exploratory.spec.js` covers three repeatable exploratory scenarios:

- invalid credentials remain recoverable
- protected routes do not expose an authenticated surface
- authenticated navigation survives a reload

Run:

```bash
npx playwright test e2e/exploratory.spec.js
```

## Human exploratory session

Explore authentication, uploads, detection, classification, history, reports/exports, error handling, permissions and responsive UI.

Record:

- Test session/date
- Area explored
- Steps
- Observation
- Severity
- Reproduction
- Disposition

The automated charter does not replace human exploratory testing. Record the actual human session before marking the manual exploratory phase PASS.
