from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    GEMINI_API_KEY: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    
    
    MISTRAL_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    LLM_PROVIDER_ORDER: str | None = None
    DEFAULT_LLM_PROVIDER: str | None = None
    YOUTUBE_API_KEY: str | None = None
    CHATBOT_MAX_HISTORY: int | None = None
    CHATBOT_CONTEXT_LENGTH: int | None = None
    
    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
