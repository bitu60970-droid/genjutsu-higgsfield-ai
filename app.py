import os
from typing import Optional

import httpx
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Genjutsu Higgsfield AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1:8b")


class ChatRequest(BaseModel):
    message: str
    system_prompt: Optional[str] = None
    stream: bool = False


@app.get("/")
def root():
    return {
        "name": "Genjutsu Higgsfield AI",
        "status": "online",
        "local_only": True,
        "no_api_key": True,
        "no_credits": True,
        "model": MODEL_NAME,
        "ollama_url": OLLAMA_BASE_URL,
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
async def chat(req: ChatRequest):
    if not req.message or not req.message.strip():
        return {"error": "Message cannot be empty"}

    prompt = req.message.strip()

    if req.system_prompt:
        prompt = f"{req.system_prompt}\n\nUser: {prompt}"

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": req.stream,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        text = data.get("response", "").strip()
        if not text:
            return {"error": "No response from local model"}

        return {
            "reply": text,
            "model": MODEL_NAME,
            "local_only": True,
        }

    except Exception as e:
        return {
            "error": f"Local model failed: {str(e)}",
            "hint": "Make sure Ollama is running and the model is installed: ollama pull llama3.1:8b",
        }
