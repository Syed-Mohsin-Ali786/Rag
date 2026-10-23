from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import IngestResponse
from app.services.ingestion import ingest_document

router = APIRouter()

@router.post("/ingest", response_model=IngestResponse)
def ingest(file: UploadFile = File(...)):
    data = file.file.read()
    count = ingest_document(file.filename, data)
    if count == 0:
        raise HTTPException(400, "No extractable text found in file.")
    return IngestResponse(filename=file.filename, chunks_stored=count)