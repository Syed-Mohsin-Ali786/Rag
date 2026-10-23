import uuid
from io import BytesIO
from pypdf import PdfReader

from app.core.embeddings import embed_text
from app.core import vector_store

CHUNK_SIZE = 800      # characters
CHUNK_OVERLAP = 150
EMBED_BATCH = 32

def extract_text(filename: str, data: bytes) -> str:
    if filename.lower().endswith(".pdf"):
        reader = PdfReader(BytesIO(data))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return data.decode("utf-8", errors="ignore")

def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    text = " ".join(text.split())  # normalize whitespace
    chunks, start = [], 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = end - overlap
    return chunks

def ingest_document(filename: str, data: bytes) -> int:
    text = extract_text(filename, data)
    chunks = chunk_text(text)
    if not chunks:
        return 0

    stored = 0
    for i in range(0, len(chunks), EMBED_BATCH):
        batch = chunks[i : i + EMBED_BATCH]
        vectors = embed_text(batch)
        vector_store.ensure_collection(len(vectors[0]))  # size comes from the model itself
        vector_store.upsert_chunks(
            ids=[str(uuid.uuid4()) for _ in batch],
            vectors=vectors,
            payloads=[
                {"text": c, "source": filename, "chunk_index": i + j}
                for j, c in enumerate(batch)
            ],
        )
        stored += len(batch)
    return stored