"""
MLflow Model Utility untuk mendownload dan manage model dari DagsHub
"""

import os
import mlflow
import mlflow.sklearn
import dagshub
import pandas as pd
import joblib
import logging
import requests
from datetime import datetime
import shutil
from pathlib import Path
import json
import sys
sys.path.append('..')

from config.mlflow_config import (
    DAGSHUB_REPO_OWNER, 
    DAGSHUB_REPO_NAME, 
    MLFLOW_TRACKING_URI,
    DAGSHUB_USERNAME,
    DAGSHUB_TOKEN,
    DEFAULT_MODEL_NAME
)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MLflowModelManager:
    """
    Utility class untuk mengambil model ML dari MLflow dan menyimpan ke lokal
    """
    
    def __init__(self, dagshub_repo_owner=None, dagshub_repo_name=None, mlflow_tracking_uri=None):
        """
        Initialize MLflow Model Manager
        
        Args:
            dagshub_repo_owner (str): Owner/username DagsHub repository
            dagshub_repo_name (str): Nama repository DagsHub
            mlflow_tracking_uri (str): MLflow tracking URI (optional)
        """
        self.dagshub_repo_owner = dagshub_repo_owner or DAGSHUB_REPO_OWNER
        self.dagshub_repo_name = dagshub_repo_name or DAGSHUB_REPO_NAME
        self.mlflow_tracking_uri = mlflow_tracking_uri or MLFLOW_TRACKING_URI
        
        # Create models directory
        self.local_models_dir = Path("models")
        self.local_models_dir.mkdir(exist_ok=True)
        
        # Setup MLflow connection
        self._setup_mlflow_connection()
    
    def _setup_mlflow_connection(self):
        """Setup connection ke DagsHub MLflow"""
        try:
            # Set credentials if available
            if DAGSHUB_USERNAME and DAGSHUB_TOKEN:
                os.environ['MLFLOW_TRACKING_USERNAME'] = DAGSHUB_USERNAME
                os.environ['MLFLOW_TRACKING_PASSWORD'] = DAGSHUB_TOKEN
                logger.info("🔐 DagsHub credentials set from environment")
            
            # Initialize DagsHub connection
            dagshub.init(
                repo_owner=self.dagshub_repo_owner, 
                repo_name=self.dagshub_repo_name, 
                mlflow=True
            )
            
            # Set MLflow tracking URI
            mlflow.set_tracking_uri(self.mlflow_tracking_uri)
            
            logger.info(f"✅ Connected to MLflow at: {mlflow.get_tracking_uri()}")
            
            # Test connection
            self._test_connection()
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to MLflow: {str(e)}")
            logger.info("💡 Make sure your DagsHub credentials are correct and repository exists")
            raise
    
    def _test_connection(self):
        """Test MLflow connection"""
        try:
            client = mlflow.tracking.MlflowClient()
            experiments = client.search_experiments(max_results=1)
            logger.info(f"🔗 Connection test successful - Found {len(experiments)} experiments")
        except Exception as e:
            logger.warning(f"⚠️  Connection test failed: {str(e)}")
    
    def list_registered_models(self):
        """
        List semua registered models di MLflow
        
        Returns:
            list: List of registered model names
        """
        try:
            client = mlflow.tracking.MlflowClient()
            registered_models = client.search_registered_models()
            
            model_info = []
            for model in registered_models:
                model_info.append({
                    'name': model.name,
                    'description': model.description or 'No description',
                    'creation_timestamp': model.creation_timestamp,
                    'last_updated_timestamp': model.last_updated_timestamp,
                    'tags': dict(model.tags) if model.tags else {}
                })
            
            logger.info(f"📋 Found {len(model_info)} registered models")
            
            if len(model_info) == 0:
                logger.info("💡 No registered models found. Make sure you have registered models in MLflow")
                
            return model_info
            
        except Exception as e:
            logger.error(f"❌ Error listing models: {str(e)}")
            return []
    
    def get_model_versions(self, model_name):
        """
        Get all versions of a specific model
        
        Args:
            model_name (str): Name of the registered model
            
        Returns:
            list: List of model versions with metadata
        """
        try:
            client = mlflow.tracking.MlflowClient()
            versions = client.search_model_versions(f"name='{model_name}'")
            
            version_info = []
            for version in versions:
                version_info.append({
                    'version': version.version,
                    'stage': version.current_stage,
                    'status': version.status,
                    'creation_timestamp': version.creation_timestamp,
                    'last_updated_timestamp': version.last_updated_timestamp,
                    'run_id': version.run_id,
                    'source': version.source,
                    'description': version.description or 'No description'
                })
            
            # Sort by version number (descending)
            version_info.sort(key=lambda x: int(x['version']), reverse=True)
            
            logger.info(f"📊 Found {len(version_info)} versions for model '{model_name}'")
            return version_info
            
        except Exception as e:
            logger.error(f"❌ Error getting model versions: {str(e)}")
            return []
    
    def download_model(self, model_name, version=None, stage=None, local_path=None):
        """
        Download model from MLflow dan simpan ke lokal
        
        Args:
            model_name (str): Name of the registered model
            version (str): Specific version to download (optional)
            stage (str): Stage to download ('Production', 'Staging', etc.) (optional)
            local_path (str): Custom local path to save model (optional)
            
        Returns:
            dict: Information about downloaded model
        """
        try:
            # Determine model URI
            if version:
                model_uri = f"models:/{model_name}/{version}"
                version_identifier = f"v{version}"
            elif stage:
                model_uri = f"models:/{model_name}/{stage}"
                version_identifier = f"stage_{stage}"
            else:
                model_uri = f"models:/{model_name}/latest"
                version_identifier = "latest"
            
            logger.info(f"📥 Downloading model from: {model_uri}")
            
            # Set local path
            if local_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                local_path = self.local_models_dir / f"{model_name}_{version_identifier}_{timestamp}"
            else:
                local_path = Path(local_path)
            
            # Create directory if not exists
            local_path.mkdir(parents=True, exist_ok=True)
            
            # Download model using MLflow
            try:
                # Try sklearn first
                model = mlflow.sklearn.load_model(model_uri)
                model_type = "sklearn"
            except:
                try:
                    # Try generic MLflow model
                    model = mlflow.pyfunc.load_model(model_uri)
                    model_type = "pyfunc"
                except Exception as e:
                    logger.error(f"❌ Failed to load model: {str(e)}")
                    raise
            
            # Save model using joblib
            model_file_path = local_path / "model.pkl"
            joblib.dump(model, model_file_path)
            
            # Get model metadata
            client = mlflow.tracking.MlflowClient()
            try:
                if version:
                    model_version = client.get_model_version(model_name, version)
                else:
                    latest_versions = client.get_latest_versions(model_name, stages=["Production", "Staging", "None"])
                    model_version = latest_versions[0] if latest_versions else None
            except:
                model_version = None
                logger.warning("⚠️  Could not retrieve model version metadata")
            
            # Prepare metadata
            metadata = {
                'model_name': model_name,
                'version': model_version.version if model_version else 'unknown',
                'stage': model_version.current_stage if model_version else 'unknown',
                'run_id': model_version.run_id if model_version else 'unknown',
                'model_type': model_type,
                'download_timestamp': datetime.now().isoformat(),
                'local_path': str(local_path),
                'model_file': str(model_file_path),
                'mlflow_uri': model_uri,
                'dagshub_repo': f"{self.dagshub_repo_owner}/{self.dagshub_repo_name}",
                'tracking_uri': self.mlflow_tracking_uri
            }
            
            # Save metadata to JSON
            metadata_file = local_path / "metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Create a simple info file
            info_file = local_path / "model_info.txt"
            with open(info_file, 'w') as f:
                f.write(f"Model: {model_name}\n")
                f.write(f"Version: {metadata['version']}\n")
                f.write(f"Stage: {metadata['stage']}\n")
                f.write(f"Downloaded: {metadata['download_timestamp']}\n")
                f.write(f"MLflow URI: {model_uri}\n")
                f.write(f"DagsHub Repo: {metadata['dagshub_repo']}\n")
            
            logger.info(f"✅ Model downloaded successfully to: {local_path}")
            logger.info(f"📄 Model metadata saved to: {metadata_file}")
            
            return metadata
            
        except Exception as e:
            logger.error(f"❌ Error downloading model: {str(e)}")
            raise
    
    def load_local_model(self, local_path):
        """
        Load model dari local path
        
        Args:
            local_path (str): Path to local model directory
            
        Returns:
            tuple: (model, metadata)
        """
        try:
            local_path = Path(local_path)
            
            # Load model
            model_file = local_path / "model.pkl"
            if not model_file.exists():
                raise FileNotFoundError(f"Model file not found: {model_file}")
            
            model = joblib.load(model_file)
            
            # Load metadata
            metadata_file = local_path / "metadata.json"
            metadata = {}
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
            
            logger.info(f"✅ Model loaded successfully from: {local_path}")
            return model, metadata
            
        except Exception as e:
            logger.error(f"❌ Error loading local model: {str(e)}")
            raise
    
    def list_local_models(self):
        """
        List all local models
        
        Returns:
            list: List of local model directories with metadata
        """
        try:
            local_models = []
            
            for model_dir in self.local_models_dir.iterdir():
                if model_dir.is_dir():
                    metadata_file = model_dir / "metadata.json"
                    if metadata_file.exists():
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                        metadata['local_directory'] = str(model_dir)
                        local_models.append(metadata)
                    else:
                        # Basic info if no metadata
                        local_models.append({
                            'local_directory': str(model_dir),
                            'model_name': model_dir.name,
                            'download_timestamp': 'unknown',
                            'version': 'unknown'
                        })
            
            # Sort by download timestamp (newest first)
            local_models.sort(key=lambda x: x.get('download_timestamp', ''), reverse=True)
            
            logger.info(f"📁 Found {len(local_models)} local models")
            return local_models
            
        except Exception as e:
            logger.error(f"❌ Error listing local models: {str(e)}")
            return []
    
    def cleanup_old_models(self, keep_latest=3):
        """
        Cleanup old local models, keep only latest N versions
        
        Args:
            keep_latest (int): Number of latest models to keep per model name
        """
        try:
            local_models = self.list_local_models()
            
            # Group by model name
            model_groups = {}
            for model in local_models:
                name = model.get('model_name', 'unknown')
                if name not in model_groups:
                    model_groups[name] = []
                model_groups[name].append(model)
            
            deleted_count = 0
            
            # Sort and cleanup each group
            for model_name, models in model_groups.items():
                # Sort by download timestamp (newest first)
                models.sort(key=lambda x: x.get('download_timestamp', ''), reverse=True)
                
                # Remove old models
                for old_model in models[keep_latest:]:
                    old_path = Path(old_model['local_directory'])
                    if old_path.exists():
                        shutil.rmtree(old_path)
                        logger.info(f"🗑️ Removed old model: {old_path}")
                        deleted_count += 1
            
            logger.info(f"✅ Cleanup completed, removed {deleted_count} old models, kept latest {keep_latest} versions per model")
            
        except Exception as e:
            logger.error(f"❌ Error during cleanup: {str(e)}")
    
    def get_model_info(self, model_name):
        """
        Get comprehensive info about a model
        
        Args:
            model_name (str): Name of the model
            
        Returns:
            dict: Model information
        """
        try:
            client = mlflow.tracking.MlflowClient()
            
            # Get registered model info
            try:
                registered_model = client.get_registered_model(model_name)
            except:
                logger.error(f"❌ Model '{model_name}' not found in registry")
                return None
            
            # Get versions
            versions = self.get_model_versions(model_name)
            
            # Get latest production model
            production_versions = [v for v in versions if v['stage'] == 'Production']
            latest_production = production_versions[0] if production_versions else None
            
            # Get latest model
            latest_version = versions[0] if versions else None
            
            model_info = {
                'name': registered_model.name,
                'description': registered_model.description or 'No description',
                'tags': dict(registered_model.tags) if registered_model.tags else {},
                'creation_timestamp': registered_model.creation_timestamp,
                'last_updated_timestamp': registered_model.last_updated_timestamp,
                'total_versions': len(versions),
                'latest_version': latest_version,
                'latest_production_version': latest_production,
                'all_versions': versions
            }
            
            return model_info
            
        except Exception as e:
            logger.error(f"❌ Error getting model info: {str(e)}")
            return None

# Convenience functions
def quick_download_model(model_name, version=None, stage=None):
    """
    Quick function to download model
    """
    try:
        manager = MLflowModelManager()
        return manager.download_model(model_name, version=version, stage=stage)
    except Exception as e:
        logger.error(f"❌ Quick download failed: {str(e)}")
        raise

def quick_load_model(local_path):
    """
    Quick function to load local model
    """
    try:
        manager = MLflowModelManager()  
        return manager.load_local_model(local_path)
    except Exception as e:
        logger.error(f"❌ Quick load failed: {str(e)}")
        raise

def list_available_models():
    """
    Quick function to list available models
    """
    try:
        manager = MLflowModelManager()
        return manager.list_registered_models()
    except Exception as e:
        logger.error(f"❌ Failed to list models: {str(e)}")
        return []

if __name__ == "__main__":
    # Test the functionality
    print("🚀 Testing MLflow Model Manager...")
    
    try:
        manager = MLflowModelManager()
        
        # List models
        print("\n📋 Listing registered models...")
        models = manager.list_registered_models()
        
        if models:
            print(f"Found {len(models)} models:")
            for model in models:
                print(f"  - {model['name']}: {model['description']}")
        else:
            print("No models found in registry")
            
        # List local models
        print("\n📁 Listing local models...")
        local_models = manager.list_local_models()
        
        if local_models:
            print(f"Found {len(local_models)} local models:")
            for model in local_models:
                print(f"  - {model['model_name']} (v{model.get('version', 'unknown')})")
        else:
            print("No local models found")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")