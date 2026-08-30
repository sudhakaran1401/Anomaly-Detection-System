# Smart Anomaly Detection & Classification Platform — SDLC Stage 1: Planning

## 1. Project Overview
The Smart Anomaly Detection & Classification Platform is a full-stack machine-learning analytics application. It allows an authenticated user to upload a structured CSV dataset, validate and preprocess it, run anomaly-detection algorithms, inspect analytics and explanations, optionally perform supervised classification, view history, and export results.

The repository implements the application with React/Vite on the frontend and Django/Django REST Framework on the backend. Machine-learning functionality uses Scikit-Learn and XGBoost.

## 2. Objectives
1. Provide authenticated access to the analytics application.
2. Accept and validate CSV datasets.
3. Clean and engineer usable numeric features.
4. Support multiple unsupervised anomaly-detection algorithms.
5. Support weighted-ensemble anomaly detection.
6. Calculate anomaly counts, scores and evaluation metrics where labels are available.
7. Provide PCA-based visualization and dashboard analytics.
8. Provide human-readable anomaly explanations.
9. Support supervised classification using four configured classifiers.
10. Persist detection/classification history and generated model/report artifacts.
11. Provide CSV/PDF reporting.
12. Provide automated backend, frontend and browser testing.
13. Provide reproducible benchmarking and performance-testing tooling.
14. Provide Docker-based deployment.

## 3. Primary User Workflow
Login → upload CSV → validate → feature engineering → scaling → anomaly detection → evaluation/analytics → explanation/PCA visualization → history/report export → optional classification workflow.

## 4. Scope
### In scope
Authentication, CSV upload/validation, preprocessing, anomaly detection, ensemble detection, classification, analytics, explainability, history, reporting/export, security checks, automated testing, benchmarking and Docker deployment.

### Out of scope unless separately configured
Enterprise-scale distributed ML infrastructure, managed production monitoring/SLA, automated database failover and enterprise point-in-time recovery.

## 5. Major Components
- `backend/accounts`
- `backend/anomaly`
- `backend/classification`
- `backend/core`
- `frontend/src`
- `testing/e2e`
- `testing/performance`
- `backend/benchmark`
