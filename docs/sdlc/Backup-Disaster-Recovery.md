# Smart Anomaly Detection & Classification Platform — Backup & Disaster Recovery

## 1. Scope
The supplied Docker Compose deployment persists:
- SQLite database volume
- media volume
- static-files volume

Generated result files and saved model artifacts are part of the application's runtime data and should be included in an operational backup strategy.

## 2. What Should Be Backed Up
- Git repository/release source
- database data
- `MEDIA_ROOT` contents
- generated result/report files
- saved model artifacts
- environment configuration templates
- deployment configuration

Secrets should be stored separately and securely.

## 3. Recovery Procedure
1. Restore the known-good source/release.
2. Restore the database volume.
3. Restore media/result/model artifacts.
4. Restore required environment configuration.
5. Start the backend and frontend containers.
6. Run migrations if required.
7. Verify authentication.
8. Upload a known-good CSV.
9. Run anomaly detection.
10. Run classification on a suitable labelled dataset.
11. Verify history and exports.

## 4. Recovery Verification
| Check | Expected result |
|---|---|
| Backend starts | API available |
| Database restored | Existing records accessible |
| Media restored | Result/model/report files available |
| Detection | Known-good dataset processes |
| Classification | Known-good labelled dataset processes |
| History | User history accessible |
| Export | CSV/PDF generation works |

This is an application/deployment recovery procedure. It does not claim enterprise point-in-time recovery or automated failover.
