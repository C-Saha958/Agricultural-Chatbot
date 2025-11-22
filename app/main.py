from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes_chat import router as chat_router
from app.api.v1.routes_voice import router as voice_router

app = FastAPI(title="AgriBot API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api/v1")
app.include_router(voice_router, prefix="/api/v1")
