"""
AskSQL Guardrails
SQL validation and safety checks to ensure only safe queries are executed.

Implements:
  1. SELECT-only enforcement (reject DDL/DML)
  2. Automatic LIMIT injection
  3. SQL injection pattern detection
  4. Query complexity checks
"""

import re
import logging
from dataclasses import dataclass
from typing import Optional

import sqlparse

from app.config import settings

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of SQL validation."""

    is_valid: bool
    sql: str  # The (possibly modified) SQL
    error: Optional[str] = None
    warning: Optional[str] = None


# Dangerous SQL keywords that indicate non-SELECT operations
BLOCKED_KEYWORDS = [
    "DROP",
    "DELETE",
    "TRUNCATE",
    "ALTER",
    "CREATE",
    "INSERT",
    "UPDATE",
    "GRANT",
    "REVOKE",
    "EXEC",
    "EXECUTE",
    "MERGE",
    "CALL",
    "COPY",
    "VACUUM",
    "REINDEX",
    "CLUSTER",
    "COMMENT",
    "LOCK",
    "SET ROLE",
    "SET SESSION",
    "RESET",
    "DISCARD",
    "REASSIGN",
]

# Suspicious patterns that might indicate SQL injection
INJECTION_PATTERNS = [
    r";\s*(DROP|DELETE|UPDATE|INSERT|ALTER|CREATE|TRUNCATE|GRANT|EXEC)",  # Stacked queries
    r"--\s*$",  # Comment at end (potential injection)
    r"/\*.*?\*/",  # Block comments (potential obfuscation)
    r"xp_\w+",  # Extended stored procedures
    r"UNION\s+ALL\s+SELECT\s+NULL",  # Classic UNION injection probe
    r"0x[0-9a-fA-F]+",  # Hex-encoded values
    r"CHAR\(\d+\)",  # CHAR() obfuscation
    r"CONCAT\(.+\)",  # String concatenation tricks
    r"SLEEP\(\d+\)",  # Time-based injection
    r"BENCHMARK\(\d+",  # MySQL benchmark injection
    r"pg_sleep\(",  # PostgreSQL sleep
    r"WAITFOR\s+DELAY",  # SQL Server delay
    r"INTO\s+(OUT|DUMP)FILE",  # File write attempts
    r"LOAD_FILE\(",  # File read attempts
]


def validate_sql(sql: str) -> ValidationResult:
    """
    Validate a SQL query for safety before execution.

    Checks:
      1. Must be a SELECT statement (no DDL/DML)
      2. No SQL injection patterns
      3. Must have reasonable structure
      4. Auto-injects LIMIT if missing

    Args:
        sql: The SQL query to validate

    Returns:
        ValidationResult with is_valid flag, cleaned SQL, and any error/warning
    """
    if not sql or not sql.strip():
        return ValidationResult(
            is_valid=False,
            sql="",
            error="Empty query. Please try rephrasing your question.",
        )

    # Clean the SQL
    sql = sql.strip()

    # Remove markdown code fences if present (LLMs sometimes wrap SQL in them)
    sql = re.sub(r"^```\w*\n?", "", sql)
    sql = re.sub(r"\n?```$", "", sql)
    sql = sql.strip()

    # Remove trailing semicolons (we add our own)
    sql = sql.rstrip(";").strip()

    # ---- Check 1: Must be a SELECT statement ----
    parsed = sqlparse.parse(sql)
    if not parsed:
        return ValidationResult(
            is_valid=False,
            sql=sql,
            error="Could not parse the SQL query. Please try a different question.",
        )

    first_statement = parsed[0]
    statement_type = first_statement.get_type()

    # sqlparse returns 'SELECT' for select statements
    if statement_type != "SELECT":
        # Also check manually for WITH (CTE) queries which sqlparse may not identify
        normalized = sql.upper().lstrip()
        if not (
            normalized.startswith("SELECT")
            or normalized.startswith("WITH")
            or normalized.startswith("(SELECT")
        ):
            return ValidationResult(
                is_valid=False,
                sql=sql,
                error=(
                    "⚠️ Only SELECT queries are allowed. "
                    "This system is read-only and cannot modify the database. "
                    "Please rephrase your question as a data retrieval query."
                ),
            )

    # ---- Check 2: Blocked keywords anywhere in the query ----
    sql_upper = sql.upper()
    for keyword in BLOCKED_KEYWORDS:
        # Match as whole word (not part of column/table name)
        pattern = r"\b" + keyword + r"\b"
        if re.search(pattern, sql_upper):
            return ValidationResult(
                is_valid=False,
                sql=sql,
                error=(
                    f"⚠️ Query contains blocked keyword '{keyword}'. "
                    "Only read-only SELECT queries are permitted."
                ),
            )

    # ---- Check 3: Check for multiple statements ----
    if len(parsed) > 1:
        return ValidationResult(
            is_valid=False,
            sql=sql,
            error=(
                "⚠️ Multiple SQL statements detected. "
                "Please ask one question at a time."
            ),
        )

    # ---- Check 4: SQL injection pattern detection ----
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, sql, re.IGNORECASE):
            logger.warning(f"SQL injection pattern detected: {pattern} in query: {sql}")
            return ValidationResult(
                is_valid=False,
                sql=sql,
                error=(
                    "⚠️ Suspicious SQL pattern detected. "
                    "The query has been blocked for safety."
                ),
            )

    # ---- Check 5: Auto-inject LIMIT if missing ----
    warning = None
    if not re.search(r"\bLIMIT\b", sql_upper):
        sql = f"{sql}\nLIMIT {settings.max_query_rows}"
        warning = f"Added LIMIT {settings.max_query_rows} to prevent large result sets."

    return ValidationResult(
        is_valid=True,
        sql=sql,
        warning=warning,
    )


def format_error_for_user(error: str) -> str:
    """
    Convert technical database errors into user-friendly messages.
    """
    error_lower = error.lower()

    if "relation" in error_lower and "does not exist" in error_lower:
        return (
            "The query references a table that doesn't exist in the database. "
            "This might be due to a typo in the generated SQL. "
            "Please try rephrasing your question."
        )

    if "column" in error_lower and "does not exist" in error_lower:
        return (
            "The query references a column that doesn't exist. "
            "Please try rephrasing your question with different terms."
        )

    if "syntax error" in error_lower:
        return (
            "The generated SQL has a syntax error. "
            "Please try rephrasing your question more simply."
        )

    if "permission denied" in error_lower:
        return (
            "The database user doesn't have permission for this operation. "
            "Only read queries are allowed."
        )

    if "timeout" in error_lower or "cancel" in error_lower:
        return (
            "The query took too long to execute. "
            "Try asking a more specific question or adding filters."
        )

    return f"Database error: {error}"
