# Smart Anomaly Detection & Classification Platform — SDLC Stage 3: System Analysis

## 1. System Context
The application is a React/Vite frontend communicating with Django REST Framework APIs. The backend coordinates file validation, feature engineering, anomaly detection, classification, persistence, analytics, explainability and reporting.

## 2. Actors
### Authenticated User
Uploads datasets, selects analysis options, reviews results, uses history and downloads reports.

### Developer/Operator
Maintains the application, runs tests/benchmarks and performs deployment/recovery activities.

## 3. Functional Decomposition
```text
Smart Anomaly Detection Platform
|
+-- Authentication
|
+-- Dataset Upload & Validation
|   +-- CSV validation
|   +-- size/type/name checks
|   +-- UTF-8 / structure checks
|
+-- Dataset Analysis / Feature Engineering
|
+-- Scaling
|   +-- Standard
|   +-- MinMax
|   +-- Robust
|
+-- Anomaly Detection
|   +-- Isolation Forest
|   +-- LOF
|   +-- One-Class SVM
|   +-- DBSCAN
|   +-- Weighted Ensemble
|
+-- Evaluation / Analytics
|   +-- anomaly counts
|   +-- anomaly scores
|   +-- PCA coordinates
|   +-- labelled-dataset metrics
|
+-- Explainability
|
+-- History / Persistence
|
+-- Classification
|   +-- Random Forest
|   +-- Decision Tree
|   +-- Logistic Regression
|   +-- XGBoost
|
+-- Reporting / Export
|   +-- CSV
|   +-- PDF
|
+-- Frontend Dashboards
```

## 4. Core Detection Flow
1. Authenticate user.
2. Upload CSV.
3. Validate file.
4. Read CSV into a DataFrame.
5. Generate implemented features.
6. Analyze dataset type/target information.
7. Select anomaly model, scaler and contamination.
8. Detect anomalies.
9. Generate anomaly reasons and analytics.
10. Evaluate when labels are available.
11. Persist history/result/model information.
12. Save processed result data.
13. Return dashboard/session data to the frontend.

## 5. Classification Flow
1. Authenticate user.
2. Upload a valid CSV.
3. Validate/read dataset.
4. Prepare labelled data.
5. Select classifier and scaler.
6. Train and predict.
7. Calculate classification metrics.
8. Store the classification result for the authenticated user.
9. Generate confusion-matrix/report information.
10. Return the result to the frontend.

## 6. Security Boundaries
Protected APIs use `IsAuthenticated`. Detection history, anomaly results and classification results are filtered by the authenticated user. File validation also prevents unsafe filenames, unsupported content and path traversal conditions.
