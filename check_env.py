import sys
import platform
import os

def print_divider():
    print("-" * 80)

print("\nPython Environment Information:")
print_divider()
print(f"Python executable: {sys.executable}")
print(f"Python version: {platform.python_version()}")
print(f"System: {platform.system()} {platform.release()} {platform.version()}")
print(f"Working directory: {os.getcwd()}")

print("\nPython Path:")
print_divider()
for path in sys.path:
    print(f"- {path}")

print("\nTrying to import ZenML...")
try:
    import zenml
    print_divider()
    print(f"ZenML version: {zenml.__version__}")
    print("ZenML is installed and working correctly!")
    
    # Try to initialize ZenML
    print("\nTrying to initialize ZenML...")
    try:
        zenml_client = zenml.Client()
        print("ZenML client initialized successfully!")
        print(f"ZenML server URL: {zenml_client.zen_store.url}")
    except Exception as e:
        print(f"Error initializing ZenML client: {e}")
        
except ImportError as e:
    print_divider()
    print(f"Error importing ZenML: {e}")
    print("\nPlease make sure ZenML is installed in your Python environment.")
    print("You can install it using: pip install zenml")
