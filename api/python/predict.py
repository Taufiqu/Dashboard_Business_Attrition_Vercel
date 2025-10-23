import sys
import json
import os
import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from sklearn.preprocessing import StandardScaler
# Removed unused BaseHTTPRequestHandler import
import time

# --- Salin SEMUA fungsi helper Anda dari skrip lama ---
# (load_model_and_scaler, get_model_feature_names, get_feature_columns, 
#  preprocess_input_data, predict_attrition)

def load_model_and_scaler():
    """Load trained Random Forest model and scaler"""
    try:
        # --- PERUBAHAN PATH ---
        # Path(__file__) sekarang ada di 'api/python/predict.py'
        # Jadi 'models' ada di 'api/python/models/'
        model_dir = Path(__file__).parent / 'models'
        
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

def get_feature_columns():
    """Return the exact 47 feature columns that the model expects"""
    return [
        'EmployeeId', 'Age', 'DailyRate', 'DistanceFromHome', 'Education', 
        'EmployeeCount', 'EnvironmentSatisfaction', 'HourlyRate', 'JobInvolvement',
        'JobLevel', 'JobSatisfaction', 'MonthlyIncome', 'MonthlyRate',
        'NumCompaniesWorked', 'PercentSalaryHike', 'PerformanceRating',
        'RelationshipSatisfaction', 'StandardHours', 'StockOptionLevel',
        'TotalWorkingYears', 'TrainingTimesLastYear', 'WorkLifeBalance',
        'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion',
        'YearsWithCurrManager',
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
        expected_columns = get_feature_columns()
        result_df = pd.DataFrame(0, index=[0], columns=expected_columns)
        
        if 'EmployeeNumber' in input_data:
            input_data['EmployeeId'] = input_data['EmployeeNumber']
        
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
                # Pastikan konversi ke float, tangani string kosong
                val = input_data[col]
                result_df[col] = float(val) if val not in [None, ''] else 0.0
        
        categorical_mappings = {
            'BusinessTravel': {
                'Travel_Frequently': 'BusinessTravel_Travel_Frequently',
                'Travel_Rarely': 'BusinessTravel_Travel_Rarely',
                'Non-Travel': None
            },
            'Department': {
                'Research & Development': 'Department_Research & Development',
                'Sales': 'Department_Sales',
                'Human Resources': None
            },
            'EducationField': {
                'Life Sciences': 'EducationField_Life Sciences',
                'Marketing': 'EducationField_Marketing',
                'Medical': 'EducationField_Medical',
                'Other': 'EducationField_Other',
                'Technical Degree': 'EducationField_Technical Degree',
                'Human Resources': None
            },
            'Gender': { 'Male': 'Gender_Male', 'Female': None },
            'JobRole': {
                'Human Resources': 'JobRole_Human Resources',
                'Laboratory Technician': 'JobRole_Laboratory Technician',
                'Manager': 'JobRole_Manager',
                'Manufacturing Director': 'JobRole_Manufacturing Director',
                'Research Director': 'JobRole_Research Director',
                'Research Scientist': 'JobRole_Research Scientist',
                'Sales Executive': 'JobRole_Sales Executive',
                'Sales Representative': 'JobRole_Sales Representative',
                'Healthcare Representative': None
            },
            'MaritalStatus': {
                'Married': 'MaritalStatus_Married',
                'Single': 'MaritalStatus_Single',
                'Divorced': None
            },
            'OverTime': { 'Yes': 'OverTime_Yes', 'No': None }
        }
        
        for cat_col, mapping in categorical_mappings.items():
            if cat_col in input_data and input_data[cat_col] in mapping:
                encoded_col = mapping[input_data[cat_col]]
                if encoded_col and encoded_col in result_df.columns:
                    result_df[encoded_col] = 1
        
        return result_df
        
    except Exception as e:
        print(f"Error preprocessing data: {e}", file=sys.stderr)
        return None

# --- Muat model & scaler satu kali saat fungsi "dingin" ---
# Ini akan disimpan di memori untuk "warm start"
MODEL, SCALER = load_model_and_scaler()

def predict_attrition(input_data):
    """Make attrition prediction using trained model"""
    try:
        if MODEL is None or SCALER is None:
            return {
                "success": False,
                "error": "Failed to load model or scaler on cold start"
            }
        
        processed_data = preprocess_input_data(input_data)
        if processed_data is None:
            return {
                "success": False,
                "error": "Failed to preprocess input data"
            }
        
        scaled_data = SCALER.transform(processed_data)
        
        prediction = MODEL.predict(scaled_data)[0]
        prediction_proba = MODEL.predict_proba(scaled_data)[0]
        
        feature_names = processed_data.columns.tolist()
        feature_importance = dict(zip(feature_names, MODEL.feature_importances_))
        top_features = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:10])
        
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
            "error": str(e),
            "error_type": type(e).__name__
        }

# --- Vercel Serverless Function Handler ---
def handler(request):
    """
    Vercel serverless function handler for Python
    """
    try:
        # Parse request body
        if hasattr(request, 'get_json'):
            # Vercel request format
            input_data = request.get_json()
        else:
            # Alternative parsing
            import json
            body = request.body if hasattr(request, 'body') else request.data
            if isinstance(body, bytes):
                body = body.decode('utf-8')
            input_data = json.loads(body) if isinstance(body, str) else body
        
        # Run prediction
        result = predict_attrition(input_data)
        
        # Return JSON response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(result)
        }
        
    except Exception as e:
        # Handle errors
        error_result = {
            "success": False,
            "error": f"Internal server error in Python: {str(e)}",
            "error_type": type(e).__name__
        }
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(error_result)
        }