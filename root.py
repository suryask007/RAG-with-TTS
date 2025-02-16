import subprocess
import time
# Define the commands to run FastAPI and Streamlit
fastapi_command = ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
streamlit_command = ["streamlit", "run", "app.py"]

# Start FastAPI
fastapi_process = subprocess.Popen(fastapi_command)
time.sleep(3)  # Wait a few seconds to ensure FastAPI starts first

# Start Streamlit
streamlit_process = subprocess.Popen(streamlit_command)

# Wait for both processes to finish
try:
    fastapi_process.wait()
    streamlit_process.wait()
except KeyboardInterrupt:
    print("Shutting down processes...")
    fastapi_process.terminate()
    streamlit_process.terminate()