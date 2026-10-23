from openai import APIStatusError

from app.core.embeddings import embed_query
from app.core.llm import generate_answer
from app.core import vector_store
from app.models.schemas import ChatResponse, SourceChunk


def answer_query(query: str, top_k: int = 5) -> ChatResponse:
    if not vector_store.collection_ready():
        return ChatResponse(answer="No documents have been ingested yet.", sources=[])

    hits = vector_store.search(embed_query(query), top_k)
    if not hits:
        return ChatResponse(answer="I couldn't find anything relevant.", sources=[])

    try:
        answer = generate_answer(query, [h.payload["text"] for h in hits])
    except APIStatusError as e:
        return ChatResponse(
            answer="The chat model is currently unavailable. Please check the backend configuration and try again later.",
            sources=[],
        )

    sources = [
        SourceChunk(
            text=h.payload["text"],
            source=h.payload["source"],
            chunk_index=h.payload["chunk_index"],
            score=h.score,
        )
        for h in hits
    ]
    return ChatResponse(answer=answer, sources=sources)