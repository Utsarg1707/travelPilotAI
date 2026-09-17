"""Unit tests for Settings and Configuration."""

from backend.app.config.settings import Settings, settings


def test_default_settings():
    assert settings.APP_MODE == "demo"
    assert settings.GROQ_MODEL == "llama-3.3-70b-versatile"
    assert settings.GROQ_TEMPERATURE == 0.2
    assert settings.GROQ_MAX_TOKENS == 2048
    assert settings.HOST == "0.0.0.0"
    assert settings.PORT == 8000


def test_custom_settings_override():
    custom = Settings(APP_MODE="live", GROQ_TEMPERATURE=0.7)
    assert custom.APP_MODE == "live"
    assert custom.GROQ_TEMPERATURE == 0.7
