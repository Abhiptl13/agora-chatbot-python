import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from mongo_db import (
    documents_collection,
    knowledge_collection,
    website_content_collection
)

from services.vector_embedding_service import run_vector_search


test_question = "Which courses are offered?"

collections = [
    ("documents", documents_collection),
    ("knowledge_base", knowledge_collection),
    ("website_content", website_content_collection)
]

for name, collection in collections:
    print("\n" + "=" * 50)
    print(f"Testing Vector Search on: {name}")
    print("=" * 50)

    results = run_vector_search(
        collection=collection,
        query_text=test_question,
        limit=3
    )

    if not results:
        print("No vector results found.")
        continue

    for result in results:
        print("Title:", result.get("title", "No title"))
        print("Score:", result.get("vector_score"))
        print("Summary:", result.get("summary", result.get("answer", ""))[:200])
        print("-" * 30)