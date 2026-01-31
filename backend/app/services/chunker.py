def chunk_text(text: str, size: int = 400, overlap: int = 50):
    words = text.split()
    chunks = []

    i = 0
    while i < len(words):
        chunk = words[i : i + size]
        chunks.append(" ".join(chunk))
        i += size - overlap

    return chunks
