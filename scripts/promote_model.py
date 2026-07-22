# promote model

import os
import mlflow

def promote_model():
    # Set up DagsHub credentials for MLflow tracking
    dagshub_token = os.getenv("CAPSTONE_TEST")
    if not dagshub_token:
        raise EnvironmentError("CAPSTONE_TEST environment variable is not set")

    os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

    dagshub_url = os.getenv("DAGSHUB_URL")
    repo_owner = os.getenv("REPO_OWNER")
    repo_name = os.getenv("REPO_NAME")

    # Set up MLflow tracking URI
    mlflow.set_tracking_uri(dagshub_url)

    client = mlflow.MlflowClient()

    model_name = "my_model"
    # Get the latest version in staging
    staging_versions = client.get_latest_versions(
    model_name,
    stages=["Staging"]
)

    if not staging_versions:
        raise Exception(
            f"No model version found in the Staging stage for '{model_name}'. "
            "Run register_model.py first or verify that the model was transitioned to Staging."
        )

    latest_version_staging = staging_versions[0].version

    # Archive the current production model
    prod_versions = client.get_latest_versions(model_name, stages=["Production"])
    for version in prod_versions:
        client.transition_model_version_stage(
            name=model_name,
            version=version.version,
            stage="Archived"
        )

    # Promote the new model to production
    client.transition_model_version_stage(
        name=model_name,
        version=latest_version_staging,
        stage="Production"
    )
    print(f"Model version {latest_version_staging} promoted to Production")

if __name__ == "__main__":
    promote_model()
