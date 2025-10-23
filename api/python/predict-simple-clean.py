from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse JSON data
            input_data = json.loads(post_data.decode('utf-8'))
            
            # Simple rule-based prediction
            age = input_data.get('Age', 30)
            income = input_data.get('MonthlyIncome', 5000)
            overtime = input_data.get('OverTime', 'No')
            
            # Simple scoring
            risk_score = 0.0
            if age < 25 or age > 55:
                risk_score += 0.3
            if income < 3000:
                risk_score += 0.4
            if overtime == 'Yes':
                risk_score += 0.3
            
            probability = min(risk_score, 0.9)
            prediction = 1 if probability > 0.5 else 0
            
            result = {
                "success": True,
                "prediction": prediction,
                "prediction_label": "Will Leave" if prediction == 1 else "Will Stay",
                "probability": {
                    "will_stay": 1 - probability,
                    "will_leave": probability
                },
                "risk_level": "High" if probability > 0.7 else "Medium" if probability > 0.4 else "Low",
                "confidence": max(probability, 1 - probability),
                "model_type": "Simple Rule-Based (Vercel Serverless)"
            }
            
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
                "error": f"Error: {str(e)}"
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