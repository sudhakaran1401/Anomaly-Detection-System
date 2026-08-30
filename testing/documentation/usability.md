# Usability Test Record

## Automated usability smoke coverage

`testing/e2e/usability.spec.js` provides repeatable checks for:

1. Login
2. Upload surface
3. History navigation
4. Logout

Run:

```bash
npx playwright test e2e/usability.spec.js
```

## Human usability session

The following tasks remain suitable for manual observation because completion time, user error and subjective clarity cannot be established reliably by an automated test alone:

1. Login
2. Upload CSV
3. Run anomaly detection
4. Review results/evaluation
5. Open history
6. Run classification
7. Export results
8. Logout

For each task record completion, time, error, observation and action. Do not mark the manual session PASS until it has been executed against the running UI.
