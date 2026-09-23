from .gemini_service import gemini_service


def get_learning_recommendations(topic: str, level: str) -> str:
    prompt = f"""
Create a structured learning path for a student who wants to learn "{topic}".

Current level: {level}

Include:
1. Goal
2. Prerequisites
3. Ordered stages from the current level toward advanced understanding
4. Suggested timeline for each stage
5. Practice activities or mini-projects
6. Suggested resource types (videos, documentation, articles, books)
7. A simple checkpoint to know when to move to the next stage

Keep the plan practical and concise. Do not invent specific URLs.
"""
    return gemini_service.generate(prompt, temperature=0.4, max_output_tokens=1500)
