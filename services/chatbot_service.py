from services.ai_service import generate_ai_response
from mongo_db import knowledge_collection


def chatbot_response(question, role):
    knowledge = list(
        knowledge_collection.find({})
    )

    question_lower = question.lower()
    matches = []

    for item in knowledge:
        if role not in item.get("audience", []):
            continue

        score = 0

        # Match title
        title = item.get("title", "").lower()
        if title and title in question_lower:
            score += 5

        # Match category
        category = item.get("category", "").lower()
        if category and category in question_lower:
            score += 2

        # Match keywords and keyword words
        for keyword in item.get("keywords", []):
            keyword_lower = keyword.lower()

            if keyword_lower in question_lower:
                score += 3

            for word in keyword_lower.split():
                if word in question_lower:
                    score += 1

        if score > 0:
            matches.append((score, item))

    if matches:
        matches.sort(
            reverse=True,
            key=lambda x: x[0]
        )

        best_match = matches[0][1]

        prompt = f"""
Context:
{best_match.get("answer", "")}

User Question:
{question}

Instructions:
Answer in a short and clean format.
Use bullet points only if helpful.
Do not exceed 5 bullet points.
Avoid long paragraphs.
Keep the answer clear and professional.
"""

        answer = generate_ai_response(prompt)

        return answer, best_match.get("title", "Knowledge Base")

    return (
        "I could not find information related to your question. Please contact administration or try asking in another way.",
        "Fallback"
    )