from typing import Any, Dict, List, Optional

from services.embedding_service import (
    create_text_embedding,
    validate_embedding
)


# -----------------------------
# VECTOR SEARCH CONFIGURATION
# -----------------------------

VECTOR_INDEX_NAME = "vector_index"
VECTOR_FIELD_NAME = "embedding"

VECTOR_SEARCH_LIMIT = 5
VECTOR_NUM_CANDIDATES = 100
VECTOR_MIN_SCORE = 0.60


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


def truncate_text(text: str, limit: int = 1800) -> str:
    text = clean_text(text).strip()

    if len(text) <= limit:
        return text

    return text[:limit].rsplit(" ", 1)[0] + "..."


def extract_first_available_content(item: Dict[str, Any], fields: List[str]) -> str:
    for field in fields:
        value = clean_text(item.get(field, "")).strip()

        if value:
            return truncate_text(value)

    return ""


# -----------------------------
# ROLE ACCESS HELPERS
# -----------------------------

def normalize_text(value: Any) -> str:
    return clean_text(value).lower().strip()


def is_admin_role(role: str) -> bool:
    return normalize_text(role) in ["admin", "administrator"]


def role_can_access(role: str, audience: Any) -> bool:
    role_lower = normalize_text(role)

    if role_lower in ["admin", "administrator"]:
        return True

    if isinstance(audience, list):
        audience_values = [normalize_text(item) for item in audience]
        return (
            role_lower in audience_values
            or "all" in audience_values
            or "general" in audience_values
        )

    audience_lower = normalize_text(audience)

    if not audience_lower:
        return False

    return audience_lower == role_lower or audience_lower in ["all", "general"]


def build_role_match_filter(role: Optional[str]) -> Dict[str, Any]:
    """
    Used after $vectorSearch to remove results that the current user role
    should not access.
    """

    if not role:
        return {}

    if is_admin_role(role):
        return {}

    role_lower = normalize_text(role)

    return {
        "audience": {
            "$in": [
                role,
                role_lower,
                role_lower.capitalize(),
                "all",
                "general"
            ]
        }
    }


# -----------------------------
# VECTOR SEARCH PIPELINE
# -----------------------------

def build_vector_search_pipeline(
    query_embedding: List[float],
    role: Optional[str] = None,
    limit: int = VECTOR_SEARCH_LIMIT,
    num_candidates: int = VECTOR_NUM_CANDIDATES,
    index_name: str = VECTOR_INDEX_NAME,
    vector_field: str = VECTOR_FIELD_NAME
) -> List[Dict[str, Any]]:
    """
    Builds a real MongoDB Atlas Vector Search pipeline.

    Important:
    - MongoDB Atlas requires a Vector Search index named "vector_index".
    - The indexed vector field must be "embedding".
    - The embedding dimension must be 384 for all-MiniLM-L6-v2.
    """

    vector_stage = {
        "$vectorSearch": {
            "index": index_name,
            "path": vector_field,
            "queryVector": query_embedding,
            "numCandidates": num_candidates,
            "limit": limit
        }
    }

    pipeline = [vector_stage]

    role_match_filter = build_role_match_filter(role)

    if role_match_filter:
        pipeline.append({
            "$match": role_match_filter
        })

    pipeline.append({
        "$project": {
            "_id": 1,
            "title": 1,
            "category": 1,
            "section": 1,
            "keywords": 1,
            "summary": 1,
            "description": 1,
            "answer": 1,
            "content": 1,
            "text": 1,
            "content_text": 1,
            "source": 1,
            "audience": 1,
            "type": 1,
            "file_name": 1,
            "original_file_name": 1,
            "file_url": 1,
            "download_url": 1,
            "action_label": 1,
            "action_url": 1,
            "embedding_model": 1,
            "embedding_dimensions": 1,
            "vector_score": {
                "$meta": "vectorSearchScore"
            }
        }
    })

    return pipeline


def run_vector_search(
    collection,
    query_text: str,
    role: Optional[str] = None,
    limit: int = VECTOR_SEARCH_LIMIT,
    min_score: float = VECTOR_MIN_SCORE
) -> List[Dict[str, Any]]:
    """
    Runs real MongoDB Atlas Vector Search.

    Returns an empty list if:
    - embedding model is unavailable
    - query embedding cannot be created
    - MongoDB Atlas Vector Search index is missing
    - collection has no valid embeddings
    """

    query_embedding = create_text_embedding(query_text)

    if not validate_embedding(query_embedding):
        return []

    pipeline = build_vector_search_pipeline(
        query_embedding=query_embedding,
        role=role,
        limit=limit
    )

    try:
        results = list(collection.aggregate(pipeline))
    except Exception:
        return []

    filtered_results = []

    for item in results:
        vector_score = float(item.get("vector_score", 0))

        if vector_score < min_score:
            continue

        if role is not None and not role_can_access(role, item.get("audience", [])):
            continue

        item["vector_score"] = vector_score
        filtered_results.append(item)

    return filtered_results


# -----------------------------
# RESULT BUILDING HELPERS
# -----------------------------

def vector_score_to_relevance_score(vector_score: float) -> int:
    """
    Converts Vector Search score into the same rough scoring scale
    used by the regex fallback search.
    """

    return max(1, int(vector_score * 100))


def get_vector_content_for_type(result_type: str, item: Dict[str, Any]) -> str:
    result_type_lower = clean_text(result_type).lower()

    if result_type_lower == "document":
        content = clean_text(item.get("summary", "")).strip()
        pdf_text = clean_text(item.get("content_text", "")).strip()

        if pdf_text:
            if content:
                content += "\n\n"
            content += f"Extracted PDF Content:\n{truncate_text(pdf_text, 2500)}"

        if item.get("file_url"):
            content += f"\n\nPreview Link: {item.get('file_url')}."

        if item.get("download_url"):
            content += f"\nDownload Link: {item.get('download_url')}."

        return truncate_text(content, 3000)

    return extract_first_available_content(
        item,
        [
            "answer",
            "content",
            "summary",
            "text",
            "description",
            "content_text"
        ]
    )


def build_vector_result(
    item: Dict[str, Any],
    result_type: str,
    default_source: str
) -> Optional[Dict[str, Any]]:
    vector_score = float(item.get("vector_score", 0))
    content = get_vector_content_for_type(result_type, item)

    if not content:
        return None

    title = item.get("title", result_type)
    source = item.get("source") or item.get("title") or default_source

    return {
        "score": vector_score_to_relevance_score(vector_score),
        "title": title,
        "content": content,
        "source": source,
        "type": result_type,
        "search_method": "MongoDB Atlas Vector Search",
        "vector_score": vector_score,
        "action_label": item.get("action_label"),
        "action_url": item.get("action_url")
    }