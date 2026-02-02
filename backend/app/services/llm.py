import os
from groq import Groq
from app.services.embeddings import search

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(question: str) -> str:
    chunks = search(question, k=3)

    if not chunks:
        return "I don't know"

    context = "\n\n".join(chunks)

    prompt = f"""
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=300,
    )

    return response.choices[0].message.content.strip()
