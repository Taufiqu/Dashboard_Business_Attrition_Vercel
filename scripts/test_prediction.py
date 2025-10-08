#!/usr/bin/env python3
"""
Test script untuk model attrition menggunakan model lokal
"""

import json
import sys
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def create_sample_model():
    """Create a sample model for testing"""
    print("Creating sample model for testing...")
    
    # Create sample data
    data = {
        'Age': [25, 35, 45, 28, 52, 33, 41, 29, 37, 44],
        'DistanceFromHome': [1, 8, 2, 3, 24, 4, 6, 10, 12, 18],
        'MonthlyIncome': [2094, 5993, 2909, 4193, 3291, 8896, 2396, 3068, 9526, 5237],
        'YearsAtCompany': [6, 10, 0, 8, 1, 5, 7, 4, 17, 6],
        'JobLevel': [2, 3, 1, 2, 1, 4, 1, 2, 5, 3],
        'OverTime': [1, 0, 1, 1, 0, 0, 1, 0, 0, 1],
        'JobSatisfaction': [4, 2, 3, 4, 2, 4, 1, 3, 3, 2],
        'WorkLifeBalance': [1, 3, 3, 3, 2, 3, 2, 3, 2, 4],
        'Department_Human Resources': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'Department_Research & Development': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'Department_Sales': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'EducationField_Human Resources': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'EducationField_Life Sciences': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'EducationField_Marketing': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'EducationField_Medical': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'EducationField_Other': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'EducationField_Technical Degree': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'MaritalStatus_Divorced': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'MaritalStatus_Married': [0, 1, 0, 1, 1, 1, 0, 1, 1, 1],
        'MaritalStatus_Single': [1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        'Attrition': [1, 0, 1, 0, 1, 0, 1, 0, 0, 1]
    }
    
    df = pd.DataFrame(data)
    
    # Prepare features and target
    X = df.drop('Attrition', axis=1)
    y = df['Attrition']
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/sample_attrition_model.pkl')
    
    # Save feature names
    with open('models/feature_names.json', 'w') as f:
        json.dump(list(X.columns), f)
    
    return model, list(X.columns)

def preprocess_input(input_data, feature_names):
    """Preprocess input data to match model format"""
    
    # Create a dataframe with all required features
    processed_data = pd.DataFrame(columns=feature_names)
    
    # Fill basic features
    for col in ['Age', 'DistanceFromHome', 'MonthlyIncome', 'YearsAtCompany', 
                'JobLevel', 'JobSatisfaction', 'WorkLifeBalance']:
        if col in input_data:
            processed_data.loc[0, col] = float(input_data[col])
    
    # Handle OverTime
    processed_data.loc[0, 'OverTime'] = 1 if input_data.get('OverTime') == 'Yes' else 0
    
    # Handle Department
    dept_columns = [col for col in feature_names if col.startswith('Department_')]
    for col in dept_columns:
        processed_data.loc[0, col] = 0
    
    dept_value = input_data.get('Department', 'Research & Development')
    dept_col = f'Department_{dept_value}'
    if dept_col in processed_data.columns:
        processed_data.loc[0, dept_col] = 1
    
    # Handle EducationField
    edu_columns = [col for col in feature_names if col.startswith('EducationField_')]
    for col in edu_columns:
        processed_data.loc[0, col] = 0
    
    edu_value = input_data.get('EducationField', 'Life Sciences')
    edu_col = f'EducationField_{edu_value}'
    if edu_col in processed_data.columns:
        processed_data.loc[0, edu_col] = 1
    
    # Handle MaritalStatus
    marital_columns = [col for col in feature_names if col.startswith('MaritalStatus_')]
    for col in marital_columns:
        processed_data.loc[0, col] = 0
    
    marital_value = input_data.get('MaritalStatus', 'Single')
    marital_col = f'MaritalStatus_{marital_value}'
    if marital_col in processed_data.columns:
        processed_data.loc[0, marital_col] = 1
    
    # Fill any remaining NaN values with 0
    processed_data = processed_data.fillna(0)
    
    return processed_data

def predict_attrition(input_data):
    """Make prediction using the model"""
    
    try:
        # Try to load existing model
        if os.path.exists('models/sample_attrition_model.pkl'):
            model = joblib.load('models/sample_attrition_model.pkl')
            with open('models/feature_names.json', 'r') as f:
                feature_names = json.load(f)
        else:
            # Create sample model if not exists
            model, feature_names = create_sample_model()
        
        # Preprocess input
        processed_data = preprocess_input(input_data, feature_names)
        
        # Make prediction
        prediction = model.predict(processed_data)[0]
        probability = model.predict_proba(processed_data)[0]
        
        # Get feature importance
        feature_importance = dict(zip(feature_names, model.feature_importances_))
        
        result = {
            'success': True,
            'prediction': int(prediction),
            'attrition_probability': float(probability[1]),  # Probability of attrition (class 1)
            'model_info': {
                'name': 'Sample Random Forest',
                'version': '1.0',
                'type': 'RandomForestClassifier'
            },
            'feature_importance': feature_importance,
            'input_data': input_data
        }
        
        return result
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Prediction failed: {str(e)}',
            'input_data': input_data
        }

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Called from API
        input_data = json.loads(sys.argv[1])
        result = predict_attrition(input_data)
        print(json.dumps(result))
    else:
        # Interactive testing
        print("Testing attrition prediction...")
        
        sample_input = {
            'Age': 35,
            'DistanceFromHome': 10,
            'MonthlyIncome': 5000,
            'YearsAtCompany': 5,
            'JobLevel': 3,
            'OverTime': 'Yes',
            'JobSatisfaction': 2,
            'WorkLifeBalance': 2,
            'Department': 'Research & Development',
            'EducationField': 'Life Sciences',
            'MaritalStatus': 'Married'
        }
        
        result = predict_attrition(sample_input)
        print(json.dumps(result, indent=2))