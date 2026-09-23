from .config import get_settings
from .gemini_service import gemini_service


def explain_topic(topic: str) -> str:
    settings = get_settings()
    provider = settings.explanation_provider.lower().strip()

    if provider in {"local", "auto"}:
        try:
            from .local_explanation import explain_locally
            return explain_locally(topic)
        except Exception:
            if provider == "local":
                raise

    prompt = f"""
You are EduGenie, an educational assistant.

Explain this topic to a beginner: {topic}

Requirements:
- Start with a one-sentence definition.
- Explain the idea using simple language.
- Give one practical or everyday example.
- Mention 2-4 key points.
- Avoid unnecessary jargon.
- Keep the response concise and suitable for a student.
"""
    return gemini_service.generate(prompt, temperature=0.3, max_output_tokens=700)
