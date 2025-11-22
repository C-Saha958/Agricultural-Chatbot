from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: Optional[str] = None         # text input
    message_audio: Optional[str] = None   # base64 audio (optional)
    language: str = "en"                  # "en" or "hi"

class ChatResponse(BaseModel):
    reply_text: str
    reply_audio: str                      # base64 audio