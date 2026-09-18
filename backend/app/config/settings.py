"""Centralized Application Configuration for TravelPilot AI."""


from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""

    APP_MODE: str = "demo"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Groq API Configuration
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_TEMPERATURE: float = 0.2
    GROQ_MAX_TOKENS: int = 2048

    # LangSmith Observability
    LANGSMITH_API_KEY: str = ""
    LANGSMITH_TRACING: bool = False
    LANGSMITH_PROJECT: str = "travelpilot-ai"

    # Database Configuration
    DATABASE_URL: str = "sqlite:///./travelpilot.db"

    # CORS Configuration
    CORS_ORIGINS: list[str] | str = ["http://localhost:3000", "http://localhost:5173"]

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS_ORIGINS string or list into valid list of origin URLs."""
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        if isinstance(self.CORS_ORIGINS, str):
            val = self.CORS_ORIGINS.strip()
            if val.startswith("[") and val.endswith("]"):
                import json
                try:
                    res = json.loads(val)
                    if isinstance(res, list):
                        return [str(x) for x in res]
                except Exception:
                    pass
            return [x.strip() for x in val.split(",") if x.strip()]
        return ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Singleton settings instance
settings = Settings()
