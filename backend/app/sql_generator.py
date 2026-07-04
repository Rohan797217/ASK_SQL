"""
AskSQL SQL Generator
Builds prompts with schema context and few-shot examples,
sends to LLM, and extracts clean SQL from the response.
"""

import re
import logging
from typing import Optional

from app.schema_rag import retrieve_relevant_schema
from app.llm_providers import invoke_with_fallback
from app.guardrails import validate_sql, ValidationResult

logger = logging.getLogger(__name__)


# ============================================
# System prompt for SQL generation
# ============================================
SYSTEM_PROMPT = """You are an expert SQL assistant for a PostgreSQL database. Your job is to convert natural language questions into accurate, efficient SQL queries.

RULES:
1. Generate ONLY a single SELECT query — never use INSERT, UPDATE, DELETE, DROP, or any DDL/DML.
2. Use ONLY the tables and columns described in the schema context below. Do not hallucinate table or column names.
3. Use proper PostgreSQL syntax (e.g., use || for string concatenation, ILIKE for case-insensitive matching).
4. Always use table aliases for readability (e.g., `orders o`, `products p`).
5. When calculating revenue or totals from order_details, use: unit_price * quantity * (1 - discount)
6. If the question is ambiguous, make reasonable assumptions and note them.
7. Return ONLY the SQL query — no explanations, no markdown fences, no commentary.

DATABASE SCHEMA:
{schema_context}
"""

# ============================================
# Few-shot examples for better accuracy
# ============================================
FEW_SHOT_EXAMPLES = """
EXAMPLES:

Question: "How many customers are from Germany?"
SQL: SELECT COUNT(*) AS customer_count FROM customers WHERE country = 'Germany'

Question: "What are the top 5 products by total revenue?"
SQL: SELECT p.product_name, SUM(od.unit_price * od.quantity * (1 - od.discount)) AS total_revenue FROM order_details od JOIN products p ON od.product_id = p.product_id GROUP BY p.product_name ORDER BY total_revenue DESC LIMIT 5

Question: "Show me all orders that haven't been shipped yet"
SQL: SELECT o.order_id, c.company_name, o.order_date, o.required_date FROM orders o JOIN customers c ON o.customer_id = c.customer_id WHERE o.shipped_date IS NULL ORDER BY o.order_date

Question: "How many orders were placed each month?"
SQL: SELECT DATE_TRUNC('month', o.order_date) AS month, COUNT(*) AS order_count FROM orders o GROUP BY DATE_TRUNC('month', o.order_date) ORDER BY month

Question: "Which employees have handled the most orders and what is the total freight?"
SQL: SELECT e.first_name || ' ' || e.last_name AS employee_name, e.title, COUNT(o.order_id) AS total_orders, SUM(o.freight) AS total_freight FROM employees e JOIN orders o ON e.employee_id = o.employee_id GROUP BY e.employee_id, e.first_name, e.last_name, e.title ORDER BY total_orders DESC
"""


def _build_prompt(question: str, schema_context: str) -> str:
    """Build the full prompt with system instructions, schema, examples, and question."""
    system = SYSTEM_PROMPT.format(schema_context=schema_context)

    full_prompt = f"""{system}

{FEW_SHOT_EXAMPLES}

Now answer this question:

Question: "{question}"
SQL:"""

    return full_prompt


def _extract_sql(response: str) -> str:
    """
    Extract clean SQL from the LLM response.
    Handles common LLM output quirks like markdown fences, explanations, etc.
    """
    text = response.strip()

    # Remove markdown code fences
    # Match ```sql\n...\n``` or ```\n...\n```
    code_block_match = re.search(
        r"```(?:sql)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL | re.IGNORECASE
    )
    if code_block_match:
        text = code_block_match.group(1).strip()
    else:
        # If no code block, try to find SQL by looking for SELECT/WITH
        lines = text.split("\n")
        sql_lines = []
        in_sql = False

        for line in lines:
            stripped = line.strip().upper()
            if stripped.startswith(("SELECT", "WITH", "(SELECT")):
                in_sql = True
            if in_sql:
                sql_lines.append(line)
                # Check if we've reached the end of the SQL
                if stripped.endswith(";"):
                    break

        if sql_lines:
            text = "\n".join(sql_lines)

    # Clean up
    text = text.strip().rstrip(";").strip()

    return text


def _generate_explanation(question: str, sql: str) -> str:
    """Generate a brief explanation of what the SQL query does."""
    # Simple heuristic-based explanation (avoids extra LLM call)
    explanation_parts = []

    sql_upper = sql.upper()

    if "JOIN" in sql_upper:
        # Count joins
        join_count = sql_upper.count("JOIN")
        explanation_parts.append(f"Joins {join_count + 1} tables")

    if "GROUP BY" in sql_upper:
        explanation_parts.append("with aggregation")

    if "WHERE" in sql_upper:
        explanation_parts.append("with filters applied")

    if "ORDER BY" in sql_upper:
        if "DESC" in sql_upper:
            explanation_parts.append("sorted in descending order")
        else:
            explanation_parts.append("sorted")

    if "LIMIT" in sql_upper:
        limit_match = re.search(r"LIMIT\s+(\d+)", sql_upper)
        if limit_match:
            explanation_parts.append(f"limited to {limit_match.group(1)} results")

    if explanation_parts:
        return f"Query: {' '.join(explanation_parts)}."
    return "Retrieves the requested data from the database."


def generate_sql(
    question: str, retry_on_failure: bool = True
) -> tuple[str, str, str, Optional[str]]:
    """
    Generate SQL from a natural language question.

    Pipeline:
      1. Retrieve relevant schema via RAG
      2. Build prompt with schema + few-shot examples
      3. Send to LLM (with fallback across providers)
      4. Extract clean SQL from response
      5. Validate with guardrails
      6. Retry once if validation fails

    Args:
        question: Natural language question
        retry_on_failure: Whether to retry with error feedback if first attempt fails

    Returns:
        Tuple of (validated_sql, explanation, provider_name, error_or_none)
    """
    try:
        # Step 1: Retrieve relevant schema context
        schema_context = retrieve_relevant_schema(question)
        logger.info(f"Retrieved schema context ({len(schema_context)} chars)")

        # Step 2: Build prompt
        prompt = _build_prompt(question, schema_context)

        # Step 3: Send to LLM
        response, provider = invoke_with_fallback(prompt)
        logger.info(f"LLM response from {provider}: {response[:200]}...")

        # Step 4: Extract SQL
        sql = _extract_sql(response)

        if not sql:
            return "", "Could not generate SQL.", provider, "The AI could not generate a valid SQL query. Please try rephrasing your question."

        # Step 5: Validate with guardrails
        validation = validate_sql(sql)

        if not validation.is_valid and retry_on_failure:
            # Step 6: Retry with error feedback
            logger.info(f"First attempt failed validation: {validation.error}. Retrying...")

            retry_prompt = f"""{prompt}

IMPORTANT: Your previous attempt generated invalid SQL. The error was:
{validation.error}

Previous (invalid) SQL:
{sql}

Please fix the SQL and try again. Remember: only SELECT queries are allowed.
SQL:"""

            response, provider = invoke_with_fallback(retry_prompt)
            sql = _extract_sql(response)

            if sql:
                validation = validate_sql(sql)

        if not validation.is_valid:
            return sql, "", provider, validation.error

        # Generate explanation
        explanation = _generate_explanation(question, validation.sql)

        warning_suffix = f" ({validation.warning})" if validation.warning else ""

        return validation.sql, explanation + warning_suffix, provider, None

    except Exception as e:
        logger.error(f"SQL generation failed: {e}")
        return "", "", "none", str(e)
