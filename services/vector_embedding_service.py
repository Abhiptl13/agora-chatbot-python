import re
from collections import Counter


SEARCH_LIMIT_DEFAULT = 5
MIN_SCORE = 0.05


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


def tokenize(text):
    text = clean_text(text).lower()
    return re.findall(r"\b[a-zA-Z0-9]+\b", text)


def calculate_text_score(query_text, document_text):
    query_tokens = tokenize(query_text)
    document_tokens = tokenize(document_text)

    if not query_tokens or not document_tokens:
        return 0.0

    query_counter = Counter(query_tokens)
    document_counter = Counter(document_tokens)

    matched_score = 0
    total_score = sum(query_counter.values())

    for token, count in query_counter.items():
        if token in document_counter:
            matched_score += count

    if total_score > 0:
        return matched_score / total_score

    return 0.0


def document_matches_filter(document, role_filter):
    if not role_filter:
        return True

    for key, expected_value in role_filter.items():
        actual_value = document.get(key)

        if isinstance(expected_value, dict):
            if "$in" in expected_value:
                allowed_values = expected_value["$in"]

                if isinstance(actual_value, list):
                    if not any(value in allowed_values for value in actual_value):
                        return False
                else:
                    if actual_value not in allowed_values:
                        return False
            else:
                continue
        else:
            if actual_value != expected_value:
                return False

    return True


def run_vector_search(collection, query_text, role_filter=None, limit=SEARCH_LIMIT_DEFAULT):
    try:
        documents = list(collection.find({}))
        results = []

        for document in documents:
            if not document_matches_filter(document, role_filter):
                continue

            searchable_text = build_embedding_text(document)
            score = calculate_text_score(query_text, searchable_text)

            if score >= MIN_SCORE:
                document["vector_score"] = score
                results.append(document)

        results = sorted(
            results,
            key=lambda item: item.get("vector_score", 0),
            reverse=True
        )

        return results[:limit]

    except Exception as error:
        print("Lightweight search error:", error)
        return []


def build_vector_search_pipeline(query_text, role_filter=None, limit=5, num_candidates=100):
    return []