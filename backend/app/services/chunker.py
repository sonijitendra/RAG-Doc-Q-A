def chunk_text(text: str):
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    chunks = []
    current = []

    for line in lines:
        # force section-based chunking
        if line.lower().startswith((
            "education",
            "experience",
            "projects",
            "certifications",
            "skills"
        )):
            if current:
                chunks.append(" ".join(current))
                current = []

        current.append(line)

    if current:
        chunks.append(" ".join(current))

    return chunks
