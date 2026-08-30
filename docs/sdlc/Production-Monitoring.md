# Smart Anomaly Detection & Classification Platform — Production Monitoring & Observability

## 1. Monitoring Scope
Where deployed, monitor:
- backend availability
- frontend availability
- HTTP 4xx/5xx responses
- authentication failures
- database connectivity
- file-processing failures
- anomaly/classification inference failures
- report/export failures
- container status
- CPU/memory/disk usage

## 2. ML/Application Indicators
Useful application indicators include:
- inference/runtime duration
- dataset processing failures
- number of records processed
- anomaly counts
- model loading failures
- classification failures
- repeated API failures

## 3. Logging
The application configures an `anomaly` logger and an error file handler. Logs must not expose passwords, JWT secrets, database credentials or unnecessary sensitive dataset information.

## 4. Post-Deployment Verification
1. Open frontend.
2. Login.
3. Upload a small known-good CSV.
4. Run anomaly detection.
5. Review results.
6. Run classification if applicable.
7. Verify history/export.
8. Check backend logs.

## 5. Limitation
The repository does not establish a managed 24/7 monitoring service, SLA or production alerting platform. Such claims require actual deployment configuration.
