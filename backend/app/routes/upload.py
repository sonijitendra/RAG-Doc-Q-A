from fastapi import APIRouter, UploadFile, File
import os
from PyPDF2 import PdfReader
import whisper

from app.services.chunker import chunk_text
from app.services.embeddings import add_texts

router = APIRouter(prefix="/files", tags=["File Upload"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

whisper_model = whisper.load_model("base")

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    text = ""

    if file.filename.lower().endswith(".pdf"):
        reader = PdfReader(path)
        for p in reader.pages:
            text += p.extract_text() or ""

    elif file.filename.lower().endswith((".mp3", ".wav", ".mp4", ".mkv")):
        result = whisper_model.transcribe(path)
        text = result["text"]

    else:
        return {"error": "Unsupported file type"}

    chunks = chunk_text(text)
    add_texts(chunks)

    return {
        "file": file.filename,
        "chunks_added": len(chunks)
    }
