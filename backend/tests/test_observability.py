"""Unit tests for Observability and LangSmith configuration."""

import os

from backend.app.config.settings import settings
from backend.app.observability import logger, setup_langsmith_tracing


def test_langsmith_tracing_without_key():
    settings.LANGSMITH_API_KEY = ""
    settings.LANGSMITH_TRACING = False
    setup_langsmith_tracing()
    assert os.environ.get("LANGCHAIN_TRACING_V2") == "false"


def test_langsmith_tracing_with_key():
    settings.LANGSMITH_API_KEY = "lsv2_dummy_key_12345"
    settings.LANGSMITH_TRACING = True
    setup_langsmith_tracing()
    assert os.environ.get("LANGCHAIN_TRACING_V2") == "true"
    assert os.environ.get("LANGCHAIN_API_KEY") == "lsv2_dummy_key_12345"

    # Reset
    settings.LANGSMITH_API_KEY = ""
    settings.LANGSMITH_TRACING = False
    setup_langsmith_tracing()


def test_logger_instance():
    assert logger is not None
    logger.info("Test log event", test_key="test_value")
