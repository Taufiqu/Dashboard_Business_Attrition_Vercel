from http.server import BaseHTTPRequestHandler
import json
import sys
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse JSON data
            input_data = json.loads(post_data.decode('utf-8'))
            
            # Try to import ML libraries and run prediction
            try:
                from pathlib import Path
                import pandas as pd
                import numpy as np
                import joblib
                from sklearn.preprocessing import StandardScaler
                
                # Simple prediction logic for now
                result = {
                    "success": True,
                    "prediction": 0,
                    "prediction_label": "Will Stay",
                    "probability": {
                        "will_stay": 0.7,
                        "will_leave": 0.3
                    },
                    "risk_level": "Low",
                    "confidence": 0.7,
                    "model_type": "Simple Test Model",
                    "message": "Python ML function is working with all dependencies!"
                }
                
            except ImportError as e:
                # Fallback if ML libraries fail
                result = {
                    "success": True,
                    "prediction": 0,
                    "prediction_label": "Will Stay",
                    "probability": {
                        "will_stay": 0.6,
                        "will_leave": 0.4
                    },
                    "risk_level": "Medium",
                    "confidence": 0.6,
                    "model_type": "Fallback Model",
                    "message": f"Using fallback due to import error: {str(e)}"
                }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # Write response body
            response_data = json.dumps(result).encode('utf-8')
            self.wfile.write(response_data)
            
        except Exception as e:
            # Handle errors
            error_result = {
                "success": False,
                "error": f"Internal server error in Python: {str(e)}",
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