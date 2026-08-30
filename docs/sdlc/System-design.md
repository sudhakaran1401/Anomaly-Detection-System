# Smart Anomaly Detection & Classification Platform — SDLC Stage 4: System Design

## 1. Architecture
```text
React / Vite Frontend
        |
     HTTP/REST
        |
Django / Django REST Framework
        |
+-------+-------------------------------+
| Accounts / Authentication             |
| File Validation / Feature Engineering |
| Anomaly ML / Analytics / XAI          |
| Classification ML / Reports           |
| History / Persistence                 |
+----------------+----------------------+
                 |
              Database
                 |
          Media / Result Files
```

## 2. Backend Applications
- `accounts` — authentication/session functionality
- `anomaly` — anomaly models, APIs, ML algorithms, analytics, history and reports
- `classification` — classification APIs, models and reports
- `core` — shared ML preprocessing and security/file services

## 3. ML Design
### Anomaly Models
- Isolation Forest: deterministic `random_state=42`, configurable estimators and contamination.
- LOF: novelty-enabled implementation with configurable neighbours and contamination.
- One-Class SVM: RBF kernel with configurable gamma.
- DBSCAN: configurable `eps` and `min_samples`.

### Ensemble
The weighted ensemble converts model anomaly predictions to binary votes and combines them using configured weights and a threshold.

### Classification
- Random Forest: 100 estimators, `random_state=42`.
- Decision Tree: `random_state=42`.
- Logistic Regression: `max_iter=1000`.
- XGBoost: 100 estimators, learning rate 0.1, max depth 5, `random_state=42`.

## 4. Scaling
`ScalerFactory` provides StandardScaler, MinMaxScaler and RobustScaler.

## 5. Persistence
The anomaly application stores detection/history information and saved model paths. Classification results store metrics, confusion matrix, summaries and generated chart information.

## 6. API Design
The project exposes:
- anomaly APIs under `/api/anomaly/`
- classification APIs under `/api/classification/`
- JWT token endpoints
- OpenAPI schema at `/api/schema/`
- Swagger UI at `/api/docs/`

## 7. Deployment Design
Docker Compose runs separate backend and frontend services and persists the SQLite database, media and static-file volumes.
