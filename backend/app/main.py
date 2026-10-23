from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import ingest, chat

app = FastAPI(title="RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React Router dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router, prefix="/api", tags=["ingest"])
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/health")
def health():
    return {"status": "ok"}