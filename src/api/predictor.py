"""
Model loading and prediction logic
"""
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from features.feature_engineering import FeatureEngineer


class ChurnPredictor:
    """Load model and make predictions"""
    
    def __init__(self, model_path='models/best_model_optimized.pkl'):
        """Load the trained model"""
        print(f"Loading model from {model_path}...")
        
        model_data = joblib.load(model_path)
        
        if isinstance(model_data, dict):
            self.full_pipeline = model_data['pipeline']
            self.threshold = model_data.get('threshold', 0.5)
        else:
            self.full_pipeline = model_data
            self.threshold = 0.5
        
        # Initialize feature engineer to transform input
        self.fe = FeatureEngineer()
        self.fe.build_preprocessor()
        
        print(f"✅ Model loaded! Threshold: {self.threshold}")
        
        self.model_info = {
            'model_name': 'Tuned XGBoost',
            'model_version': 'v3.0',
            'f1_score': 0.6305,
            'precision': 0.7914,
            'recall': 0.5239,
            'roc_auc': 0.8378
        }
    
    def predict_single(self, customer_data: dict) -> dict:
        """Predict for one customer"""
        # Convert to DataFrame
        df = pd.DataFrame([customer_data])
        
        # Add dummy Churn column (needed for feature engineering)
        df['Churn'] = 0
        
        # Apply feature engineering
        df_engineered = self.fe.create_features(df)
        
        # Use the FULL pipeline (preprocessor + model)
        # The pipeline handles: feature engineering → preprocessing → prediction
        proba = self.full_pipeline.predict_proba(df_engineered)[0, 1]
        
        # Apply threshold
        prediction = 1 if proba >= self.threshold else 0
        
        # Determine confidence
        if proba > 0.7 or proba < 0.3:
            confidence = "High"
        elif proba > 0.6 or proba < 0.4:
            confidence = "Medium"
        else:
            confidence = "Low"
        
        # Generate recommendation
        if prediction == 1:
            if proba > 0.75:
                recommendation = "High risk - immediate retention offer recommended"
            elif proba > 0.6:
                recommendation = "Moderate risk - consider proactive outreach"
            else:
                recommendation = "Low-moderate risk - monitor closely"
        else:
            recommendation = "Low risk - no immediate action needed"
        
        return {
            'will_churn': 'Yes' if prediction == 1 else 'No',
            'churn_probability': round(float(proba), 4),
            'confidence': confidence,
            'recommendation': recommendation
        }
    
    def predict_batch(self, customers: list) -> list:
        """Predict for multiple customers"""
        predictions = []
        for customer in customers:
            pred = self.predict_single(customer.dict())
            predictions.append(pred)
        return predictions
    
    def get_model_info(self) -> dict:
        """Return model metadata"""
        return self.model_info


predictor = None

def get_predictor():
    """Get or create predictor instance"""
    global predictor
    if predictor is None:
        predictor = ChurnPredictor()
    return predictor