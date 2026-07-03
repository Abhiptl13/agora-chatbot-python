import os
import re
from datetime import datetime
from typing import Any, Dict, List

from mongo_db import (
    website_content_collection,
    portal_services_collection,
    portal_departments_collection
)


# -----------------------------
# WEBSITE CONTENT SYNC SETTINGS
# -----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

SYNC_SOURCE = "Agora Portal Website"
SYNC_VERSION = "website_content_sync_v1"


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


def normalize_space(text: str) -> str:
    text = clean_text(text)

    text = re.sub(r"\s+", " ", text)
    text = text.replace("{", " ")
    text = text.replace("}", " ")
    text = text.replace("%", " ")
    text = text.replace("#", " ")

    return text.strip()


def extract_template_text(template_name: str) -> str:
    """
    Reads a local Flask/Jinja template and extracts visible text-like content.
    This helps connect the chatbot to real website page/template content.

    It does not execute Jinja. It only extracts text from existing template files.
    """

    template_path = os.path.join(TEMPLATES_DIR, template_name)

    if not os.path.exists(template_path):
        return ""

    try:
        with open(template_path, "r", encoding="utf-8") as file:
            html = file.read()
    except Exception:
        return ""

    html = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.IGNORECASE)
    html = re.sub(r"<style[\s\S]*?</style>", " ", html, flags=re.IGNORECASE)

    html = re.sub(r"{#[\s\S]*?#}", " ", html)
    html = re.sub(r"{%[\s\S]*?%}", " ", html)
    html = re.sub(r"{{[\s\S]*?}}", " ", html)

    html = re.sub(r"<[^>]+>", " ", html)

    html = html.replace("&nbsp;", " ")
    html = html.replace("&amp;", "&")
    html = html.replace("&lt;", "<")
    html = html.replace("&gt;", ">")
    html = html.replace("&quot;", '"')
    html = html.replace("&#39;", "'")

    return normalize_space(html)


def combine_content(*parts: str) -> str:
    clean_parts = []

    for part in parts:
        part = normalize_space(part)

        if part:
            clean_parts.append(part)

    return "\n\n".join(clean_parts).strip()


def build_keywords(*items: Any) -> List[str]:
    keywords = []

    for item in items:
        item_text = clean_text(item).lower()
        tokens = re.findall(r"[a-zA-Z0-9]+", item_text)

        for token in tokens:
            if len(token) < 3:
                continue

            if token not in keywords:
                keywords.append(token)

    return keywords[:40]


# -----------------------------
# WEBSITE PAGE RECORDS
# -----------------------------

def build_website_content_records() -> List[Dict[str, Any]]:
    """
    Builds website content records from the portal pages and templates.

    These records make the chatbot aware of real application pages,
    routes, sections, and available actions.
    """

    demo_template_text = extract_template_text("demo_site.html")
    dashboard_template_text = extract_template_text("dashboard.html")
    chat_template_text = extract_template_text("chat.html")
    documents_template_text = extract_template_text("documents.html")
    appointments_template_text = extract_template_text("appointments.html")
    history_template_text = extract_template_text("history.html")
    admin_appointments_template_text = extract_template_text("admin_appointments.html")

    records = [
        {
            "sync_key": "page_demo_site",
            "title": "Agora Portal Home",
            "section": "home",
            "summary": "The portal home page provides access to the dashboard, AI assistant, documents, appointments, services, departments, and user navigation.",
            "content": combine_content(
                "The Agora Portal Home is the main landing page after login. It helps users navigate the College Lasalle portal, open the AI assistant, access documents, book appointments, view services, and explore departments.",
                demo_template_text
            ),
            "source": SYNC_SOURCE,
            "route": "/demo-site",
            "action_label": "Go to Portal Home",
            "action_url": "/demo-site",
            "content_type": "website_page",
            "audience": "all"
        },
        {
            "sync_key": "page_dashboard",
            "title": "Dashboard",
            "section": "dashboard",
            "summary": "The dashboard shows user activity such as accessible documents, conversations, and appointment counts. Admin users can also see administrative statistics.",
            "content": combine_content(
                "The Dashboard gives users a quick overview of their portal activity. Students and teachers can see their documents, conversations, and appointments. Admin users can see total appointments, pending appointments, approved appointments, rejected appointments, total conversations, and total documents.",
                dashboard_template_text
            ),
            "source": SYNC_SOURCE,
            "route": "/dashboard",
            "action_label": "Open Dashboard",
            "action_url": "/dashboard",
            "content_type": "website_page",
            "audience": "all"
        },
        {
            "sync_key": "page_chat",
            "title": "AI Assistant Chat Page",
            "section": "chatbot",
            "summary": "The chat page allows users to ask questions to Agora Assistant and receive answers based on MongoDB retrieval, Vector Search, and portal content.",
            "content": combine_content(
                "The AI Assistant Chat Page allows users to ask questions about documents, appointments, services, departments, website navigation, and uploaded PDF content. The chatbot retrieves relevant context from MongoDB and generates a concise answer using AI.",
                chat_template_text
            ),
            "source": SYNC_SOURCE,
            "route": "/chat",
            "action_label": "Open AI Assistant",
            "action_url": "/chat",
            "content_type": "website_page",
            "audience": "all"
        },
        {
            "sync_key": "page_documents",
            "title": "Document Center",
            "section": "documents",
            "summary": "The Document Center lets users search, preview, download, and upload PDF documents depending on their role.",
            "content": combine_content(
                "The Document Center stores PDF documents in MongoDB GridFS. Users can search documents, preview PDFs, download files, and ask the chatbot questions about extracted PDF text. Admins and teachers can upload documents based on their role permissions.",
                documents_template_text
            ),
            "source": SYNC_SOURCE,
            "route": "/documents",
            "action_label": "Open Document Center",
            "action_url": "/documents",
            "content_type": "website_page",
            "audience": "all"
        },
        {
            "sync_key": "page_appointments",
            "title": "Appointment Booking",
            "section": "appointments",
            "summary": "The appointment page allows users to submit appointment requests with advisors. Requests are saved as Pending until reviewed by an admin.",
            "content": combine_content(
                "The Appointment Booking page lets users create appointment requests by entering their name, appointment type, advisor, date, time, and optional notes. Appointment requests are stored in MongoDB with Pending status. Admin users can approve or reject appointments.",
                appointments_template_text
            ),
            "source": SYNC_SOURCE,
            "route": "/appointments",
            "action_label": "Open Appointment Page",
            "action_url": "/appointments",
            "content_type": "website_page",
            "audience": "all"
        },
        {
            "sync_key": "page_history",
            "title": "Conversation History",
            "section": "history",
            "summary": "The conversation history page shows previous chatbot questions, answers, sources, and timestamps for the logged-in user.",
            "content": combine_content(
                "The Conversation History page stores and displays previous chatbot interactions. It helps users review earlier questions, answers, matched sources, and timestamps. Conversation logs are stored in MongoDB.",
                history_template_text
            ),
            "source": SYNC_SOURCE,
            "route": "/history",
            "action_label": "Open Conversation History",
            "action_url": "/history",
            "content_type": "website_page",
            "audience": "all"
        },
        {
            "sync_key": "page_admin_appointments",
            "title": "Admin Appointment Management",
            "section": "admin",
            "summary": "The admin appointment page allows administrators to view, filter, approve, and reject appointment requests.",
            "content": combine_content(
                "The Admin Appointment Management page is available to administrators. It allows admins to view appointment requests, filter by status, approve pending appointments, reject appointments, and track appointment statistics.",
                admin_appointments_template_text
            ),
            "source": SYNC_SOURCE,
            "route": "/admin/appointments",
            "action_label": "Open Admin Appointments",
            "action_url": "/admin/appointments",
            "content_type": "website_page",
            "audience": "admin"
        }
    ]

    now = create_timestamp()

    for record in records:
        record["keywords"] = build_keywords(
            record.get("title"),
            record.get("section"),
            record.get("summary"),
            record.get("content"),
            record.get("route"),
            record.get("action_label")
        )
        record["sync_source"] = SYNC_VERSION
        record["updated_at"] = now

    return records


# -----------------------------
# PORTAL SERVICE RECORDS
# -----------------------------

def build_portal_service_records() -> List[Dict[str, Any]]:
    records = [
        {
            "sync_key": "service_document_center",
            "title": "Document Center Service",
            "description": "Students and staff can access uploaded PDF documents, preview files, download documents, and search extracted PDF text.",
            "content": "The Document Center service supports PDF upload, MongoDB GridFS storage, document preview, document download, role-based access, and chatbot retrieval from extracted PDF content.",
            "source": "Portal Service",
            "route": "/documents",
            "action_label": "Open Document Center",
            "action_url": "/documents",
            "audience": "all"
        },
        {
            "sync_key": "service_appointment_booking",
            "title": "Appointment Booking Service",
            "description": "Users can submit appointment requests with advisors. Admins can approve or reject appointment requests.",
            "content": "The Appointment Booking service allows users to book academic or support appointments. Appointment requests are saved with Pending status and can be reviewed by administrators.",
            "source": "Portal Service",
            "route": "/appointments",
            "action_label": "Open Appointment Page",
            "action_url": "/appointments",
            "audience": "all"
        },
        {
            "sync_key": "service_ai_assistant",
            "title": "AI Assistant Service",
            "description": "Agora Assistant answers questions using MongoDB retrieval, Vector Search, website content, documents, services, departments, and conversation memory.",
            "content": "The AI Assistant service helps users find information, understand portal pages, retrieve document content, navigate services, and access relevant actions through chatbot response buttons.",
            "source": "Portal Service",
            "route": "/chat",
            "action_label": "Open AI Assistant",
            "action_url": "/chat",
            "audience": "all"
        },
        {
            "sync_key": "service_conversation_history",
            "title": "Conversation History Service",
            "description": "Users can view previous chatbot conversations, sources, and timestamps.",
            "content": "The Conversation History service stores chatbot questions, AI answers, matched sources, user role, module, and timestamp in MongoDB for future review.",
            "source": "Portal Service",
            "route": "/history",
            "action_label": "Open Conversation History",
            "action_url": "/history",
            "audience": "all"
        },
        {
            "sync_key": "service_admin_appointment_review",
            "title": "Admin Appointment Review Service",
            "description": "Administrators can review pending appointments and change their status to Approved or Rejected.",
            "content": "The Admin Appointment Review service allows administrators to manage appointment requests, view appointment statistics, filter requests by status, and approve or reject pending appointments.",
            "source": "Portal Service",
            "route": "/admin/appointments",
            "action_label": "Open Admin Appointments",
            "action_url": "/admin/appointments",
            "audience": "admin"
        }
    ]

    now = create_timestamp()

    for record in records:
        record["section"] = "services"
        record["keywords"] = build_keywords(
            record.get("title"),
            record.get("description"),
            record.get("content"),
            record.get("route"),
            record.get("action_label")
        )
        record["sync_source"] = SYNC_VERSION
        record["updated_at"] = now

    return records


# -----------------------------
# PORTAL DEPARTMENT RECORDS
# -----------------------------

def build_portal_department_records() -> List[Dict[str, Any]]:
    records = [
        {
            "sync_key": "department_computer_science_ai",
            "title": "Computer Science and Artificial Intelligence Department",
            "description": "This department focuses on programming, databases, artificial intelligence, machine learning, software development, and applied technology projects.",
            "content": "The Computer Science and Artificial Intelligence Department supports students studying programming, AI, machine learning, databases, web development, software engineering, chatbot systems, and data-driven applications.",
            "source": "Portal Department",
            "route": "/demo-site#departments",
            "action_label": "Open Departments",
            "action_url": "/demo-site#departments",
            "audience": "all"
        },
        {
            "sync_key": "department_student_services",
            "title": "Student Services Department",
            "description": "Student Services supports students with academic help, appointment booking, document access, guidance, and general support.",
            "content": "The Student Services Department helps students access support resources, book appointments, find forms, understand academic processes, and connect with advisors through the portal.",
            "source": "Portal Department",
            "route": "/demo-site#services",
            "action_label": "Open Services",
            "action_url": "/demo-site#services",
            "audience": "all"
        },
        {
            "sync_key": "department_academic_advising",
            "title": "Academic Advising Department",
            "description": "Academic Advising helps students with course planning, appointments, schedules, academic questions, and program guidance.",
            "content": "The Academic Advising Department supports students with program questions, course planning, academic appointments, document guidance, and advisor communication.",
            "source": "Portal Department",
            "route": "/appointments",
            "action_label": "Book Advisor Appointment",
            "action_url": "/appointments",
            "audience": "student"
        },
        {
            "sync_key": "department_administration",
            "title": "Administration Department",
            "description": "Administration manages documents, appointments, records, and portal operations.",
            "content": "The Administration Department manages uploaded documents, reviews appointment requests, controls role-based access, and monitors system usage through the admin dashboard.",
            "source": "Portal Department",
            "route": "/admin/appointments",
            "action_label": "Open Admin Appointments",
            "action_url": "/admin/appointments",
            "audience": "admin"
        }
    ]

    now = create_timestamp()

    for record in records:
        record["section"] = "departments"
        record["keywords"] = build_keywords(
            record.get("title"),
            record.get("description"),
            record.get("content"),
            record.get("route"),
            record.get("action_label")
        )
        record["sync_source"] = SYNC_VERSION
        record["updated_at"] = now

    return records


# -----------------------------
# DATABASE UPSERT HELPERS
# -----------------------------

def ensure_indexes(collection) -> None:
    try:
        collection.create_index("sync_key", unique=True)
        collection.create_index("section")
        collection.create_index("title")
        collection.create_index("updated_at")
    except Exception:
        pass


def upsert_records(collection, records: List[Dict[str, Any]]) -> Dict[str, int]:
    ensure_indexes(collection)

    inserted_or_updated = 0
    failed = 0

    for record in records:
        sync_key = record.get("sync_key")

        if not sync_key:
            failed += 1
            continue

        try:
            collection.update_one(
                {"sync_key": sync_key},
                {
                    "$set": record,
                    "$setOnInsert": {
                        "created_at": create_timestamp()
                    }
                },
                upsert=True
            )
            inserted_or_updated += 1

        except Exception:
            failed += 1

    return {
        "processed": len(records),
        "inserted_or_updated": inserted_or_updated,
        "failed": failed
    }


# -----------------------------
# MAIN SYNC FUNCTION
# -----------------------------

def sync_website_content_to_mongodb() -> Dict[str, Any]:
    """
    Main sync function.

    It updates:
    - website_content collection
    - portal_services collection
    - portal_departments collection

    This gives the chatbot a real website-connected content layer.
    """

    website_records = build_website_content_records()
    service_records = build_portal_service_records()
    department_records = build_portal_department_records()

    website_result = upsert_records(
        website_content_collection,
        website_records
    )

    service_result = upsert_records(
        portal_services_collection,
        service_records
    )

    department_result = upsert_records(
        portal_departments_collection,
        department_records
    )

    return {
        "status": "completed",
        "sync_source": SYNC_VERSION,
        "synced_at": create_timestamp(),
        "website_content": website_result,
        "portal_services": service_result,
        "portal_departments": department_result
    }


def get_sync_preview() -> Dict[str, Any]:
    """
    Returns preview data without writing to MongoDB.
    Useful for testing.
    """

    website_records = build_website_content_records()
    service_records = build_portal_service_records()
    department_records = build_portal_department_records()

    return {
        "website_content_count": len(website_records),
        "portal_services_count": len(service_records),
        "portal_departments_count": len(department_records),
        "website_content_titles": [record.get("title") for record in website_records],
        "portal_service_titles": [record.get("title") for record in service_records],
        "portal_department_titles": [record.get("title") for record in department_records]
    }


if __name__ == "__main__":
    result = sync_website_content_to_mongodb()
    print(result)