# MongoDB Atlas Vector Search Setup

This project supports MongoDB Atlas Vector Search for semantic chatbot retrieval.

The chatbot uses:

1. Local sentence-transformers embeddings
2. MongoDB Atlas Vector Search
3. Optimized MongoDB regex retrieval as fallback
4. Groq AI for final response generation

---

## 1. Embedding Model

The project uses:

```text
sentence-transformers/all-MiniLM-L6-v2