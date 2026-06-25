import re

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
            "I’m here to help you with College Lasalle services, documents, appointments, and general portal support."
        )

    if question_lower in thanks:
        return "You’re welcome! Let me know if you need help with anything else."

    if question_lower in bye:
        return "Goodbye! Have a great day."

    if question_lower in identity:
        return (
            "I’m Agora Assistant, the AI chatbot for the College Lasalle portal. "
            "I can help users find documents, book appointments, understand services, and navigate the portal."
        )

    if question_lower in help_questions:
        return (
            "I can help you with document searches, appointment booking, student services, department information, "
            "portal navigation, and general College Lasalle support."
        )

    return None


def normalize_text(value):
    return str(value or "").lower().strip()


def role_can_access(role, audience):
    role_lower = normalize_text(role)

    if role_lower in ["admin", "administrator"]:
        return True

    if isinstance(audience, list):
        audience_values = [normalize_text(item) for item in audience]
        return role_lower in audience_values or "all" in audience_values or "general" in audience_values

    audience_lower = normalize_text(audience)

    if not audience_lower:
        return False

    return audience_lower == role_lower or audience_lower in ["all", "general"]


def calculate_score(question_lower, item, fields):
    score = 0

    for field in fields:
        value = item.get(field, "")

        if isinstance(value, list):
            for element in value:
                element_lower = str(element).lower()

                if element_lower and element_lower in question_lower:
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


def extract_relevant_pdf_snippet(question_lower, pdf_text, max_chars=2500):
    if not pdf_text:
        return ""

    keywords = re.findall(r"\b[a-zA-Z]{4,}\b", question_lower.lower())
    keywords = list(set(keywords))

    sentences = re.split(r'(?<=[.!?])\s+', pdf_text.strip())

    scored_sentences = []

    for sentence in sentences:
        sentence_clean = sentence.strip()

        if not sentence_clean:
            continue

        sentence_lower = sentence_clean.lower()
        score = 0

        for keyword in keywords:
            if keyword in sentence_lower:
                score += 1

        if score > 0:
            scored_sentences.append((score, sentence_clean))

    if scored_sentences:
        scored_sentences.sort(reverse=True, key=lambda item: item[0])

        selected_text = ""

        for score, sentence in scored_sentences[:8]:
            if len(selected_text) + len(sentence) > max_chars:
                break

            selected_text += sentence + " "

        return selected_text.strip()

    return pdf_text[:max_chars].strip()


def format_conversation_memory(recent_history):
    if not recent_history:
        return ""

    memory_lines = []

    # recent_history comes newest first from app.py.
    # Reverse it so the AI sees the conversation in natural order.
    for item in reversed(recent_history):
        previous_question = item.get("question", "")
        previous_answer = item.get("answer", "")
        previous_source = item.get("source", "")

        if previous_question:
            memory_lines.append(f"Previous User Question: {previous_question}")

        if previous_answer:
            memory_lines.append(f"Previous Assistant Answer: {previous_answer}")

        if previous_source:
            memory_lines.append(f"Previous Source: {previous_source}")

        memory_lines.append("---")

    return "\n".join(memory_lines).strip()


def build_memory_search_text(question, recent_history):
    memory_text = format_conversation_memory(recent_history)

    if not memory_text:
        return question.lower()

    combined_text = f"{question}\n{memory_text}"

    # Keep memory search text controlled.
    return combined_text.lower()[:2500]


def is_appointment_question(text):
    text_lower = text.lower()

    appointment_words = [
        "appointment",
        "appointments",
        "advisor",
        "book",
        "booking",
        "meeting",
        "schedule",
        "counsellor",
        "counselor"
    ]

    return any(word in text_lower for word in appointment_words)


def clean_unsupported_claims(answer, question):
    """
    Prevent the chatbot from promising features that the application does not implement.
    The project saves appointment requests as Pending, but it does not send confirmation emails.
    """

    if not answer:
        return answer

    if not is_appointment_question(question):
        return answer

    answer_lower = answer.lower()

    email_promise_detected = (
        "email" in answer_lower and (
            "confirmation" in answer_lower
            or "sent" in answer_lower
            or "receive" in answer_lower
            or "notify" in answer_lower
            or "notification" in answer_lower
        )
    )

    if not email_promise_detected:
        return answer

    sentences = re.split(r'(?<=[.!?])\s+', answer.strip())

    filtered_sentences = []

    for sentence in sentences:
        sentence_lower = sentence.lower()

        contains_email_promise = (
            "email" in sentence_lower and (
                "confirmation" in sentence_lower
                or "sent" in sentence_lower
                or "receive" in sentence_lower
                or "notify" in sentence_lower
                or "notification" in sentence_lower
            )
        )

        if not contains_email_promise:
            filtered_sentences.append(sentence)

    corrected_answer = " ".join(filtered_sentences).strip()

    correction_note = (
        "Your appointment request will be saved as Pending in the system. "
        "Email confirmation is not currently implemented in this version."
    )

    if corrected_answer:
        return f"{corrected_answer} {correction_note}"

    return correction_note


def get_action_metadata(result_type, title, source):
    text = f"{result_type} {title} {source}".lower()

    if "appointment" in text or "advisor" in text or "book" in text:
        return {
            "label": "Open Appointment Page",
            "url": "/appointments"
        }

    if "document" in text or "course" in text or "form" in text or "guide" in text or "pdf" in text:
        return {
            "label": "Open Document Center",
            "url": "/documents"
        }

    if "department" in text or "computer science" in text or "business" in text:
        return {
            "label": "Open Departments",
            "url": "/demo-site#departments"
        }

    if "service" in text or "support" in text:
        return {
            "label": "Open Services",
            "url": "/demo-site#services"
        }

    if "chatbot" in text or "assistant" in text:
        return {
            "label": "Open Chatbot",
            "url": "/demo-site#chatbot"
        }

    if "history" in text or "conversation" in text:
        return {
            "label": "Open History",
            "url": "/history"
        }

    return {
        "label": "Go to Portal Home",
        "url": "/demo-site"
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
        if not role_can_access(role, item.get("audience", [])):
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
        if not role_can_access(role, item.get("audience", [])):
            continue

        score = calculate_score(
            question_lower,
            item,
            [
                "title",
                "category",
                "summary",
                "type",
                "original_file_name",
                "file_name",
                "content_text"
            ]
        )

        if score > 0:
            content = item.get("summary", "")

            pdf_text = item.get("content_text", "")

            if pdf_text:
                relevant_pdf_text = extract_relevant_pdf_snippet(
                    question_lower,
                    pdf_text,
                    max_chars=2500
                )

                if relevant_pdf_text:
                    content += f"\n\nRelevant Extracted PDF Content:\n{relevant_pdf_text}"

            if item.get("file_url"):
                content += f"\n\nPreview Link: {item.get('file_url')}."

            if item.get("download_url"):
                content += f"\nDownload Link: {item.get('download_url')}."

            results.append(
                build_result(
                    score=score,
                    title=item.get("title", "Document"),
                    content=content,
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


def build_fallback_answer(best_result):
    """
    Used if the AI API fails or returns an unavailable response.
    This prevents the chatbot from showing only a generic API error.
    """

    content = best_result.get("content", "")
    source = best_result.get("source", "internal knowledge base")

    if content:
        return (
            "I found related information from the internal knowledge base, "
            "but the AI response service may be temporarily unavailable. "
            f"Here is the relevant information from {source}: {content}"
        )

    return (
        "I found a related record, but the AI response service may be temporarily unavailable. "
        "Please try again or use the suggested portal section."
    )


def build_memory_only_answer(question, recent_history):
    memory_context = format_conversation_memory(recent_history)

    if not memory_context:
        return None

    prompt = f"""
You are Agora Assistant, an AI chatbot embedded inside the College Lasalle portal.

The user is asking a follow-up question. Use the recent conversation memory only to understand the user's topic.
Do not invent information. If the information is not available, guide the user to the correct portal page.

Recent Conversation Memory:
{memory_context}

Current User Question:
{question}

Important Application Rules:
- The application can save appointment requests with the status "Pending".
- The application does not currently send appointment confirmation emails.
- Do not say that an email confirmation will be sent.
- Do not promise email notifications, SMS notifications, automatic approval, or features that are not implemented.
- If the user asks about appointments, say that the request can be submitted and saved as Pending.
- If the user asks about documents, guide them to the Document Center.
- If the user asks about previous conversation, answer based on memory.

Instructions:
- Answer clearly and professionally.
- Keep the answer concise.
- Do not exceed 6 bullet points.
- Do not invent unsupported information.
"""

    try:
        answer = generate_ai_response(prompt)
    except Exception:
        answer = None

    if answer:
        return clean_unsupported_claims(answer, question)

    return None


def chatbot_response(question, role, recent_history=None):
    recent_history = recent_history or []

    casual_answer = get_casual_response(question)

    if casual_answer:
        return casual_answer, "General Conversation"

    question_lower = build_memory_search_text(question, recent_history)

    all_results = []

    all_results.extend(search_knowledge_base(question_lower, role))
    all_results.extend(search_documents(question_lower, role))
    all_results.extend(search_website_content(question_lower))
    all_results.extend(search_portal_services(question_lower))
    all_results.extend(search_portal_departments(question_lower))

    memory_context = format_conversation_memory(recent_history)

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
You are Agora Assistant, an AI chatbot embedded inside the College Lasalle portal.

Use the provided portal, document, service, department, knowledge-base context, and recent conversation memory to answer the user's question.

Recent Conversation Memory:
{memory_context if memory_context else "No previous conversation memory available."}

Retrieved Context:
{context}

Current User Question:
{question}

Important Application Rules:
- The application can save appointment requests with the status "Pending".
- The application does not currently send appointment confirmation emails.
- Do not say that an email confirmation will be sent.
- Do not promise email notifications, SMS notifications, automatic approval, or features that are not implemented.
- If the user asks about appointments, say that the request can be submitted and saved as Pending.
- If the user asks about uploaded PDFs, documents, or files, tell the user to use the Document Center preview/download buttons.
- If extracted PDF content is provided, answer using that content first.

Instructions:
- Answer clearly and professionally.
- Prefer information from the retrieved context.
- Use recent conversation memory only to understand follow-up questions.
- If the user asks where to go, mention the correct section or page.
- If the question is about appointments, documents, departments, services, support, or chatbot features, tell the user what action they can take.
- Keep the answer concise.
- Use bullet points only when helpful.
- Do not exceed 6 bullet points.
- Do not invent unsupported information.
"""

        try:
            answer = generate_ai_response(prompt)
        except Exception:
            answer = build_fallback_answer(best_result)

        if not answer:
            answer = build_fallback_answer(best_result)

        unavailable_phrases = [
            "ai service is currently unavailable",
            "service is currently unavailable",
            "please try again later",
            "connection error"
        ]

        if any(phrase in answer.lower() for phrase in unavailable_phrases):
            answer = build_fallback_answer(best_result)

        answer = clean_unsupported_claims(answer, question)

        return answer, best_result["source"]

    # If no database search result matched, still try to answer using recent memory.
    memory_answer = build_memory_only_answer(question, recent_history)

    if memory_answer:
        return memory_answer, "Conversation Memory"

    return (
        "I could not find information related to your question. You can try asking about services, documents, appointments, departments, registration, support, or chatbot features.",
        "Fallback"
    )