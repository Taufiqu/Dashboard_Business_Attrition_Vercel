from http.server import BaseHTTPRequestHandler
import json
import sys
import os

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
        import pandas as pd
        
        expected_columns = get_feature_columns()
        result_df = pd.DataFrame(0, index=[0], columns=expected_columns)
        
        # Handle EmployeeNumber/EmployeeId
        if 'EmployeeNumber' in input_data:
            input_data['EmployeeId'] = input_data['EmployeeNumber']
        
        # Fill numerical columns
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
                val = input_data[col]
                result_df[col] = float(val) if val not in [None, ''] else 0.0
        
        # Set default values for required fields
        result_df['EmployeeCount'] = 1
        result_df['StandardHours'] = 80
        
        # Handle categorical columns with one-hot encoding
        if input_data.get('BusinessTravel') == 'Travel_Frequently':
            result_df['BusinessTravel_Travel_Frequently'] = 1
        elif input_data.get('BusinessTravel') == 'Travel_Rarely':
            result_df['BusinessTravel_Travel_Rarely'] = 1
            
        if input_data.get('Department') == 'Research & Development':
            result_df['Department_Research & Development'] = 1
        elif input_data.get('Department') == 'Sales':
            result_df['Department_Sales'] = 1
            
        if input_data.get('EducationField') == 'Life Sciences':
            result_df['EducationField_Life Sciences'] = 1
        elif input_data.get('EducationField') == 'Marketing':
            result_df['EducationField_Marketing'] = 1
        elif input_data.get('EducationField') == 'Medical':
            result_df['EducationField_Medical'] = 1
        elif input_data.get('EducationField') == 'Other':
            result_df['EducationField_Other'] = 1
        elif input_data.get('EducationField') == 'Technical Degree':
            result_df['EducationField_Technical Degree'] = 1
            
        if input_data.get('Gender') == 'Male':
            result_df['Gender_Male'] = 1
            
        # Job roles
        job_role = input_data.get('JobRole', '')
        if job_role == 'Human Resources':
            result_df['JobRole_Human Resources'] = 1
        elif job_role == 'Laboratory Technician':
            result_df['JobRole_Laboratory Technician'] = 1
        elif job_role == 'Manager':
            result_df['JobRole_Manager'] = 1
        elif job_role == 'Manufacturing Director':
            result_df['JobRole_Manufacturing Director'] = 1
        elif job_role == 'Research Director':
            result_df['JobRole_Research Director'] = 1
        elif job_role == 'Research Scientist':
            result_df['JobRole_Research Scientist'] = 1
        elif job_role == 'Sales Executive':
            result_df['JobRole_Sales Executive'] = 1
        elif job_role == 'Sales Representative':
            result_df['JobRole_Sales Representative'] = 1
            
        if input_data.get('MaritalStatus') == 'Married':
            result_df['MaritalStatus_Married'] = 1
        elif input_data.get('MaritalStatus') == 'Single':
            result_df['MaritalStatus_Single'] = 1
            
        if input_data.get('OverTime') == 'Yes':
            result_df['OverTime_Yes'] = 1
        
        return result_df
        
    except Exception as e:
        print(f"Error preprocessing data: {e}", file=sys.stderr)
        return None

def try_ml_prediction(input_data):
    """Try to use the ML model first"""
    try:
        # Import ML libraries
        from pathlib import Path
        import pandas as pd
        import numpy as np
        import joblib
        
        # Debug: Print current working directory and file locations
        current_dir = Path(__file__).parent
        model_dir = current_dir / 'models'
        model_path = model_dir / 'rf_model.pkl'
        scaler_path = model_dir / 'scaler.pkl'
        
        print(f"Current file: {__file__}", file=sys.stderr)
        print(f"Current dir: {current_dir}", file=sys.stderr)
        print(f"Model dir: {model_dir}", file=sys.stderr)
        print(f"Model path exists: {model_path.exists()}", file=sys.stderr)
        print(f"Scaler path exists: {scaler_path.exists()}", file=sys.stderr)
        
        # List files in the directory
        try:
            files_in_dir = list(current_dir.iterdir())
            print(f"Files in current dir: {files_in_dir}", file=sys.stderr)
            if model_dir.exists():
                model_files = list(model_dir.iterdir())
                print(f"Files in model dir: {model_files}", file=sys.stderr)
        except Exception as list_error:
            print(f"Error listing files: {list_error}", file=sys.stderr)
        
        if not model_path.exists() or not scaler_path.exists():
            return None, f"ML model files not found - model: {model_path.exists()}, scaler: {scaler_path.exists()}"
        
        # Load model and scaler
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        
        # Preprocess input data to 47 features
        processed_data = preprocess_input_data(input_data)
        if processed_data is None:
            return None, "Failed to preprocess input data"
        
        print(f"Processed data shape: {processed_data.shape}", file=sys.stderr)
        print(f"Processed data columns: {list(processed_data.columns)}", file=sys.stderr)
        
        # Scale and predict
        scaled_data = scaler.transform(processed_data)
        prediction = model.predict(scaled_data)[0]
        prediction_proba = model.predict_proba(scaled_data)[0]
        
        # Get feature importance
        feature_names = processed_data.columns.tolist()
        feature_importance = dict(zip(feature_names, model.feature_importances_))
        top_features = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:10])
        
        attrition_prob = prediction_proba[1]
        risk_level = "High" if attrition_prob > 0.7 else "Medium" if attrition_prob > 0.4 else "Low"
        
        return {
            "success": True,
            "prediction": int(prediction),
            "prediction_label": "Will Leave" if prediction == 1 else "Will Stay",
            "probability": {
                "will_stay": float(prediction_proba[0]),
                "will_leave": float(prediction_proba[1])
            },
            "risk_level": risk_level,
            "confidence": float(max(prediction_proba)),
            "model_type": "Random Forest ML Model (47 Features)",
            "top_feature_importance": top_features
        }, None
        
    except Exception as e:
        return None, f"ML model error: {str(e)}"

def simple_rule_based_prediction(input_data):
    """Fallback rule-based prediction"""
    try:
        age = input_data.get('Age', 30)
        income = input_data.get('MonthlyIncome', 5000)
        overtime = input_data.get('OverTime', 'No')
        job_satisfaction = input_data.get('JobSatisfaction', 3)
        work_life_balance = input_data.get('WorkLifeBalance', 3)
        distance = input_data.get('DistanceFromHome', 5)
        years_at_company = input_data.get('YearsAtCompany', 5)
        
        # Calculate risk score
        risk_score = 0.0
        
        if age < 25 or age > 55:
            risk_score += 0.2
        if income < 3000:
            risk_score += 0.25
        if overtime == 'Yes':
            risk_score += 0.2
        if job_satisfaction <= 2:
            risk_score += 0.3
        if work_life_balance <= 2:
            risk_score += 0.25
        if distance > 20:
            risk_score += 0.15
        if years_at_company < 1 or years_at_company > 20:
            risk_score += 0.15
        
        probability = min(risk_score, 0.95)
        prediction = 1 if probability > 0.5 else 0
        
        return {
            "success": True,
            "prediction": prediction,
            "prediction_label": "Will Leave" if prediction == 1 else "Will Stay",
            "probability": {
                "will_stay": 1 - probability,
                "will_leave": probability
            },
            "risk_level": "High" if probability > 0.7 else "Medium" if probability > 0.4 else "Low",
            "confidence": max(probability, 1 - probability),
            "model_type": "Rule-Based Model (Python Serverless)"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Rule-based prediction failed: {str(e)}"
        }

def ml_prediction(input_data):
    """Try ML prediction with pandas/sklearn"""
    try:
        import pandas as pd
        import numpy as np
        import joblib
        from pathlib import Path
        from sklearn.preprocessing import StandardScaler
        
        # Load model
        model_dir = Path(__file__).parent / 'models'
        model_path = model_dir / 'rf_model.pkl'
        scaler_path = model_dir / 'scaler.pkl'
        
        if not model_path.exists() or not scaler_path.exists():
            return None  # Fall back to rule-based
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        
        # Feature engineering (simplified version)
        expected_columns = [
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
        
        # Create feature dataframe
        result_df = pd.DataFrame(0, index=[0], columns=expected_columns)
        
        # Fill numerical features
        numerical_features = [
            'EmployeeId', 'Age', 'DailyRate', 'DistanceFromHome', 'Education',
            'EmployeeCount', 'EnvironmentSatisfaction', 'HourlyRate', 'JobInvolvement',
            'JobLevel', 'JobSatisfaction', 'MonthlyIncome', 'MonthlyRate',
            'NumCompaniesWorked', 'PercentSalaryHike', 'PerformanceRating',
            'RelationshipSatisfaction', 'StandardHours', 'StockOptionLevel',
            'TotalWorkingYears', 'TrainingTimesLastYear', 'WorkLifeBalance',
            'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion',
            'YearsWithCurrManager'
        ]
        
        for col in numerical_features:
            if col in input_data:
                result_df[col] = float(input_data[col]) if input_data[col] not in [None, ''] else 0.0
        
        # Handle categorical features
        if input_data.get('OverTime') == 'Yes':
            result_df['OverTime_Yes'] = 1
        if input_data.get('Gender') == 'Male':
            result_df['Gender_Male'] = 1
            
        # Scale and predict
        scaled_data = scaler.transform(result_df)
        prediction = model.predict(scaled_data)[0]
        prediction_proba = model.predict_proba(scaled_data)[0]
        
        return {
            "success": True,
            "prediction": int(prediction),
            "prediction_label": "Will Leave" if prediction == 1 else "Will Stay",
            "probability": {
                "will_stay": float(prediction_proba[0]),
                "will_leave": float(prediction_proba[1])
            },
            "risk_level": "High" if prediction_proba[1] > 0.7 else "Medium" if prediction_proba[1] > 0.4 else "Low",
            "confidence": float(max(prediction_proba)),
            "model_type": "Random Forest ML Model"
        }
        
    except Exception as e:
        print(f"ML prediction failed: {e}", file=sys.stderr)
        return None  # Fall back to rule-based

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse JSON data
            input_data = json.loads(post_data.decode('utf-8'))
            
            # Validate required fields
            required_fields = ['Age', 'DistanceFromHome', 'MonthlyIncome', 'YearsAtCompany']
            for field in required_fields:
                if field not in input_data or input_data[field] == '' or input_data[field] is None:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    
                    error_result = {
                        "success": False,
                        "error": f"Missing required field: {field}"
                    }
                    self.wfile.write(json.dumps(error_result).encode('utf-8'))
                    return
            
            # Try ML prediction first
            ml_result, ml_error = try_ml_prediction(input_data)
            
            if ml_result and ml_result.get('success'):
                result = ml_result
                result["note"] = "Using Random Forest ML model"
            else:
                # Fall back to rule-based
                result = simple_rule_based_prediction(input_data)
                if ml_error:
                    result["note"] = f"Using rule-based prediction (ML error: {ml_error})"
                else:
                    result["note"] = "Using rule-based prediction (ML model not available)"
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
        except Exception as e:
            # Handle errors
            error_result = {
                "success": False,
                "error": f"Internal server error: {str(e)}",
                "error_type": type(e).__name__
            }
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(error_result).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()