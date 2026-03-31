"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class CustomerData(BaseModel):
    """Single customer input for prediction"""
    
    gender: str = Field(..., description="Male or Female")
    SeniorCitizen: str = Field(..., description="Yes or No")
    Partner: str = Field(..., description="Yes or No")
    Dependents: str = Field(..., description="Yes or No")
    tenure: int = Field(..., ge=0, le=100, description="Months with company (0-100)")
    PhoneService: str = Field(..., description="Yes or No")
    MultipleLines: str = Field(..., description="Yes, No, or No phone service")
    InternetService: str = Field(..., description="DSL, Fiber optic, or No")
    OnlineSecurity: str = Field(..., description="Yes, No, or No internet service")
    OnlineBackup: str = Field(..., description="Yes, No, or No internet service")
    DeviceProtection: str = Field(..., description="Yes, No, or No internet service")
    TechSupport: str = Field(..., description="Yes, No, or No internet service")
    StreamingTV: str = Field(..., description="Yes, No, or No internet service")
    StreamingMovies: str = Field(..., description="Yes, No, or No internet service")
    Contract: str = Field(..., description="Month-to-month, One year, or Two year")
    PaperlessBilling: str = Field(..., description="Yes or No")
    PaymentMethod: str = Field(..., description="Payment method type")
    MonthlyCharges: float = Field(..., ge=0, description="Monthly charges in dollars")
    TotalCharges: float = Field(..., ge=0, description="Total charges in dollars")
    
    class Config:
        schema_extra = {
            "example": {
                "gender": "Female",
                "SeniorCitizen": "No",
                "Partner": "Yes",
                "Dependents": "No",
                "tenure": 24,
                "PhoneService": "Yes",
                "MultipleLines": "No",
                "InternetService": "Fiber optic",
                "OnlineSecurity": "No",
                "OnlineBackup": "Yes",
                "DeviceProtection": "No",
                "TechSupport": "No",
                "StreamingTV": "Yes",
                "StreamingMovies": "Yes",
                "Contract": "Month-to-month",
                "PaperlessBilling": "Yes",
                "PaymentMethod": "Electronic check",
                "MonthlyCharges": 89.85,
                "TotalCharges": 2156.40
            }
        }


class PredictionResponse(BaseModel):
    """Prediction output"""
    
    will_churn: str = Field(..., description="Yes or No")
    churn_probability: float = Field(..., description="Probability of churn (0-1)")
    confidence: str = Field(..., description="Low, Medium, or High")
    recommendation: str = Field(..., description="Action recommendation")


class BatchPredictionRequest(BaseModel):
    """Multiple customers for batch prediction"""
    customers: List[CustomerData]


class BatchPredictionResponse(BaseModel):
    """Batch prediction output"""
    predictions: List[PredictionResponse]
    total_customers: int
    predicted_to_churn: int


class ModelInfo(BaseModel):
    """Model metadata"""
    model_name: str
    model_version: str
    f1_score: float
    precision: float
    recall: float
    roc_auc: float