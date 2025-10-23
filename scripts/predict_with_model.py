import sys
import json
import os
import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from sklearn.preprocessing import StandardScaler

def load_model_and_scaler():
    """Load trained Random Forest model and scaler"""
    try:
        model_dir = Path(__file__).parent.parent / 'models'
        
        model_path = model_dir / 'rf_model.pkl'
        scaler_path = model_dir / 'scaler.pkl'
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found at {model_path}")
        if not scaler_path.exists():
            raise FileNotFoundError(f"Scaler not found at {scaler_path}")
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        
        return model, scaler
    
    except Exception as e:
        print(f"Error loading model: {e}", file=sys.stderr)
        return None, None

def get_model_feature_names(model):
    """Get the actual feature names that the model expects"""
    if hasattr(model, 'feature_names_in_'):
        return list(model.feature_names_in_)
    else:
        # Exact feature names from the trained model
        return [
            'EmployeeId', 'Age', 'DailyRate', 'DistanceFromHome', 'Education', 
            'EmployeeCount', 'EnvironmentSatisfaction', 'HourlyRate', 'JobInvolvement',
            'JobLevel', 'JobSatisfaction', 'MonthlyIncome', 'MonthlyRate',
            'NumCompaniesWorked', 'PercentSalaryHike', 'PerformanceRating',
            'RelationshipSatisfaction', 'StandardHours', 'StockOptionLevel',
            'TotalWorkingYears', 'TrainingTimesLastYear', 'WorkLifeBalance',
            'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion',
            'YearsWithCurrManager',
            # Categorical encoded columns (exact from model)
            'BusinessTravel_Travel_Frequently', 'BusinessTravel_Travel_Rarely',
            'Department_Research & Development', 'Department_Sales',
            'EducationField_Life Sciences', 'EducationField_Marketing', 
            'EducationField_Medical', 'EducationField_Other', 'EducationField_Technical Degree',
            'Gender_Male',
            'JobRole_Human Resources', 'JobRole_Laboratory Technician', 'JobRole_Manager', 
            'JobRole_Manufacturing Director', 'JobRole_Research Director', 'JobRole_Research Scientist',
            'JobRole_Sales Executive', 'JobRole_Sales Representative',
            'MaritalStatus_Married', 'MaritalStatus_Single',
            'OverTime_Yes'
        ]

def get_feature_columns():
    """Return the exact 47 feature columns that the model expects"""
    return [
        # Numerical features (26 features)
        'EmployeeId', 'Age', 'DailyRate', 'DistanceFromHome', 'Education', 
        'EmployeeCount', 'EnvironmentSatisfaction', 'HourlyRate', 'JobInvolvement',
        'JobLevel', 'JobSatisfaction', 'MonthlyIncome', 'MonthlyRate',
        'NumCompaniesWorked', 'PercentSalaryHike', 'PerformanceRating',
        'RelationshipSatisfaction', 'StandardHours', 'StockOptionLevel',
        'TotalWorkingYears', 'TrainingTimesLastYear', 'WorkLifeBalance',
        'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion',
        'YearsWithCurrManager',
        
        # Categorical features (21 features) - exact names from model
        'BusinessTravel_Travel_Frequently', 'BusinessTravel_Travel_Rarely',
        'Department_Research & Development', 'Department_Sales',
        'EducationField_Life Sciences', 'EducationField_Marketing',
        'EducationField_Medical', 'EducationField_Other', 'EducationField_Technical Degree',
        'Gender_Male',
        'JobRole_Human Resources', 'JobRole_Laboratory Technician', 'JobRole_Manager',
        'JobRole_Manufacturing Director', 'JobRole_Research Director', 'JobRole_Research Scientist',
        'JobRole_Sales Executive', 'JobRole_Sales Representative',
        'MaritalStatus_Married', 'MaritalStatus_Single',
        'OverTime_Yes'
    ]

def preprocess_input_data(input_data):
    """Preprocess input data to match exact training format"""
    try:
        # Get expected feature columns
        expected_columns = get_feature_columns()
        
        # Initialize result DataFrame with all expected columns set to 0
        result_df = pd.DataFrame(0, index=[0], columns=expected_columns)
        
        # Map EmployeeNumber to EmployeeId if needed
        if 'EmployeeNumber' in input_data:
            input_data['EmployeeId'] = input_data['EmployeeNumber']
        
        # Fill numerical columns directly
        numerical_columns = [
            'EmployeeId', 'Age', 'DailyRate', 'DistanceFromHome', 'Education',
            'EmployeeCount', 'EnvironmentSatisfaction', 'HourlyRate', 'JobInvolvement',
            'JobLevel', 'JobSatisfaction', 'MonthlyIncome', 'MonthlyRate',
            'NumCompaniesWorked', 'PercentSalaryHike', 'PerformanceRating',
            'RelationshipSatisfaction', 'StandardHours', 'StockOptionLevel',
            'TotalWorkingYears', 'TrainingTimesLastYear', 'WorkLifeBalance',
            'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion',
            'YearsWithCurrManager'
        ]
        
        for col in numerical_columns:
            if col in input_data:
                result_df[col] = float(input_data[col])
        
        # Handle categorical variables - exact mapping to model features
        categorical_mappings = {
            'BusinessTravel': {
                'Travel_Frequently': 'BusinessTravel_Travel_Frequently',
                'Travel_Rarely': 'BusinessTravel_Travel_Rarely',
                'Non-Travel': None  # Default case (all 0s)
            },
            'Department': {
                'Research & Development': 'Department_Research & Development',
                'Sales': 'Department_Sales',
                'Human Resources': None  # Default case (all 0s)
            },
            'EducationField': {
                'Life Sciences': 'EducationField_Life Sciences',
                'Marketing': 'EducationField_Marketing',
                'Medical': 'EducationField_Medical',
                'Other': 'EducationField_Other',
                'Technical Degree': 'EducationField_Technical Degree',
                'Human Resources': None  # Default case (all 0s)
            },
            'Gender': {
                'Male': 'Gender_Male',
                'Female': None  # Default case (all 0s)
            },
            'JobRole': {
                'Human Resources': 'JobRole_Human Resources',
                'Laboratory Technician': 'JobRole_Laboratory Technician',
                'Manager': 'JobRole_Manager',
                'Manufacturing Director': 'JobRole_Manufacturing Director',
                'Research Director': 'JobRole_Research Director',
                'Research Scientist': 'JobRole_Research Scientist',
                'Sales Executive': 'JobRole_Sales Executive',
                'Sales Representative': 'JobRole_Sales Representative',
                'Healthcare Representative': None  # Default case (all 0s)
            },
            'MaritalStatus': {
                'Married': 'MaritalStatus_Married',
                'Single': 'MaritalStatus_Single',
                'Divorced': None  # Default case (all 0s)
            },
            'OverTime': {
                'Yes': 'OverTime_Yes',
                'No': None  # Default case (all 0s)
            }
        }
        
        # Apply categorical mappings
        for cat_col, mapping in categorical_mappings.items():
            if cat_col in input_data and input_data[cat_col] in mapping:
                encoded_col = mapping[input_data[cat_col]]
                if encoded_col and encoded_col in result_df.columns:
                    result_df[encoded_col] = 1
        
        return result_df
        
    except Exception as e:
        print(f"Error preprocessing data: {e}", file=sys.stderr)
        return None
    
def predict_attrition(input_data):
    """Make attrition prediction using trained model"""
    try:
        # Load model and scaler
        model, scaler = load_model_and_scaler()
        if model is None or scaler is None:
            return {
                "success": False,
                "error": "Failed to load model or scaler"
            }
        
        # Preprocess input data
        processed_data = preprocess_input_data(input_data)
        if processed_data is None:
            return {
                "success": False,
                "error": "Failed to preprocess input data"
            }
        
        # Apply scaling
        scaled_data = scaler.transform(processed_data)
        
        # Make prediction
        prediction = model.predict(scaled_data)[0]
        prediction_proba = model.predict_proba(scaled_data)[0]
        
        # Get feature importance (top 10)
        feature_names = processed_data.columns.tolist()
        feature_importance = dict(zip(feature_names, model.feature_importances_))
        top_features = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:10])
        
        # Determine risk level
        attrition_prob = prediction_proba[1]
        if attrition_prob > 0.7:
            risk_level = "High"
        elif attrition_prob > 0.4:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        return {
            "success": True,
            "prediction": int(prediction),
            "prediction_label": "Will Leave" if prediction == 1 else "Will Stay",
            "probability": {
                "will_stay": float(prediction_proba[0]),
                "will_leave": float(prediction_proba[1])
            },
            "risk_level": risk_level,
            "top_feature_importance": top_features,
            "confidence": float(max(prediction_proba))
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    try:
        # Get input data from command line argument
        if len(sys.argv) < 2:
            raise ValueError("No input data provided")
        
        input_json = sys.argv[1]
        input_data = json.loads(input_json)
        
        # Make prediction
        result = predict_attrition(input_data)
        
        # Output result as JSON
        print(json.dumps(result))
    
    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e)
        }
        print(json.dumps(error_result))