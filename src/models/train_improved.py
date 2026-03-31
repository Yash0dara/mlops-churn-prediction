"""
Improved model training with class balancing and advanced algorithms
"""
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    roc_auc_score, classification_report, confusion_matrix
)
from imblearn.over_sampling import SMOTE
from sklearn.pipeline import Pipeline
from pathlib import Path
import joblib
import sys
sys.path.append(str(Path(__file__).parent.parent))

from features.feature_engineering import FeatureEngineer


class ImprovedModelTrainer:
    """Train improved churn models with class balancing"""
    
    def __init__(self, config_path='configs/config.yaml'):
        import yaml
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        mlflow.set_tracking_uri(self.config['mlflow']['tracking_uri'])
        experiment = mlflow.set_experiment("churn-prediction-improved")
        self.experiment_id = experiment.experiment_id
        
        self.fe = FeatureEngineer(config_path)
        self.best_model = None
        self.best_metrics = None
        self.best_name = None
    
    def prepare_data(self, use_smote=True):
        """Load, engineer, and balance data"""
        print("📊 Preparing data...")
        df = pd.read_parquet('data/processed/churn_cleaned.parquet')
        df_engineered = self.fe.create_features(df)
        self.fe.build_preprocessor()
        X, y = self.fe.fit_transform(df_engineered, target_col='Churn')
        
        # Split first
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y,
            test_size=self.config['model']['test_size'],
            random_state=self.config['model']['random_state'],
            stratify=y
        )
        
        # Apply SMOTE only to training data
        if use_smote:
            print("\n⚖️ Applying SMOTE to balance classes...")
            print(f"Before SMOTE: {self.y_train.value_counts().to_dict()}")
            smote = SMOTE(random_state=42)
            self.X_train, self.y_train = smote.fit_resample(self.X_train, self.y_train)
            print(f"After SMOTE:  {pd.Series(self.y_train).value_counts().to_dict()}")
        
        print(f"\nTrain: {self.X_train.shape} | Test: {self.X_test.shape}")
        return self
    
    def evaluate(self, y_true, y_pred, y_prob, name='model'):
        """Detailed evaluation"""
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred),
            'recall': recall_score(y_true, y_pred),
            'f1': f1_score(y_true, y_pred),
            'roc_auc': roc_auc_score(y_true, y_prob)
        }
        
        print(f"\n{'='*60}")
        print(f"📈 {name} Results")
        print(f"{'='*60}")
        for k, v in metrics.items():
            print(f"{k:>12}: {v:.4f}")
        
        print("\nConfusion Matrix:")
        cm = confusion_matrix(y_true, y_pred)
        print(f"              Predicted")
        print(f"              0      1")
        print(f"Actual  0   {cm[0,0]:>4}   {cm[0,1]:>4}")
        print(f"        1   {cm[1,0]:>4}   {cm[1,1]:>4}")
        
        # Business interpretation
        total_churners = cm[1,0] + cm[1,1]
        caught_churners = cm[1,1]
        print(f"\n💼 Business Impact:")
        print(f"   Caught {caught_churners}/{total_churners} churners ({metrics['recall']*100:.1f}%)")
        print(f"   Missed {cm[1,0]} churners (they will leave!)")
        print(f"   {cm[0,1]} false alarms (wasted effort)")
        
        return metrics
    
    def train_single(self, model, name, params):
        """Train one model with MLflow tracking"""
        with mlflow.start_run(run_name=name):
            mlflow.log_param('model_type', name)
            mlflow.log_params(params)
            
            # Train
            model.fit(self.X_train, self.y_train)
            
            # Predict
            y_pred = model.predict(self.X_test)
            y_prob = model.predict_proba(self.X_test)[:, 1]
            
            # Evaluate
            metrics = self.evaluate(self.y_test, y_pred, y_prob, name)
            mlflow.log_metrics(metrics)
            
            # Save full pipeline
            full_pipeline = Pipeline([
                ('preprocessor', self.fe.preprocessor),
                ('classifier', model)
            ])
            mlflow.sklearn.log_model(full_pipeline, name='model')
            
            # Track best
            if self.best_metrics is None or metrics['f1'] > self.best_metrics['f1']:
                self.best_model = full_pipeline
                self.best_metrics = metrics
                self.best_name = name
            
            print(f"\n✅ Logged to MLflow: {name}")
    
    def run_experiments(self):
        """Compare improved models"""
        print("\n" + "="*60)
        print("🚀 TRAINING IMPROVED MODELS")
        print("="*60)
        
        models = [
            # Baseline with class weight
            (
                'RandomForest_Balanced',
                RandomForestClassifier(
                    n_estimators=200,
                    max_depth=15,
                    class_weight='balanced',
                    random_state=42,
                    n_jobs=-1
                ),
                {'n_estimators': 200, 'max_depth': 15, 'class_weight': 'balanced'}
            ),
            
            # XGBoost (often best for tabular data)
            (
                'XGBoost',
                XGBClassifier(
                    n_estimators=200,
                    max_depth=6,
                    learning_rate=0.1,
                    scale_pos_weight=2.77,  # Ratio of negative/positive
                    random_state=42,
                    n_jobs=-1,
                    eval_metric='logloss'
                ),
                {'n_estimators': 200, 'max_depth': 6, 'learning_rate': 0.1}
            ),
            
            # LightGBM (fast and powerful)
            (
                'LightGBM',
                LGBMClassifier(
                    n_estimators=200,
                    max_depth=8,
                    learning_rate=0.1,
                    class_weight='balanced',
                    random_state=42,
                    n_jobs=-1,
                    verbose=-1
                ),
                {'n_estimators': 200, 'max_depth': 8, 'learning_rate': 0.1}
            ),
            
            # XGBoost tuned for recall
            (
                'XGBoost_HighRecall',
                XGBClassifier(
                    n_estimators=300,
                    max_depth=8,
                    learning_rate=0.05,
                    scale_pos_weight=3.5,  # Higher = more focus on minority class
                    min_child_weight=1,
                    random_state=42,
                    n_jobs=-1,
                    eval_metric='logloss'
                ),
                {'n_estimators': 300, 'max_depth': 8, 'scale_pos_weight': 3.5}
            ),
        ]
        
        for name, model, params in models:
            self.train_single(model, name, params)
        
        print("\n" + "="*60)
        print(f"🏆 BEST MODEL: {self.best_name}")
        print("="*60)
        print(f"F1 Score:  {self.best_metrics['f1']:.4f}")
        print(f"Recall:    {self.best_metrics['recall']:.4f}")
        print(f"Precision: {self.best_metrics['precision']:.4f}")
        print(f"ROC AUC:   {self.best_metrics['roc_auc']:.4f}")
        
        # Save best model
        Path('models').mkdir(exist_ok=True)
        joblib.dump(self.best_model, 'models/best_model_improved.pkl')
        print(f"\n💾 Saved to: models/best_model_improved.pkl")
        
        # Register in MLflow
        with mlflow.start_run(run_name=f"PRODUCTION_{self.best_name}"):
            mlflow.sklearn.log_model(
                self.best_model,
                name='model',
                registered_model_name='churn-predictor-improved'
            )
        print("📦 Registered in MLflow as 'churn-predictor-improved'")
        
        return self.best_model


if __name__ == "__main__":
    trainer = ImprovedModelTrainer()
    trainer.prepare_data(use_smote=True)  # Try with SMOTE
    best = trainer.run_experiments()
    
    print("\n" + "="*60)
    print("✅ TRAINING COMPLETE!")
    print("="*60)
    print("\nTo view results:")
    print("1. Run: mlflow ui")
    print("2. Open: http://localhost:5000")
    print("3. Compare 'churn-prediction-improved' experiment")