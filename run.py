import subprocess
import sys
import time

def main():
    print("Starting FastAPI Backend...")
    backend = subprocess.Popen([sys.executable, "-m", "uvicorn", "api.main:app", "--reload"])
    
    time.sleep(2) # Wait for backend to start
    
    print("Starting Streamlit Frontend...")
    frontend = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app.py"])
    
    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        backend.terminate()
        frontend.terminate()

if __name__ == "__main__":
    main()
