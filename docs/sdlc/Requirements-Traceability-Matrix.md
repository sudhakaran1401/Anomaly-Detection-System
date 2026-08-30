# Smart Anomaly Detection & Classification Platform — Requirements Traceability Matrix

| ID | Requirement | Implementation Evidence | Verification Evidence |
|---|---|---|---|
| FR-01 | Authentication | `accounts`, JWT endpoints, frontend Login | account tests, security tests, E2E |
| FR-02 | CSV upload | anomaly/classification upload APIs | API tests, E2E |
| FR-03 | File validation | `core/services/file_service.py` | file/security tests |
| FR-04 | Dataset analysis | `DatasetAnalyzer` | anomaly unit tests |
| FR-05 | Feature engineering | `FeatureEngineeringService` | anomaly pipeline tests |
| FR-06 | Four anomaly algorithms | anomaly model factory/ML modules | model/API/E2E tests |
| FR-07 | Three scalers | `ScalerFactory` | API/E2E/model combination tests |
| FR-08 | Contamination/model/scaler controls | anomaly API validation | API status tests |
| FR-09 | Weighted ensemble | `WeightedEnsembleDetector` | benchmark/ensemble tests |
| FR-10 | Analytics/PCA/scores | anomaly analytics/chart/PCA services | anomaly/E2E tests |
| FR-11 | Explainability | `ExplainabilityService` | anomaly pipeline coverage |
| FR-12 | Evaluation | `EvaluationService` | evaluation tests |
| FR-13 | Detection history | `DetectionHistory` + viewsets | integration/security/E2E |
| FR-14 | Model persistence | `ModelPersistenceService`, `TrainedModel` | anomaly processing/integration tests |
| FR-15 | Classification models | classification model factory | classification/API/E2E tests |
| FR-16 | Classification metrics | `SupervisedPredictor` | classification tests |
| FR-17 | Classification security/history | user-filtered result APIs | classification security tests |
| FR-18 | CSV/PDF reporting | report/PDF services and APIs | export/API/E2E tests |
| FR-19 | Frontend dashboards | React pages/components | frontend tests/E2E |
| FR-20 | API documentation | DRF Spectacular schema/Swagger | API configuration |

## Non-Functional Traceability

| ID | Requirement | Evidence |
|---|---|---|
| NFR-01 | Authentication/security | JWT, permissions, security tests |
| NFR-02 | User isolation | cross-user API/security tests |
| NFR-03 | Reliability | integration/repeated-run/performance tests |
| NFR-04 | Accessibility | Playwright accessibility checks + manual checklist |
| NFR-05 | Compatibility | Playwright browser configuration + compatibility plan |
| NFR-06 | Performance | benchmark/load/stress tooling |
| NFR-07 | Reproducibility | deterministic model settings and benchmark seeds |
| NFR-08 | Deployability | Docker/Docker Compose |
