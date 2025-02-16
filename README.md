AI-Powered Q&A with File Upload

This is a Streamlit-based web application that allows users to upload PDF files, ask questions based on the content, and receive both text and audio answers using a FastAPI backend.

Features

Upload PDF Files: Users can upload multiple PDFs for processing.

File Processing via FastAPI: The backend extracts information from PDFs.

AI-Powered Q&A: Users can ask questions based on the uploaded PDFs, and the system returns answers.

Text-to-Speech (TTS) Support: Converts the answer into audio format for playback.

Prerequisites

Ensure you have the following installed:

Python 3.8+

pip (Python package manager)

Installation

Clone the repository:

git clone https://github.com/suryask007/RAG-with-TTS.git
cd RAG-with-TTS

Install the required dependencies:

pip install -r requirements.txt

Running the Application

Run the root.py script, which starts both FastAPI and Streamlit:

python root.py

Usage

Upload PDFs: Click on the upload button and select PDF files.

Process Files: The app sends the files to FastAPI for processing.

Ask a Question: Enter a question related to the uploaded files.

Get Text Answer: The model will return an answer based on the PDFs.

Generate Audio Answer: Click on "Get Audio Answer" to listen to the response.

API Endpoints

POST /file_upload → Uploads and processes PDFs.

POST /model → Takes a question and returns an answer.

GET /audio → Converts the text answer to an audio response.

Troubleshooting

App restarts on button clicks: This is due to Streamlit's rerun behavior. The app uses st.session_state to prevent reprocessing on every button click.

FastAPI Not Running: Ensure FastAPI is running before launching Streamlit.

Audio Not Playing: If pydub fails, download the file manually from the UI.



Contributors: Surya K (surya.tvm.apm@gmail.com)