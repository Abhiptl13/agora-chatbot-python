import re

from services.ai_service import generate_ai_response

from mongo_db import (
    knowledge_collection,
    documents_collection,
    website_content_collection,
    portal_services_collection,
    portal_departments_collection,
    appointments_collection
)


# -----------------------------
# OPTIONAL VECTOR SEARCH IMPORT
# -----------------------------

try:
    from services.vector_search_service import (
        run_vector_search,
        build_vector_result
    )
    VECTOR_SEARCH_AVAILABLE = True
except Exception:
    run_vector_search = None
    build_vector_result = None
    VECTOR_SEARCH_AVAILABLE = False


# -----------------------------
# CHATBOT SEARCH SETTINGS
# -----------------------------

STOP_WORDS = {
    "the", "and", "for", "are", "you", "your", "with", "that", "this",
    "from", "have", "has", "had", "was", "were", "will", "can", "could",
    "would", "should", "what", "which", "when", "where", "who", "why",
    "how", "about", "into", "onto", "than", "then", "there", "their",
    "they", "them", "his", "her", "him", "she", "our", "out", "get",
    "got", "not", "yes", "no", "please", "tell", "give", "show", "list",
    "me", "my", "i", "a", "an", "to", "of", "in", "on", "is", "am",
    "be", "do", "does", "did"
}

SHORT_ALLOWED_TOKENS = {
    "ai", "it", "hr", "id", "pdf", "ui", "db"
}

MAX_SEARCH_TOKENS = 10
MAX_RESULTS_PER_COLLECTION = 25
MIN_RELEVANCE_SCORE = 4
TOP_CONTEXT_RESULTS = 3


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


def normalize_text(value):
    return clean_text(value).lower().strip()


def expand_token(token):
    token = token.lower().strip()
    variants = {token}

    if len(token) > 4 and token.endswith("ies"):
        variants.add(token[:-3] + "y")

    if len(token) > 3 and token.endswith("es"):
        variants.add(token[:-2])

    if len(token) > 3 and token.endswith("s"):
        variants.add(token[:-1])

    return variants


def tokenize(text):
    raw_text = clean_text(text).lower()
    raw_tokens = re.findall(r"[a-zA-Z0-9]+", raw_text)

    tokens = set()

    for token in raw_tokens:
        token = token.strip().lower()

        if not token:
            continue

        if token in STOP_WORDS:
            continue

        if len(token) <= 2 and token not in SHORT_ALLOWED_TOKENS:
            continue

        tokens.update(expand_token(token))

    return tokens


def get_stable_search_tokens(tokens):
    """
    Converts a token set into a stable search order.
    Longer words are searched first because they are usually more meaningful.
    """

    return sorted(
        tokens,
        key=lambda token: (-len(token), token)
    )[:MAX_SEARCH_TOKENS]


def truncate_text(text, limit=1800):
    text = clean_text(text).strip()

    if len(text) <= limit:
        return text

    return text[:limit].rsplit(" ", 1)[0] + "..."


def extract_first_available_content(item, fields):
    for field in fields:
        value = clean_text(item.get(field, "")).strip()

        if value:
            return truncate_text(value)

    return ""


# -----------------------------
# CHATBOT ACTION URL HELPERS
# -----------------------------

def make_chatbot_reactive_url(url):
    """
    Adds a chatbot source marker to internal action URLs.
    This allows pages to show a banner or highlight when opened from chatbot.

    Examples:
    /appointments -> /appointments?from_chatbot=1
    /documents -> /documents?from_chatbot=1
    /demo-site#services -> /demo-site?from_chatbot=services#services
    """

    url = clean_text(url).strip()

    if not url:
        return ""

    if "from_chatbot=" in url:
        return url

    if not url.startswith("/"):
        return url

    if url.startswith("/appointments"):
        return "/appointments?from_chatbot=1"

    if url.startswith("/documents"):
        return "/documents?from_chatbot=1"

    if url.startswith("/history"):
        return "/history?from_chatbot=1"

    if url.startswith("/chat"):
        return "/chat?from_chatbot=1"

    if url.startswith("/dashboard"):
        return "/dashboard?from_chatbot=1"

    if url.startswith("/demo-site#services"):
        return "/demo-site?from_chatbot=services#services"

    if url.startswith("/demo-site#departments"):
        return "/demo-site?from_chatbot=departments#departments"

    if url.startswith("/demo-site"):
        return "/demo-site?from_chatbot=1"

    return url


def build_chatbot_return(answer, source, action_label="", action_url=""):
    return answer, source, action_label, make_chatbot_reactive_url(action_url)


# -----------------------------
# CASUAL CHAT
# -----------------------------

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
            "Hi! I’m Agora Assistant. I can help you with College Lasalle documents, "
            "appointments, services, departments, uploaded PDF information, and portal navigation."
        )

    if question_lower in how_are_you:
        return (
            "I’m doing well, thank you! I’m here to help you with College Lasalle services, "
            "documents, appointments, and general portal support."
        )

    if question_lower in thanks:
        return "You’re welcome! Let me know if you need help with anything else."

    if question_lower in bye:
        return "Goodbye! Have a great day."

    if question_lower in identity:
        return (
            "I’m Agora Assistant, the AI chatbot for the College Lasalle portal. "
            "I help users find documents, book appointments, understand services, and navigate the portal."
        )

    if question_lower in help_questions:
        return (
            "I can help with document searches, uploaded PDF information, appointment booking, "
            "student services, department information, portal navigation, and general College Lasalle support."
        )

    return None


# -----------------------------
# ROLE ACCESS HELPERS
# -----------------------------

def is_admin_role(role):
    return normalize_text(role) in ["admin", "administrator"]


def role_can_access(role, audience):
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


def build_role_filter(role):
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
# MONGODB SEARCH HELPERS
# -----------------------------

def build_regex_filter(tokens, fields):
    regex_conditions = []

    search_tokens = get_stable_search_tokens(tokens)

    for token in search_tokens:
        safe_token = re.escape(token)

        for field in fields:
            regex_conditions.append({
                field: {
                    "$regex": safe_token,
                    "$options": "i"
                }
            })

    if not regex_conditions:
        return {}

    return {
        "$or": regex_conditions
    }


def build_mongo_query(tokens, fields, role=None):
    regex_filter = build_regex_filter(tokens, fields)

    if not regex_filter:
        return {}

    if role is None:
        return regex_filter

    role_filter = build_role_filter(role)

    if not role_filter:
        return regex_filter

    return {
        "$and": [
            role_filter,
            regex_filter
        ]
    }


def find_candidates(collection, tokens, fields, role=None):
    mongo_query = build_mongo_query(tokens, fields, role)

    if not mongo_query:
        return []

    try:
        return list(
            collection.find(mongo_query).limit(MAX_RESULTS_PER_COLLECTION)
        )
    except Exception:
        return []


def get_result_dedup_key(result):
    return (
        f"{result.get('type', '')}|"
        f"{result.get('title', '')}|"
        f"{result.get('source', '')}"
    ).lower()


def deduplicate_results(results):
    unique_results = {}

    for result in results:
        key = get_result_dedup_key(result)

        if key not in unique_results:
            unique_results[key] = result
            continue

        existing_score = unique_results[key].get("score", 0)
        new_score = result.get("score", 0)

        if new_score > existing_score:
            unique_results[key] = result

    return list(unique_results.values())


# -----------------------------
# SCORING
# -----------------------------

def calculate_relevance_score(question, item, field_weights):
    question_lower = normalize_text(question)
    question_tokens = tokenize(question)

    if not question_tokens:
        return 0

    score = 0

    for field, weight in field_weights.items():
        field_text = clean_text(item.get(field, ""))
        field_text_lower = field_text.lower()
        field_tokens = tokenize(field_text)

        if not field_text:
            continue

        common_tokens = question_tokens.intersection(field_tokens)

        if common_tokens:
            score += len(common_tokens) * weight

        if len(question_lower) > 6 and question_lower in field_text_lower:
            score += weight * 3

    return score


def extract_relevant_pdf_snippet(question, pdf_text, max_chars=2500):
    if not pdf_text:
        return ""

    question_tokens = tokenize(question)

    if not question_tokens:
        return pdf_text[:max_chars].strip()

    sentences = re.split(r'(?<=[.!?])\s+', pdf_text.strip())

    scored_sentences = []

    for sentence in sentences:
        sentence_clean = sentence.strip()

        if not sentence_clean:
            continue

        sentence_tokens = tokenize(sentence_clean)
        common_tokens = question_tokens.intersection(sentence_tokens)
        score = len(common_tokens)

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


# -----------------------------
# ACTION LINKS
# -----------------------------

def get_action_metadata(result_type, title, source):
    text = f"{result_type} {title} {source}".lower()

    if "appointment" in text or "advisor" in text or "book" in text:
        return {
            "label": "Open Appointment Page",
            "url": "/appointments?from_chatbot=1"
        }

    if "document" in text or "course" in text or "form" in text or "guide" in text or "pdf" in text:
        return {
            "label": "Open Document Center",
            "url": "/documents?from_chatbot=1"
        }

    if "department" in text or "computer science" in text or "business" in text:
        return {
            "label": "Open Departments",
            "url": "/demo-site?from_chatbot=departments#departments"
        }

    if "service" in text or "support" in text:
        return {
            "label": "Open Services",
            "url": "/demo-site?from_chatbot=services#services"
        }

    if "chatbot" in text or "assistant" in text:
        return {
            "label": "Open AI Assistant",
            "url": "/chat?from_chatbot=1"
        }

    if "history" in text or "conversation" in text:
        return {
            "label": "Open History",
            "url": "/history?from_chatbot=1"
        }

    if "dashboard" in text:
        return {
            "label": "Open Dashboard",
            "url": "/dashboard?from_chatbot=1"
        }

    return {
        "label": "Go to Portal Home",
        "url": "/demo-site?from_chatbot=1"
    }


def build_result(
    score,
    title,
    content,
    source,
    result_type,
    search_method="Optimized MongoDB Retrieval",
    action_label=None,
    action_url=None,
    vector_score=None
):
    fallback_action = get_action_metadata(result_type, title, source)

    final_action_label = action_label or fallback_action["label"]
    final_action_url = action_url or fallback_action["url"]

    result = {
        "score": score,
        "title": title,
        "content": content,
        "source": source,
        "type": result_type,
        "action_label": final_action_label,
        "action_url": make_chatbot_reactive_url(final_action_url),
        "search_method": search_method
    }

    if vector_score is not None:
        result["vector_score"] = vector_score

    return result


def normalize_result_action(result):
    if result.get("action_label") and result.get("action_url"):
        result["action_url"] = make_chatbot_reactive_url(result.get("action_url"))
        return result

    action = get_action_metadata(
        result.get("type", ""),
        result.get("title", ""),
        result.get("source", "")
    )

    result["action_label"] = result.get("action_label") or action["label"]
    result["action_url"] = make_chatbot_reactive_url(
        result.get("action_url") or action["url"]
    )

    return result


# -----------------------------
# VECTOR SEARCH FUNCTIONS
# -----------------------------

def vector_search_collection(collection, question, role, result_type, default_source):
    if not VECTOR_SEARCH_AVAILABLE:
        return []

    if run_vector_search is None or build_vector_result is None:
        return []

    try:
        candidates = run_vector_search(
            collection=collection,
            query_text=question,
            role=role
        )
    except Exception:
        return []

    results = []

    for item in candidates:
        result = build_vector_result(
            item=item,
            result_type=result_type,
            default_source=default_source
        )

        if not result:
            continue

        result = normalize_result_action(result)
        results.append(result)

    return results


def vector_search_knowledge_base(question, role):
    return vector_search_collection(
        collection=knowledge_collection,
        question=question,
        role=role,
        result_type="Knowledge Base",
        default_source="Knowledge Base"
    )


def vector_search_documents(question, role):
    return vector_search_collection(
        collection=documents_collection,
        question=question,
        role=role,
        result_type="Document",
        default_source="Document Center"
    )


def vector_search_website_content(question, role):
    return vector_search_collection(
        collection=website_content_collection,
        question=question,
        role=role,
        result_type="Website Content",
        default_source="Portal Website"
    )


def vector_search_portal_services(question, role):
    return vector_search_collection(
        collection=portal_services_collection,
        question=question,
        role=role,
        result_type="Portal Service",
        default_source="Portal Service"
    )


def vector_search_portal_departments(question, role):
    return vector_search_collection(
        collection=portal_departments_collection,
        question=question,
        role=role,
        result_type="Portal Department",
        default_source="Portal Department"
    )


# -----------------------------
# REGEX COLLECTION SEARCH FUNCTIONS
# -----------------------------

def search_knowledge_base(question, role):
    results = []

    search_fields = [
        "title",
        "category",
        "keywords",
        "answer",
        "summary",
        "text",
        "content",
        "description"
    ]

    field_weights = {
        "title": 8,
        "keywords": 7,
        "category": 5,
        "answer": 6,
        "summary": 5,
        "text": 5,
        "content": 5,
        "description": 5
    }

    tokens = tokenize(question)

    candidates = find_candidates(
        knowledge_collection,
        tokens,
        search_fields,
        role
    )

    for item in candidates:
        if not role_can_access(role, item.get("audience", [])):
            continue

        score = calculate_relevance_score(
            question,
            item,
            field_weights
        )

        content = extract_first_available_content(
            item,
            ["answer", "text", "summary", "content", "description"]
        )

        if score >= MIN_RELEVANCE_SCORE and content:
            results.append(
                build_result(
                    score=score,
                    title=item.get("title", "Knowledge Base"),
                    content=content,
                    source=item.get("title", "Knowledge Base"),
                    result_type="Knowledge Base",
                    action_label=item.get("action_label"),
                    action_url=item.get("action_url")
                )
            )

    return results


def search_documents(question, role):
    results = []

    search_fields = [
        "title",
        "category",
        "summary",
        "type",
        "original_file_name",
        "file_name",
        "content_text",
        "text",
        "answer",
        "description"
    ]

    field_weights = {
        "title": 8,
        "category": 5,
        "summary": 6,
        "type": 2,
        "original_file_name": 4,
        "file_name": 4,
        "content_text": 5,
        "text": 5,
        "answer": 5,
        "description": 5
    }

    tokens = tokenize(question)

    candidates = find_candidates(
        documents_collection,
        tokens,
        search_fields,
        role
    )

    for item in candidates:
        if not role_can_access(role, item.get("audience", [])):
            continue

        score = calculate_relevance_score(
            question,
            item,
            field_weights
        )

        content = item.get("summary", "")

        pdf_text = item.get("content_text", "")

        if pdf_text:
            relevant_pdf_text = extract_relevant_pdf_snippet(
                question,
                pdf_text,
                max_chars=2500
            )

            if relevant_pdf_text:
                content += f"\n\nRelevant Extracted PDF Content:\n{relevant_pdf_text}"

        content = content.strip()

        if item.get("file_url"):
            content += f"\n\nPreview Link: {item.get('file_url')}."

        if item.get("download_url"):
            content += f"\nDownload Link: {item.get('download_url')}."

        if score >= MIN_RELEVANCE_SCORE and content:
            results.append(
                build_result(
                    score=score,
                    title=item.get("title", "Document"),
                    content=truncate_text(content, 3000),
                    source=item.get("title", "Document Center"),
                    result_type="Document",
                    action_label=item.get("action_label"),
                    action_url=item.get("action_url")
                )
            )

    return results


def search_website_content(question, role):
    results = []

    search_fields = [
        "title",
        "section",
        "keywords",
        "content",
        "summary",
        "text",
        "description",
        "route",
        "action_label",
        "action_url"
    ]

    field_weights = {
        "title": 8,
        "section": 5,
        "keywords": 7,
        "content": 5,
        "summary": 5,
        "text": 5,
        "description": 5,
        "route": 4,
        "action_label": 4,
        "action_url": 3
    }

    tokens = tokenize(question)

    candidates = find_candidates(
        website_content_collection,
        tokens,
        search_fields,
        role
    )

    for item in candidates:
        if not role_can_access(role, item.get("audience", "all")):
            continue

        score = calculate_relevance_score(
            question,
            item,
            field_weights
        )

        content = extract_first_available_content(
            item,
            ["content", "summary", "text", "description"]
        )

        if score >= MIN_RELEVANCE_SCORE and content:
            results.append(
                build_result(
                    score=score,
                    title=item.get("title", "Website Content"),
                    content=content,
                    source=item.get("source", "Portal Website"),
                    result_type="Website Content",
                    action_label=item.get("action_label"),
                    action_url=item.get("action_url")
                )
            )

    return results


def search_portal_services(question, role):
    results = []

    search_fields = [
        "title",
        "keywords",
        "description",
        "content",
        "summary",
        "text",
        "route",
        "action_label",
        "action_url"
    ]

    field_weights = {
        "title": 8,
        "keywords": 7,
        "description": 6,
        "content": 5,
        "summary": 5,
        "text": 5,
        "route": 4,
        "action_label": 4,
        "action_url": 3
    }

    tokens = tokenize(question)

    candidates = find_candidates(
        portal_services_collection,
        tokens,
        search_fields,
        role
    )

    for item in candidates:
        if not role_can_access(role, item.get("audience", "all")):
            continue

        score = calculate_relevance_score(
            question,
            item,
            field_weights
        )

        content = extract_first_available_content(
            item,
            ["description", "content", "summary", "text"]
        )

        if score >= MIN_RELEVANCE_SCORE and content:
            results.append(
                build_result(
                    score=score,
                    title=item.get("title", "Portal Service"),
                    content=content,
                    source=item.get("source", "Portal Service"),
                    result_type="Portal Service",
                    action_label=item.get("action_label"),
                    action_url=item.get("action_url")
                )
            )

    return results


def search_portal_departments(question, role):
    results = []

    search_fields = [
        "title",
        "keywords",
        "description",
        "content",
        "summary",
        "text",
        "route",
        "action_label",
        "action_url"
    ]

    field_weights = {
        "title": 8,
        "keywords": 7,
        "description": 6,
        "content": 5,
        "summary": 5,
        "text": 5,
        "route": 4,
        "action_label": 4,
        "action_url": 3
    }

    tokens = tokenize(question)

    candidates = find_candidates(
        portal_departments_collection,
        tokens,
        search_fields,
        role
    )

    for item in candidates:
        if not role_can_access(role, item.get("audience", "all")):
            continue

        score = calculate_relevance_score(
            question,
            item,
            field_weights
        )

        content = extract_first_available_content(
            item,
            ["description", "content", "summary", "text"]
        )

        if score >= MIN_RELEVANCE_SCORE and content:
            results.append(
                build_result(
                    score=score,
                    title=item.get("title", "Portal Department"),
                    content=content,
                    source=item.get("source", "Portal Department"),
                    result_type="Portal Department",
                    action_label=item.get("action_label"),
                    action_url=item.get("action_url")
                )
            )

    return results


# -----------------------------
# STRUCTURED QUERY INTENT HELPERS
# -----------------------------

def is_show_appointments_intent(question):
    question_lower = normalize_text(question)

    appointment_terms = [
        "my appointment",
        "my appointments",
        "show appointment",
        "show appointments",
        "list appointment",
        "list appointments",
        "view appointment",
        "view appointments",
        "check appointment",
        "check appointments",
        "appointment status",
        "appointments status"
    ]

    return any(term in question_lower for term in appointment_terms)


def is_book_appointment_intent(question):
    question_lower = normalize_text(question)

    booking_terms = [
        "book appointment",
        "book an appointment",
        "make appointment",
        "make an appointment",
        "schedule appointment",
        "schedule an appointment",
        "new appointment",
        "create appointment"
    ]

    return any(term in question_lower for term in booking_terms)


def is_show_documents_intent(question):
    question_lower = normalize_text(question)

    document_terms = [
        "show documents",
        "list documents",
        "view documents",
        "my documents",
        "available documents",
        "open document center",
        "document center",
        "uploaded documents",
        "uploaded pdf"
    ]

    return any(term in question_lower for term in document_terms)


def format_appointment_list(appointments):
    if not appointments:
        return "I cannot find any appointment requests for your account."

    lines = [
        "Here are your latest appointment requests:"
    ]

    for item in appointments:
        appointment_type = clean_text(item.get("appointment_type", "Appointment"))
        advisor = clean_text(item.get("advisor", "Advisor not specified"))
        date = clean_text(item.get("date", "Date not specified"))
        time = clean_text(item.get("time", "Time not specified"))
        status = clean_text(item.get("status", "Pending"))

        lines.append(
            f"- {appointment_type} with {advisor} on {date} at {time}. Status: {status}."
        )

    return "\n".join(lines)


def format_document_list(documents):
    if not documents:
        return "I cannot find any accessible documents for your role."

    lines = [
        "Here are some documents available to you:"
    ]

    for item in documents:
        title = clean_text(item.get("title", "Document"))
        category = clean_text(item.get("category", "General"))
        summary = truncate_text(item.get("summary", ""), 180)

        if summary:
            lines.append(f"- {title} ({category}): {summary}")
        else:
            lines.append(f"- {title} ({category})")

    return "\n".join(lines)


def build_structured_query_answer(question, role, user_email=None):
    """
    Handles direct structured database questions without sending them to AI first.
    This shows the difference between structured MongoDB queries and AI retrieval.
    """

    if is_show_appointments_intent(question):
        if not user_email:
            return build_chatbot_return(
                "You can view your appointment requests from the Appointment Page.",
                "Appointments",
                "Open Appointment Page",
                "/appointments?from_chatbot=1"
            )

        try:
            appointment_results = list(
                appointments_collection.find({
                    "user": user_email
                }).sort("created_at", -1).limit(5)
            )
        except Exception:
            appointment_results = []

        answer = format_appointment_list(appointment_results)

        return build_chatbot_return(
            answer,
            "Appointments",
            "Open Appointment Page",
            "/appointments?from_chatbot=1"
        )

    if is_book_appointment_intent(question):
        answer = (
            "You can book an appointment from the Appointment Page. "
            "Select the appointment type, advisor, date, and time, then submit the request. "
            "Your request will be saved as Pending until reviewed."
        )

        return build_chatbot_return(
            answer,
            "Appointment Booking",
            "Open Appointment Page",
            "/appointments?from_chatbot=1"
        )

    if is_show_documents_intent(question):
        document_query = build_role_filter(role)

        try:
            document_results = list(
                documents_collection.find(document_query).sort("uploaded_at", -1).limit(5)
            )
        except Exception:
            document_results = []

        answer = format_document_list(document_results)

        return build_chatbot_return(
            answer,
            "Document Center",
            "Open Document Center",
            "/documents?from_chatbot=1"
        )

    return None


# -----------------------------
# MEMORY HELPERS
# -----------------------------

def format_conversation_memory(recent_history):
    if not recent_history:
        return ""

    memory_lines = []

    for item in reversed(recent_history[:3]):
        previous_question = clean_text(item.get("question", "")).strip()
        previous_answer = clean_text(item.get("answer", "")).strip()
        previous_source = clean_text(item.get("source", "")).strip()

        if previous_question:
            memory_lines.append(f"Previous User Question: {previous_question}")

        if previous_answer:
            memory_lines.append(f"Previous Assistant Answer: {truncate_text(previous_answer, 600)}")

        if previous_source:
            memory_lines.append(f"Previous Source: {previous_source}")

        memory_lines.append("---")

    return "\n".join(memory_lines).strip()


def is_memory_question(question):
    question_lower = normalize_text(question)

    memory_keywords = [
        "previous question",
        "last question",
        "what did i ask",
        "what i asked",
        "previous conversation",
        "last conversation",
        "chat history",
        "history"
    ]

    return any(keyword in question_lower for keyword in memory_keywords)


# -----------------------------
# APPOINTMENT CLAIM CLEANER
# -----------------------------

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


# -----------------------------
# RESPONSE BUILDERS
# -----------------------------

def build_fallback_answer(best_result):
    content = best_result.get("content", "")
    source = best_result.get("source", "internal knowledge base")
    action_label = best_result.get("action_label", "")
    action_url = make_chatbot_reactive_url(best_result.get("action_url", ""))

    if content:
        answer = (
            "I found related information in the database, but the AI response service may be temporarily unavailable.\n\n"
            f"Source: {source}\n\n"
            f"{content}"
        )

        if action_label and action_url:
            answer += f"\n\nYou can also use: {action_label} ({action_url})"

        return answer

    return "I cannot find this information in the database."


def build_memory_only_answer(question, recent_history):
    if not is_memory_question(question):
        return None

    memory_context = format_conversation_memory(recent_history)

    if not memory_context:
        return "I cannot find previous conversation information in the database."

    prompt = f"""
You are Agora Assistant, an AI chatbot embedded inside the College Lasalle portal.

The user is asking about recent conversation memory. Use only the recent conversation memory below.

Recent Conversation Memory:
{memory_context}

Current User Question:
{question}

Strict Instructions:
- Use only the Recent Conversation Memory.
- Do not invent information.
- If the memory does not contain the answer, reply exactly:
  "I cannot find previous conversation information in the database."
- Keep the answer concise.
"""

    try:
        answer = generate_ai_response(prompt)
    except Exception:
        answer = None

    if answer and answer.strip():
        return answer.strip()

    return "I cannot find previous conversation information in the database."


# -----------------------------
# MAIN CHATBOT RESPONSE
# -----------------------------

def chatbot_response(question, role, recent_history=None, user_email=None):
    recent_history = recent_history or []

    casual_answer = get_casual_response(question)

    if casual_answer:
        return build_chatbot_return(
            casual_answer,
            "General Conversation",
            "",
            ""
        )

    structured_answer = build_structured_query_answer(
        question=question,
        role=role,
        user_email=user_email
    )

    if structured_answer:
        return structured_answer

    question_tokens = tokenize(question)

    if not question_tokens:
        return build_chatbot_return(
            "I cannot find this information in the database.",
            "No matching database source",
            "",
            ""
        )

    if is_memory_question(question):
        memory_answer = build_memory_only_answer(question, recent_history)

        if memory_answer:
            return build_chatbot_return(
                memory_answer,
                "Conversation Memory",
                "Open Conversation History",
                "/history?from_chatbot=1"
            )

    all_results = []

    # 1. Semantic search first: MongoDB Atlas Vector Search
    # Vector indexes are created only for the main retrieval collections:
    # documents, knowledge_base, and website_content.
    all_results.extend(vector_search_knowledge_base(question, role))
    all_results.extend(vector_search_documents(question, role))
    all_results.extend(vector_search_website_content(question, role))

    # 2. Reliable fallback: Optimized MongoDB regex retrieval
    # Fallback still searches all collections, including services and departments.
    all_results.extend(search_knowledge_base(question, role))
    all_results.extend(search_documents(question, role))
    all_results.extend(search_website_content(question, role))
    all_results.extend(search_portal_services(question, role))
    all_results.extend(search_portal_departments(question, role))

    all_results = deduplicate_results(all_results)

    memory_context = format_conversation_memory(recent_history)

    if not all_results:
        return build_chatbot_return(
            "I cannot find this information in the database.",
            "No matching database source",
            "",
            ""
        )

    all_results.sort(
        reverse=True,
        key=lambda result: result["score"]
    )

    top_results = all_results[:TOP_CONTEXT_RESULTS]
    best_result = normalize_result_action(top_results[0])

    if best_result["score"] < MIN_RELEVANCE_SCORE:
        return build_chatbot_return(
            "I cannot find this information in the database.",
            "No matching database source",
            "",
            ""
        )

    context_parts = []

    for result in top_results:
        result = normalize_result_action(result)

        vector_score_text = ""

        if result.get("vector_score") is not None:
            vector_score_text = f"Vector Score: {result.get('vector_score')}"

        context_parts.append(
            f"""
Source Type: {result["type"]}
Title: {result["title"]}
Content: {result["content"]}
Source: {result["source"]}
Search Method: {result.get("search_method", "Optimized MongoDB Retrieval")}
Recommended Action: {result["action_label"]}
Recommended Link: {result["action_url"]}
Relevance Score: {result["score"]}
{vector_score_text}
"""
        )

    context = "\n---\n".join(context_parts).strip()

    if not context:
        return build_chatbot_return(
            "I cannot find this information in the database.",
            "No matching database source",
            "",
            ""
        )

    prompt = f"""
You are Agora Assistant, an AI chatbot embedded inside the College Lasalle portal.

Use only the provided database context to answer the user's question.

Database Context:
{context}

Recent Conversation Memory:
{memory_context if memory_context else "No previous conversation memory available."}

Current User Question:
{question}

Important Application Rules:
- The application can save appointment requests with the status "Pending".
- The application does not currently send appointment confirmation emails.
- Do not say that an email confirmation will be sent.
- Do not promise email notifications, SMS notifications, automatic approval, or features that are not implemented.
- If the user asks about uploaded PDFs, documents, or files, tell the user to use the Document Center preview/download buttons only if the context supports it.
- If the context includes a Recommended Action and Recommended Link, mention the action naturally when useful.

Strict Instructions:
- Use only the Database Context above.
- Do not guess.
- Do not invent courses, policies, schedules, departments, documents, services, or technical topics.
- Do not answer from general knowledge.
- If the Database Context is empty or does not contain the answer, reply exactly:
  "I cannot find this information in the database."
- If the context is relevant, answer clearly and professionally.
- Keep the response concise.
- Use bullet points only when helpful.
- Do not exceed 6 bullet points.
"""

    try:
        answer = generate_ai_response(prompt)
    except Exception:
        answer = build_fallback_answer(best_result)

    if not answer or not answer.strip():
        answer = build_fallback_answer(best_result)

    unavailable_phrases = [
        "ai service is currently unavailable",
        "service is currently unavailable",
        "please try again later",
        "connection error"
    ]

    if any(phrase in answer.lower() for phrase in unavailable_phrases):
        answer = build_fallback_answer(best_result)

    answer = clean_unsupported_claims(answer.strip(), question)

    return build_chatbot_return(
        answer,
        best_result["source"],
        best_result.get("action_label", ""),
        best_result.get("action_url", "")
    )