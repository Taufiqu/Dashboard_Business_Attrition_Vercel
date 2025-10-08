"""
Example script untuk menggunakan model_util.py
"""

import sys
import os
sys.path.append('..')

from utils.model_util import MLflowModelManager, quick_download_model, list_available_models
from config.mlflow_config import DAGSHUB_REPO_OWNER, DAGSHUB_REPO_NAME, DEFAULT_MODEL_NAME

def main():
    print("🚀 MLflow Model Management Example")
    print("=" * 50)
    
    try:
        # Initialize model manager
        print("🔗 Initializing MLflow Model Manager...")
        manager = MLflowModelManager()
        
        # List all registered models
        print("\n📋 Available Models in Registry:")
        models = manager.list_registered_models()
        
        if not models:
            print("❌ No models found in MLflow registry")
            print(f"   Repository: {DAGSHUB_REPO_OWNER}/{DAGSHUB_REPO_NAME}")
            print("   Please make sure you have models registered in MLflow")
            return
        
        for i, model in enumerate(models, 1):
            print(f"{i}. {model['name']}")
            print(f"   Description: {model['description']}")
            print(f"   Created: {model['creation_timestamp']}")
            print()
        
        # Get model versions for first model
        if models:
            model_name = models[0]['name']
            print(f"📊 Versions for '{model_name}':")
            versions = manager.get_model_versions(model_name)
            
            if versions:
                for version in versions:
                    print(f"   Version {version['version']} - Stage: {version['stage']} - Status: {version['status']}")
            else:
                print("   No versions found")
            
            # Download latest model
            try:
                print(f"\n📥 Downloading latest version of '{model_name}'...")
                metadata = manager.download_model(model_name)
                print(f"✅ Downloaded successfully!")
                print(f"   Local path: {metadata['local_path']}")
                print(f"   Version: {metadata['version']}")
                print(f"   Stage: {metadata['stage']}")
                
                # Test loading the downloaded model
                print(f"\n🔄 Testing model loading...")
                model, model_metadata = manager.load_local_model(metadata['local_path'])
                print(f"✅ Model loaded successfully!")
                print(f"   Model type: {type(model)}")
                print(f"   Model metadata: {model_metadata.get('model_type', 'unknown')}")
                
            except Exception as e:
                print(f"❌ Download failed: {str(e)}")
        
        # List local models
        print(f"\n📁 Local Models:")
        local_models = manager.list_local_models()
        
        if local_models:
            for model in local_models:
                print(f"   - {model['model_name']} (v{model.get('version', 'unknown')})")
                print(f"     Downloaded: {model.get('download_timestamp', 'unknown')}")
                print(f"     Path: {model['local_directory']}")
                print()
        else:
            print("   No local models found")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n💡 Troubleshooting:")
        print("   1. Check your DagsHub credentials in .env file")
        print("   2. Verify your repository name and owner")
        print("   3. Make sure you have models registered in MLflow")
        print("   4. Check your internet connection")

if __name__ == "__main__":
    main()