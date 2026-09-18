"""Centralized LLM Factory Abstraction for TravelPilot AI."""

import os

from langchain_core.language_models import BaseChatModel
from langchain_groq import ChatGroq

from backend.app.config.settings import settings


class LLMFactory:
    """Factory for instantiating configurable LLM providers (Groq primary)."""

    @staticmethod
    def get_chat_model(
        temperature: float | None = None,
        max_tokens: int | None = None,
        model_name: str | None = None,
        api_key: str | None = None,
    ) -> BaseChatModel:
        """Get an instance of ChatGroq using centralized configuration.

        If GROQ_API_KEY is missing, raises a clear operational exception
        only when caller requests a live LLM model.
        """
        key = (
            api_key
            if api_key is not None
            else (settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY", ""))
        )
        model = model_name or settings.GROQ_MODEL
        temp = temperature if temperature is not None else settings.GROQ_TEMPERATURE
        tokens = max_tokens if max_tokens is not None else settings.GROQ_MAX_TOKENS

        if not key:
            raise ValueError(
                "GROQ_API_KEY is not configured. "
                "Set GROQ_API_KEY in your .env file or environment to enable Groq LLM features."
            )

        return ChatGroq(
            groq_api_key=key,
            model_name=model,
            temperature=temp,
            max_tokens=tokens,
        )

    @staticmethod
    def is_groq_available() -> bool:
        """Check if Groq API key is available in environment/settings."""
        key = settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY", "")
        return bool(key.strip())
