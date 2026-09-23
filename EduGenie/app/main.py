from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import get_settings
from .explanation_module import explain_topic
from .learning_path import get_learning_recommendations
from .qna import answer_question
from .quiz_module import generate_quiz
from .schemas import (
    AnswerResponse,
    ExplanationResponse,
    LearningPathRequest,
    LearningPathResponse,
    QuizResponse,
    SummaryResponse,
    TextRequest,
    TopicRequest,
)
from .summary_module import summarize_text

BASE_DIR = Path(__file__).resolve().parent.parent
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Google Gemini powered educational learning assistant.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.app_name},
    )


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "gemini_configured": bool(settings.gemini_api_key),
        "gemini_model": settings.gemini_model,
        "explanation_provider": settings.explanation_provider,
    }


@app.post("/qa", response_model=AnswerResponse)
async def qa(request: TextRequest):
    try:
        return AnswerResponse(answer=answer_question(request.text))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/explain", response_model=ExplanationResponse)
async def explain(request: TopicRequest):
    try:
        return ExplanationResponse(explanation=explain_topic(request.topic))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/quiz", response_model=QuizResponse)
async def quiz(request: TextRequest):
    try:
        return QuizResponse(questions=generate_quiz(request.text))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/summarize", response_model=SummaryResponse)
async def summarize(request: TextRequest):
    try:
        return SummaryResponse(summary=summarize_text(request.text))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/learn/recommendations", response_model=LearningPathResponse)
async def learning_path(request: LearningPathRequest):
    try:
        result = get_learning_recommendations(request.topic, request.level)
        return LearningPathResponse(
            topic=request.topic,
            level=request.level,
            recommendations=result,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
