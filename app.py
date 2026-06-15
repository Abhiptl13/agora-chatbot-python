import os
from flask import Flask, render_template, request, redirect, session, jsonify
from datetime import datetime
from dotenv import load_dotenv

from mongo_db import (
    users_collection,
    knowledge_collection,
    documents_collection,
    appointments_collection,
    conversations_collection
)

from services.chatbot_service import chatbot_response


# -----------------------------
# APP CONFIGURATION
# -----------------------------

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def login_required():
    return "user" in session


def current_user():
    return session.get("user")


def serialize_document(document):
    document["_id"] = str(document["_id"])
    return document


def create_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_request_question():
    data = request.get_json(silent=True) or {}
    return (data.get("question") or data.get("message") or "").strip()


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
            "email": email,
            "password": password
        })

        if user:
            session["user"] = {
                "id": user.get("id"),
                "name": user.get("name"),
                "email": user.get("email"),
                "role": user.get("role"),
                "department": user.get("department", "")
            }

            # After successful login, open the portal-style demo page
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

    dashboard_stats = {
        "documents": documents_collection.count_documents({
            "audience": user["role"]
        }),
        "conversations": conversations_collection.count_documents({
            "user": user["email"]
        }),
        "appointments": appointments_collection.count_documents({
            "user": user["email"]
        })
    }

    return render_template(
        "dashboard.html",
        user=user,
        stats=dashboard_stats
    )


@app.route("/chat")
def chat():
    if not login_required():
        return redirect("/login")

    return render_template("chat.html", user=current_user())


@app.route("/documents")
def documents():
    if not login_required():
        return redirect("/login")

    user = current_user()
    role = user["role"]
    query = request.args.get("q", "").lower().strip()

    mongo_query = {
        "audience": role
    }

    if query:
        mongo_query["$or"] = [
            {"title": {"$regex": query, "$options": "i"}},
            {"category": {"$regex": query, "$options": "i"}},
            {"summary": {"$regex": query, "$options": "i"}},
            {"type": {"$regex": query, "$options": "i"}}
        ]

    document_results = list(documents_collection.find(mongo_query))

    document_results = [
        serialize_document(doc) for doc in document_results
    ]

    return render_template(
        "documents.html",
        user=user,
        documents=document_results,
        query=query
    )


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
                "created_at": create_timestamp()
            }

            appointments_collection.insert_one(appointment_data)
            success = "Appointment request submitted successfully."

    return render_template(
        "appointments.html",
        user=user,
        success=success,
        error=error
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
        "ai_provider": "Groq API"
    })


# -----------------------------
# API ROUTES
# -----------------------------

@app.route("/api/widget/message", methods=["POST"])
def api_widget_message():
    question = get_request_question()

    if not question:
        return jsonify({
            "error": "Message cannot be empty."
        }), 400

    # If the user is logged in, use their role.
    # Otherwise default to student for public widget behavior.
    user = current_user()
    role = user["role"] if user else "student"

    answer, source = chatbot_response(question, role)

    if user:
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
        "matched": source != "Fallback",
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

    answer, source = chatbot_response(question, role)

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
        "matched": source != "Fallback"
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

    mongo_query = {
        "audience": role
    }

    if query:
        mongo_query["$or"] = [
            {"title": {"$regex": query, "$options": "i"}},
            {"category": {"$regex": query, "$options": "i"}},
            {"summary": {"$regex": query, "$options": "i"}},
            {"type": {"$regex": query, "$options": "i"}}
        ]

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
            "created_at": create_timestamp()
        }

        appointments_collection.insert_one(appointment_data)
        appointment_data = serialize_document(appointment_data)

        return jsonify({
            "message": "Appointment request submitted successfully.",
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


# -----------------------------
# ERROR HANDLERS
# -----------------------------

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


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