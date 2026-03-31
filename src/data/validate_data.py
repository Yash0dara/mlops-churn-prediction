"""
Data validation using pandas (custom validation)
"""
import pandas as pd
from pathlib import Path


class DataValidator:
    """Validate data quality before processing"""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.errors = []
    
    def load_data(self):
        """Load data for validation"""
        print(f"📂 Loading data from {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        print(f"✅ Loaded {len(self.df)} rows, {len(self.df.columns)} columns\n")
        return self
    
    def validate(self):
        """Run all validation checks"""
        print("🔍 Starting data validation...\n")
        
        # Reset errors
        self.errors = []
        
        # 1. Check required columns exist
        print("  ✓ Checking required columns exist...")
        required_columns = ['customerID', 'Churn', 'tenure', 'MonthlyCharges', 'TotalCharges']
        for col in required_columns:
            if col not in self.df.columns:
                self.errors.append(f"Missing required column: {col}")
        
        # Only continue other checks if required columns exist
        if len(self.errors) > 0:
            print("    ⚠️ Missing columns detected - skipping other checks")
            return self
        
        # 2. Check for missing values in critical columns
        print("  ✓ Checking for missing values in critical columns...")
        for col in ['customerID', 'Churn']:
            if col in self.df.columns:
                if self.df[col].isnull().sum() > 0:
                    self.errors.append(f"Column {col} has {self.df[col].isnull().sum()} missing values")
        
        # 3. Check Churn values are valid
        print("  ✓ Validating Churn values...")
        if 'Churn' in self.df.columns:
            valid_churn = ['Yes', 'No']
            invalid_churn = self.df[~self.df['Churn'].isin(valid_churn)]['Churn'].unique()
            if len(invalid_churn) > 0:
                self.errors.append(f"Invalid Churn values found: {invalid_churn}")
        
        # 4. Check numeric ranges
        print("  ✓ Checking numeric value ranges...")
        if 'tenure' in self.df.columns:
            if (self.df['tenure'] < 0).any() or (self.df['tenure'] > 100).any():
                self.errors.append("tenure has values outside 0-100 range")
        
        if 'MonthlyCharges' in self.df.columns:
            if (self.df['MonthlyCharges'] < 0).any():
                self.errors.append("MonthlyCharges has negative values")
        
        # 5. Check categorical values
        print("  ✓ Validating categorical columns...")
        if 'Contract' in self.df.columns:
            valid_contracts = ['Month-to-month', 'One year', 'Two year']
            invalid_contracts = self.df[~self.df['Contract'].isin(valid_contracts)]['Contract'].unique()
            if len(invalid_contracts) > 0:
                self.errors.append(f"Invalid Contract values: {invalid_contracts}")
        
        # 6. Check row count
        print("  ✓ Checking dataset size...")
        if len(self.df) < 1000 or len(self.df) > 10000:
            self.errors.append(f"Row count {len(self.df)} is outside expected range (1000-10000)")
        
        return self
    
    def show_results(self):
        """Display validation results"""
        print("\n" + "="*60)
        print("VALIDATION RESULTS")
        print("="*60)
        
        if len(self.errors) == 0:
            print("✅ ALL CHECKS PASSED!")
            print(f"\nTotal rows: {len(self.df)}")
            print(f"Total columns: {len(self.df.columns)}")
            print("\n🎉 Data quality is good! Safe to proceed.")
            return True
        else:
            print("❌ VALIDATION FAILED!")
            print(f"\nFound {len(self.errors)} issues:")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")
            print("\n🛑 DO NOT PROCEED - Fix data issues first!")
            return False
    
    def save_report(self, output_path: str = 'monitoring/validation_report.html'):
        """Save validation report as HTML"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        status = "PASSED" if len(self.errors) == 0 else "FAILED"
        
        html_content = f"""
        <html>
        <head><title>Data Validation Report</title></head>
        <body>
            <h1>Data Validation Report</h1>
            <h2>Status: {'✅ ' + status if status == "PASSED" else '❌ ' + status}</h2>
            <p>Total Rows: {len(self.df)}</p>
            <p>Total Columns: {len(self.df.columns)}</p>
            <h3>Issues Found: {len(self.errors)}</h3>
            <ul>
                {''.join([f'<li>{e}</li>' for e in self.errors]) if self.errors else '<li>None - All checks passed!</li>'}
            </ul>
        </body>
        </html>
        """
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n📄 Validation report saved to: {output_path}")
        return self


if __name__ == "__main__":
    validator = DataValidator('data/raw/churn.csv')
    validator.load_data()
    validator.validate()
    is_valid = validator.show_results()
    validator.save_report()
    
    if not is_valid:
        print("\n❌ Exiting due to validation failures")
        exit(1)
    else:
        print("\n✅ Validation complete - data is ready!")
        exit(0)