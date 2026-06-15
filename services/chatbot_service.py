from services.ai_service import generate_ai_response

from mongo_db import (
    knowledge_collection,
    documents_collection,
    website_content_collection,
    portal_services_collection,
    portal_departments_collection
)


def get_casual_response(question):
    question_lower = question.lower().strip()

    question_lower = question_lower.replace("?", "")
    question_lower = question_lower.replace("!", "")
    question_lower = question_lower.replace(".", "")
    question_lower = question_lower.replace(",", "")

    greetings = [
        "hi", "hii", "hiii", "hello", "hey", "heyy",
        "good morning", "good afternoon", "good evening"
    ]

    how_are_you = [
        "how are you", "how r u", "how are u", "how you doing",
        "how is it going", "whats up", "what's up", "sup"
    ]

    thanks = [
        "thanks", "thank you", "thankyou", "thx", "ty"
    ]

    bye = [
        "bye", "goodbye", "see you", "see ya", "take care"
    ]

    identity = [
        "who are you", "what are you", "your name",
        "what is your name", "tell me your name"
    ]

    help_questions = [
        "help", "what can you do", "what you can do",
        "how can you help me", "what can u do"
    ]

    if question_lower in greetings:
        return (
            "Hi! How are you? I’m Agora Assistant. "
            "I can help you with documents, appointments, services, departments, and portal information."
        )

    if question_lower in how_are_you:
        return (
            "I’m doing well, thank you! How are you? "
            "I’m here to help you with College Agora services, documents, appointments, and general portal support."
        )

    if question_lower in thanks:
        return "You’re welcome! Let me know if you need help with anything else."

    if question_lower in bye:
        return "Goodbye! Have a great day."

    if question_lower in identity:
        return (
            "I’m Agora Assistant, the AI chatbot for the College Agora portal. "
            "I can help users find documents, book appointments, understand services, and navigate the portal."
        )

    if question_lower in help_questions:
        return (
            "I can help you with document searches, appointment booking, student services, department information, "
            "portal navigation, and general College Agora support."
        )

    return None


def calculate_score(question_lower, item, fields):
    score = 0

    for field in fields:
        value = item.get(field, "")

        if isinstance(value, list):
            for element in value:
                element_lower = str(element).lower()

                if element_lower in question_lower:
                    score += 4

                for word in element_lower.split():
                    if len(word) > 2 and word in question_lower:
                        score += 1

        else:
            value_lower = str(value).lower()

            if value_lower and value_lower in question_lower:
                score += 4

            for word in value_lower.split():
                if len(word) > 2 and word in question_lower:
                    score += 1

    return score


def get_action_metadata(result_type, title, source):
    text = f"{result_type} {title} {source}".lower()

    if "appointment" in text or "advisor" in text or "book" in text:
        return {
            "label": "Open Appointment Page",
            "url": "/appointments"
        }

    if "document" in text or "course" in text or "form" in text or "guide" in text:
        return {
            "label": "Open Document Center",
            "url": "#documents"
        }

    if "department" in text or "computer science" in text or "business" in text:
        return {
            "label": "Open Departments",
            "url": "#departments"
        }

    if "service" in text or "support" in text:
        return {
            "label": "Open Services",
            "url": "#services"
        }

    if "chatbot" in text or "assistant" in text:
        return {
            "label": "Open Chatbot",
            "url": "#chatbot"
        }

    if "history" in text or "conversation" in text:
        return {
            "label": "Open History",
            "url": "/history"
        }

    return {
        "label": "Go to Portal Home",
        "url": "#home"
    }


def build_result(score, title, content, source, result_type):
    action = get_action_metadata(result_type, title, source)

    return {
        "score": score,
        "title": title,
        "content": content,
        "source": source,
        "type": result_type,
        "action_label": action["label"],
        "action_url": action["url"]
    }


def search_knowledge_base(question_lower, role):
    results = []
    knowledge = list(knowledge_collection.find({}))

    for item in knowledge:
        if role not in item.get("audience", []):
            continue

        score = calculate_score(
            question_lower,
            item,
            ["title", "category", "keywords", "answer"]
        )

        if score > 0:
            results.append(
                build_result(
                    score=score,
                    title=item.get("title", "Knowledge Base"),
                    content=item.get("answer", ""),
                    source=item.get("title", "Knowledge Base"),
                    result_type="Knowledge Base"
                )
            )

    return results


def search_documents(question_lower, role):
    results = []
    documents = list(documents_collection.find({}))

    for item in documents:
        if role not in item.get("audience", []):
            continue

        score = calculate_score(
            question_lower,
            item,
            ["title", "category", "summary", "type"]
        )

        if score > 0:
            results.append(
                build_result(
                    score=score,
                    title=item.get("title", "Document"),
                    content=item.get("summary", ""),
                    source=item.get("title", "Document Center"),
                    result_type="Document"
                )
            )

    return results


def search_website_content(question_lower):
    results = []
    website_items = list(website_content_collection.find({}))

    for item in website_items:
        score = calculate_score(
            question_lower,
            item,
            ["title", "section", "keywords", "content"]
        )

        if score > 0:
            results.append(
                build_result(
                    score=score,
                    title=item.get("title", "Website Content"),
                    content=item.get("content", ""),
                    source=item.get("source", "Portal Website"),
                    result_type="Website Content"
                )
            )

    return results


def search_portal_services(question_lower):
    results = []
    services = list(portal_services_collection.find({}))

    for item in services:
        score = calculate_score(
            question_lower,
            item,
            ["title", "keywords", "description"]
        )

        if score > 0:
            results.append(
                build_result(
                    score=score,
                    title=item.get("title", "Portal Service"),
                    content=item.get("description", ""),
                    source=item.get("source", "Portal Service"),
                    result_type="Portal Service"
                )
            )

    return results


def search_portal_departments(question_lower):
    results = []
    departments = list(portal_departments_collection.find({}))

    for item in departments:
        score = calculate_score(
            question_lower,
            item,
            ["title", "keywords", "description"]
        )

        if score > 0:
            results.append(
                build_result(
                    score=score,
                    title=item.get("title", "Portal Department"),
                    content=item.get("description", ""),
                    source=item.get("source", "Portal Department"),
                    result_type="Portal Department"
                )
            )

    return results


def chatbot_response(question, role):
    casual_answer = get_casual_response(question)

    if casual_answer:
        return casual_answer, "General Conversation"

    question_lower = question.lower()

    all_results = []

    all_results.extend(search_knowledge_base(question_lower, role))
    all_results.extend(search_documents(question_lower, role))
    all_results.extend(search_website_content(question_lower))
    all_results.extend(search_portal_services(question_lower))
    all_results.extend(search_portal_departments(question_lower))

    if all_results:
        all_results.sort(
            reverse=True,
            key=lambda x: x["score"]
        )

        top_results = all_results[:3]
        best_result = top_results[0]

        context = ""

        for result in top_results:
            context += f"""
Source Type: {result["type"]}
Title: {result["title"]}
Content: {result["content"]}
Source: {result["source"]}
Recommended Action: {result["action_label"]}
Recommended Link: {result["action_url"]}
---
"""

        prompt = f"""
You are Agora Assistant, an AI chatbot embedded inside the College Agora portal.

Use the provided portal, document, service, department, and knowledge-base context to answer the user's question.

Context:
{context}

User Question:
{question}

Instructions:
- Answer clearly and professionally.
- Prefer information from the provided context.
- If the user asks where to go, mention the correct section or page.
- If the question is about appointments, documents, departments, services, support, or chatbot features, tell the user what action they can take.
- Keep the answer concise.
- Use bullet points only when helpful.
- Do not exceed 6 bullet points.
- Do not invent unsupported information.
"""

        answer = generate_ai_response(prompt)

        return answer, best_result["source"]

    return (
        "I could not find information related to your question. You can try asking about services, documents, appointments, departments, registration, support, or chatbot features.",
        "Fallback"
    )