import os
import time
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import tiktoken

from agent import get_motivation
from auth import api_key_auth
from models import ChatRequest, ChatResponse

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("⚠️ GEMINI_API_KEY is missing! Check the .env file or environment variables.")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def count_tokens(text: str) -> int:
    encoding = tiktoken.get_encoding("gpt2")
    return len(encoding.encode(text))

@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_with_pir(request: ChatRequest, token: str = Depends(api_key_auth)):
    try:
        if not request.messages:
            raise HTTPException(status_code=400, detail="No messages provided.")

        user_message = next((msg["content"] for msg in reversed(request.messages) if msg.get("role") == "user"), None)
        if not user_message:
            raise HTTPException(status_code=400, detail="User message not found.")

        response_text = get_motivation(user_message)

        prompt_tokens = count_tokens(user_message)
        completion_tokens = count_tokens(response_text)

        return {
            "id": f"chatcmpl-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": request.model,
            "choices": [{"message": {"role": "assistant", "content": response_text}, "index": 0}],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/")
def root():
    return {"message": "Pir AI is ready! Use /v1/chat/completions to chat."}
