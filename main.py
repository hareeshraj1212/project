from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from explanation_module import explain_concept
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie - AI Learning Assistant",
    description="Gemini-powered educational assistant with Q&A, explanations, quizzes, summaries and learning paths.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=30000)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=10000)


class QuizRequest(BaseModel):
    text: str = Field(..., min_length=20, max_length=30000)


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=500)
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"
    hours_per_week: int = Field(default=5, ge=1, le=40)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
async def qa(payload: QuestionRequest):
    try:
        return {"answer": answer_question(payload.question)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/explain")
async def explain(payload: TextRequest):
    try:
        return {"explanation": explain_concept(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/quiz")
async def quiz(payload: QuizRequest):
    try:
        return {"quiz": generate_quiz(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/summarize")
async def summarize(payload: TextRequest):
    try:
        return {"summary": summarize_text(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/learn/recommendations")
async def learning_path(payload: LearningPathRequest):
    try:
        return {
            "recommendations": get_learning_recommendations(
                payload.topic, payload.level, payload.hours_per_week
            )
        }
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
