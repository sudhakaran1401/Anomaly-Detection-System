# 🔍 Smart Anomaly Detection & Classification Platform

A full-stack Machine Learning Analytics Platform built with **Django**, **Django REST Framework**, and **Scikit-Learn** that enables organizations to detect anomalies, evaluate labelled datasets, generate explainable insights, visualize results, and export professional reports.

The platform supports both **unsupervised anomaly detection** and **supervised classification workflows** through a modular, service-oriented architecture.

---

## 🚀 Key Features

### 📂 Intelligent Dataset Processing

- CSV dataset upload and validation
- Automatic dataset type detection
- Labelled and unlabelled dataset support
- Missing value handling
- Numerical feature extraction
- Dataset preprocessing pipeline
- File size and format validation

---

### 🧠 Multi-Model Machine Learning Engine

#### Unsupervised Anomaly Detection

- Isolation Forest
- Local Outlier Factor (LOF)
- One-Class SVM
- DBSCAN

#### Supervised Classification

- Random Forest
- Logistic Regression
- Decision Tree
- XGBoost

Models are dynamically selected through a centralized Factory Pattern architecture.

---

### ⚙️ Feature Engineering Pipeline

The platform automatically generates additional analytical features including:

- Z-Score Features
- CPU-to-Memory Ratios
- Response-Time Efficiency Metrics

This improves anomaly detection quality without requiring manual preprocessing.

---

### 📊 Interactive Analytics Dashboard

#### Real-Time Metrics

- Total Records
- Normal Records
- Anomalies Detected
- Detection Percentage
- Model Evaluation Statistics

#### Visual Insights

- PCA Scatter Visualization
- Anomaly Distribution Analysis
- Score Histograms
- Confusion Matrix Charts

---

### 🔍 Explainable AI (XAI)

The platform generates human-readable explanations for anomalies.

Examples:

```text
salary deviates significantly from normal behaviour
```

```text
Anomaly influenced by: salary, transaction_amount, cpu_usage
```

This helps users understand why a record was flagged.

---

### 📈 Model Evaluation & Metrics

#### Classification Metrics

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC Score
- Confusion Matrix

#### Anomaly Detection Metrics

- Total Records
- Anomaly Count
- Anomaly Percentage
- Average Anomaly Score

---

### 💾 Model Persistence

Models are automatically saved for future reuse.

Features:

- Model Versioning
- Joblib Serialization
- Persistent Storage
- Model Reloading

---

### 📋 Detection History Management

Stores:

- Dataset Name
- Model Used
- Scaler Selected
- Contamination Rate
- Total Records Processed
- Anomalies Detected
- Evaluation Metrics

---

### 📥 Professional Report Generation

#### CSV Export

Export processed results for further analysis.

#### PDF Export

Generated reports include:

- Dataset Information
- Detection Summary
- Statistical Insights
- PCA Visualizations
- Anomaly Distribution Charts
- Performance Evaluation

---

### 🔐 Authentication & Security

- User Authentication
- Login & Logout
- Protected Routes
- JWT Authentication
- User-Specific API Access

---

### 🌐 REST API Support

#### Available Endpoints

```http
POST /api/analyze/
```

Upload datasets and receive anomaly detection results.

```http
GET /api/results/
```

Retrieve historical detection results.

Features:

- JWT Authentication
- Serializer Validation
- ModelViewSet Architecture
- Pagination Support

---

## 🏗 System Architecture

```text
CSV Dataset Upload
          │
          ▼
File Validation Service
          │
          ▼
Feature Engineering
          │
          ▼
Dataset Analyzer
          │
          ▼
Model Factory
          │
          ▼
Scaler Factory
          │
          ▼
Prediction Engine
          │
          ▼
Evaluation Service
          │
          ▼
Explainability Engine
          │
          ▼
Dashboard + Reports + APIs
```

---

## 🛠 Technology Stack

### Backend

- Python
- Django 6
- Django REST Framework
- JWT Authentication

### Machine Learning

- Scikit-Learn
- XGBoost
- Pandas
- NumPy

### Visualization

- Matplotlib
- PCA Analytics

### Reporting

- ReportLab

### Database

- SQLite
- PostgreSQL Ready

---

## 📂 Project Structure

```text
Anomaly_Detection/
│
├── anomaly/
│   ├── api/
│   ├── ml/
│   │   ├── model_factory.py
│   │   ├── predictor.py
│   │   ├── scaler_factory.py
│   │   ├── supervised_predictor.py
│   │   └── anomaly.py
│   │
│   ├── services/
│   │   ├── anomaly_service.py
│   │   ├── analytics_service.py
│   │   ├── explainability_service.py
│   │   ├── feature_engineering_service.py
│   │   ├── report_service.py
│   │   ├── pdf_service.py
│   │   ├── chart_service.py
│   │   └── model_persistence.py
│   │
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── classification/
├── media/
├── saved_models/
├── requirements.txt
├── manage.py
└── README.md
```

---

## ⚙️ Installation & Setup

### Clone Repository

```bash
git clone https://github.com/your-username/anomaly-detection-platform.git

cd anomaly-detection-platform
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Migrations

```bash
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Start Development Server

```bash
python manage.py runserver
```

---

## 📊 Sample Workflow

1. Upload a CSV dataset
2. Dataset validation begins
3. Feature engineering is applied
4. Dataset type is identified
5. Selected model processes the data
6. Anomalies are detected or classifications are generated
7. Explanations are created
8. Charts and analytics are generated
9. Results are stored
10. Reports become available for export

---

## ✨ Design Patterns & Architecture

### Factory Pattern

- ModelFactory
- ScalerFactory

### Service Layer Pattern

- AnomalyService
- EvaluationService
- ReportService
- ExplainabilityService
- AnalyticsService

### Modular ML Pipeline

- Feature Engineering
- Scaling
- Training
- Prediction
- Evaluation
- Reporting

---

## 🔥 Advanced Features

- Multi-Model Detection Framework
- Hybrid Supervised + Unsupervised Support
- Explainable AI
- PCA Visualization
- Automatic Feature Engineering
- Model Persistence
- Detection History Tracking
- REST APIs
- JWT Authentication
- PDF Report Generation
- Service-Oriented Architecture
- Factory Design Pattern

---

## 🔮 Future Enhancements

- Docker Support
- PostgreSQL Production Configuration
- Celery Background Tasks
- Redis Caching
- Real-Time Monitoring
- AutoML Integration
- Kubernetes Deployment
- AWS / Azure Deployment

---

## 👨‍💻 Author

**Sudha Karan**

Full Stack Developer | Machine Learning Enthusiast

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
