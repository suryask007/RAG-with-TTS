from io import BytesIO
import os
from gtts import gTTS

def text_speech(text):
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        
        # Reset the buffer's position to the start
        audio_buffer.seek(0)
        
        return audio_buffer
    except Exception as e:
        print(e)


        
    # tts.save("welcome.mp3")

    # # Playing the converted file
    # os.system("start welcome.mp3")
# text_speech("I don't know. The provided context does not contain any information about 'pm'.")
        