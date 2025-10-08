#!/usr/bin/env python3
"""
Test DagsHub connection and MLflow setup
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_dagshub_connection():
    """Test connection to DagsHub repository"""
    print("🔍 Testing DagsHub connection...")
    
    username = os.getenv('DAGSHUB_USERNAME', 'Taufiqu')
    token = os.getenv('DAGSHUB_TOKEN', 'f18642f3d0e8e9ab137f67f4f64a23c372af5d1e')
    repo_url = "https://dagshub.com/Taufiqu/dsp-attrition-model"
    
    print(f"Repository: {repo_url}")
    print(f"Username: {username}")
    print(f"Token: {token[:8]}...{token[-4:]}")
    
    try:
        # Test basic repository access
        response = requests.get(f"{repo_url}/api/v1/repo", 
                              auth=(username, token),
                              timeout=10)
        
        if response.status_code == 200:
            print("✅ DagsHub repository access successful!")
            return True
        else:
            print(f"❌ DagsHub access failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_mlflow_connection():
    """Test MLflow tracking server connection"""
    print("\n🔍 Testing MLflow connection...")
    
    try:
        import mlflow
        
        # Set tracking URI
        tracking_uri = os.getenv('MLFLOW_TRACKING_URI', 'https://dagshub.com/Taufiqu/dsp-attrition-model.mlflow')
        username = os.getenv('DAGSHUB_USERNAME', 'Taufiqu')
        token = os.getenv('DAGSHUB_TOKEN', 'f18642f3d0e8e9ab137f67f4f64a23c372af5d1e')
        
        print(f"MLflow URI: {tracking_uri}")
        
        # Set credentials
        os.environ['MLFLOW_TRACKING_USERNAME'] = username
        os.environ['MLFLOW_TRACKING_PASSWORD'] = token
        
        mlflow.set_tracking_uri(tracking_uri)
        
        # Try to get experiments
        experiments = mlflow.search_experiments()
        print(f"✅ MLflow connection successful!")
        print(f"📊 Found {len(experiments)} experiments")
        
        for exp in experiments:
            print(f"  - {exp.name} (ID: {exp.experiment_id})")
        
        return True
        
    except ImportError:
        print("❌ MLflow not installed. Please run: pip install mlflow")
        return False
    except Exception as e:
        print(f"❌ MLflow connection failed: {e}")
        return False

def test_model_registry():
    """Test MLflow Model Registry access"""
    print("\n🔍 Testing MLflow Model Registry...")
    
    try:
        import mlflow
        from mlflow.tracking import MlflowClient
        
        client = MlflowClient()
        
        # List registered models
        models = client.search_registered_models()
        
        print(f"✅ Model Registry access successful!")
        print(f"🤖 Found {len(models)} registered models")
        
        for model in models:
            print(f"  - {model.name}")
            
            # Get latest version
            try:
                latest_version = client.get_latest_versions(model.name, stages=["None", "Staging", "Production"])
                if latest_version:
                    version = latest_version[0]
                    print(f"    Latest version: {version.version} (Stage: {version.current_stage})")
            except Exception as e:
                print(f"    Could not get versions: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model Registry access failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 DagsHub & MLflow Connection Test")
    print("=" * 40)
    
    # Test DagsHub connection
    dagshub_ok = test_dagshub_connection()
    
    # Test MLflow connection
    mlflow_ok = test_mlflow_connection()
    
    # Test Model Registry
    registry_ok = test_model_registry()
    
    print("\n" + "=" * 40)
    print("📋 Test Summary:")
    print(f"  DagsHub Connection: {'✅' if dagshub_ok else '❌'}")
    print(f"  MLflow Connection:  {'✅' if mlflow_ok else '❌'}")
    print(f"  Model Registry:     {'✅' if registry_ok else '❌'}")
    
    if all([dagshub_ok, mlflow_ok, registry_ok]):
        print("\n🎉 All tests passed! Your setup is ready.")
        return True
    else:
        print("\n❌ Some tests failed. Please check your configuration.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)