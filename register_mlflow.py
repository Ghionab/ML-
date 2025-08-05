from zenml.client import Client
from zenml.integrations.mlflow.experiment_trackers.mlflow_experiment_tracker import MLFlowExperimentTracker
from zenml.integrations.mlflow.model_deployers.mlflow_model_deployer import MLFlowModelDeployer

def main():
    # Initialize the ZenML client
    client = Client()
    
    print("Registering MLflow experiment tracker...")
    try:
        # Register MLflow experiment tracker
        mlflow_tracker = MLFlowExperimentTracker(
            name="mlflow_tracker",
            tracking_uri="http://127.0.0.1:5000"  # Default MLflow UI
        )
        mlflow_tracker._register()
        print("✅ Successfully registered MLflow experiment tracker")
    except Exception as e:
        print(f"❌ Error registering MLflow experiment tracker: {e}")
    
    print("\nRegistering MLflow model deployer...")
    try:
        # Register MLflow model deployer
        mlflow_deployer = MLFlowModelDeployer(
            name="mlflow",
            workers=1,
            timeout=30,
        )
        mlflow_deployer._register()
        print("✅ Successfully registered MLflow model deployer")
    except Exception as e:
        print(f"❌ Error registering MLflow model deployer: {e}")
    
    print("\nRegistering MLflow stack...")
    try:
        # Register the stack
        client.create_stack(
            name="local-mlflow-stack",
            components={
                "experiment_tracker": "mlflow_tracker",
                "model_deployer": "mlflow",
            },
            is_shared=False,
        )
        print("✅ Successfully registered MLflow stack")
    except Exception as e:
        print(f"❌ Error registering MLflow stack: {e}")
    
    print("\nCurrent stack configuration:")
    try:
        active_stack = client.active_stack
        print(f"Active stack: {active_stack.name}" 
              f"(Experiment Tracker: {active_stack.experiment_tracker.name}, "
              f"Model Deployer: {active_stack.model_deployer.name if hasattr(active_stack, 'model_deployer') else 'None'})")
    except Exception as e:
        print(f"❌ Error getting stack information: {e}")

if __name__ == "__main__":
    main()
