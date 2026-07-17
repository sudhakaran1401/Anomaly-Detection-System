# 🔍 Smart Anomaly Detection & Classification Platform

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-REST_Framework-0C4B33?style=for-the-badge&logo=django)
![React](https://img.shields.io/badge/React-Vite-61DAFB?style=for-the-badge&logo=react)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?style=for-the-badge)
![XGBoost](https://img.shields.io/badge/XGBoost-Learning-red?style=for-the-badge)
![JWT](https://img.shields.io/badge/JWT-Authentication-success?style=for-the-badge)

</p>

<p align="center">

# An End-to-End Machine Learning Analytics Platform

Upload datasets, detect anomalies, classify data, visualize insights, generate explainable AI predictions, and export professional reports through an intuitive full-stack web application.

Built using **React**, **Django REST Framework**, **Scikit-Learn**, **XGBoost**, and **JWT Authentication**.

</p>

---

# 📖 Overview

The **Smart Anomaly Detection & Classification Platform** is a full-stack Machine Learning Analytics application that enables users to upload structured datasets and perform intelligent anomaly detection through multiple machine learning algorithms.

Unlike conventional ML projects that only execute a single model, this platform provides a complete analytics workflow—from data preprocessing to explainable AI, interactive dashboards, classification, visualization, and automated report generation.

The project combines **React** for the frontend, **Django REST Framework** for backend APIs, and **Scikit-Learn** for machine learning, resulting in a scalable and modular analytics platform.

---

# 🚀 Core Features

## 📂 Dataset Management

- Upload CSV datasets
- Automatic validation
- Missing value handling
- Numerical feature extraction
- Data preprocessing
- Dataset summary

---

## 🧠 Anomaly Detection

Supports multiple anomaly detection algorithms:

- Isolation Forest
- Local Outlier Factor (LOF)
- One-Class SVM
- DBSCAN
- Weighted Ensemble

Users can compare the performance of different algorithms on the same dataset.

---

## 🏷 Classification Module

The platform also supports supervised learning using:

- Random Forest
- Decision Tree
- Logistic Regression
- XGBoost

When labelled data is unavailable, anomaly predictions can be converted into pseudo-labels for supervised learning.

---

## 🔍 Explainable AI (XAI)

Instead of only detecting anomalies, the system explains why predictions were made.

Features include:

- Feature Importance
- Human-readable explanations
- Prediction reasoning

---

## 📊 Analytics Dashboard

Interactive dashboards provide:

- Total Records
- Normal Records
- Anomaly Count
- Detection Percentage
- Average Anomaly Score
- PCA Visualization
- Histograms
- Confusion Matrix
- Classification Metrics

---

## 📑 Reporting

Generate professional reports including:

- PDF Reports
- CSV Export
- Charts
- Statistical Summary
- PCA Visualization

---

## 💾 Model Persistence

The application supports:

- Saving trained models
- Reloading saved models
- Model versioning
- Prediction history

---

## 🔐 Authentication

- JWT Authentication
- User Login
- Protected APIs
- Session Management

---

# 📸 Application Screenshots

## Login

<p align="center">
<img src="images/Login.png" width="650">
</p>

---

## Upload Dataset

<p align="center">
<img src="images/Upload%20Form.png" width="650">
</p>

---

## Detection Dashboard

<p align="center">
<img src="images/Detection%20Dashboard.png" width="650">
</p>

---

## Classification Dashboard

<p align="center">
<img src="images/Classification%20Dashboard.png" width="650">
</p>

---

## Detection History

<p align="center">
<img src="images/History.png" width="650">
</p>

---

## Dark Mode

<p align="center">
<img src="images/Dark%20Mode.png" width="650">
</p>

---

# 🧠 Complete Workflow

```text
User Login
      │
      ▼
Upload Dataset
      │
      ▼
Dataset Validation
      │
      ▼
Data Cleaning
      │
      ▼
Feature Engineering
      │
      ▼
Scaling
      │
      ▼
Anomaly Detection
      │
      ▼
Pseudo Label Generation
      │
      ▼
Classification
      │
      ▼
Model Evaluation
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
Report Generation
      │
      ▼
Detection History
```

---

# 🛠 Technology Stack

## Frontend

- React
- Vite
- Axios
- Bootstrap

## Backend

- Python
- Django
- Django REST Framework
- JWT Authentication

## Machine Learning

- Scikit-Learn
- XGBoost
- Pandas
- NumPy

## Visualization

- Matplotlib
- PCA

## Reporting

- ReportLab

## Database

- SQLite
- PostgreSQL Ready

---

# 📂 Project Structure

The project follows a **full-stack architecture** with separate frontend and backend modules.

```text
Anomaly_Detection/
│
├── backend/
│   │
│   ├── accounts/                  # User Authentication & Authorization
│   ├── anomaly/                   # Core anomaly detection module
│   ├── Anomaly_Detection/         # Django project configuration
│   ├── classification/           # Classification module
│   ├── core/                     # Shared utilities & common components
│   ├── media/                    # Uploaded datasets & generated reports
│   ├── saved_models/             # Persisted ML models
│   ├── static/                   # Static assets
│   ├── templates/                # Django templates
│   │
│   ├── manage.py
│   ├── requirements.txt
│   └── db.sqlite3
│
├── frontend/
│   │
│   ├── src/
│   ├── public/
│   ├── images/
│   ├── package.json
│   ├── vite.config.js
│   └── eslint.config.js
│
├── images/                       # README screenshots
├── README.md
└── .gitignore
```

---

# 🏗 System Architecture

```text
                    React Frontend
                          │
                          │ Axios
                          ▼
               Django REST Framework APIs
                          │
                          ▼
                  Service Layer
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
 Dataset Processing   ML Pipeline     Report Generator
        │                 │                 │
        └──────────────┬──┴─────────────────┘
                       ▼
            Scikit-Learn Models
                       │
                       ▼
                SQLite Database
```

---

# ⚙ Installation

## 1. Clone Repository

```bash
git clone https://github.com/sudhakaran1401/Anomaly-Detection-System.git

cd Anomaly_Detection
```

---

## 2. Backend Setup

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

---

## 3. Configure Environment

Create a `.env` file inside the **backend** directory.

Example:

```env
SECRET_KEY=your-secret-key

DEBUG=True

DATABASE_URL=sqlite:///db.sqlite3
```

---

## 4. Apply Migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

---

## 5. Create Superuser

```bash
python manage.py createsuperuser
```

---

## 6. Start Backend Server

```bash
python manage.py runserver
```

Backend URL

```
http://127.0.0.1:8000/
```

---

## 7. Frontend Setup

Open another terminal.

```bash
cd frontend

npm install

npm run dev
```

Frontend URL

```
http://localhost:5173
```

---

# 🔌 REST APIs

The application exposes REST APIs through Django REST Framework.

Major API groups include:

- Authentication
- Dataset Upload
- Anomaly Detection
- Classification
- Dashboard
- Detection History
- Reporting
- Model Management

---

# 🧠 Machine Learning Pipeline

The anomaly detection engine performs the following operations automatically:

- Dataset validation
- Missing value handling
- Feature engineering
- Data scaling
- Model selection
- Anomaly prediction
- Ensemble prediction
- Pseudo-label generation
- Classification
- Evaluation
- Explainability
- PCA visualization
- Report generation

---

# 📈 Evaluation Metrics

## Classification

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

## Anomaly Detection

- Total Anomalies
- Detection Percentage
- Average Anomaly Score
- PCA Visualization
- Confusion Matrix

---

# 🔐 Security Features

- JWT Authentication
- Protected REST APIs
- User-specific datasets
- Session management
- Password validation

---

# 🎯 Design Patterns

- Factory Pattern
- Service Layer Pattern
- Modular Architecture
- REST API Architecture
- Model Persistence Pattern

---

# 🌟 Highlights

- Full Stack Machine Learning Platform
- React + Django REST Framework
- Multiple Anomaly Detection Algorithms
- Supervised Classification
- Explainable AI (XAI)
- Interactive Analytics Dashboard
- PCA Visualization
- PDF Report Generation
- CSV Export
- Model Persistence
- Detection History
- JWT Authentication
- Responsive User Interface
- Dark Mode Support

---

# 🚀 Future Enhancements

- Docker Support
- PostgreSQL Production Database
- Redis Caching
- Celery Background Tasks
- AutoML Integration
- Kubernetes Deployment
- Cloud Deployment (AWS / Azure)
- Real-time Streaming Analytics
- Model Monitoring Dashboard
- CI/CD Pipeline

---

# 👨‍💻 Author

## Sudha Karan

**Python Full Stack Developer | Machine Learning Enthusiast**

GitHub:

https://github.com/sudhakaran1401

---

# ⭐ Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub.

It helps support future development and makes the repository more discoverable.