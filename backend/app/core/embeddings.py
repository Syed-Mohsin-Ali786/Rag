from openai import OpenAI
from app.config import settings

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.openrouter_api_key,
)

def embed_text(texts: list[str]) -> list[list[float]]:
    """Embed a batch of text chunks. Returns list of vectors."""
    response = client.embeddings.create(
        model=settings.embedding_model,
        input=texts,
    )
    return [item.embedding for item in response.data]

def embed_query(query: str) -> list[float]:
    """Embed a single query string."""
    return embed_text([query])[0]