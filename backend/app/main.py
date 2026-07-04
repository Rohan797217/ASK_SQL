"""
AskSQL — FastAPI Backend
Main application entry point with /ask and /health endpoints.
"""

import logging
from contextlib import asynccontextmanager
from datetime import date, datetime
from decimal import Decimal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import os

from app.config import settings
from app.models import AskRequest, AskResponse, HealthResponse
from app.database import check_connection, execute_query
from app.schema_rag import initialize_rag, is_initialized
from app.sql_generator import generate_sql
from app.guardrails import format_error_for_user
from app.llm_providers import get_available_providers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)-20s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ============================================
# Application Lifespan (startup/shutdown)
# ============================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize RAG system on startup."""
    logger.info("=" * 60)
    logger.info("🚀 AskSQL starting up...")
    logger.info("=" * 60)

    # Check database connection
    db_status = check_connection()
    logger.info(f"Database: {db_status}")

    # Initialize RAG
    try:
        initialize_rag()
        logger.info("Schema RAG: initialized")
    except Exception as e:
        logger.error(f"Schema RAG initialization failed: {e}")
        logger.warning("The app will start but /ask requests will fail until RAG is initialized")

    # Show available providers
    providers = get_available_providers()
    logger.info(f"LLM providers available: {', '.join(providers) if providers else 'NONE'}")

    logger.info("=" * 60)
    logger.info("✅ AskSQL ready! Docs at http://localhost:8000/docs")
    logger.info("=" * 60)

    yield  # App runs

    logger.info("AskSQL shutting down...")


# ============================================
# FastAPI App
# ============================================
app = FastAPI(
    title="AskSQL",
    description=(
        "Text-to-SQL AI Assistant — Ask questions in plain English, "
        "get SQL queries and real results from a PostgreSQL database."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow React frontend (local dev + production)
_cors_origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # Alternative dev port
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]
# Add production frontend URL if set
_frontend_url = os.getenv("FRONTEND_URL", "")
if _frontend_url:
    _cors_origins.append(_frontend_url.rstrip("/"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _serialize_value(val):
    """Convert non-JSON-serializable types to serializable ones."""
    if isinstance(val, Decimal):
        return float(val)
    if isinstance(val, (date, datetime)):
        return val.isoformat()
    return val


# ============================================
# Endpoints
# ============================================
@app.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """
    Ask a natural language question about the database.

    The pipeline:
    1. Retrieves relevant schema via RAG
    2. Generates SQL using an LLM
    3. Validates with guardrails
    4. Executes against PostgreSQL
    5. Returns SQL + results
    """
    question = request.question.strip()
    logger.info(f"📝 Question: {question}")

    # Check RAG is initialized
    if not is_initialized():
        raise HTTPException(
            status_code=503,
            detail="Schema RAG system is not initialized. Please restart the server.",
        )

    # Step 1-3: Generate and validate SQL
    sql, explanation, provider, error = generate_sql(question)

    if error:
        logger.warning(f"SQL generation error: {error}")
        return AskResponse(
            question=question,
            sql=sql or "",
            error=error,
            explanation=explanation,
            provider=provider,
        )

    logger.info(f"🔍 Generated SQL ({provider}): {sql}")

    # Step 4: Execute the query
    try:
        result = execute_query(sql)

        # Serialize values for JSON response
        serialized_rows = [
            {k: _serialize_value(v) for k, v in row.items()} for row in result["rows"]
        ]

        logger.info(f"✅ Query returned {result['row_count']} rows")

        return AskResponse(
            question=question,
            sql=sql,
            results=serialized_rows,
            columns=result["columns"],
            row_count=result["row_count"],
            explanation=explanation,
            provider=provider,
        )

    except TimeoutError as e:
        logger.warning(f"Query timeout: {e}")
        return AskResponse(
            question=question,
            sql=sql,
            error=str(e),
            explanation=explanation,
            provider=provider,
        )
    except Exception as e:
        logger.error(f"Query execution failed: {e}")
        friendly_error = format_error_for_user(str(e))
        return AskResponse(
            question=question,
            sql=sql,
            error=friendly_error,
            explanation=explanation,
            provider=provider,
        )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check the health of all system components."""
    db_status = check_connection()
    providers = get_available_providers()

    return HealthResponse(
        status="healthy" if db_status == "connected" else "degraded",
        database=db_status,
        rag_initialized=is_initialized(),
        available_providers=providers,
    )


@app.get("/")
async def root():
    """Root endpoint — redirect to docs."""
    return {
        "app": "AskSQL",
        "version": "1.0.0",
        "description": "Text-to-SQL AI Assistant",
        "docs": "/docs",
        "health": "/health",
    }
