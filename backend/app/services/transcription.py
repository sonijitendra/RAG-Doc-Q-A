import whisper
import tempfile
import os

_model = whisper.load_model("base")

def transcribe(file_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".media") as tmp:
        tmp.write(file_bytes)
        temp_path = tmp.name

    result = _model.transcribe(temp_path)
    os.remove(temp_path)

    return result["text"]
