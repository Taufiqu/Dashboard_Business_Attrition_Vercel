from http.server import BaseHTTPRequestHandler
import json
import sys
import os

def simple_rule_based_prediction(input_data):
    """Simple rule-based prediction without ML dependencies"""
    try:
        # Simple scoring based on key factors
        risk_score = 0.0
        
        # Age factor (young or old employees more likely to leave)
        age = input_data.get('Age', 30)
        if age < 25 or age > 55:
            risk_score += 0.2
        
        # Distance factor
        distance = input_data.get('DistanceFromHome', 5)
        if distance > 20:
            risk_score += 0.15
        
        # Income factor (low income = higher risk)
        income = input_data.get('MonthlyIncome', 5000)
        if income < 3000:
            risk_score += 0.25
        
        # Overtime factor
        overtime = input_data.get('OverTime', 'No')
        if overtime == 'Yes':
            risk_score += 0.2
        
        # Job satisfaction (1-4 scale, lower = higher risk)
        job_satisfaction = input_data.get('JobSatisfaction', 3)
        if job_satisfaction <= 2:
            risk_score += 0.3
        
        # Work-life balance (1-4 scale, lower = higher risk)
        work_life_balance = input_data.get('WorkLifeBalance', 3)
        if work_life_balance <= 2:
            risk_score += 0.25
        
        # Years at company (too short or too long can be risky)
        years_at_company = input_data.get('YearsAtCompany', 5)
        if years_at_company < 1 or years_at_company > 20:
            risk_score += 0.15
        
        # Cap the risk score at 0.95
        probability = min(risk_score, 0.95)
        prediction = 1 if probability > 0.5 else 0
        
        # Determine risk level
        if probability > 0.7:
            risk_level = "High"
        elif probability > 0.4:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        return {
            "success": True,
            "prediction": prediction,
            "prediction_label": "Will Leave" if prediction == 1 else "Will Stay", 
            "probability": {
                "will_stay": 1 - probability,
                "will_leave": probability
            },
            "risk_level": risk_level,
            "confidence": max(probability, 1 - probability),
            "model_type": "Rule-Based Model (Serverless Optimized)",
            "feature_importance": {
                "Job Satisfaction": 0.3 if job_satisfaction <= 2 else 0,
                "Work Life Balance": 0.25 if work_life_balance <= 2 else 0,
                "Monthly Income": 0.25 if income < 3000 else 0,
                "Over Time": 0.2 if overtime == 'Yes' else 0,
                "Age": 0.2 if (age < 25 or age > 55) else 0,
                "Distance From Home": 0.15 if distance > 20 else 0,
                "Years At Company": 0.15 if (years_at_company < 1 or years_at_company > 20) else 0
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Rule-based prediction failed: {str(e)}",
            "error_type": type(e).__name__
        }

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
            
            # Try to use ML model first, fallback to rule-based
            try:
                # Attempt to import ML libraries
                import pandas as pd
                import numpy as np
                import joblib
                from pathlib import Path
                
                # Try to load model
                model_dir = Path(__file__).parent / 'models'
                model_path = model_dir / 'rf_model.pkl'
                scaler_path = model_dir / 'scaler.pkl'
                
                if model_path.exists() and scaler_path.exists():
                    # Use ML model (if imports and files work)
                    result = {"success": False, "error": "ML model loading not implemented in this version"}
                else:
                    # Use rule-based fallback
                    result = simple_rule_based_prediction(input_data)
                    result["note"] = "Using rule-based prediction (ML model files not found)"
                    
            except ImportError as e:
                # ML libraries not available, use rule-based
                result = simple_rule_based_prediction(input_data)
                result["note"] = f"Using rule-based prediction (ML libraries not available: {str(e)})"
                
            except Exception as e:
                # Any other error, use rule-based
                result = simple_rule_based_prediction(input_data)
                result["note"] = f"Using rule-based prediction (ML model error: {str(e)})"
            
            # Send successful response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            response_data = json.dumps(result).encode('utf-8')
            self.wfile.write(response_data)
            
        except Exception as e:
            # Handle any errors
            error_result = {
                "success": False,
                "error": f"Internal server error: {str(e)}",
                "error_type": type(e).__name__
            }
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response_data = json.dumps(error_result).encode('utf-8')
            self.wfile.write(response_data)
    
    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()