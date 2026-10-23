from pydantic import BaseModel, Field

class IngestResponse(BaseModel):
    filename: str
    chunks_stored: int

class ChatRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=20)

class SourceChunk(BaseModel):
    text: str
    source: str
    chunk_index: int
    score: float

class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]