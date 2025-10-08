#!/usr/bin/env python3
"""
Real ML prediction script for employee attrition
"""

import json
import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path

def load_real_model():
    """Load model from MLflow or create trained model from data"""
    try:
        # Try to load MLflow model first
        try:
            import mlflow
            from dotenv import load_dotenv
            load_dotenv()
            
            mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI'))
            
            # Try to load registered model
            model_uri = "models:/attrition-model/latest"
            model = mlflow.sklearn.load_model(model_uri)
            
            return model, "MLflow Attrition Model", "1.0", get_feature_names_mlflow()
            
        except Exception as mlflow_error:
            # If MLflow fails, train model from local data
            return train_model_from_data()
            
    except Exception as e:
        # Ultimate fallback - simple rule-based model
        return None, f"Error: {str(e)}", "0.0", []

def train_model_from_data():
    """Train model from local CSV data"""
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import LabelEncoder
        
        # Load the actual data
        csv_path = Path("public/data/hasil_output_DSP (2).csv")
        if not csv_path.exists():
            raise FileNotFoundError("CSV data not found")
        
        df = pd.read_csv(csv_path)
        
        # Select relevant features (matching the form)
        feature_columns = [
            'Age', 'DistanceFromHome', 'MonthlyIncome', 'YearsAtCompany',
            'JobLevel', 'OverTime', 'JobSatisfaction', 'WorkLifeBalance',
            'Department', 'EducationField', 'MaritalStatus'
        ]
        
        target_column = 'Attrition'  # Adjust based on actual column name
        
        # Check if target column exists
        if target_column not in df.columns:
            # Try alternative column names
            possible_targets = ['Final_Attrition', 'attrition', 'Attrition_Flag']
            for col in possible_targets:
                if col in df.columns:
                    target_column = col
                    break
        
        # Clean data
        available_features = [col for col in feature_columns if col in df.columns]
        df_clean = df[available_features + [target_column]].copy()
        
        # Handle categorical variables
        le_dict = {}
        categorical_cols = ['Department', 'EducationField', 'MaritalStatus', 'OverTime']
        
        for col in categorical_cols:
            if col in df_clean.columns:
                le = LabelEncoder()
                df_clean[col] = le.fit_transform(df_clean[col].astype(str))
                le_dict[col] = le
        
        # Handle target variable
        if df_clean[target_column].dtype == 'object':
            le_target = LabelEncoder()
            df_clean[target_column] = le_target.fit_transform(df_clean[target_column])
        
        # Remove rows with missing values
        df_clean = df_clean.dropna()
        
        if len(df_clean) < 10:
            raise ValueError("Not enough clean data for training")
        
        # Prepare features and target
        X = df_clean[available_features]
        y = df_clean[target_column]
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        
        # Split data for validation
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        model.fit(X_train, y_train)
        
        # Calculate accuracy
        accuracy = model.score(X_test, y_test)
        
        return model, f"Trained Random Forest (Accuracy: {accuracy:.2f})", "1.0", available_features, le_dict
        
    except Exception as e:
        raise Exception(f"Failed to train model: {str(e)}")

def get_feature_names_mlflow():
    """Get feature names for MLflow model"""
    return [
        'Age', 'DistanceFromHome', 'MonthlyIncome', 'YearsAtCompany',
        'JobLevel', 'OverTime', 'JobSatisfaction', 'WorkLifeBalance'
    ]

def preprocess_input(input_data, feature_names, label_encoders=None):
    """Preprocess input data for prediction"""
    try:
        # Create feature vector
        features = {}
        
        # Map form field names to model feature names
        field_mapping = {
            'Age': 'Age',
            'DistanceFromHome': 'DistanceFromHome', 
            'MonthlyIncome': 'MonthlyIncome',
            'YearsAtCompany': 'YearsAtCompany',
            'JobLevel': 'JobLevel',
            'OverTime': 'OverTime',
            'JobSatisfaction': 'JobSatisfaction',
            'WorkLifeBalance': 'WorkLifeBalance',
            'Department': 'Department',
            'EducationField': 'EducationField',
            'MaritalStatus': 'MaritalStatus'
        }
        
        # Fill numerical features
        for form_field, model_field in field_mapping.items():
            if model_field in feature_names:
                if form_field in ['Age', 'DistanceFromHome', 'MonthlyIncome', 'YearsAtCompany', 'JobLevel', 'JobSatisfaction', 'WorkLifeBalance']:
                    features[model_field] = float(input_data.get(form_field, 0))
                elif form_field == 'OverTime':
                    if label_encoders and 'OverTime' in label_encoders:
                        # Use trained encoder
                        overtime_val = input_data.get('OverTime', 'No')
                        try:
                            features[model_field] = label_encoders['OverTime'].transform([overtime_val])[0]
                        except:
                            features[model_field] = 1 if overtime_val == 'Yes' else 0
                    else:
                        features[model_field] = 1 if input_data.get('OverTime', 'No') == 'Yes' else 0
                elif form_field in ['Department', 'EducationField', 'MaritalStatus']:
                    if label_encoders and form_field in label_encoders:
                        # Use trained encoder
                        cat_val = input_data.get(form_field, '')
                        try:
                            features[model_field] = label_encoders[form_field].transform([cat_val])[0]
                        except:
                            features[model_field] = 0  # Default encoding
                    else:
                        # Simple hash-based encoding
                        features[model_field] = hash(input_data.get(form_field, '')) % 10
        
        # Create DataFrame for prediction
        feature_df = pd.DataFrame([features])
        
        # Ensure all required features are present
        for feat in feature_names:
            if feat not in feature_df.columns:
                feature_df[feat] = 0
        
        # Reorder columns to match training
        feature_df = feature_df[feature_names]
        
        return feature_df
        
    except Exception as e:
        raise Exception(f"Preprocessing failed: {str(e)}")

def predict_attrition(input_data):
    """Make attrition prediction"""
    try:
        # Load model
        result = load_real_model()
        if len(result) == 5:
            model, model_name, version, feature_names, label_encoders = result
        else:
            model, model_name, version, feature_names = result
            label_encoders = None
        
        if model is None:
            # Rule-based fallback
            return rule_based_prediction(input_data, model_name)
        
        # Preprocess input
        X = preprocess_input(input_data, feature_names, label_encoders)
        
        # Make prediction
        prediction = model.predict(X)[0]
        
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(X)[0]
            attrition_prob = probabilities[1] if len(probabilities) > 1 else probabilities[0]
        else:
            attrition_prob = 0.7 if prediction == 1 else 0.3
        
        # Get feature importance
        if hasattr(model, 'feature_importances_'):
            importance = dict(zip(feature_names, model.feature_importances_))
        else:
            importance = {feat: 0.1 for feat in feature_names}
        
        return {
            'success': True,
            'prediction': int(prediction),
            'attrition_probability': float(attrition_prob),
            'model_info': {
                'name': model_name,
                'version': version,
                'type': type(model).__name__
            },
            'feature_importance': importance,
            'input_data': input_data
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Prediction failed: {str(e)}',
            'input_data': input_data
        }

def rule_based_prediction(input_data, error_msg):
    """Fallback rule-based prediction"""
    try:
        age = float(input_data.get('Age', 30))
        distance = float(input_data.get('DistanceFromHome', 10))
        income = float(input_data.get('MonthlyIncome', 5000))
        years = float(input_data.get('YearsAtCompany', 2))
        job_level = int(input_data.get('JobLevel', 1))
        overtime = input_data.get('OverTime', 'No') == 'Yes'
        satisfaction = int(input_data.get('JobSatisfaction', 3))
        worklife = int(input_data.get('WorkLifeBalance', 3))
        
        # Risk scoring
        risk_score = 0.1  # Base risk
        
        if age < 25: risk_score += 0.2
        if age > 55: risk_score += 0.15
        if distance > 25: risk_score += 0.25
        if income < 3000: risk_score += 0.3
        if years < 1: risk_score += 0.4
        if job_level <= 1: risk_score += 0.15
        if overtime: risk_score += 0.2
        if satisfaction <= 2: risk_score += 0.25
        if worklife <= 2: risk_score += 0.2
        
        # Cap at 0.95
        attrition_prob = min(risk_score, 0.95)
        prediction = 1 if attrition_prob > 0.5 else 0
        
        return {
            'success': True,
            'prediction': prediction,
            'attrition_probability': attrition_prob,
            'model_info': {
                'name': 'Rule-Based Predictor',
                'version': '1.0',
                'type': 'RuleBasedClassifier',
                'note': error_msg
            },
            'feature_importance': {
                'Age': 0.15,
                'DistanceFromHome': 0.18,
                'MonthlyIncome': 0.22,
                'YearsAtCompany': 0.20,
                'JobLevel': 0.08,
                'OverTime': 0.12,
                'JobSatisfaction': 0.18,
                'WorkLifeBalance': 0.15
            },
            'input_data': input_data
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Rule-based prediction failed: {str(e)}',
            'input_data': input_data
        }

def main():
    """Main function"""
    try:
        input_data = None
        
        # Check if using file input
        if len(sys.argv) > 2 and sys.argv[1] == '--file':
            # Read from file
            file_path = sys.argv[2]
            with open(file_path, 'r') as f:
                input_data = json.load(f)
            # Clean up temp file
            try:
                os.remove(file_path)
            except:
                pass
        elif len(sys.argv) > 1:
            # Parse from command line
            json_input = sys.argv[1]
            input_data = json.loads(json_input)
        else:
            print(json.dumps({
                'success': False,
                'error': 'No input data provided'
            }))
            return
        
        # Make prediction
        result = predict_attrition(input_data)
        
        # Output result
        print(json.dumps(result))
        
    except json.JSONDecodeError as e:
        print(json.dumps({
            'success': False,
            'error': f'Invalid JSON input: {str(e)}'
        }))
    except Exception as e:
        print(json.dumps({
            'success': False,
            'error': f'Prediction error: {str(e)}'
        }))

if __name__ == '__main__':
    main()