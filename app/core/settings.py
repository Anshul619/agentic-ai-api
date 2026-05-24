from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "agentic-ai-api"

    GEMINI_API_KEY: str

    GEMINI_MODEL: str = "gemini-2.5-flash"

    REDIS_URL: str

    MEMORY_TTL: int = 86400

    MAX_HISTORY_MESSAGES: int = 20

    DEBUG: bool = True

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()