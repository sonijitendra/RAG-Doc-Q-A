import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

dimension = 384
index = faiss.IndexFlatL2(dimension)
stored_chunks = []

def add_texts(chunks):
    global stored_chunks
    embeddings = model.encode(chunks)
    index.add(np.array(embeddings).astype("float32"))
    stored_chunks.extend(chunks)

def search(query, k=3):
    if index.ntotal == 0:
        return []

    q_emb = model.encode([query])
    _, I = index.search(np.array(q_emb).astype("float32"), k)

    return [stored_chunks[i] for i in I[0] if i < len(stored_chunks)]
