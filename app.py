import os
import re
import gridfs
from io import BytesIO
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    jsonify,
    send_file
)
from datetime import datetime
from dotenv import load_dotenv
from bson import ObjectId
from bson.errors import InvalidId
from gridfs.errors import NoFile
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from pypdf import PdfReader

from mongo_db import (
    db,
    users_collection,
    documents_collection,
    appointments_collection,
    conversations_collection
)

from services.chatbot_service import chatbot_response
from services.vector_embedding_service import build_embedding_text


# -----------------------------
# APP CONFIGURATION
# -----------------------------

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")

ALLOWED_EXTENSIONS = {"pdf"}
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


# -----------------------------
# MONGODB GRIDFS CONFIGURATION
# -----------------------------

def create_gridfs_storage():
    return gridfs.GridFS(
        db,
        collection="document_files"
    )


document_file_storage = create_gridfs_storage()


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def login_required():
    return "user" in session


def current_user():
    return session.get("user")


def is_admin():
    user = current_user()

    if not user:
        return False

    return user.get("role", "").lower() in ["admin", "administrator"]


def is_teacher():
    user = current_user()

    if not user:
        return False

    return user.get("role", "").lower() == "teacher"


def can_upload_documents():
    user = current_user()

    if not user:
        return False

    return user.get("role", "").lower() in ["admin", "administrator", "teacher"]


def get_allowed_upload_audiences(user):
    if not user:
        return []

    role = user.get("role", "").lower()

    if role in ["admin", "administrator"]:
        return ["student", "teacher", "admin", "administrator", "all", "general"]

    if role == "teacher":
        return ["student", "teacher"]

    return []


def admin_required():
    return login_required() and is_admin()


def make_json_safe(value):
    if isinstance(value, ObjectId):
        return str(value)

    if isinstance(value, list):
        return [make_json_safe(item) for item in value]

    if isinstance(value, dict):
        return {
            key: make_json_safe(item)
            for key, item in value.items()
        }

    return value


def serialize_document(document):
    return make_json_safe(document)


def create_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_object_id_or_none(value):
    try:
        return ObjectId(str(value))
    except (InvalidId, TypeError, ValueError):
        return None


def get_safe_filename_or_none(filename):
    safe_filename = secure_filename(filename)

    if not safe_filename:
        return None

    if safe_filename != filename:
        return None

    return safe_filename


def get_request_question():
    data = request.get_json(silent=True) or {}
    return (data.get("question") or data.get("message") or "").strip()


def is_matched_source(source):
    return source not in [
        "Fallback",
        "No matching database source"
    ]


def get_status_class(status):
    status_lower = str(status).lower()

    if status_lower == "approved":
        return "status-approved"

    if status_lower == "rejected":
        return "status-rejected"

    return "status-pending"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def can_access_document(user, document):
    if not user or not document:
        return False

    role = user.get("role", "").lower()
    audience = document.get("audience", "")

    if role in ["admin", "administrator"]:
        return True

    if isinstance(audience, list):
        audience_values = [str(item).lower() for item in audience]
        return role in audience_values or "all" in audience_values or "general" in audience_values

    audience = str(audience).lower()

    return audience == role or audience in ["all", "general"]


def build_document_access_query(role):
    role_lower = str(role).lower()

    if role_lower in ["admin", "administrator"]:
        return {}

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


def verify_and_upgrade_password(user, entered_password):
    stored_password = str(user.get("password", ""))

    if stored_password.startswith("scrypt:") or stored_password.startswith("pbkdf2:"):
        return check_password_hash(stored_password, entered_password)

    if stored_password == entered_password:
        hashed_password = generate_password_hash(entered_password)

        users_collection.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "password": hashed_password,
                    "password_updated_at": create_timestamp()
                }
            }
        )

        return True

    return False


def extract_pdf_text_from_bytes(file_bytes):
    text = ""

    try:
        reader = PdfReader(BytesIO(file_bytes))

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    except Exception:
        text = ""

    return text.strip()[:15000]


def build_safe_document_search_query(query):
    safe_query = re.escape(query)

    return {
        "$or": [
            {"title": {"$regex": safe_query, "$options": "i"}},
            {"category": {"$regex": safe_query, "$options": "i"}},
            {"summary": {"$regex": safe_query, "$options": "i"}},
            {"type": {"$regex": safe_query, "$options": "i"}},
            {"original_file_name": {"$regex": safe_query, "$options": "i"}},
            {"content_text": {"$regex": safe_query, "$options": "i"}},
            {"search_text": {"$regex": safe_query, "$options": "i"}}
        ]
    }


def get_pdf_response_from_gridfs(document, as_attachment=False):
    if document_file_storage is None:
        return None

    file_id = document.get("file_id")
    file_object_id = get_object_id_or_none(file_id)

    if not file_object_id:
        return None

    try:
        grid_file = document_file_storage.get(file_object_id)
    except NoFile:
        return None
    except Exception:
        return None

    file_bytes = grid_file.read()

    download_name = (
        document.get("original_file_name")
        or document.get("file_name")
        or "document.pdf"
    )

    return send_file(
        BytesIO(file_bytes),
        mimetype="application/pdf",
        as_attachment=as_attachment,
        download_name=download_name
    )


# -----------------------------
# MAIN ROUTES
# -----------------------------

@app.route("/")
def home():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not password:
            error = "Please enter both email and password."
            return render_template("login.html", error=error)

        user = users_collection.find_one({
            "email": email
        })

        if user and verify_and_upgrade_password(user, password):
            session["user"] = {
                "id": user.get("id"),
                "name": user.get("name"),
                "email": user.get("email"),
                "role": user.get("role"),
                "department": user.get("department", "")
            }

            return redirect("/demo-site")

        error = "Invalid email or password. Please try again."

    return render_template("login.html", error=error)


@app.route("/demo-site")
def demo_site():
    if not login_required():
        return redirect("/login")

    return render_template(
        "demo_site.html",
        user=current_user()
    )


@app.route("/dashboard")
def dashboard():
    if not login_required():
        return redirect("/login")

    user = current_user()

    document_count = documents_collection.count_documents(
        build_document_access_query(user["role"])
    )

    dashboard_stats = {
        "documents": document_count,
        "conversations": conversations_collection.count_documents({
            "user": user["email"]
        }),
        "appointments": appointments_collection.count_documents({
            "user": user["email"]
        })
    }

    admin_stats = None

    if is_admin():
        admin_stats = {
            "total_appointments": appointments_collection.count_documents({}),
            "pending_appointments": appointments_collection.count_documents({
                "status": "Pending"
            }),
            "approved_appointments": appointments_collection.count_documents({
                "status": "Approved"
            }),
            "rejected_appointments": appointments_collection.count_documents({
                "status": "Rejected"
            }),
            "total_conversations": conversations_collection.count_documents({}),
            "total_documents": documents_collection.count_documents({})
        }

    return render_template(
        "dashboard.html",
        user=user,
        stats=dashboard_stats,
        admin_stats=admin_stats
    )


@app.route("/chat")
def chat():
    if not login_required():
        return redirect("/login")

    return render_template("chat.html", user=current_user())


@app.route("/documents", methods=["GET", "POST"])
def documents():
    if not login_required():
        return redirect("/login")

    user = current_user()
    role = user["role"]
    query = request.args.get("q", "").lower().strip()

    success = None
    error = None

    if request.method == "POST":
        if not can_upload_documents():
            error = "Only administrators and teachers can upload documents."

        elif document_file_storage is None:
            error = "MongoDB file storage is not configured. Please check MONGO_URI."

        else:
            title = request.form.get("title", "").strip()
            category = request.form.get("category", "").strip()
            summary = request.form.get("summary", "").strip()
            audience = request.form.get("audience", "").strip().lower()
            document_file = request.files.get("document_file")

            allowed_audiences = get_allowed_upload_audiences(user)

            if not title or not category or not summary or not audience:
                error = "Please fill all required document fields."

            elif audience not in allowed_audiences:
                error = "You are not allowed to upload documents for this audience."

            elif not document_file or document_file.filename == "":
                error = "Please select a PDF file to upload."

            elif not allowed_file(document_file.filename):
                error = "Only PDF files are allowed."

            else:
                original_filename = secure_filename(document_file.filename)

                if not original_filename:
                    error = "Invalid PDF file name."

                else:
                    gridfs_file_id = None

                    try:
                        file_bytes = document_file.read()

                        if not file_bytes:
                            error = "The selected PDF file is empty."

                        else:
                            timestamp_name = datetime.now().strftime("%Y%m%d%H%M%S")
                            saved_filename = f"{timestamp_name}_{original_filename}"

                            pdf_text = extract_pdf_text_from_bytes(file_bytes)

                            gridfs_file_id = document_file_storage.put(
                                file_bytes,
                                filename=saved_filename,
                                content_type="application/pdf",
                                metadata={
                                    "title": title,
                                    "category": category,
                                    "audience": audience,
                                    "uploaded_by": user["email"],
                                    "uploaded_by_role": user["role"],
                                    "uploaded_at": create_timestamp(),
                                    "original_file_name": original_filename
                                }
                            )

                            document_data = {
                                "title": title,
                                "category": category,
                                "summary": summary,
                                "type": "PDF",
                                "audience": audience,
                                "file_id": gridfs_file_id,
                                "file_name": saved_filename,
                                "original_file_name": original_filename,
                                "file_url": f"/documents/preview/{saved_filename}",
                                "download_url": f"/documents/download/{saved_filename}",
                                "uploaded_by": user["email"],
                                "uploaded_by_role": user["role"],
                                "uploaded_at": create_timestamp(),
                                "has_file": True,
                                "storage": "MongoDB GridFS",
                                "content_type": "application/pdf",
                                "file_size_bytes": len(file_bytes),
                                "content_text": pdf_text,
                                "content_text_available": bool(pdf_text)
                            }

                            search_text = build_embedding_text(document_data)

                            document_data["search_text"] = search_text
                            document_data["search_method"] = "Lightweight Text Search"
                            document_data["search_index_created_at"] = create_timestamp()

                            documents_collection.insert_one(document_data)

                            if pdf_text:
                                success = "PDF document uploaded successfully to MongoDB. Text was extracted and lightweight search indexing was prepared."
                            else:
                                success = "PDF document uploaded successfully to MongoDB. Text could not be extracted, but preview and download are available."

                    except Exception:
                        if gridfs_file_id:
                            try:
                                document_file_storage.delete(gridfs_file_id)
                            except Exception:
                                pass

                        error = "PDF document upload failed. Please try again."

    mongo_query = build_document_access_query(role)

    if query:
        search_query = build_safe_document_search_query(query)

        if mongo_query:
            mongo_query = {
                "$and": [
                    mongo_query,
                    search_query
                ]
            }
        else:
            mongo_query = search_query

    document_results = list(
        documents_collection.find(mongo_query).sort("uploaded_at", -1)
    )

    document_results = [
        serialize_document(doc) for doc in document_results
    ]

    return render_template(
        "documents.html",
        user=user,
        documents=document_results,
        query=query,
        success=success,
        error=error
    )


@app.route("/documents/preview/<filename>")
def preview_document(filename):
    if not login_required():
        return redirect("/login")

    safe_filename = get_safe_filename_or_none(filename)

    if not safe_filename:
        return render_template("404.html"), 404

    document = documents_collection.find_one({
        "file_name": safe_filename
    })

    if not document:
        return render_template("404.html"), 404

    user = current_user()

    if not can_access_document(user, document):
        return redirect("/documents")

    pdf_response = get_pdf_response_from_gridfs(
        document,
        as_attachment=False
    )

    if not pdf_response:
        return render_template("404.html"), 404

    return pdf_response


@app.route("/documents/download/<filename>")
def download_document(filename):
    if not login_required():
        return redirect("/login")

    safe_filename = get_safe_filename_or_none(filename)

    if not safe_filename:
        return render_template("404.html"), 404

    document = documents_collection.find_one({
        "file_name": safe_filename
    })

    if not document:
        return render_template("404.html"), 404

    user = current_user()

    if not can_access_document(user, document):
        return redirect("/documents")

    pdf_response = get_pdf_response_from_gridfs(
        document,
        as_attachment=True
    )

    if not pdf_response:
        return render_template("404.html"), 404

    return pdf_response


@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    if not login_required():
        return redirect("/login")

    user = current_user()
    success = None
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        appointment_type = request.form.get("appointment_type", "").strip()
        advisor = request.form.get("advisor", "").strip()
        date = request.form.get("date", "").strip()
        time = request.form.get("time", "").strip()
        notes = request.form.get("notes", "").strip()

        if not name or not appointment_type or not advisor or not date or not time:
            error = "Please fill all required fields."
        else:
            appointment_data = {
                "user": user["email"],
                "role": user["role"],
                "name": name,
                "appointment_type": appointment_type,
                "advisor": advisor,
                "date": date,
                "time": time,
                "notes": notes,
                "status": "Pending",
                "created_at": create_timestamp(),
                "updated_at": create_timestamp()
            }

            appointments_collection.insert_one(appointment_data)
            success = "Appointment request submitted successfully. Your request is saved as Pending."

    appointment_results = list(
        appointments_collection.find({
            "user": user["email"]
        }).sort("created_at", -1)
    )

    appointment_results = [
        serialize_document(item) for item in appointment_results
    ]

    return render_template(
        "appointments.html",
        user=user,
        success=success,
        error=error,
        appointments=appointment_results,
        get_status_class=get_status_class
    )


@app.route("/history")
def history():
    if not login_required():
        return redirect("/login")

    user = current_user()

    conversation_results = list(
        conversations_collection.find({
            "user": user["email"]
        }).sort("timestamp", -1)
    )

    conversation_results = [
        serialize_document(item) for item in conversation_results
    ]

    return render_template(
        "history.html",
        user=user,
        history=conversation_results
    )


# -----------------------------
# ADMIN ROUTES
# -----------------------------

@app.route("/admin")
def admin_home():
    if not admin_required():
        return redirect("/dashboard")

    return redirect("/admin/appointments")


@app.route("/admin/appointments")
def admin_appointments():
    if not admin_required():
        return redirect("/dashboard")

    status_filter = request.args.get("status", "").strip()

    mongo_query = {}

    if status_filter:
        mongo_query["status"] = status_filter

    appointment_results = list(
        appointments_collection.find(mongo_query).sort("created_at", -1)
    )

    appointment_results = [
        serialize_document(item) for item in appointment_results
    ]

    stats = {
        "total": appointments_collection.count_documents({}),
        "pending": appointments_collection.count_documents({"status": "Pending"}),
        "approved": appointments_collection.count_documents({"status": "Approved"}),
        "rejected": appointments_collection.count_documents({"status": "Rejected"})
    }

    return render_template(
        "admin_appointments.html",
        user=current_user(),
        appointments=appointment_results,
        stats=stats,
        status_filter=status_filter,
        get_status_class=get_status_class
    )


@app.route("/admin/appointments/<appointment_id>/approve", methods=["POST"])
def approve_appointment(appointment_id):
    if not admin_required():
        return redirect("/dashboard")

    appointment_object_id = get_object_id_or_none(appointment_id)

    if not appointment_object_id:
        return render_template("404.html"), 404

    result = appointments_collection.update_one(
        {"_id": appointment_object_id},
        {
            "$set": {
                "status": "Approved",
                "updated_at": create_timestamp(),
                "reviewed_by": current_user()["email"]
            }
        }
    )

    if result.matched_count == 0:
        return render_template("404.html"), 404

    return redirect("/admin/appointments")


@app.route("/admin/appointments/<appointment_id>/reject", methods=["POST"])
def reject_appointment(appointment_id):
    if not admin_required():
        return redirect("/dashboard")

    appointment_object_id = get_object_id_or_none(appointment_id)

    if not appointment_object_id:
        return render_template("404.html"), 404

    result = appointments_collection.update_one(
        {"_id": appointment_object_id},
        {
            "$set": {
                "status": "Rejected",
                "updated_at": create_timestamp(),
                "reviewed_by": current_user()["email"]
            }
        }
    )

    if result.matched_count == 0:
        return render_template("404.html"), 404

    return redirect("/admin/appointments")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/health")
def health():
    return jsonify({
        "status": "running",
        "project": "Agora Assistant Chatbot - Python Version",
        "database": "MongoDB Atlas",
        "file_storage": "MongoDB GridFS",
        "ai_provider": "Groq API",
        "vector_search_ready": False,
        "search_method": "Lightweight Text Search",
        "embedding_model": "Disabled for free deployment",
        "embedding_dimensions": 0
    })


# -----------------------------
# API ROUTES
# -----------------------------

@app.route("/api/widget/message", methods=["POST"])
def api_widget_message():
    if not login_required():
        return jsonify({
            "error": "Unauthorized. Please log in to use the chatbot widget."
        }), 401

    question = get_request_question()

    if not question:
        return jsonify({
            "error": "Message cannot be empty."
        }), 400

    user = current_user()
    role = user["role"]

    recent_history = list(
        conversations_collection.find({
            "user": user["email"]
        }).sort("timestamp", -1).limit(3)
    )

    answer, source = chatbot_response(question, role, recent_history)

    conversation_data = {
        "user": user["email"],
        "name": user["name"],
        "role": role,
        "question": question,
        "answer": answer,
        "source": source,
        "module": "embedded_widget",
        "timestamp": create_timestamp()
    }

    conversations_collection.insert_one(conversation_data)

    return jsonify({
        "question": question,
        "answer": answer,
        "source": source,
        "matched": is_matched_source(source),
        "module": "embedded_widget"
    })


@app.route("/api/chat/message", methods=["POST"])
def api_chat_message():
    if not login_required():
        return jsonify({"error": "Unauthorized"}), 401

    question = get_request_question()

    if not question:
        return jsonify({
            "error": "Message cannot be empty."
        }), 400

    user = current_user()
    role = user["role"]

    recent_history = list(
        conversations_collection.find({
            "user": user["email"]
        }).sort("timestamp", -1).limit(3)
    )

    answer, source = chatbot_response(question, role, recent_history)

    conversation_data = {
        "user": user["email"],
        "name": user["name"],
        "role": role,
        "question": question,
        "answer": answer,
        "source": source,
        "module": "chat_page",
        "timestamp": create_timestamp()
    }

    conversations_collection.insert_one(conversation_data)

    return jsonify({
        "question": question,
        "answer": answer,
        "source": source,
        "matched": is_matched_source(source)
    })


@app.route("/chat/message", methods=["POST"])
def chat_message():
    return api_chat_message()


@app.route("/api/chat/history")
def api_chat_history():
    if not login_required():
        return jsonify({"error": "Unauthorized"}), 401

    user = current_user()

    history_results = list(
        conversations_collection.find({
            "user": user["email"]
        }).sort("timestamp", -1)
    )

    history_results = [
        serialize_document(item) for item in history_results
    ]

    return jsonify(history_results)


@app.route("/api/documents")
def api_documents():
    if not login_required():
        return jsonify({"error": "Unauthorized"}), 401

    user = current_user()
    role = user["role"]
    query = request.args.get("q", "").lower().strip()

    mongo_query = build_document_access_query(role)

    if query:
        search_query = build_safe_document_search_query(query)

        if mongo_query:
            mongo_query = {
                "$and": [
                    mongo_query,
                    search_query
                ]
            }
        else:
            mongo_query = search_query

    documents_data = list(documents_collection.find(mongo_query))

    documents_data = [
        serialize_document(doc) for doc in documents_data
    ]

    return jsonify(documents_data)


@app.route("/api/appointments", methods=["GET", "POST"])
def api_appointments():
    if not login_required():
        return jsonify({"error": "Unauthorized"}), 401

    user = current_user()

    if request.method == "POST":
        data = request.get_json(silent=True) or {}

        required_fields = [
            "name",
            "appointment_type",
            "advisor",
            "date",
            "time"
        ]

        missing_fields = [
            field for field in required_fields
            if not data.get(field)
        ]

        if missing_fields:
            return jsonify({
                "error": "Missing required fields",
                "missing_fields": missing_fields
            }), 400

        appointment_data = {
            "user": user["email"],
            "role": user["role"],
            "name": data.get("name"),
            "appointment_type": data.get("appointment_type"),
            "advisor": data.get("advisor"),
            "date": data.get("date"),
            "time": data.get("time"),
            "notes": data.get("notes", ""),
            "status": "Pending",
            "created_at": create_timestamp(),
            "updated_at": create_timestamp()
        }

        appointments_collection.insert_one(appointment_data)
        appointment_data = serialize_document(appointment_data)

        return jsonify({
            "message": "Appointment request submitted successfully. Status is Pending.",
            "appointment": appointment_data
        }), 201

    appointments_data = list(
        appointments_collection.find({
            "user": user["email"]
        }).sort("created_at", -1)
    )

    appointments_data = [
        serialize_document(item) for item in appointments_data
    ]

    return jsonify(appointments_data)


@app.route("/api/admin/appointments/<appointment_id>/status", methods=["POST"])
def api_admin_update_appointment_status(appointment_id):
    if not admin_required():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    status = data.get("status", "").strip()

    if status not in ["Pending", "Approved", "Rejected"]:
        return jsonify({
            "error": "Invalid status. Use Pending, Approved, or Rejected."
        }), 400

    appointment_object_id = get_object_id_or_none(appointment_id)

    if not appointment_object_id:
        return jsonify({
            "error": "Invalid appointment ID."
        }), 404

    result = appointments_collection.update_one(
        {"_id": appointment_object_id},
        {
            "$set": {
                "status": status,
                "updated_at": create_timestamp(),
                "reviewed_by": current_user()["email"]
            }
        }
    )

    if result.matched_count == 0:
        return jsonify({
            "error": "Appointment request not found."
        }), 404

    return jsonify({
        "message": "Appointment status updated successfully.",
        "status": status
    })


# -----------------------------
# ERROR HANDLERS
# -----------------------------

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(413)
def file_too_large(error):
    return jsonify({
        "error": "Uploaded file is too large. Maximum PDF size is 10 MB."
    }), 413


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


# -----------------------------
# RUN APP
# -----------------------------

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)