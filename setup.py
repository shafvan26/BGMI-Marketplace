import os
import subprocess
import sys

def setup_project():
    print("Setting up BGMI Account Marketplace...")
    
    # Create project structure
    directories = [
        'backend/app',
        'backend/app/routers',
        'frontend/static/css',
        'frontend/static/js',
        'frontend/static/img'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

    # Install requirements
    print("\nInstalling Python dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"])

    print("\nSetup completed successfully!")

if __name__ == "__main__":
    setup_project()
