import logging
from functools import lru_cache

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_pipeline():
    """
    Lazily load LaMini-Flan-T5-783M so normal application startup stays fast.
    The first local explanation may download the model from Hugging Face.
    """
    from transformers import pipeline

    return pipeline(
        "text2text-generation",
        model="MBZUAI/LaMini-Flan-T5-783M",
        tokenizer="MBZUAI/LaMini-Flan-T5-783M",
        device=-1,
    )


def explain_locally(topic: str) -> str:
    prompt = (
        "Explain the following topic to a beginner in simple language. "
        "Use short paragraphs and, when useful, a small example. "
        f"Topic: {topic}"
    )
    result = get_pipeline()(
        prompt,
        max_new_tokens=220,
        do_sample=False,
    )
    return result[0]["generated_text"].strip()
