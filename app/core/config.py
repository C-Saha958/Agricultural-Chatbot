import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    MODEL: str = "llama-3.3-70b-versatile"

settings = Settings()


# --- DEBUGGING CHECK ---
if not settings.GROQ_API_KEY:
    print("\n\n#####################################################################")
    print("## FATAL ERROR: GROQ_API_KEY NOT LOADED. Check your .env file. ##")
    print("## The .env file must be in the backend/ directory. ##")
    print("#####################################################################\n")
