from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from app.services.embeddings import search
import torch

MODEL_NAME = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def generate_answer(question: str) -> str:
    # 1. Retrieve relevant chunks
    chunks = search(question, k=3)

    if not chunks:
        return "No relevant information found in the document."

    # 2. Build context (LIMIT SIZE)
    context = "\n".join(chunks)
    context = context[:1200]  # VERY IMPORTANT

    # 3. Prompt
    prompt = f"""
Answer the question based on the context below.

Context:
{context}

Question:
{question}

Answer:
"""

    # 4. Tokenize
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    # 5. Generate
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=128,
            do_sample=False
        )

    # 6. Decode
    answer = tokenizer.decode(output[0], skip_special_tokens=True)
    return answer.strip()
