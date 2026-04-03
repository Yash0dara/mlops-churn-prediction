# MLOps Customer Churn Prediction

End-to-end MLOps pipeline for predicting telecom customer churn.

## 🎯 Project Goal
Predict which customers will leave so the company can take retention actions.

## 📊 Project Goal
Predict which customers will leave so the company can take retention actions.

## 🏗️ Pipeline Steps
1. **Data Validation** - Automatic quality checks before processing ✅
2. **Data Cleaning** - Fix types, handle missing values, standardize format ✅
3. **Feature Engineering** - 12 engineered features for better predictions ✅
4. **Model Training** - Experiment tracking with MLflow ✅
5. **API Backend** - REST API with FastAPI ✅
6. **Frontend** - React UI with glassmorphism design ✅
7. **Docker** - Containerized deployment ✅

## 📊 Dataset
- Source: [Telco Customer Churn (Kaggle)](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- 7,043 customers, 21 features
- Target: Churn (Yes/No)


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

## 🎨 Frontend
React UI with glassmorphism design at `http://localhost:3000`

```bash
cd frontend
npm install
npm start

## 🐳 Docker
docker build -t churn-prediction-api .
docker run -p 8000:8000 churn-prediction-api

##🛠️ Technologies
Backend: Python, FastAPI, scikit-learn, XGBoost, MLflow
Frontend: React, Material-UI, Recharts
DevOps: Docker, Git

##👤 Author
GitHub: @Yash0dara

## 🚀 How to Run
### Option 1: Run Locally

**Backend (Terminal 1):**
```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

pip install -r requirements.txt
uvicorn src.api.main:app --reload --port 8000

**Frontend (Terminal 2):**
cd frontend
npm install
npm start
# Opens at http://localhost:3000

### Option 2: Run with Docker
docker build -t churn-prediction-api .
docker run -p 8000:8000 churn-prediction-api
# API at: http://localhost:8000/docs


### Option 3: Docker Compose (Full Stack)
docker-compose up
# Backend: http://localhost:8000/docs
# Frontend: http://localhost:3000


