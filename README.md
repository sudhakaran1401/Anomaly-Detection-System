# 🔍 Smart Anomaly Detection & Classification Platform

**An End-to-End Machine Learning Analytics Platform**

Built with **Django • Django REST Framework • React • Scikit-Learn •
XGBoost**

Detect anomalies, classify data, generate explainable insights,
visualize results, and export professional reports.
:::

------------------------------------------------------------------------

## ✨ Overview

This project is a full-stack **Machine Learning Analytics Platform** for
analyzing structured datasets. It supports both **unsupervised anomaly
detection** and **supervised classification**, integrating data
ingestion, preprocessing, feature engineering, explainable AI (XAI),
visualization, reporting, model persistence, and REST APIs into one
modular application.

------------------------------------------------------------------------

## 🚀 Features

### 📂 Intelligent Dataset Processing

-   CSV upload and validation
-   Automatic dataset analysis
-   Labelled & unlabelled dataset support
-   Missing value handling
-   Numerical feature extraction
-   Preprocessing pipeline

### 🧠 Machine Learning

#### Unsupervised

-   Isolation Forest
-   Local Outlier Factor (LOF)
-   One-Class SVM
-   DBSCAN
-   Weighted Ensemble

#### Supervised

-   Random Forest
-   Logistic Regression
-   Decision Tree
-   XGBoost

### 🏷️ Pseudo-Labeling Pipeline

``` text
Dataset
   │
   ▼
Anomaly Detection
   │
   ▼
Pseudo Labels
   │
   ▼
Classification Model
```

Converts anomaly detection outputs into pseudo-labels that can be used
to train supervised classifiers when labelled data is unavailable.

### ⚙️ Feature Engineering

-   Z-Score Features
-   CPU-to-Memory Ratio
-   Response-Time Efficiency Metrics

### 🔍 Explainable AI

Human-readable explanations for anomaly predictions.

Example:

> Salary deviates significantly from expected behaviour.

### 📊 Analytics Dashboard

-   Total Records
-   Normal Records
-   Anomaly Count
-   Detection Percentage
-   PCA Visualization
-   Confusion Matrix
-   Histograms

### 📈 Model Evaluation

**Classification** - Accuracy - Precision - Recall - F1 Score - ROC-AUC

**Anomaly Detection** - Anomaly Count - Detection Percentage - Average
Anomaly Score

### 💾 Model Persistence

-   Joblib serialization
-   Model versioning
-   Model reloading

### 📋 Detection History

Stores: - Dataset - Model - Scaler - Metrics - Configuration - Timestamp

### 📥 Reporting

-   CSV Export
-   PDF Reports
-   Charts
-   PCA Visualizations
-   Statistical Summary

### 🔐 Security

-   JWT Authentication
-   Protected APIs
-   User-specific access

------------------------------------------------------------------------

# 🏗️ Machine Learning Workflow

``` text
Authentication
      │
      ▼
Upload Dataset
      │
      ▼
Dataset Validation
      │
      ▼
Feature Engineering
      │
      ▼
Scaling
      │
      ▼
Model Factory
      │
      ▼
Anomaly Detection
      │
      ▼
Pseudo-Label Generation
      │
      ▼
Classification
      │
      ▼
Evaluation
      │
      ▼
Explainability
      │
      ▼
PCA Visualization
      │
      ▼
Analytics Dashboard
      │
      ▼
Reports & REST APIs
```

------------------------------------------------------------------------

# 🛠️ Technology Stack

## Backend

-   Python
-   Django
-   Django REST Framework
-   JWT Authentication

## Frontend

-   React
-   Vite
-   Axios

## Machine Learning

-   Scikit-Learn
-   XGBoost
-   Pandas
-   NumPy

## Visualization

-   Matplotlib
-   PCA

## Reporting

-   ReportLab

## Database

-   SQLite
-   PostgreSQL Ready

------------------------------------------------------------------------

# 📂 Project Structure

``` text
Anomaly_Detection/
│
├── anomaly/
│   ├── api/
│   ├── ml/
│   ├── services/
│   ├── templates/
│   ├── static/
│
├── classification/
├── frontend/
├── accounts/
├── saved_models/
├── media/
├── requirements.txt
└── manage.py
```

------------------------------------------------------------------------

# ⚙️ Installation

``` bash
git clone https://github.com/your-username/anomaly-detection-platform.git
cd anomaly-detection-platform

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

------------------------------------------------------------------------

# ✨ Design Patterns

-   Factory Pattern
-   Service Layer Pattern
-   Modular ML Pipeline

------------------------------------------------------------------------

# 🌟 Highlights

-   Multi-Model ML Framework
-   Hybrid Unsupervised + Supervised Learning
-   Pseudo-Labeling
-   Explainable AI (XAI)
-   PCA Visualization
-   Interactive Dashboard
-   Model Persistence
-   Detection History
-   REST APIs
-   JWT Authentication
-   PDF Reporting

------------------------------------------------------------------------

# 🔮 Future Enhancements

-   Docker
-   Redis
-   Celery
-   AutoML
-   Kubernetes
-   AWS / Azure Deployment

------------------------------------------------------------------------

# 👨‍💻 Author

**Sudha Karan**

Full Stack Developer \| Machine Learning Enthusiast

------------------------------------------------------------------------

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on
GitHub.
