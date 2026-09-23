import json
import logging
from typing import Any

from google import genai
from google.genai import types

from .config import get_settings

logger = logging.getLogger(__name__)


class GeminiService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._client: genai.Client | None = None

    @property
    def client(self) -> genai.Client:
        if not self.settings.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. Add it to the .env file."
            )
        if self._client is None:
            self._client = genai.Client(api_key=self.settings.gemini_api_key)
        return self._client

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.4,
        max_output_tokens: int = 1200,
        response_mime_type: str | None = None,
        response_schema: Any | None = None,
    ) -> str:
        config_kwargs: dict[str, Any] = {
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
        }
        if response_mime_type:
            config_kwargs["response_mime_type"] = response_mime_type
        if response_schema:
            config_kwargs["response_schema"] = response_schema

        response = self.client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(**config_kwargs),
        )

        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()


gemini_service = GeminiService()
