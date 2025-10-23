import sys
import joblib
from pathlib import Path

def check_model_features():
    """Check the actual feature names used in the trained model"""
    try:
        model_dir = Path(__file__).parent.parent / 'models'
        
        model_path = model_dir / 'rf_model.pkl'
        scaler_path = model_dir / 'scaler.pkl'
        
        if not model_path.exists():
            print(f"Model not found at {model_path}")
            return
        
        # Load model and scaler
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        
        # Check if model has feature names
        if hasattr(model, 'feature_names_in_'):
            print("Model feature names:")
            for i, feature in enumerate(model.feature_names_in_):
                print(f"{i+1:2d}. {feature}")
            print(f"\nTotal features: {len(model.feature_names_in_)}")
        else:
            print("Model doesn't have feature_names_in_ attribute")
            print(f"Model expects {model.n_features_in_} features")
        
        # Check scaler features
        if hasattr(scaler, 'feature_names_in_'):
            print("\nScaler feature names:")
            for i, feature in enumerate(scaler.feature_names_in_):
                print(f"{i+1:2d}. {feature}")
        else:
            print("Scaler doesn't have feature_names_in_ attribute")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_model_features()