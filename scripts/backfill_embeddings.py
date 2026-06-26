import os
import sys
import argparse



PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from mongo_db import (
    knowledge_collection,
    documents_collection,
    website_content_collection,
    portal_services_collection,
    portal_departments_collection
)

from services.vector_embedding_service import (
    create_text_embedding,
    build_embedding_text,
    EMBEDDING_DIMENSIONS
)


# -----------------------------
# COLLECTIONS TO BACKFILL
# -----------------------------

SEARCHABLE_COLLECTIONS = [
    ("knowledge_base", knowledge_collection),
    ("documents", documents_collection),
    ("website_content", website_content_collection),
    ("portal_services", portal_services_collection),
    ("portal_departments", portal_departments_collection)
]


# -----------------------------
# HELPERS
# -----------------------------

def has_valid_embedding(item):
    embedding = item.get("embedding")

    if not isinstance(embedding, list):
        return False

    if len(embedding) != EMBEDDING_DIMENSIONS:
        return False

    return True


def backfill_collection(collection_name, collection, force=False):
    print(f"\nChecking collection: {collection_name}")

    scanned_count = 0
    updated_count = 0
    skipped_count = 0

    cursor = collection.find({})

    for item in cursor:
        scanned_count += 1

        if has_valid_embedding(item) and not force:
            skipped_count += 1
            continue

        embedding_text = build_embedding_text(item)

        if not embedding_text:
            skipped_count += 1
            continue

        embedding = create_text_embedding(embedding_text)

        collection.update_one(
            {"_id": item["_id"]},
            {
                "$set": {
                    "embedding": embedding,
                    "embedding_model": "all-MiniLM-L6-v2",
                    "embedding_dimensions": EMBEDDING_DIMENSIONS,
                    "embedding_source_text_length": len(embedding_text)
                }
            }
        )

        updated_count += 1

    print(f"Scanned: {scanned_count}")
    print(f"Updated: {updated_count}")
    print(f"Skipped: {skipped_count}")

    return {
        "collection": collection_name,
        "scanned": scanned_count,
        "updated": updated_count,
        "skipped": skipped_count
    }


def run_backfill(force=False):
    print("Starting embedding backfill...")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Embedding dimensions: {EMBEDDING_DIMENSIONS}")

    summary = []

    for collection_name, collection in SEARCHABLE_COLLECTIONS:
        result = backfill_collection(
            collection_name=collection_name,
            collection=collection,
            force=force
        )

        summary.append(result)

    print("\nBackfill completed.")
    print("\nSummary:")

    for item in summary:
        print(
            f"{item['collection']} | "
            f"Scanned: {item['scanned']} | "
            f"Updated: {item['updated']} | "
            f"Skipped: {item['skipped']}"
        )


# -----------------------------
# RUN SCRIPT
# -----------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Backfill MongoDB records with vector embeddings."
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate embeddings even if they already exist."
    )

    args = parser.parse_args()

    run_backfill(force=args.force)