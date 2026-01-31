from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# FAISS setup
EMBEDDING_DIM = 384
index = faiss.IndexFlatL2(EMBEDDING_DIM)

# Store original chunks (for retrieval)
texts = []


def add_texts(chunks: list[str]):
    global texts

    if not chunks:
        return

    embeddings = model.encode(chunks, convert_to_numpy=True)

    index.add(embeddings)
    texts.extend(chunks)


def search(query: str, k: int = 3):
    if index.ntotal == 0:
        return []

    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, k)

    results = []
    for idx in indices[0]:
        if idx < len(texts):
            results.append(texts[idx])

    return results
