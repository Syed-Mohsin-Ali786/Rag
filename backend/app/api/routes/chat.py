from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.retrieval import answer_query

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    return answer_query(req.query, req.top_k)