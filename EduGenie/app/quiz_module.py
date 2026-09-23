from pydantic import TypeAdapter

from .config import get_settings
from .gemini_service import gemini_service
from .schemas import QuizQuestion


def generate_quiz(text: str) -> list[QuizQuestion]:
    settings = get_settings()
    schema = list[QuizQuestion]  # used as documentation; JSON mode is validated below

    prompt = f"""
Create a student-friendly multiple-choice quiz from the material below.

Rules:
- Generate exactly 3 questions.
- Each question must have exactly 4 distinct options.
- "answer" must exactly match one option.
- Include a short explanation for the correct answer.
- Questions must be answerable from the supplied material or basic reasoning directly related to it.
- Return ONLY a JSON array. No Markdown fences.

Each array item must have:
{{
  "question": "...",
  "options": ["...", "...", "...", "..."],
  "answer": "...",
  "explanation": "..."
}}

Material:
{text[:settings.max_input_chars]}
"""
    raw = gemini_service.generate(
        prompt,
        temperature=0.5,
        max_output_tokens=1400,
        response_mime_type="application/json",
    )

    try:
        data = TypeAdapter(list[QuizQuestion]).validate_json(raw)
    except Exception as exc:
        raise RuntimeError(f"Gemini returned invalid quiz JSON: {exc}") from exc

    if not data:
        raise RuntimeError("Gemini returned an empty quiz.")

    for item in data:
        if item.answer not in item.options:
            raise RuntimeError("A quiz answer did not match one of its options.")

    return data[: settings.max_quiz_questions]
