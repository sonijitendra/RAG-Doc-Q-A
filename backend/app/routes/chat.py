from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm import generate_answer

router = APIRouter(prefix="/chat", tags=["Chat"])

class Question(BaseModel):
    question: str

@router.post("/ask")
def ask_question(q: Question):
    return {"answer": generate_answer(q.question)}
