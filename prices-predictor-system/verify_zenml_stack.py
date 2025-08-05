from zenml.client import Client
from zenml.integrations.mlflow.experiment_trackers.mlflow_experiment_tracker import MLFlowExperimentTracker
from zenml.integrations.mlflow.model_deployers.mlflow_model_deployer import MLFlowModelDeployer

def main():
    # Initialize the ZenML client
    client = Client()
    
    print("\n=== Current Stack ===")
    try:
        active_stack = client.active_stack
        print(f"Active stack: {active_stack.name}")
        print(f"Components: {list(active_stack.components.keys())}")
    except Exception as e:
        print(f"Error getting active stack: {e}")
    
    # Check if MLflow experiment tracker exists
    print("\n=== MLflow Experiment Tracker ===")
    try:
        trackers = client.get_stack_components(component_type="experiment_tracker")
        mlflow_tracker = next((t for t in trackers if t.flavor == "mlflow"), None)
        if mlflow_tracker:
            print(f"Found MLflow experiment tracker: {mlflow_tracker.name}")
        else:
            print("No MLflow experiment tracker found. Registering one...")
            mlflow_tracker = MLFlowExperimentTracker(
                name="mlflow_tracker",
                tracking_uri="http://127.0.0.1:5000"
            )
            mlflow_tracker._register()
            print(f"Registered new MLflow experiment tracker: {mlflow_tracker.name}")
    except Exception as e:
        print(f"Error with experiment tracker: {e}")
    
    # Check if MLflow model deployer exists
    print("\n=== MLflow Model Deployer ===")
    try:
        deployers = client.get_stack_components(component_type="model_deployer")
        mlflow_deployer = next((d for d in deployers if d.flavor == "mlflow"), None)
        if mlflow_deployer:
            print(f"Found MLflow model deployer: {mlflow_deployer.name}")
        else:
            print("No MLflow model deployer found. Registering one...")
            mlflow_deployer = MLFlowModelDeployer(
                name="mlflow",
                workers=1,
                timeout=30,
            )
            mlflow_deployer._register()
            print(f"Registered new MLflow model deployer: {mlflow_deployer.name}")
    except Exception as e:
        print(f"Error with model deployer: {e}")
    
    # Create or update the stack
    print("\n=== Updating Stack ===")
    try:
        stack_name = "local-mlflow-stack"
        stack = client.get_stack(name=stack_name)
        print(f"Updating existing stack: {stack_name}")
    except KeyError:
        print(f"Creating new stack: {stack_name}")
        stack = None
    
    try:
        components = {
            "experiment_tracker": "mlflow_tracker",
            "model_deployer": "mlflow"
        }
        
        if stack:
            client.update_stack(
                name_id_or_prefix=stack_name,
                component_updates=components
            )
        else:
            client.create_stack(
                name=stack_name,
                components=components,
                is_shared=False,
            )
        
        # Set the stack as active
        client.activate_stack(stack_name)
        print(f"Stack '{stack_name}' is now active with MLflow components")
    except Exception as e:
        print(f"Error updating stack: {e}")
    
    # Verify the active stack
    print("\n=== Verification ===")
    try:
        active_stack = client.active_stack
        print(f"Active stack: {active_stack.name}")
        print("Components:")
        for comp_type, comp in active_stack.components.items():
            print(f"  - {comp_type}: {comp.name} ({comp.flavor if hasattr(comp, 'flavor') else 'N/A'})")
    except Exception as e:
        print(f"Error verifying stack: {e}")

if __name__ == "__main__":
    main()
