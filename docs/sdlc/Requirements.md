# Smart Anomaly Detection & Classification Platform — Requirements Analysis

## 1. Functional Requirements

### FR-01 — Authentication
The system shall authenticate users and protect application/API functionality with Django authentication/JWT-based API authentication.

### FR-02 — CSV Dataset Upload
Authenticated users shall be able to upload CSV files for analysis.

### FR-03 — File Validation
Uploaded files shall be validated for CSV extension, filename safety, maximum size, supported content type, UTF-8 encoding, duplicate columns, empty columns, valid CSV structure and presence of data rows.

The implemented maximum file size is 5 MB.

### FR-04 — Dataset Analysis
The system shall determine whether a dataset is labelled or unlabelled where supported and identify a target/label column using the project's label-column rules.

### FR-05 — Feature Engineering and Preprocessing
The system shall perform the implemented feature-engineering/preprocessing steps before model execution and handle missing/infinite numeric values according to the implemented services.

### FR-06 — Anomaly Detection
The system shall support:
- Isolation Forest
- Local Outlier Factor (LOF)
- One-Class SVM
- DBSCAN

The implementation also accepts the `svm` alias for One-Class SVM in the model factory.

### FR-07 — Scalers
The anomaly/classification workflows shall support:
- StandardScaler
- MinMaxScaler
- RobustScaler

### FR-08 — Anomaly Configuration
The anomaly API shall accept model, scaler and contamination parameters. Contamination must be greater than 0 and less than 0.5.

### FR-09 — Weighted Ensemble
The platform shall provide a weighted ensemble detector for models that support the project's ensemble prediction interface. DBSCAN is excluded from the benchmark ensemble because it does not provide the required `predict(X)` interface.

### FR-10 — Anomaly Analytics
The detection workflow shall provide total records, normal records, anomaly count, anomaly scores and visualization data, including PCA coordinates where generated.

### FR-11 — Explainability
The system shall generate human-readable anomaly reasons based on unusual numeric feature values/statistics.

### FR-12 — Evaluation
For labelled datasets, the system shall evaluate anomaly predictions against normalized labels. The evaluation services support accuracy, precision, recall, F1, confusion-matrix-derived measures and related anomaly metrics.

### FR-13 — Detection History
Authenticated users shall be able to view, retrieve and delete their own detection history. Cross-user history must not be accessible.

### FR-14 — Model Persistence
The anomaly workflow shall save trained anomaly models and retain the generated model path in the relevant result/history records.

### FR-15 — Classification
The classification module shall support:
- Random Forest
- Decision Tree
- Logistic Regression
- XGBoost

### FR-16 — Classification Evaluation
Classification shall produce accuracy, precision, recall, F1, confusion matrix, summary information and ROC-AUC when probability output is available.

### FR-17 — Classification History and Security
Classification results shall be associated with the authenticated user. Users shall only retrieve, download or delete their own classification results.

### FR-18 — Reporting and Export
The system shall support CSV result export and PDF reporting for anomaly detection and classification.

### FR-19 — Frontend Analytics
The React application shall provide login, upload, anomaly dashboard, classification dashboard, history, charts, tables, metrics, theme handling and responsive UI components.

### FR-20 — API Documentation
The backend shall expose OpenAPI schema/Swagger endpoints through the configured DRF Spectacular integration.

## 2. Non-Functional Requirements
- Authentication and authorization
- User-data isolation
- File/path security
- Input validation
- Reliability
- Maintainability
- Browser/E2E testability
- Accessibility checks
- Performance benchmarking
- Reproducibility
- Containerized deployment
