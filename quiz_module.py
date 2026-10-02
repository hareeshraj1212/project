import json
from typing import List

from pydantic import BaseModel, Field, field_validator

from gemini_client import generate_json


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str

    @field_validator("correct_answer")
    @classmethod
    def correct_answer_must_be_option(cls, value: str, info):
        options = info.data.get("options", [])
        if options and value not in options:
            raise ValueError("correct_answer must exactly match one option")
        return value


class Quiz(BaseModel):
    questions: List[QuizQuestion] = Field(min_length=3, max_length=3)


def clean_json_block(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines).strip()
    return raw


def generate_quiz(passage: str) -> dict:
    prompt = f"""Create exactly 3 multiple-choice questions from the passage below.
Each question must test information supported by the passage.
Every question must have exactly 4 distinct options and one correct answer.
The correct_answer field must exactly equal one option.
Add a short explanation for the correct answer.

PASSAGE:
{passage}
"""
    raw = clean_json_block(generate_json(prompt, Quiz))
    try:
        quiz = Quiz.model_validate(json.loads(raw))
    except Exception as exc:
        raise RuntimeError(f"Quiz JSON could not be validated: {exc}") from exc
    return quiz.model_dump()
