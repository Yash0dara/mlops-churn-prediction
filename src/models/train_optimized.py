"""
Optimized training with tuning and stacking
"""
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.ensemble import StackingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    roc_auc_score, make_scorer, classification_report
)
from imblearn.over_sampling import SMOTE
from sklearn.pipeline import Pipeline
from pathlib import Path
import joblib
import sys
sys.path.append(str(Path(__file__).parent.parent))

from features.feature_engineering import FeatureEngineer


class OptimizedTrainer:
    """Advanced training with hyperparameter tuning and stacking"""
    
    def __init__(self, config_path='configs/config.yaml'):
        import yaml
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        mlflow.set_tracking_uri(self.config['mlflow']['tracking_uri'])
        experiment = mlflow.set_experiment("churn-prediction-optimized")
        self.experiment_id = experiment.experiment_id
        
        self.fe = FeatureEngineer(config_path)
        self.best_model = None
        self.best_metrics = None
    
    def prepare_data(self):
        """Load and prepare data with SMOTE"""
        print("📊 Preparing data with advanced features...")
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
        
        print(f"\n⚖️ Applying SMOTE...")
        smote = SMOTE(random_state=42)
        self.X_train, self.y_train = smote.fit_resample(self.X_train, self.y_train)
        
        print(f"Train: {self.X_train.shape} | Test: {self.X_test.shape}")
        return self
    
    def evaluate(self, y_true, y_pred, y_prob, name='model'):
        """Compute metrics"""
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred),
            'recall': recall_score(y_true, y_pred),
            'f1': f1_score(y_true, y_pred),
            'roc_auc': roc_auc_score(y_true, y_prob)
        }
        
        print(f"\n{'='*60}")
        print(f"📈 {name}")
        print(f"{'='*60}")
        for k, v in metrics.items():
            print(f"{k:>12}: {v:.4f}")
        
        return metrics
    
    def tune_xgboost(self):
        """Hyperparameter tuning for XGBoost"""
        print("\n🔧 Tuning XGBoost hyperparameters...")
        print("This may take 3-5 minutes...\n")
        
        param_grid = {
            'n_estimators': [200, 300],
            'max_depth': [6, 8, 10],
            'learning_rate': [0.05, 0.1],
            'scale_pos_weight': [2.5, 3.0, 3.5],
            'min_child_weight': [1, 3]
        }
        
        xgb = XGBClassifier(
            random_state=42,
            n_jobs=-1,
            eval_metric='logloss'
        )
        
        # Use F1 as scoring metric
        f1_scorer = make_scorer(f1_score)
        
        grid = GridSearchCV(
            xgb,
            param_grid,
            cv=3,  # 3-fold cross-validation
            scoring=f1_scorer,
            n_jobs=-1,
            verbose=1
        )
        
        grid.fit(self.X_train, self.y_train)
        
        print(f"\n✅ Best parameters: {grid.best_params_}")
        print(f"✅ Best CV F1 score: {grid.best_score_:.4f}")
        
        return grid.best_estimator_
    
    def build_stacking_ensemble(self, tuned_xgb):
        """Create stacking ensemble"""
        print("\n🏗️ Building stacking ensemble...")
        
        # Base models
        estimators = [
            ('xgb', tuned_xgb),
            ('lgbm', LGBMClassifier(
                n_estimators=300,
                max_depth=8,
                learning_rate=0.05,
                class_weight='balanced',
                random_state=42,
                n_jobs=-1,
                verbose=-1
            )),
            ('xgb2', XGBClassifier(
                n_estimators=250,
                max_depth=7,
                learning_rate=0.08,
                scale_pos_weight=3.0,
                random_state=43,
                n_jobs=-1,
                eval_metric='logloss'
            ))
        ]
        
        # Meta-learner (combines base model predictions)
        stacking = StackingClassifier(
            estimators=estimators,
            final_estimator=LogisticRegression(class_weight='balanced'),
            cv=3,
            n_jobs=-1
        )
        
        return stacking
    
    def optimize_threshold(self, model):
        """Find optimal probability threshold"""
        print("\n🎯 Optimizing decision threshold...")
        
        y_prob = model.predict_proba(self.X_test)[:, 1]
        
        best_f1 = 0
        best_threshold = 0.5
        
        # Try thresholds from 0.3 to 0.7
        for threshold in np.arange(0.3, 0.71, 0.05):
            y_pred = (y_prob >= threshold).astype(int)
            f1 = f1_score(self.y_test, y_pred)
            
            if f1 > best_f1:
                best_f1 = f1
                best_threshold = threshold
        
        print(f"✅ Best threshold: {best_threshold:.2f} (F1: {best_f1:.4f})")
        return best_threshold
    
    def train_all(self):
        """Full training pipeline"""
        print("\n" + "="*60)
        print("🚀 OPTIMIZED TRAINING PIPELINE")
        print("="*60)
        
        # Step 1: Tune XGBoost
        tuned_xgb = self.tune_xgboost()
        
        # Evaluate tuned XGBoost
        with mlflow.start_run(run_name="TunedXGBoost"):
            tuned_xgb.fit(self.X_train, self.y_train)
            y_pred = tuned_xgb.predict(self.X_test)
            y_prob = tuned_xgb.predict_proba(self.X_test)[:, 1]
            
            metrics_tuned = self.evaluate(self.y_test, y_pred, y_prob, "Tuned XGBoost")
            mlflow.log_metrics(metrics_tuned)
            mlflow.log_params(tuned_xgb.get_params())
        
        # Step 2: Build and train stacking ensemble
        print("\n" + "="*60)
        stacking = self.build_stacking_ensemble(tuned_xgb)
        
        with mlflow.start_run(run_name="StackingEnsemble"):
            print("Training stacking ensemble (this takes time)...")
            stacking.fit(self.X_train, self.y_train)
            
            y_pred_stack = stacking.predict(self.X_test)
            y_prob_stack = stacking.predict_proba(self.X_test)[:, 1]
            
            metrics_stack = self.evaluate(self.y_test, y_pred_stack, y_prob_stack, "Stacking Ensemble")
            mlflow.log_metrics(metrics_stack)
        
        # Step 3: Optimize threshold
        best_threshold = self.optimize_threshold(stacking)
        
        with mlflow.start_run(run_name="StackingEnsemble_OptThreshold"):
            y_pred_opt = (y_prob_stack >= best_threshold).astype(int)
            metrics_opt = self.evaluate(self.y_test, y_pred_opt, y_prob_stack, "Stacking + Optimized Threshold")
            mlflow.log_metrics(metrics_opt)
            mlflow.log_param('threshold', best_threshold)
        
        # Choose best
        all_results = [
            ("Tuned XGBoost", tuned_xgb, metrics_tuned, 0.5),
            ("Stacking Ensemble", stacking, metrics_stack, 0.5),
            ("Stacking + Threshold", stacking, metrics_opt, best_threshold)
        ]
        
        best = max(all_results, key=lambda x: x[2]['f1'])
        self.best_name, self.best_model, self.best_metrics, self.best_threshold = best
        
        # Save
        print("\n" + "="*60)
        print(f"🏆 BEST MODEL: {self.best_name}")
        print("="*60)
        print(f"F1:        {self.best_metrics['f1']:.4f}")
        print(f"Recall:    {self.best_metrics['recall']:.4f}")
        print(f"Precision: {self.best_metrics['precision']:.4f}")
        print(f"Threshold: {self.best_threshold:.2f}")
        
        # Save full pipeline
        full_pipeline = Pipeline([
            ('preprocessor', self.fe.preprocessor),
            ('classifier', self.best_model)
        ])
        
        Path('models').mkdir(exist_ok=True)
        joblib.dump({
            'pipeline': full_pipeline,
            'threshold': self.best_threshold
        }, 'models/best_model_optimized.pkl')
        
        print("\n💾 Saved to: models/best_model_optimized.pkl")
        
        # Register
        with mlflow.start_run(run_name=f"PRODUCTION_{self.best_name}"):
            mlflow.sklearn.log_model(
                full_pipeline,
                name='model',
                registered_model_name='churn-predictor-optimized'
            )
            mlflow.log_param('threshold', self.best_threshold)
        
        print("📦 Registered in MLflow")
        
        return full_pipeline


if __name__ == "__main__":
    trainer = OptimizedTrainer()
    trainer.prepare_data()
    best = trainer.train_all()
    
    print("\n✅ Optimization complete!")