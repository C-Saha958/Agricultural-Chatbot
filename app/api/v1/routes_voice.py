from fastapi import APIRouter
from app.services.voice_service import speech_to_text
import base64

router = APIRouter()

@router.post("/speech-to-text")
async def speech_to_text_endpoint(payload: dict):
    # accept both camelCase & snake_case
    audio_base64 = payload.get("audio_base64") or payload.get("audioBase64")

    if not audio_base64:
        return {"text": ""}

    # decode base64 audio → raw bytes
    audio_bytes = base64.b64decode(audio_base64)

    # send to speech-to-text model
    text = speech_to_text(audio_bytes)

    return {"text": text}
