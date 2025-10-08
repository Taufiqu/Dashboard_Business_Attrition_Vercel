"""
Prediction script untuk model attrition
"""

import sys
import json
import pandas as pd
import numpy as np
from pathlib import Path

# Add parent directory to path
sys.path.append('..')

try:
    from utils.model_util import MLflowModelManager, quick_load_model
    from config.mlflow_config import DEFAULT_MODEL_NAME
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class AttritionPredictor:
    def __init__(self, model_path=None, model_name=None):
        """
        Initialize predictor
        
        Args:
            model_path (str): Path to local model (optional)
            model_name (str): Name of model to download from MLflow (optional)
        """
        self.model = None
        self.model_metadata = None
        
        if model_path:
            self.load_local_model(model_path)
        elif model_name:
            self.download_and_load_model(model_name)
        else:
            self.load_latest_local_model()
    
    def load_local_model(self, model_path):
        """Load model from local path"""
        try:
            self.model, self.model_metadata = quick_load_model(model_path)
            print(f"✅ Model loaded from: {model_path}")
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            raise
    
    def download_and_load_model(self, model_name):
        """Download model from MLflow and load"""
        try:
            manager = MLflowModelManager()
            metadata = manager.download_model(model_name)
            self.load_local_model(metadata['local_path'])
        except Exception as e:
            print(f"❌ Failed to download model: {e}")
            raise
    
    def load_latest_local_model(self):
        """Load the latest local model"""
        try:
            manager = MLflowModelManager()
            local_models = manager.list_local_models()
            
            if not local_models:
                # Try to download default model
                print(f"📥 No local models found, downloading {DEFAULT_MODEL_NAME}...")
                self.download_and_load_model(DEFAULT_MODEL_NAME)
                return
            
            # Use the most recent model
            latest_model = local_models[0]  # Already sorted by timestamp
            self.load_local_model(latest_model['local_directory'])
            
        except Exception as e:
            print(f"❌ Failed to load latest model: {e}")
            raise
    
    def preprocess_input(self, input_data):
        """
        Preprocess input data for prediction
        
        Args:
            input_data (dict): Input features
            
        Returns:
            np.array: Preprocessed features
        """
        try:
            # Convert to DataFrame for easier handling
            if isinstance(input_data, dict):
                df = pd.DataFrame([input_data])
            else:
                df = pd.DataFrame(input_data)
            
            # Example preprocessing (adjust based on your model requirements)
            # This should match the preprocessing used during training
            
            # Handle categorical variables (example)
            categorical_columns = ['Department', 'JobRole', 'MaritalStatus', 'Gender', 'BusinessTravel']
            for col in categorical_columns:
                if col in df.columns:
                    # Simple label encoding (in practice, use same encoder as training)
                    df[col] = pd.Categorical(df[col]).codes
            
            # Handle missing values
            df = df.fillna(0)
            
            # Select features (adjust based on your model)
            # This should match the features used during training
            feature_columns = [
                'Age', 'DailyRate', 'DistanceFromHome', 'Education', 'EmployeeCount',
                'EnvironmentSatisfaction', 'HourlyRate', 'JobInvolvement', 'JobLevel',
                'JobSatisfaction', 'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked',
                'PercentSalaryHike', 'PerformanceRating', 'RelationshipSatisfaction',
                'StandardHours', 'StockOptionLevel', 'TotalWorkingYears', 'TrainingTimesLastYear',
                'WorkLifeBalance', 'YearsAtCompany', 'YearsInCurrentRole',
                'YearsSinceLastPromotion', 'YearsWithCurrManager'
            ]
            
            # Add categorical columns
            feature_columns.extend(categorical_columns)
            
            # Select only available columns
            available_columns = [col for col in feature_columns if col in df.columns]
            
            if not available_columns:
                raise ValueError("No valid feature columns found in input data")
            
            X = df[available_columns].values
            
            return X
            
        except Exception as e:
            print(f"❌ Preprocessing error: {e}")
            raise
    
    def predict(self, input_data):
        """
        Make prediction
        
        Args:
            input_data (dict or list): Input features
            
        Returns:
            dict: Prediction results
        """
        try:
            if self.model is None:
                raise ValueError("Model not loaded")
            
            # Preprocess input
            X = self.preprocess_input(input_data)
            
            # Make prediction
            if hasattr(self.model, 'predict_proba'):
                # Get probability predictions
                probabilities = self.model.predict_proba(X)
                predictions = self.model.predict(X)
                
                # Assuming binary classification (0: No Attrition, 1: Attrition)
                results = []
                for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
                    results.append({
                        'prediction': int(pred),
                        'prediction_label': 'Attrition' if pred == 1 else 'No Attrition',
                        'probability_no_attrition': float(prob[0]),
                        'probability_attrition': float(prob[1]),
                        'confidence': float(max(prob))
                    })
            else:
                # Simple predictions
                predictions = self.model.predict(X)
                results = []
                for pred in predictions:
                    results.append({
                        'prediction': int(pred),
                        'prediction_label': 'Attrition' if pred == 1 else 'No Attrition'
                    })
            
            return {
                'success': True,
                'predictions': results,
                'model_info': {
                    'model_name': self.model_metadata.get('model_name', 'unknown'),
                    'version': self.model_metadata.get('version', 'unknown'),
                    'model_type': self.model_metadata.get('model_type', 'unknown')
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'predictions': []
            }

def main():
    """Main function for command line usage"""
    if len(sys.argv) < 2:
        print("Usage: python predict.py '<json_input>'")
        print("Example: python predict.py '{\"Age\": 30, \"MonthlyIncome\": 5000}'")
        return
    
    try:
        # Parse input JSON
        input_json = sys.argv[1]
        input_data = json.loads(input_json)
        
        # Initialize predictor
        predictor = AttritionPredictor()
        
        # Make prediction
        results = predictor.predict(input_data)
        
        # Output results as JSON
        print(json.dumps(results, indent=2))
        
    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'predictions': []
        }
        print(json.dumps(error_result, indent=2))

if __name__ == "__main__":
    main()