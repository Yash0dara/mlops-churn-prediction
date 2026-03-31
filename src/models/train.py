"""
Model training with MLflow experiment tracking
"""
from sklearn.pipeline import Pipeline
from pathlib import Path
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
)
import joblib

import sys
sys.path.append('src')
from features.feature_engineering import FeatureEngineer


class ModelTrainer:
    """Train churn prediction models and log with MLflow"""
    
    def __init__(self, config_path='configs/config.yaml'):
        """Initialize trainer with config"""
        import yaml
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        mlflow.set_tracking_uri(self.config['mlflow']['tracking_uri'])
        experiment = mlflow.set_experiment(self.config['mlflow']['experiment_name'])
        self.experiment_id = experiment.experiment_id
        
        self.fe = FeatureEngineer(config_path)
        self.models = []
        self.best_model = None
        self.best_metrics = None
    
    def prepare_data(self):
        """Load, engineer features, split data"""
        print("📊 Preparing data for modeling...")
        df = pd.read_parquet('data/processed/churn_cleaned.parquet')
        df_engineered = self.fe.create_features(df)
        self.fe.build_preprocessor()
        X, y = self.fe.fit_transform(df_engineered, target_col='Churn')
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y,
            test_size=self.config['model']['test_size'],
            random_state=self.config['model']['random_state'],
            stratify=y
        )
        print(f"Train shape: {self.X_train.shape} | Test shape: {self.X_test.shape}")
        return self
    
    def evaluate(self, y_true, y_pred, y_prob=None, name='model'):
        """Compute classification metrics"""
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred),
            'recall': recall_score(y_true, y_pred),
            'f1': f1_score(y_true, y_pred),
            'roc_auc': roc_auc_score(y_true, y_prob) if y_prob is not None else np.nan
        }
        print(f"\n📈 Metrics for {name}:")
        for k, v in metrics.items():
            print(f"  {k:>8}: {v:.4f}")
        return metrics
    
    def train_single(self, model, name, params, use_proba=True):
        """Train one model, log with MLflow"""
        with mlflow.start_run(run_name=name):
            mlflow.log_param('model', name)
            mlflow.log_params(params)
            
            model.fit(self.X_train, self.y_train)
            y_pred = model.predict(self.X_test)
            y_prob = model.predict_proba(self.X_test)[:, 1] if use_proba else None
            
            metrics = self.evaluate(self.y_test, y_pred, y_prob, name=name)
            mlflow.log_metrics(metrics)
            
            # Log pipeline + model together for serving
            full_pipeline = Pipeline([
                ('preprocessor', self.fe.preprocessor),
                ('classifier', model)
            ])
            mlflow.sklearn.log_model(full_pipeline, artifact_path='model')
            
            print(f"✅ Logged run: {name} / F1: {metrics['f1']:.4f}")
            
            # Keep track of best
            if self.best_metrics is None or metrics['f1'] > self.best_metrics['f1']:
                self.best_model = full_pipeline
                self.best_metrics = metrics
                self.best_name = name
    
    def run_experiments(self):
        """Compare multiple models"""
        print("\n🤖 Training models and tracking with MLflow...")
        
        models_to_try = [
            ('RandomForest', RandomForestClassifier(random_state=42), {'n_estimators': 200, 'max_depth': 10}),
            ('RandomForest_deeper', RandomForestClassifier(random_state=42), {'n_estimators': 300, 'max_depth': 15}),
            ('VotingEnsemble', VotingClassifier(
                estimators=[
                    ('rf1', RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)),
                    ('rf2', RandomForestClassifier(n_estimators=300, max_depth=15, random_state=42)),
                ], voting='soft'), {}),
        ]
        
        for name, model, params in models_to_try:
            self.train_single(model, name, params)
        
        print(f"\n🏆 Best model: {self.best_name} | F1: {self.best_metrics['f1']:.4f}")
        
        # Save locally (backup)
        Path('models').mkdir(exist_ok=True)
        joblib.dump(self.best_model, 'models/best_model_full_pipeline.pkl')
        print("💾 Best model saved to models/best_model_full_pipeline.pkl")
        
        # Register best model in MLflow Model Registry (simple path)
        with mlflow.start_run(run_name=f"register_{self.best_name}"):
            mlflow.sklearn.log_model(
                self.best_model,
                artifact_path='model',
                registered_model_name='churn-predictor'
            )
        print("📦 Model registered with MLflow as 'churn-predictor'")
        return self.best_model


if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.prepare_data()
    best = trainer.run_experiments()