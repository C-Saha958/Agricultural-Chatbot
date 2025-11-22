import requests
from app.core.config import settings
from app.core.prompts import SYSTEM_PROMPT

# Import specific exceptions for better handling
from requests.exceptions import Timeout, RequestException

def get_groq_response(message, history=None):
    # Safety check: If key is empty, return error immediately
    if not settings.GROQ_API_KEY:
        return "Error: Groq API Key is missing. Check the backend terminal for 'FATAL ERROR' message."
        
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # If history exists, append it to the messages array
    if history:
        for msg in history:
            # FIX: Access dictionary keys 'role' and 'content' instead of numeric indices 0 and 1
            # We assume Gradio history elements are dictionaries like {'role': 'user', 'content': '...'}.
            # We also use a conditional check to ensure we only process valid messages.
            if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                 messages.append({
                    "role": msg["role"].lower(),  # Access by key
                    "content": msg["content"]     # Access by key
                })
            # NOTE: If your Gradio history is a list of lists/tuples [role, content], 
            # the previous version was correct. This fix assumes it's dicts.

    # Append the latest user message
    messages.append({"role": "user", "content": message})

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
            json={"model": settings.MODEL, "messages": messages},
            # CRITICAL FIX: Add explicit timeout (15s), shorter than the frontend's 20s timeout
            timeout=15
        )
        response.raise_for_status() # Raise exception for bad status codes (4xx or 5xx)
        
        # Return the generated content
        return response.json()["choices"][0]["message"]["content"]
    
    except Timeout:
        # Handle the specific timeout from the backend request
        return "Error: Groq API request timed out after 15 seconds. The model may be busy or your connection is slow."
    except RequestException as e:
        # Handle connection errors or bad status codes from the API
        status_code = response.status_code if 'response' in locals() else 'N/A'
        if status_code == 401:
            return "Authentication Error: The Groq API Key is invalid or expired. Please check your .env file."
        return f"Error connecting to Groq API: {e}. Status Code: {status_code}"
    except Exception as e:
        # Handle parsing errors or unexpected issues
        return f"An unexpected error occurred during API response processing: {e}"