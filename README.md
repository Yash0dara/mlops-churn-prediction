# MLOps Customer Churn Prediction

End-to-end MLOps pipeline for predicting telecom customer churn.

## 🎯 Project Goal
Predict which customers will leave so the company can take retention actions.

## 🏗️ Pipeline Steps
1. **Data Validation** - Automatic quality checks before processing
2. **Data Cleaning** - Fix types, handle missing values, standardize format
3. **Feature Engineering** - Create ML-ready features (upcoming)
4. **Model Training** - Experiment tracking with MLflow (upcoming)
5. **Deployment** - REST API with FastAPI + Docker (upcoming)
6. **Monitoring** - Detect data drift & performance drops (upcoming)

## 📊 Dataset
- Source: [Telco Customer Churn (Kaggle)](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- 7,043 customers, 21 features
- Target: Churn (Yes/No)

## 🚀 Quick Start
```bash
# 1. Setup
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Run validation & cleaning
python src/data/data_loader.py