"""
AskSQL LLM Providers
Multi-provider LLM routing with automatic fallback:
  Gemini (primary) → Groq (backup) → Ollama (local fallback)
"""

import logging
from typing import Optional

from langchain_core.language_models import BaseChatModel

from app.config import settings

logger = logging.getLogger(__name__)


def _get_gemini() -> Optional[BaseChatModel]:
    """Initialize Google Gemini provider."""
    if not settings.google_api_key:
        logger.warning("GOOGLE_API_KEY not set — Gemini unavailable")
        return None
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.google_api_key,
            temperature=0,
            max_output_tokens=2048,
        )
    except Exception as e:
        logger.error(f"Failed to initialize Gemini: {e}")
        return None


def _get_groq() -> Optional[BaseChatModel]:
    """Initialize Groq provider."""
    if not settings.groq_api_key:
        logger.warning("GROQ_API_KEY not set — Groq unavailable")
        return None
    try:
        from langchain_groq import ChatGroq

        return ChatGroq(
            model=settings.groq_model,
            api_key=settings.groq_api_key,
            temperature=0,
            max_tokens=2048,
        )
    except Exception as e:
        logger.error(f"Failed to initialize Groq: {e}")
        return None


def _get_ollama() -> Optional[BaseChatModel]:
    """Initialize Ollama (local) provider."""
    try:
        from langchain_ollama import ChatOllama

        llm = ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=0,
            num_predict=2048,
        )
        return llm
    except ImportError:
        logger.info("langchain-ollama not installed — Ollama unavailable (install with: pip install langchain-ollama)")
        return None
    except Exception as e:
        logger.error(f"Failed to initialize Ollama: {e}")
        return None


# Provider registry: ordered by priority
PROVIDERS = [
    ("gemini", _get_gemini),
    ("groq", _get_groq),
    ("ollama", _get_ollama),
]


def get_available_providers() -> list[str]:
    """Return list of available provider names based on configured API keys."""
    available = []
    for name, init_fn in PROVIDERS:
        if name == "gemini" and settings.google_api_key:
            available.append(name)
        elif name == "groq" and settings.groq_api_key:
            available.append(name)
        elif name == "ollama":
            available.append(name)  # Ollama is always "available" (local)
    return available


def invoke_with_fallback(prompt: str) -> tuple[str, str]:
    """
    Send a prompt to the LLM, trying providers in priority order.
    Falls back to the next provider if the current one fails.

    Args:
        prompt: The full prompt to send to the LLM

    Returns:
        Tuple of (response_text, provider_name)

    Raises:
        RuntimeError: If all providers fail
    """
    errors = []

    for name, init_fn in PROVIDERS:
        try:
            llm = init_fn()
            if llm is None:
                continue

            logger.info(f"Trying LLM provider: {name}")
            response = llm.invoke(prompt)

            # Extract text content
            if hasattr(response, "content"):
                text = response.content
            else:
                text = str(response)

            logger.info(f"✅ Got response from {name} ({len(text)} chars)")
            return text, name

        except Exception as e:
            error_msg = f"{name}: {str(e)}"
            errors.append(error_msg)
            logger.warning(f"Provider {name} failed: {e}")
            continue

    # All providers failed
    error_detail = "\n".join(f"  - {e}" for e in errors)
    raise RuntimeError(
        f"All LLM providers failed:\n{error_detail}\n\n"
        "Please check your API keys in the .env file."
    )
