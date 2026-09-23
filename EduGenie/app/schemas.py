from typing import Literal

from pydantic import BaseModel, Field, field_validator


class TextRequest(BaseModel):
    text: str = Field(..., min_length=2)

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        return value.strip()


class TopicRequest(BaseModel):
    topic: str = Field(..., min_length=2)

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value: str) -> str:
        return value.strip()


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=2)
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value: str) -> str:
        return value.strip()


class AnswerResponse(BaseModel):
    answer: str


class ExplanationResponse(BaseModel):
    explanation: str


class SummaryResponse(BaseModel):
    summary: str


class LearningPathResponse(BaseModel):
    topic: str
    level: str
    recommendations: str


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(..., min_length=4, max_length=4)
    answer: str
    explanation: str = ""


class QuizResponse(BaseModel):
    questions: list[QuizQuestion]
