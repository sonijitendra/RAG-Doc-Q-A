from fastapi import APIRouter, UploadFile, File
import os
from PyPDF2 import PdfReader
from app.services.chunker import chunk_text
from app.services.embeddings import add_texts

router = APIRouter(prefix="/files", tags=["File Upload"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    chunks = chunk_text(text)
    add_texts(chunks)

    return {
        "status": "success",
        "filename": file.filename,
        "chunks_added": len(chunks)
    }
