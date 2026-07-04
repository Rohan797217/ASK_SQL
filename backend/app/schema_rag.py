"""
AskSQL Schema RAG
Embeds table/column descriptions into Chroma vector store and retrieves
relevant schema context for a given natural language question.
"""

import json
import os
import logging

import chromadb
from chromadb.config import Settings as ChromaSettings
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

from app.config import settings

logger = logging.getLogger(__name__)

# Module-level state
_chroma_client = None
_collection = None
_embedding_fn = None


def _get_embedding_fn():
    """Lazy-load Chroma's built-in embedding function (uses ONNXRuntime, no PyTorch needed)."""
    global _embedding_fn
    if _embedding_fn is None:
        logger.info("Loading embedding model (ONNXRuntime all-MiniLM-L6-v2)...")
        _embedding_fn = DefaultEmbeddingFunction()
        logger.info("✅ Embedding model loaded")
    return _embedding_fn


def _embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a list of texts using Chroma's built-in embedding function."""
    fn = _get_embedding_fn()
    return fn(texts)


def _load_schema_descriptions() -> list[dict]:
    """Load schema descriptions from the JSON file."""
    data_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
    )
    schema_file = os.path.join(data_dir, "schema_descriptions.json")

    with open(schema_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def _build_documents(schema_data: dict) -> tuple[list[str], list[str], list[dict]]:
    """
    Build document chunks from schema descriptions.
    Each table becomes one document with all its column descriptions.

    Returns:
        (documents, ids, metadatas)
    """
    documents = []
    ids = []
    metadatas = []

    for table in schema_data["tables"]:
        # Build a rich text document for this table
        doc_parts = [
            f"Table: {table['table_name']}",
            f"Description: {table['description']}",
            "",
            "Columns:",
        ]

        for col in table["columns"]:
            doc_parts.append(
                f"  - {col['name']} ({col['type']}): {col['description']}"
            )

        if table.get("sample_questions"):
            doc_parts.append("")
            doc_parts.append("Example questions this table can answer:")
            for q in table["sample_questions"]:
                doc_parts.append(f"  - {q}")

        document = "\n".join(doc_parts)
        documents.append(document)
        ids.append(f"table_{table['table_name']}")
        metadatas.append({"table_name": table["table_name"]})

    # Add relationship info as a separate document
    if schema_data.get("relationships"):
        rel_doc = "Database Relationships:\n" + "\n".join(
            f"  - {r}" for r in schema_data["relationships"]
        )
        documents.append(rel_doc)
        ids.append("relationships")
        metadatas.append({"table_name": "_relationships"})

    # Add common patterns as a document
    if schema_data.get("common_patterns"):
        patterns_parts = ["Common SQL Patterns:"]
        for name, pattern in schema_data["common_patterns"].items():
            patterns_parts.append(f"  - {name}: {pattern}")
        patterns_doc = "\n".join(patterns_parts)
        documents.append(patterns_doc)
        ids.append("common_patterns")
        metadatas.append({"table_name": "_patterns"})

    return documents, ids, metadatas


def initialize_rag():
    """
    Initialize the RAG system:
    1. Load schema descriptions
    2. Embed them with sentence-transformers
    3. Store in Chroma
    """
    global _chroma_client, _collection

    logger.info("Initializing Schema RAG system...")

    # Load schema descriptions
    schema_data = _load_schema_descriptions()

    # Build documents
    documents, ids, metadatas = _build_documents(schema_data)

    # Initialize Chroma
    _chroma_client = chromadb.Client(
        ChromaSettings(
            persist_directory=settings.chroma_persist_dir,
            anonymized_telemetry=False,
        )
    )

    # Delete existing collection if it exists (re-index on startup)
    try:
        _chroma_client.delete_collection("schema_descriptions")
    except Exception:
        pass

    _collection = _chroma_client.create_collection(
        name="schema_descriptions",
        metadata={"hnsw:space": "cosine"},
    )

    # Embed and add documents
    embeddings = _embed_texts(documents)

    _collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas,
    )

    logger.info(
        f"✅ Schema RAG initialized with {len(documents)} documents in Chroma"
    )


def retrieve_relevant_schema(question: str, top_k: int = None) -> str:
    """
    Given a natural language question, retrieve the most relevant
    table/column descriptions from the vector store.

    Args:
        question: The user's natural language question
        top_k: Number of most relevant documents to retrieve

    Returns:
        Formatted string of relevant schema information
    """
    if _collection is None:
        raise RuntimeError("RAG system not initialized. Call initialize_rag() first.")

    if top_k is None:
        top_k = settings.schema_top_k

    # Embed the question
    question_embedding = _embed_texts([question])[0]

    # Query Chroma
    results = _collection.query(
        query_embeddings=[question_embedding],
        n_results=min(top_k, _collection.count()),
    )

    # Format results
    if not results["documents"] or not results["documents"][0]:
        return "No relevant schema information found."

    schema_context = "\n\n---\n\n".join(results["documents"][0])

    return schema_context


def is_initialized() -> bool:
    """Check if the RAG system has been initialized."""
    return _collection is not None
