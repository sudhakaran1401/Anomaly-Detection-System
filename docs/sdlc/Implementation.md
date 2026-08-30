# Smart Anomaly Detection & Classification Platform — SDLC Stage 5: Implementation

## 1. Technology Stack
- Python 3.11
- Django
- Django REST Framework
- React
- Vite
- Scikit-Learn
- XGBoost
- pandas / NumPy
- JWT authentication
- Docker / Docker Compose
- Playwright

## 2. Backend Implementation

### Accounts
Provides user authentication and token/session functionality.

### Core
`FileService` validates and reads CSV files. It enforces:
- `.csv` extension
- safe filename
- maximum 5 MB file size
- supported content types
- UTF-8
- non-empty data
- non-empty column names
- no duplicate column names

Core ML services provide dataset analysis, feature engineering and scaler selection.

### Anomaly
The anomaly module implements:
- anomaly model factory
- predictor
- Isolation Forest
- LOF
- One-Class SVM
- DBSCAN
- weighted ensemble
- evaluation
- analytics/chart data
- PCA data
- explainability
- model persistence
- session handling
- result/report generation

The detection service calculates total/normal/anomaly counts, creates anomaly reasons, evaluates labelled data when available, stores detection history and saves processed result data.

### Classification
The classification module implements four supervised classifiers and stores classification metrics/results for the authenticated user.

## 3. Frontend Implementation
The React application includes:
- Login
- Home/upload
- Anomaly dashboard
- Classification dashboard
- History
- Navigation
- Theme context
- charts
- tables
- metric cards
- report/download actions
- loading/error messaging
- responsive UI

## 4. Testing Implementation
The repository contains backend tests, frontend tests under `frontend/src/test`, Playwright E2E tests, accessibility checks and performance/load/stress tooling.
