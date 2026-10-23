from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.config import settings

client = QdrantClient(path=settings.qdrant_path)

def ensure_collection(vector_size: int):
    collections = [c.name for c in client.get_collections().collections]
    if settings.collection_name not in collections:
        client.create_collection(
            collection_name=settings.collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

def upsert_chunks(ids: list[str], vectors: list[list[float]], payloads: list[dict]):
    client.upsert(
        collection_name=settings.collection_name,
        points=[
            PointStruct(id=ids[i], vector=vectors[i], payload=payloads[i])
            for i in range(len(ids))
        ],
    )

def search(query_vector: list[float], top_k: int = 5):
    return client.query_points(
        collection_name=settings.collection_name,
        query=query_vector,
        limit=top_k,
    ).points

def collection_ready() -> bool:
    return client.collection_exists(settings.collection_name)