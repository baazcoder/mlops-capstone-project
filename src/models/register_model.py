# register model

import json
import mlflow
import logging
from src.logger import logging
import os
import dagshub
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

import warnings
warnings.simplefilter("ignore", UserWarning)
warnings.filterwarnings("ignore")

# Below code block is for production use
# -------------------------------------------------------------------------------------
# Set up DagsHub credentials for MLflow tracking
dagshub_token = os.getenv("CAPSTONE_TEST")
if not dagshub_token:
    raise EnvironmentError("CAPSTONE_TEST environment variable is not set")

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

dagshub_url = os.getenv("DAGSHUB_URL")
mlflow.set_tracking_uri(dagshub_url)
# -------------------------------------------------------------------------------------


# Below code block is for local use
# -------------------------------------------------------------------------------------
# mlflow.set_tracking_uri('https://dagshub.com/baazcoder/mlops-capstone-project.mlflow')
# dagshub.init(repo_owner='baazcoder', repo_name='mlops-capstone-project', mlflow=True)
# -------------------------------------------------------------------------------------


def load_model_info(file_path: str) -> dict:
    """Load the model info from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            model_info = json.load(file)
        logging.debug('Model info loaded from %s', file_path)
        return model_info
    except FileNotFoundError:
        logging.error('File not found: %s', file_path)
        raise
    except Exception as e:
        logging.error('Unexpected error occurred while loading the model info: %s', e)
        raise

def register_model(model_name: str, model_info: dict):
    """Register the model to the MLflow Model Registry."""

    model_uri = f"runs:/{model_info['run_id']}/{model_info['model_path']}"
    print("Registering:", model_uri)

    # Register model
    result = mlflow.register_model(model_uri, model_name)

    client = mlflow.tracking.MlflowClient()

    version = result.version

    print(f"Created version: {version}")

    # Move it to Staging
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage="Staging",
        archive_existing_versions=False
    )

    print(f"Version {version} moved to Staging")

def main():
    try:
         model_info_path = "reports/experiment_info.json"

         model_info = load_model_info(model_info_path)

         register_model("my_model", model_info)
    except Exception as e:
        logging.error('Failed to complete the model registration process: %s', e)
        print(f"Error: {e}")

if __name__ == '__main__':
    main()

