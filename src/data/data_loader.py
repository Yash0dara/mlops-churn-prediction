"""
Data loading and cleaning module
"""
import pandas as pd
from pathlib import Path


class DataLoader:
    """Load and clean customer churn data"""
    
    def __init__(self, raw_data_path: str):
        """
        Initialize DataLoader
        
        Args:
            raw_data_path: Path to the raw CSV file
        """
        self.raw_data_path = raw_data_path
        self.df = None
    
    def load_raw_data(self):
        """Load raw data from CSV"""
        print(f"Loading data from {self.raw_data_path}")
        self.df = pd.read_csv(self.raw_data_path)
        print(f"✅ Loaded {len(self.df)} rows and {len(self.df.columns)} columns")
        return self
    
    def clean_data(self):
        """Clean the data"""
        print("\n🧹 Cleaning data...")
        
        # 1. Fix TotalCharges data type
        print("  - Converting TotalCharges to numeric")
        self.df['TotalCharges'] = pd.to_numeric(
            self.df['TotalCharges'], 
            errors='coerce'
        )
        
        # 2. Handle missing values
        missing_count = self.df['TotalCharges'].isnull().sum()
        if missing_count > 0:
            print(f"  - Found {missing_count} missing TotalCharges values")
            print(f"  - Filling with MonthlyCharges")
            self.df['TotalCharges'].fillna(
                self.df['MonthlyCharges'], 
                inplace=True
            )
        
        # 3. Remove customerID
        if 'customerID' in self.df.columns:
            print("  - Removing customerID column")
            self.df = self.df.drop('customerID', axis=1)
        
        # 4. Convert Churn to binary (Yes=1, No=0)
        print("  - Converting Churn to binary")
        self.df['Churn'] = self.df['Churn'].map({'Yes': 1, 'No': 0})
        
        # 5. Convert SeniorCitizen to Yes/No
        print("  - Converting SeniorCitizen to Yes/No")
        self.df['SeniorCitizen'] = self.df['SeniorCitizen'].map({1: 'Yes', 0: 'No'})
        
        print("✅ Data cleaning complete!\n")
        return self
    
    def get_data_info(self):
        """Print information about the cleaned data"""
        print("=== Data Summary ===")
        print(f"Shape: {self.df.shape}")
        print(f"\nChurn distribution:")
        print(self.df['Churn'].value_counts())
        print(f"\nMissing values: {self.df.isnull().sum().sum()}")
        return self
    
    def save_cleaned_data(self, output_path: str):
        """Save cleaned data to parquet format"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        self.df.to_parquet(output_path, index=False)
        print(f"💾 Saved cleaned data to {output_path}")
        return self
    
    def get_dataframe(self):
        """Return the cleaned dataframe"""
        return self.df


if __name__ == "__main__":
    # Run this when script is executed directly
    loader = DataLoader('data/raw/churn.csv')
    loader.load_raw_data()
    loader.clean_data()
    loader.get_data_info()
    loader.save_cleaned_data('data/processed/churn_cleaned.parquet')
    print("\n✅ All done!")