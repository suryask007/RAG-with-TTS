# import streamlit as st
# import requests
# import io
# import time
# from pydub import AudioSegment
# from pydub.playback import play


# FASTAPI_URL = "http://localhost:8000"

# st.title("AI-Powered Q&A with File Upload")

# uploaded_files = st.file_uploader("Upload PDF", accept_multiple_files=True)

# if uploaded_files:
#     st.success("Files uploaded successfully.")
#     files_to_send = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
#     # print("files_to_send",files_to_send)
    
#     with st.spinner("Processing files..."):
#         response_text = requests.post(f"{FASTAPI_URL}/file_upload", files=files_to_send)
#         response_text_contant=response_text.text
#         # print("responcesss:",response)
        
#     if response_text.status_code == 200:
#         st.success("Files processed successfully!")

# question = st.text_input("Ask a question based on the file")

# if question:
#     if st.button("Get Answer"):
#         with st.spinner("Fetching answer..."):
#             response = requests.post(f"{FASTAPI_URL}/model",params={"input":question,"files":response_text_contant})
#             # response = requests.post(f"{FASTAPI_URL}/model",data={"input": question},files=files_to_send if uploaded_files else None,)
#             # print("responcesss1:",response.json())
            
#         if response.status_code == 200:
#             # answer = response.json().get("answer", "No answer found")
#             text_response=response.text
#             st.write("**Answer:**", text_response)

#             if st.button("Get Audio Answer"):
#                 with st.spinner("Generating audio..."):
#                     audio_response = requests.get(f"{FASTAPI_URL}/audio", params={"text":text_response})
#                     print("udio:",audio_response.content)
#                     if audio_response.status_code == 200:
#                         audio_bytes = io.BytesIO(audio_response.content)
#                         # audio_bytes.seek(0)  # Reset buffer position

#                         # # Debugging: Save the file locally to check if it's valid
#                         # with open("debug_audio.mp3", "wb") as f:
#                         #     f.write(audio_response.content)
#                         st.audio(audio_bytes, format="audio/mp3")

#                         # Play audio (if pydub is available)
#                         try:
#                             sound = AudioSegment.from_file(audio_bytes, format="mp3")
#                             play(sound)
#                         except Exception as e:
#                             st.warning("Audio playback not supported in Streamlit. Download instead.")
#                     else:
#                         st.error("Failed to generate audio.")






import streamlit as st
import requests
import io
import time
from pydub import AudioSegment
from pydub.playback import play

FASTAPI_URL = "http://localhost:8000"

st.title("AI-Powered Q&A with File Upload")

# Initialize session state for uploaded files
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = None

uploaded_files = st.file_uploader("Upload PDF", accept_multiple_files=True)

if uploaded_files:
    st.session_state.uploaded_files = uploaded_files  # Store files in session state
    st.success("Files uploaded successfully.")

# Use stored files if available
if st.session_state.uploaded_files:
    files_to_send = [("files", (file.name, file.getvalue(), file.type)) for file in st.session_state.uploaded_files]
    
    with st.spinner("Processing files..."):
        response_text = requests.post(f"{FASTAPI_URL}/file_upload", files=files_to_send)
        response_text_content = response_text.text

    if response_text.status_code == 200:
        st.session_state.response_text_content = response_text_content  # Store response
        st.success("Files processed successfully!")

question = st.text_input("Ask a question based on the file")

if question:
    if st.button("Get Answer"):
        with st.spinner("Fetching answer..."):
            response = requests.post(f"{FASTAPI_URL}/model", params={"input": question, "files": st.session_state.response_text_content})
        
        if response.status_code == 200:
            text_response = response.text
            st.session_state.text_response = text_response  # Store answer
            st.write("**Answer:**", text_response)

# Ensure the button is available only if an answer exists
if "text_response" in st.session_state:
    print(st.session_state)
    if st.button("Get Audio Answer"):
        with st.spinner("Generating audio..."):
            audio_response = requests.get(f"{FASTAPI_URL}/audio", params={"text": st.session_state.text_response})
            
            if audio_response.status_code == 200:
                audio_bytes = io.BytesIO(audio_response.content)
                st.audio(audio_bytes, format="audio/mp3")

                try:
                    sound = AudioSegment.from_file(audio_bytes, format="mp3")
                    play(sound)
                except Exception:
                    st.warning("Audio playback not supported in Streamlit. Download instead.")
            else:
                st.error("Failed to generate audio.")
