"""
AskSQL Database Layer
Handles PostgreSQL connections and read-only query execution with timeout.
"""

import logging
from contextlib import contextmanager

import psycopg2
import psycopg2.extras
import psycopg2.extensions

from app.config import settings

logger = logging.getLogger(__name__)


def get_connection():
    """Create a new database connection."""
    if not settings.database_url:
        raise ConnectionError(
            "DATABASE_URL is not set. Please configure it in your .env file."
        )
    conn = psycopg2.connect(settings.database_url)
    return conn


def check_connection() -> str:
    """Test database connectivity. Returns status string."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        return "connected"
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return f"error: {str(e)}"


def execute_query(sql: str, timeout: int = None) -> dict:
    """
    Execute a read-only SQL query against the database.

    Args:
        sql: The SQL query to execute (must be SELECT only — enforced by guardrails)
        timeout: Query timeout in seconds (defaults to settings.query_timeout)

    Returns:
        dict with keys: columns (list[str]), rows (list[dict]), row_count (int)

    Raises:
        Exception: On connection, timeout, or query errors
    """
    if timeout is None:
        timeout = settings.query_timeout

    conn = None
    try:
        conn = get_connection()

        # Set the connection to read-only mode (defense in depth)
        conn.set_session(readonly=True, autocommit=True)

        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Set statement timeout (in milliseconds)
        cur.execute(f"SET statement_timeout = {timeout * 1000}")

        # Execute the query
        cur.execute(sql)

        # Fetch results
        columns = [desc[0] for desc in cur.description] if cur.description else []
        rows = cur.fetchall()

        # Convert RealDictRow to regular dicts for JSON serialization
        rows = [dict(row) for row in rows]

        cur.close()

        return {
            "columns": columns,
            "rows": rows,
            "row_count": len(rows),
        }

    except psycopg2.extensions.QueryCanceledError:
        raise TimeoutError(
            f"Query timed out after {timeout} seconds. "
            "Try a more specific question or add filters to narrow results."
        )
    except psycopg2.Error as e:
        logger.error(f"Database error executing query: {e}")
        raise RuntimeError(f"Database error: {e.pgerror or str(e)}")
    finally:
        if conn:
            try:
                conn.close()
            except Exception:
                pass


def init_database():
    """
    Initialize the database with the Northwind schema and sample data.
    Only run this once to set up the database.
    """
    import os

    data_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
    )

    schema_file = os.path.join(data_dir, "northwind_schema.sql")
    data_file = os.path.join(data_dir, "northwind_data.sql")

    conn = get_connection()
    cur = conn.cursor()

    try:
        # Read and execute schema
        with open(schema_file, "r", encoding="utf-8") as f:
            schema_sql = f.read()
        cur.execute(schema_sql)
        conn.commit()
        logger.info("✅ Northwind schema created successfully")

        # Read and execute sample data
        with open(data_file, "r", encoding="utf-8") as f:
            data_sql = f.read()
        cur.execute(data_sql)
        conn.commit()
        logger.info("✅ Northwind sample data loaded successfully")

    except Exception as e:
        conn.rollback()
        logger.error(f"❌ Database initialization failed: {e}")
        raise
    finally:
        cur.close()
        conn.close()
