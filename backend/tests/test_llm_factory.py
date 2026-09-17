"""Unit tests for LLMFactory."""

import pytest

from backend.app.config.llm_factory import LLMFactory


def test_is_groq_available():
    # Test checking groq key availability without raising exception
    available = LLMFactory.is_groq_available()
    assert isinstance(available, bool)


def test_get_chat_model_missing_key_raises():
    # If no key is provided, should raise clean ValueError
    with pytest.raises(ValueError, match="GROQ_API_KEY is not configured"):
        LLMFactory.get_chat_model(api_key="")


def test_get_chat_model_with_dummy_key():
    # Should instantiate ChatGroq instance when key is provided
    model = LLMFactory.get_chat_model(api_key="gsk_dummy_test_key_123456789")
    assert model is not None
    assert getattr(model, "model_name", "") == "llama-3.3-70b-versatile"
