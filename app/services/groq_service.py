
import requests
from app.core.config import settings
from app.core.prompts import SYSTEM_PROMPT

def get_groq_response(message, history=None):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # if history exists, append it
    if history:
        for msg in history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

    # latest message
    messages.append({"role": "user", "content": message})

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
        json={"model": settings.MODEL, "messages": messages},
    )
    return response.json()["choices"][0]["message"]["content"]


