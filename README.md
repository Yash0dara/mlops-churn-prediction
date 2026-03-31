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

## 🏆 Model Performance

### Production Model: Tuned XGBoost
- **F1 Score:** 0.6305
- **Precision:** 79% (only 21% false alarms)
- **Recall:** 52% (catches half of churners)
- **ROC AUC:** 0.838

### Development Journey
| Version | Model | F1 | Key Innovation |
|---------|-------|----|----|
| v1.0 | Random Forest | 0.575 | Baseline ensemble |
| v2.0 | XGBoost + SMOTE | 0.614 | Class balancing |
| v3.0 | Tuned XGBoost | **0.630** | Feature engineering + tuning |

**Total Improvement:** +9.7% F1, +14% Precision

### Business Impact
- Reduced false retention offers by 48%
- Maintains 52% churn detection rate
- Estimated savings: $X per month in wasted discounts

### Techniques Applied
✅ SMOTE for class imbalance
✅ 12 engineered features (interactions, ratios, segments)
✅ GridSearchCV hyperparameter tuning (96 combinations)
✅ XGBoost gradient boosting
✅ 3-fold cross-validation
✅ MLflow experiment tracking