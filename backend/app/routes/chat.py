from fastapi import APIRouter
from pydantic import BaseModel
from app.services.embeddings import search
from app.services.llm import generate_answer

router = APIRouter(prefix="/chat", tags=["Chat"])


class Question(BaseModel):
    question: str


@router.post("/ask")
def ask_question(q: Question):
    chunks = search(q.question, k=3)

    if not chunks:
        return {"question": q.question, "answer": "I don't know"}

    context = "\n".join(chunks)
    answer = generate_answer(context, q.question)

    return {
        "question": q.question,
        "answer": answer
    }
