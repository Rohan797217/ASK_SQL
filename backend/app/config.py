"""
AskSQL Configuration
Loads environment variables and provides typed settings for the application.
"""

import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = os.getenv("DATABASE_URL", "")

    # LLM Providers
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    # Model names
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

    # Safety settings
    max_query_rows: int = int(os.getenv("MAX_QUERY_ROWS", "500"))
    query_timeout: int = int(os.getenv("QUERY_TIMEOUT", "10"))

    # RAG settings
    chroma_persist_dir: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "chroma_db"
    )
    embedding_model: str = "all-MiniLM-L6-v2"
    schema_top_k: int = 5

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
