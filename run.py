import subprocess
import webbrowser
import time
import os
import sys
import uvicorn


def run_application():
    print("Starting BGMI Account Marketplace...")
    
    # Get the path to uvicorn executable
    # uvicorn_path = os.path.join(os.path.dirname(sys.executable), "Scripts", "uvicorn")
    
    # Start backend server
    # backend_process = subprocess.Popen(
    #     [sys.executable, "-m", "uvicorn", "app.main:app", "--reload"],
    #     cwd="backend"
    # )
    
    # Wait for server to start
    # time.sleep(2)
    
    # Open frontend in browser
    # frontend_path = os.path.abspath("frontend/index.html")
    # webbrowser.open(f"file://{frontend_path}")
    
    # print("\nApplication is running!")
    # print("Backend API: http://localhost:8000")
    # print(f"Frontend: {frontend_path}")
    # print("\nPress Ctrl+C to stop the application")
    
    try:
        uvicorn.run(
            "backend.app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            workers=1
        )
    except KeyboardInterrupt:
        print("\nApplication stopped")

if __name__ == "__main__":
    run_application()
