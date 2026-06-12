# pip install fastapi uvicorn anthropic python-dotenv

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Anthropic Claude API")
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ── Request / Response schemas ──────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    max_tokens: int = 1024

class ChatResponse(BaseModel):
    response: str
    model: str
    input_tokens: int
    output_tokens: int

# ── Routes ───────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "ok", "message": "Anthropic FastAPI Created by Prakash seanpati"}

@app.post("/chatbot")
def chat_stream(req: ChatRequest):
    """Streaming version — returns text chunks as server-sent events."""
    from fastapi.responses import StreamingResponse

    def generate():
        with client.messages.stream(
            model="claude-sonnet-4-5", #claude-sonnet-4.5,opus-4.5
            max_tokens=req.max_tokens,
            messages=[{"role": "user", "content": req.message}],
        ) as stream:
            for text in stream.text_stream:
                yield f"data: {text}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")