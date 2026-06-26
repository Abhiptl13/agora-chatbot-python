from sentence_transformers import SentenceTransformer


# -----------------------------
# VECTOR SEARCH SETTINGS
# -----------------------------

VECTOR_INDEX_NAME = "vector_index"
VECTOR_FIELD_NAME = "embedding"
EMBEDDING_DIMENSIONS = 384

_embedding_model = None


# -----------------------------
# MODEL LOADER
# -----------------------------

def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    return _embedding_model


# -----------------------------
# TEXT HELPERS
# -----------------------------

def clean_text(value):
    if value is None:
        return ""

    if isinstance(value, list):
        return " ".join(str(item) for item in value)

    if isinstance(value, dict):
        return " ".join(str(item) for item in value.values())

    return str(value)


def build_embedding_text(item):
    fields = [
        "title",
        "category",
        "keywords",
        "summary",
        "answer",
        "description",
        "content",
        "text",
        "content_text",
        "original_file_name",
        "file_name"
    ]

    parts = []

    for field in fields:
        value = clean_text(item.get(field, "")).strip()

        if value:
            parts.append(value)

    return "\n".join(parts).strip()


# -----------------------------
# EMBEDDING GENERATION
# -----------------------------

def create_text_embedding(text):
    text = clean_text(text).strip()

    if not text:
        return [0.0] * EMBEDDING_DIMENSIONS

    model = get_embedding_model()

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()


# -----------------------------
# VECTOR SEARCH
# -----------------------------

def build_vector_search_pipeline(query_text, role_filter=None, limit=5, num_candidates=100):
    query_vector = create_text_embedding(query_text)

    pipeline = [
        {
            "$vectorSearch": {
                "index": VECTOR_INDEX_NAME,
                "path": VECTOR_FIELD_NAME,
                "queryVector": query_vector,
                "numCandidates": num_candidates,
                "limit": limit
            }
        }
    ]

    if role_filter:
        pipeline.append({
            "$match": role_filter
        })

    pipeline.append({
        "$project": {
            "_id": 1,
            "title": 1,
            "category": 1,
            "keywords": 1,
            "summary": 1,
            "answer": 1,
            "description": 1,
            "content": 1,
            "text": 1,
            "content_text": 1,
            "audience": 1,
            "type": 1,
            "source": 1,
            "file_url": 1,
            "download_url": 1,
            "original_file_name": 1,
            "file_name": 1,
            "vector_score": {
                "$meta": "vectorSearchScore"
            }
        }
    })

    return pipeline


def run_vector_search(collection, query_text, role_filter=None, limit=5):
    try:
        pipeline = build_vector_search_pipeline(
            query_text=query_text,
            role_filter=role_filter,
            limit=limit
        )

        return list(collection.aggregate(pipeline))

    except Exception:
        return []