"""
Feature engineering and preprocessing pipeline
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import yaml
from pathlib import Path


class FeatureEngineer:
    """Transform data into ML-ready features"""
    
    def __init__(self, config_path='configs/config.yaml'):
        """Load configuration"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.preprocessor = None
        self.feature_names = None
    
    def create_features(self, df):
        """Engineer advanced features"""
        print("🔧 Creating advanced features...")
        
        df = df.copy()
        
        # Original features
        print("  - Tenure groups")
        df['tenure_group'] = pd.cut(
            df['tenure'], 
            bins=[0, 12, 24, 48, 72],
            labels=['0-1yr', '1-2yr', '2-4yr', '4yr+']
        )
        
        print("  - Average monthly charges")
        df['avg_monthly_charges'] = df['TotalCharges'] / (df['tenure'] + 1)
        
        print("  - Has multiple services")
        df['has_multiple_services'] = (
            (df['PhoneService'] == 'Yes') & 
            (df['InternetService'] != 'No')
        ).astype(int)
        
        # NEW: Advanced interaction features
        print("  - Contract × Payment interaction")
        df['contract_payment'] = df['Contract'].astype(str) + '_' + df['PaymentMethod'].astype(str)
        
        print("  - Service bundle score")
        # Count how many services customer has
        service_cols = ['PhoneService', 'MultipleLines', 'InternetService', 
                        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                        'TechSupport', 'StreamingTV', 'StreamingMovies']
        df['service_count'] = sum([
            (df[col] == 'Yes').astype(int) for col in service_cols if col in df.columns
        ])
        
        print("  - Monthly charges per service")
        df['charges_per_service'] = df['MonthlyCharges'] / (df['service_count'] + 1)
        
        print("  - Tenure squared (non-linear relationship)")
        df['tenure_squared'] = df['tenure'] ** 2
        
        print("  - Is new customer (< 6 months)")
        df['is_new_customer'] = (df['tenure'] < 6).astype(int)
        
        print("  - Is long-term customer (> 48 months)")
        df['is_loyal_customer'] = (df['tenure'] > 48).astype(int)
        
        print("  - Monthly charges bin")
        df['charges_bin'] = pd.cut(
            df['MonthlyCharges'],
            bins=[0, 35, 70, 200],
            labels=['low', 'medium', 'high']
        )
        
        print("  - High value customer (top 25% spend)")
        df['is_high_value'] = (df['MonthlyCharges'] > df['MonthlyCharges'].quantile(0.75)).astype(int)
        
        # Interaction: Contract type + Internet service
        print("  - Contract × Internet interaction")
        df['contract_internet'] = df['Contract'].astype(str) + '_' + df['InternetService'].astype(str)
        
        print(f"✅ Created {df.shape[1] - 20} new features (total: {df.shape[1]})")
        return df
    
    def build_preprocessor(self):
        """Build sklearn preprocessing pipeline"""
        print("\n🏗️ Building preprocessing pipeline...")
        
        numeric_features = self.config['features']['numeric'].copy()
        categorical_features = self.config['features']['categorical'].copy()
        
        # Add engineered numeric features
        numeric_features.extend([
            'avg_monthly_charges',
            'service_count',
            'charges_per_service',
            'tenure_squared',
            'is_new_customer',
            'is_loyal_customer',
            'is_high_value'
        ])
        
        # Add engineered categorical features
        categorical_features.extend([
            'tenure_group',
            'has_multiple_services',
            'contract_payment',
            'charges_bin',
            'contract_internet'
        ])
        
        print(f"  - Numeric features: {len(numeric_features)}")
        print(f"  - Categorical features: {len(categorical_features)}")
        
        numeric_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])
        
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(drop='first', handle_unknown='ignore'))
        ])
        
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ],
            remainder='drop'
        )
        
        print("✅ Pipeline built!")
        return self
    
    def fit_transform(self, df, target_col='Churn'):
        """Fit pipeline and transform data"""
        print("\n🔄 Fitting and transforming data...")
        
        # Separate features and target
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        # Fit and transform
        X_transformed = self.preprocessor.fit_transform(X)
        
        # Get feature names after transformation
        self._extract_feature_names()
        
        print(f"✅ Transformed shape: {X_transformed.shape}")
        print(f"   Original features: {X.shape[1]}")
        print(f"   After encoding: {X_transformed.shape[1]}")
        
        return X_transformed, y
    
    def transform(self, df, target_col='Churn'):
        """Transform new data using fitted pipeline"""
        X = df.drop(columns=[target_col])
        X_transformed = self.preprocessor.transform(X)
        y = df[target_col]
        return X_transformed, y
    
    def _extract_feature_names(self):
        """Extract feature names after transformation"""
        feature_names = []
        
        for name, transformer, features in self.preprocessor.transformers_:
            if name == 'num':
                feature_names.extend(features)
            elif name == 'cat':
                # Get categories from OneHotEncoder
                onehot = transformer.named_steps['onehot']
                for i, feature in enumerate(features):
                    categories = onehot.categories_[i][1:]  # Skip first (dropped)
                    feature_names.extend([f"{feature}_{cat}" for cat in categories])
        
        self.feature_names = feature_names
    
    def save_pipeline(self, output_path='models/preprocessor.pkl'):
        """Save fitted pipeline"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.preprocessor, output_path)
        print(f"\n💾 Pipeline saved to {output_path}")
    
    def load_pipeline(self, path='models/preprocessor.pkl'):
        """Load pre-fitted pipeline"""
        self.preprocessor = joblib.load(path)
        print(f"📂 Pipeline loaded from {path}")
        return self


if __name__ == "__main__":
    print("="*60)
    print("FEATURE ENGINEERING PIPELINE")
    print("="*60)
    
    # Load cleaned data
    df = pd.read_parquet('data/processed/churn_cleaned.parquet')
    print(f"\n✅ Loaded data: {df.shape}")
    
    # Initialize feature engineer
    fe = FeatureEngineer()
    
    # Create new features
    df_engineered = fe.create_features(df)
    
    # Build preprocessing pipeline
    fe.build_preprocessor()
    
    # Fit and transform
    X_transformed, y = fe.fit_transform(df_engineered, target_col='Churn')
    
    # Save pipeline
    fe.save_pipeline()
    
    # Show sample
    print("\n📊 Sample of transformed data:")
    print(f"Features shape: {X_transformed.shape}")
    print(f"Target shape: {y.shape}")
    print(f"Target distribution:\n{y.value_counts()}")
    
    print("\n✅ Feature engineering complete!")