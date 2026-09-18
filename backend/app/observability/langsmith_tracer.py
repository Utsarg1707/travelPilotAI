"""Optional LangSmith Tracing Setup."""

import os

from backend.app.config.settings import settings
from backend.app.observability.logger import logger


def setup_langsmith_tracing():
    """Enable LangSmith tracing if LANGSMITH_API_KEY is configured in settings/env.

    If LANGSMITH_API_KEY is absent, tracing remains disabled with zero overhead.
    """
    key = settings.LANGSMITH_API_KEY or os.getenv("LANGSMITH_API_KEY", "")
    tracing_enabled = (
        settings.LANGSMITH_TRACING or os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
    )

    if key and tracing_enabled:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = key
        os.environ["LANGCHAIN_PROJECT"] = settings.LANGSMITH_PROJECT
        logger.info(
            "LangSmith Tracing Enabled",
            project=settings.LANGSMITH_PROJECT,
            tracing=True,
        )
    else:
        os.environ["LANGCHAIN_TRACING_V2"] = "false"
        logger.info(
            "LangSmith Tracing Disabled (Optional API key not set)",
            tracing=False,
        )
