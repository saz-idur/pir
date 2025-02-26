from pydantic import BaseModel
from typing import List, Dict

class ChatRequest(BaseModel):
    model: str = "pir"
    messages: List[Dict]
    stream: bool = False

class ChatResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Dict]
    usage: Dict