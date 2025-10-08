"""
Configuration file for MLflow settings
"""

# DagsHub Configuration
DAGSHUB_REPO_OWNER = "Taufiqu"  # Username DagsHub Anda
DAGSHUB_REPO_NAME = "dsp-attrition-model"   # Nama repository yang benar

# MLflow Configuration
MLFLOW_TRACKING_URI = f"https://dagshub.com/{DAGSHUB_REPO_OWNER}/{DAGSHUB_REPO_NAME}.mlflow"

# Model Configuration
DEFAULT_MODEL_NAME = "attrition_model"  # Nama model di MLflow registry
LOCAL_MODELS_DIR = "models"

# Serving Configuration
MODEL_SERVING_PORT = 5000
MODEL_SERVING_HOST = "0.0.0.0"

# Environment Variables
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# DagsHub Credentials (akan dibaca dari .env file)
DAGSHUB_USERNAME = os.getenv('DAGSHUB_USERNAME', DAGSHUB_REPO_OWNER)
DAGSHUB_TOKEN = os.getenv('DAGSHUB_TOKEN', '')  # DagsHub personal access token
MLFLOW_TRACKING_USERNAME = os.getenv('MLFLOW_TRACKING_USERNAME', DAGSHUB_USERNAME)
MLFLOW_TRACKING_PASSWORD = os.getenv('MLFLOW_TRACKING_PASSWORD', DAGSHUB_TOKEN)

# Validation
if not DAGSHUB_TOKEN:
    print("⚠️  Warning: DAGSHUB_TOKEN not found in environment variables")
    print("   Please set your DagsHub token in .env file for authentication")