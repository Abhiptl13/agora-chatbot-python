import os
import sys
from datetime import datetime
from typing import Any, Dict, List


# -----------------------------
# PROJECT PATH SETUP
# -----------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from mongo_db import (  # noqa: E402
    knowledge_collection,
    documents_collection,
    website_content_collection,
    portal_services_collection,
    portal_departments_collection
)

from services.embedding_service import (  # noqa: E402
    build_embedding_text,
    create_text_embedding,
    EMBEDDING_MODEL_NAME,
    EMBEDDING_DIMENSIONS
)


# -----------------------------
# SETTINGS
# -----------------------------

BATCH_LIMIT = 500


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def create_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clean_text(value: Any) -> str:
    if value is None:
        return ""

    if isinstance(value, list):
        return " ".join(str(item) for item in value if item is not None)

    if isinstance(value, dict):
        return " ".join(str(item) for item in value.values() if item is not None)

    return str(value)


def get_collection_configs() -> List[Dict[str, Any]]:
    return [
        {
            "name": "knowledge_base",
            "collection": knowledge_collection
        },
        {
            "name": "documents",
            "collection": documents_collection
        },
        {
            "name": "website_content",
            "collection": website_content_collection
        },
        {
            "name": "portal_services",
            "collection": portal_services_collection
        },
        {
            "name": "portal_departments",
            "collection": portal_departments_collection
        }
    ]


def build_missing_embedding_query() -> Dict[str, Any]:
    return {
        "$or": [
            {"embedding": {"$exists": False}},
            {"embedding": None},
            {"embedding_dimensions": {"$ne": EMBEDDING_DIMENSIONS}},
            {"embedding_model": {"$ne": EMBEDDING_MODEL_NAME}}
        ]
    }


def document_has_searchable_text(document: Dict[str, Any]) -> bool:
    embedding_text = build_embedding_text(document)
    return bool(embedding_text.strip())


def backfill_collection_embeddings(collection_name: str, collection) -> Dict[str, int]:
    query = build_missing_embedding_query()

    processed = 0
    updated = 0
    skipped = 0
    failed = 0

    try:
        cursor = collection.find(query).limit(BATCH_LIMIT)
    except Exception as error:
        print(f"[ERROR] Could not read collection {collection_name}: {error}")
        return {
            "processed": 0,
            "updated": 0,
            "skipped": 0,
            "failed": 1
        }

    for document in cursor:
        processed += 1

        document_id = document.get("_id")

        if not document_has_searchable_text(document):
            skipped += 1
            continue

        embedding_text = build_embedding_text(document)
        embedding = create_text_embedding(embedding_text)

        if not embedding:
            failed += 1
            print(f"[FAILED] {collection_name} | {document_id} | embedding not created")
            continue

        try:
            collection.update_one(
                {"_id": document_id},
                {
                    "$set": {
                        "embedding": embedding,
                        "embedding_model": EMBEDDING_MODEL_NAME,
                        "embedding_dimensions": EMBEDDING_DIMENSIONS,
                        "embedding_created_at": create_timestamp(),
                        "embedding_source": "local_sentence_transformers"
                    }
                }
            )

            updated += 1
            print(f"[UPDATED] {collection_name} | {document_id}")

        except Exception as error:
            failed += 1
            print(f"[ERROR] {collection_name} | {document_id} | {error}")

    return {
        "processed": processed,
        "updated": updated,
        "skipped": skipped,
        "failed": failed
    }


# -----------------------------
# MAIN FUNCTION
# -----------------------------

def backfill_all_embeddings() -> Dict[str, Any]:
    print("Starting embedding backfill...")
    print(f"Embedding model: {EMBEDDING_MODEL_NAME}")
    print(f"Embedding dimensions: {EMBEDDING_DIMENSIONS}")
    print("-" * 60)

    final_result = {
        "started_at": create_timestamp(),
        "embedding_model": EMBEDDING_MODEL_NAME,
        "embedding_dimensions": EMBEDDING_DIMENSIONS,
        "collections": {}
    }

    for config in get_collection_configs():
        collection_name = config["name"]
        collection = config["collection"]

        print(f"\nProcessing collection: {collection_name}")

        result = backfill_collection_embeddings(
            collection_name,
            collection
        )

        final_result["collections"][collection_name] = result

        print(
            f"Result for {collection_name}: "
            f"processed={result['processed']}, "
            f"updated={result['updated']}, "
            f"skipped={result['skipped']}, "
            f"failed={result['failed']}"
        )

    final_result["completed_at"] = create_timestamp()

    print("\n" + "-" * 60)
    print("Embedding backfill completed.")
    print(final_result)

    return final_result


if __name__ == "__main__":
    backfill_all_embeddings()