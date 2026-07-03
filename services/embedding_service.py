import os
from typing import Any, Dict, List, Optional

import numpy as np


# -----------------------------
# EMBEDDING CONFIGURATION
# -----------------------------

EMBEDDING_MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL_NAME",
    "sentence-transformers/all-MiniLM-L6-v2"
)

EMBEDDING_DIMENSIONS = int(os.getenv("EMBEDDING_DIMENSIONS", "384"))

_embedding_model = None
_embedding_model_error = None


# -----------------------------
# TEXT HELPERS
# -----------------------------

def clean_text(value: Any) -> str:
    if value is None:
        return ""

    if isinstance(value, list):
        return " ".join(str(item) for item in value if item is not None)

    if isinstance(value, dict):
        return " ".join(str(item) for item in value.values() if item is not None)

    return str(value)


def truncate_text(text: str, limit: int = 6000) -> str:
    text = clean_text(text).strip()

    if len(text) <= limit:
        return text

    return text[:limit].rsplit(" ", 1)[0]


def build_embedding_text(document: Dict[str, Any]) -> str:
    """
    Builds one clean text block from any MongoDB document.
    This is used before creating embeddings.

    It supports:
    - knowledge_base
    - documents
    - website_content
    - portal_services
    - portal_departments
    """

    fields = [
        "title",
        "category",
        "section",
        "keywords",
        "summary",
        "description",
        "answer",
        "content",
        "text",
        "content_text",
        "source",
        "action_label",
        "action_url"
    ]

    text_parts = []

    for field in fields:
        value = clean_text(document.get(field, "")).strip()

        if value:
            text_parts.append(f"{field}: {value}")

    final_text = "\n".join(text_parts).strip()

    return truncate_text(final_text, 6000)


# -----------------------------
# MODEL LOADING
# -----------------------------

def get_embedding_model():
    """
    Loads the sentence-transformers model only when needed.
    This avoids loading the model at Flask startup unless vector search is used.
    """

    global _embedding_model
    global _embedding_model_error

    if _embedding_model is not None:
        return _embedding_model

    if _embedding_model_error is not None:
        return None

    try:
        from sentence_transformers import SentenceTransformer

        _embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        return _embedding_model

    except Exception as error:
        _embedding_model_error = str(error)
        return None


def embedding_service_available() -> bool:
    model = get_embedding_model()
    return model is not None


def get_embedding_error() -> Optional[str]:
    return _embedding_model_error


# -----------------------------
# EMBEDDING CREATION
# -----------------------------

def create_text_embedding(text: str) -> Optional[List[float]]:
    """
    Converts text into a vector embedding.

    Returns:
    - list[float] when successful
    - None when model is unavailable or text is empty
    """

    text = clean_text(text).strip()

    if not text:
        return None

    model = get_embedding_model()

    if model is None:
        return None

    try:
        embedding = model.encode(
            text,
            normalize_embeddings=True
        )

        if isinstance(embedding, np.ndarray):
            embedding = embedding.tolist()

        embedding = [float(value) for value in embedding]

        if len(embedding) != EMBEDDING_DIMENSIONS:
            return None

        return embedding

    except Exception:
        return None


def create_document_embedding(document: Dict[str, Any]) -> Optional[List[float]]:
    embedding_text = build_embedding_text(document)
    return create_text_embedding(embedding_text)


def validate_embedding(embedding: Any) -> bool:
    if not isinstance(embedding, list):
        return False

    if len(embedding) != EMBEDDING_DIMENSIONS:
        return False

    try:
        for value in embedding:
            float(value)
        return True
    except Exception:
        return False


def remove_existing_embedding_fields(document: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns a copy of the document without old embedding metadata.
    Useful before rebuilding embeddings.
    """

    cleaned_document = dict(document)

    fields_to_remove = [
        "embedding",
        "embedding_model",
        "embedding_dimensions",
        "embedding_created_at",
        "embedding_source"
    ]

    for field in fields_to_remove:
        cleaned_document.pop(field, None)

    return cleaned_document