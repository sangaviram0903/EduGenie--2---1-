from .config import get_settings
from .gemini_service import gemini_service


def summarize_text(text: str) -> str:
    settings = get_settings()
    prompt = f"""
Summarize the following educational passage for a student.

Requirements:
- Preserve the important facts and meaning.
- Remove repetition and unnecessary detail.
- Use clear headings or bullet points when useful.
- Keep the summary substantially shorter than the source.
- Do not add facts that are not supported by the passage.

Passage:
{text[:settings.max_input_chars]}
"""
    return gemini_service.generate(prompt, temperature=0.2, max_output_tokens=900)
