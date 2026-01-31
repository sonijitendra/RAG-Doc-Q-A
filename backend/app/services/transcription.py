from faster_whisper import WhisperModel
import os

model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)

def transcribe_audio(file_path: str) -> str:
    if not os.path.exists(file_path):
        return ""

    segments, _ = model.transcribe(file_path)
    text = " ".join(seg.text for seg in segments)
    return text.strip()
