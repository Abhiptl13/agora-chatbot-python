from flask import Flask, render_template, request, redirect, session, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "agora_secret_key"

DATA_DIR = "data"


# -----------------------------
# JSON HELPERS
# -----------------------------

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)

    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def save_json(filename, data):
    path = os.path.join(DATA_DIR, filename)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def login_required():
    return "user" in session


def current_user():
    return session.get("user")


# -----------------------------
# CHATBOT LOGIC
# -----------------------------

def search_knowledge_base(question, role):
    knowledge = load_json("knowledge_base.json")
    question_lower = question.lower()

    best_match = None
    best_score = 0

    for item in knowledge:
        if role not in item.get("audience", []):
            continue

        score = 0

        for keyword in item.get("keywords", []):
            if keyword.lower() in question_lower:
                score += 2

        if item.get("title", "").lower() in question_lower:
            score += 3

        if score > best_score:
            best_score = score
            best_match = item

    if best_match:
        return {
            "answer": best_match["answer"],
            "source": best_match["title"],
            "matched": True
        }

    return {
        "answer": "Sorry, I could not find this information in the local knowledge base. Please contact administration for more help.",
        "source": "Local fallback response",
        "matched": False
    }


def save_conversation(user, question, answer, source):
    conversations = load_json("conversations.json")

    conversations.append({
        "user": user["email"],
        "name": user["name"],
        "role": user["role"],
        "question": question,
        "answer": answer,
        "source": source,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    save_json("conversations.json", conversations)


# -----------------------------
# MAIN ROUTES
# -----------------------------

@app.route("/")
def home():
    if login_required():
        return redirect("/dashboard")
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        users = load_json("users.json")

        for user in users:
            if user["email"] == email and user["password"] == password:
                session["user"] = user
                return redirect("/dashboard")

        error = "Invalid email or password. Please try again."

    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():
    if not login_required():
        return redirect("/login")

    return render_template("dashboard.html", user=current_user())


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

    all_documents = load_json("documents.json")
    visible_documents = []

    for doc in all_documents:
        if role in doc.get("audience", []):
            title = doc.get("title", "").lower()
            category = doc.get("category", "").lower()
            summary = doc.get("summary", "").lower()

            if query == "" or query in title or query in category or query in summary:
                visible_documents.append(doc)

    return render_template(
        "documents.html",
        user=user,
        documents=visible_documents,
        query=query
    )


@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    if not login_required():
        return redirect("/login")

    success = None
    error = None
    user = current_user()

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
            appointment_list = load_json("appointments.json")

            appointment_list.append({
                "user": user["email"],
                "role": user["role"],
                "name": name,
                "appointment_type": appointment_type,
                "advisor": advisor,
                "date": date,
                "time": time,
                "notes": notes,
                "status": "Pending",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            save_json("appointments.json", appointment_list)
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
    conversations = load_json("conversations.json")

    user_history = [
        conversation for conversation in conversations
        if conversation.get("user") == user["email"]
    ]

    return render_template(
        "history.html",
        user=user,
        history=user_history
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/health")
def health():
    return {
        "status": "running",
        "project": "Agora Assistant Chatbot - Python Version"
    }


# -----------------------------
# API ROUTES
# -----------------------------

@app.route("/api/chat/message", methods=["POST"])
def api_chat_message():
    if not login_required():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    question = data.get("question", "").strip() if data else ""

    if question == "":
        return jsonify({
            "error": "Question cannot be empty."
        }), 400

    user = current_user()
    role = user["role"]

    result = search_knowledge_base(question, role)

    save_conversation(
        user=user,
        question=question,
        answer=result["answer"],
        source=result["source"]
    )

    return jsonify({
        "question": question,
        "answer": result["answer"],
        "source": result["source"],
        "matched": result["matched"]
    })


@app.route("/chat/message", methods=["POST"])
def chat_message():
    return api_chat_message()


@app.route("/api/chat/history")
def api_chat_history():
    if not login_required():
        return jsonify({"error": "Unauthorized"}), 401

    user = current_user()
    conversations = load_json("conversations.json")

    user_history = [
        conversation for conversation in conversations
        if conversation.get("user") == user["email"]
    ]

    return jsonify(user_history)


@app.route("/api/documents")
def api_documents():
    if not login_required():
        return jsonify({"error": "Unauthorized"}), 401

    user = current_user()
    role = user["role"]
    query = request.args.get("q", "").lower().strip()

    documents_data = load_json("documents.json")
    results = []

    for doc in documents_data:
        if role in doc.get("audience", []):
            text = (
                doc.get("title", "") + " " +
                doc.get("category", "") + " " +
                doc.get("summary", "")
            ).lower()

            if query == "" or query in text:
                results.append(doc)

    return jsonify(results)


@app.route("/api/appointments")
def api_appointments():
    if not login_required():
        return jsonify({"error": "Unauthorized"}), 401

    user = current_user()
    all_appointments = load_json("appointments.json")

    user_appointments = [
        appointment for appointment in all_appointments
        if appointment.get("user") == user["email"]
    ]

    return jsonify(user_appointments)


# -----------------------------
# ERROR HANDLERS
# -----------------------------

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({
        "error": "Page not found",
        "status": 404
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "status": 500
    }), 500


# -----------------------------
# RUN APP
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)