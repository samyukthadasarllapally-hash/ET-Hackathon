from fastapi import APIRouter
from pydantic import BaseModel
from services.llm import ask_llm

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    zone_id: str = "z001"
    language: str = "en"

@router.post("/query")
def chat_query(request: ChatRequest):
    answer = ask_llm(request.query)
    return {
        "answer": answer,
        "sources": [
            {"doc": "WHO Air Quality Guidelines", "section": "2.1"},
            {"doc": "CPCB Standards",             "section": "4.2"}
        ]
    }
