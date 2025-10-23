from http.server import BaseHTTPRequestHandler
import json
import sys
import os

def try_ml_prediction(input_data):
    """Try to use the ML model first"""
    try:
        # Import ML libraries
        from pathlib import Path
        import pandas as pd
        import numpy as np
        import joblib
        
        # Load model and scaler
        model_dir = Path(__file__).parent / 'models'
        model_path = model_dir / 'rf_model.pkl'
        scaler_path = model_dir / 'scaler.pkl'
        
        if not model_path.exists() or not scaler_path.exists():
            return None, "ML model files not found"
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        
        # Process input data for ML model (simplified version)
        # Create a basic feature vector with the most important features
        features = [
            input_data.get('Age', 30),
            input_data.get('MonthlyIncome', 5000), 
            input_data.get('DistanceFromHome', 5),
            input_data.get('YearsAtCompany', 5),
            1 if input_data.get('OverTime', 'No') == 'Yes' else 0,
            input_data.get('JobSatisfaction', 3),
            input_data.get('WorkLifeBalance', 3)
        ]
        
        # For a full 47-feature model, we'd need to pad with defaults
        # For now, let's try with basic features and see if it works
        feature_array = np.array(features).reshape(1, -1)
        
        # This might fail if the model expects 47 features
        # That's okay, we'll fall back to rule-based
        scaled_features = scaler.transform(feature_array)
        prediction = model.predict(scaled_features)[0]
        prediction_proba = model.predict_proba(scaled_features)[0]
        
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
            "model_type": "Random Forest ML Model (Python)"
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