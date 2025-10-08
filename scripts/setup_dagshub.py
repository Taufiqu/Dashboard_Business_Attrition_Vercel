"""
Setup script untuk konfigurasi DagsHub dan MLflow
"""

import os
import getpass
from pathlib import Path

def setup_dagshub_config():
    print("🔧 DagsHub & MLflow Configuration Setup")
    print("=" * 50)
    
    # Check if .env already exists
    env_file = Path('.env')
    env_example_file = Path('.env.example')
    
    if env_file.exists():
        print("⚠️  .env file already exists")
        overwrite = input("Do you want to overwrite it? (y/N): ").lower().strip()
        if overwrite != 'y':
            print("Setup cancelled")
            return
    
    print("\n📝 Please provide your DagsHub credentials:")
    
    # Get user input
    dagshub_username = input("DagsHub Username: ").strip()
    if not dagshub_username:
        dagshub_username = "Taufiqu"  # Default
        
    print(f"\n💡 To get your DagsHub token:")
    print("   1. Go to https://dagshub.com/user/settings/tokens")
    print("   2. Create a new token")
    print("   3. Copy the token value")
    
    dagshub_token = getpass.getpass("DagsHub Token (input hidden): ").strip()
    
    model_name = input("\nModel name in MLflow (default: attrition_model): ").strip()
    if not model_name:
        model_name = "attrition_model"
    
    # Create .env file
    env_content = f"""# DagsHub Configuration
DAGSHUB_USERNAME={dagshub_username}
DAGSHUB_TOKEN={dagshub_token}

# MLflow Tracking Configuration  
MLFLOW_TRACKING_USERNAME={dagshub_username}
MLFLOW_TRACKING_PASSWORD={dagshub_token}

# Model Configuration
DEFAULT_MODEL_NAME={model_name}

# Dashboard Configuration (Optional)
NEXT_PUBLIC_DASHBOARD_TITLE="Business Attrition Analytics"
NEXT_PUBLIC_COMPANY_NAME="AttritionAI"
NEXT_PUBLIC_REFRESH_INTERVAL=15
NEXT_PUBLIC_ENABLE_EXPORT=true
NEXT_PUBLIC_ENABLE_NOTIFICATIONS=true
"""
    
    # Write .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print(f"\n✅ Configuration saved to .env file")
    print(f"🔐 Your credentials are now set up")
    
    # Test connection
    print(f"\n🧪 Testing connection...")
    try:
        # Import here to avoid issues if packages not installed
        import sys
        sys.path.append('.')
        
        from utils.model_util import MLflowModelManager
        
        manager = MLflowModelManager()
        models = manager.list_registered_models()
        
        print(f"✅ Connection successful!")
        print(f"📋 Found {len(models)} models in registry")
        
        if models:
            print("Models found:")
            for model in models:
                print(f"   - {model['name']}")
        else:
            print("💡 No models found. Make sure you have models registered in MLflow")
            
    except Exception as e:
        print(f"❌ Connection test failed: {str(e)}")
        print("💡 This might be normal if you haven't installed Python dependencies yet")
        print("   Run: pip install -r requirements.txt")
    
    print(f"\n🎉 Setup complete!")
    print(f"📖 Next steps:")
    print(f"   1. Install Python dependencies: pip install -r requirements.txt")
    print(f"   2. Test the setup: python scripts/test_model_util.py")
    print(f"   3. Add models to your MLflow registry if you haven't already")

if __name__ == "__main__":
    setup_dagshub_config()