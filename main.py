from fastapi.responses import StreamingResponse
from src.pdf_rag import fun_rag,load_pdf
from fastapi import FastAPI,UploadFile,File,middleware
from typing import Annotated
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from src.text_speech import text_speech
import logging 
logging.basicConfig(level=logging.INFO)
origins = [
    "*"
]
app=FastAPI()
# These lines configure CORS middleware to allow cross-origin requests from any origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/file_upload")
async def file_up(files:list[UploadFile]):
    rag_file=await load_pdf(files)
    return rag_file

@app.post("/model")
async def main(input,files):
    rag_file=await fun_rag(input,files)
    return rag_file

@app.get("/audio")
# @app.route("/audio", methods=["GET", "POST"])
async def audio(text:str):
    # audio_data=text_speech(text)
    # return StreamingResponse(audio_data, media_type='audio/mp3')
    logging.info(f"Received text: {text}")
    audio_data = text_speech(text)
    
    # Log size of the audio data
    audio_data_size = audio_data.getbuffer().nbytes
    logging.info(f"Audio data size: {audio_data_size} bytes")
    
    return StreamingResponse(audio_data, media_type='audio/mpeg')



if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)


