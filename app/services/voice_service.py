# app/services/voice_service.py

import base64
from gtts import gTTS
import speech_recognition as sr
import io

def speech_to_text(audio_file: bytes) -> str:
    recognizer = sr.Recognizer()

    audio_data = sr.AudioFile(io.BytesIO(audio_file))
    with audio_data as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="hi-IN")
        return text
    except Exception:
        return "Could not understand audio."

def text_to_speech(text: str, lang="hi"):
    tts = gTTS(text=text, lang=lang)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)

    return base64.b64encode(audio_bytes.read()).decode("utf-8")
