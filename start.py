import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import sklearn
        import transformers
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e.name}")
        print("Installing requirements...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return False

def start_backend():
    """Start the FastAPI backend server"""
    print("\n🚀 Starting backend server...")
    
    # Create necessary directories if they don't exist
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("corpus", exist_ok=True)
    os.makedirs("ipfs_mock", exist_ok=True)
    os.makedirs("blockchain_mock", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server to start
    time.sleep(2)
    print("✅ Backend server running at http://localhost:8000")
    return backend_process

def start_frontend():
    """Open the frontend in the default web browser"""
    frontend_path = Path("frontend/index.html").absolute().as_uri()
    print(f"\n🌐 Opening frontend at {frontend_path}")
    webbrowser.open(frontend_path)

def main():
    print("\n===== Decentralized Academic Plagiarism Checker =====\n")
    
    # Check if requirements are installed
    check_requirements()
    
    # Start backend server
    backend_process = start_backend()
    
    # Start frontend
    start_frontend()
    
    print("\n📝 Application is now running!")
    print("- Backend API: http://localhost:8000")
    print("- Frontend: Open in your browser")
    print("\nPress Ctrl+C to stop the application")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping application...")
        backend_process.terminate()
        print("✅ Application stopped")

if __name__ == "__main__":
    main()