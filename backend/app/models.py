"""
AskSQL Pydantic Models
Request and response schemas for the API.
"""

from pydantic import BaseModel, Field
from typing import Optional


class AskRequest(BaseModel):
    """Request body for the /ask endpoint."""

    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Natural language question about the database",
        json_schema_extra={"examples": ["What are the top 5 products by revenue?"]},
    )


class AskResponse(BaseModel):
    """Response body for the /ask endpoint."""

    question: str = Field(description="The original user question")
    sql: str = Field(description="Generated SQL query")
    results: list[dict] = Field(
        default_factory=list, description="Query results as list of row dicts"
    )
    columns: list[str] = Field(
        default_factory=list, description="Column names in result order"
    )
    row_count: int = Field(default=0, description="Number of rows returned")
    explanation: str = Field(
        default="", description="Brief explanation of what the query does"
    )
    error: Optional[str] = Field(
        default=None, description="Error message if something went wrong"
    )
    provider: str = Field(
        default="", description="Which LLM provider generated the SQL"
    )


class HealthResponse(BaseModel):
    """Response body for the /health endpoint."""

    status: str = "healthy"
    database: str = "unknown"
    rag_initialized: bool = False
    available_providers: list[str] = Field(default_factory=list)
