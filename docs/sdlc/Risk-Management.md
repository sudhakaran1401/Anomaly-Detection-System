# Smart Anomaly Detection & Classification Platform — Risk Management

| ID | Risk | Impact | Mitigation |
|---|---|---|---|
| R-01 | Incorrect anomaly predictions | High | Multiple algorithms, evaluation and benchmarking |
| R-02 | Poor contamination/threshold choice | High | contamination and threshold experiments |
| R-03 | Malformed/unsafe uploaded file | High | extension, size, encoding, column and path validation |
| R-04 | Cross-user data exposure | High | authenticated APIs and user-scoped querysets/security tests |
| R-05 | Model persistence/load failure | High | saved model paths and recovery verification |
| R-06 | Large/resource-heavy dataset | High | 5 MB upload limit and load/stress tooling |
| R-07 | ML dependency changes | Medium/High | dependency review and regression/benchmark testing |
| R-08 | Database/media loss | High | volume backup/recovery procedure |
| R-09 | Deployment failure | High | Docker, smoke tests and rollback procedure |
| R-10 | Non-reproducible benchmark | Medium | fixed seeds and recorded benchmark metadata |
| R-11 | Report/export failure | Medium | API/integration/E2E export tests |
| R-12 | Browser/UI incompatibility | Medium | Playwright multi-browser configuration and compatibility testing |

## Review Triggers
Review risks after model changes, dependency upgrades, schema changes, security defects, major feature changes and release preparation.
