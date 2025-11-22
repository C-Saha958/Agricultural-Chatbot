from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from app.services.groq_service import get_groq_response

router = APIRouter()


class ChatRequest(BaseModel):
    history: List[Dict]  # [{"role": "user", "content": "..."}]

class ChatResponse(BaseModel):
    response: str


# -------------------------------
# /chat endpoint (TEXT ONLY)
# -------------------------------
@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):

    history = req.history
    user_message = history[-1]["content"]

    llm_reply = get_groq_response(user_message, history)

    return ChatResponse(response=llm_reply)
