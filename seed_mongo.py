from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["agora_chatbot_db"]

users = [
    {
        "id": "u001",
        "name": "Student User",
        "email": "etudiant@college.local",
        "password": "Agora2026!",
        "role": "student",
        "department": "Student Services"
    },
    {
        "id": "u002",
        "name": "Teacher User",
        "email": "enseignant@college.local",
        "password": "Agora2026!",
        "role": "teacher",
        "department": "Academic Staff"
    },
    {
        "id": "u003",
        "name": "Admin User",
        "email": "admin@college.local",
        "password": "Agora2026!",
        "role": "admin",
        "department": "Administration"
    }
]

knowledge_base = [
    {
        "id": "kb001",
        "title": "Class Schedule",
        "category": "Student Services",
        "keywords": ["schedule", "class", "timetable", "course schedule"],
        "answer": "Students can view their class schedule from the Agora intranet dashboard under the Schedule section.",
        "audience": ["student"],
        "confidence": "high"
    },
    {
        "id": "kb002",
        "title": "Exam Retake",
        "category": "Academic Services",
        "keywords": ["retake", "exam", "retest", "makeup exam"],
        "answer": "Students can request an exam retake by submitting the official retake request form through the academic services section.",
        "audience": ["student"],
        "confidence": "high"
    },
    {
        "id": "kb003",
        "title": "Teaching Resources",
        "category": "Teacher Resources",
        "keywords": ["teaching", "resources", "course material", "lesson"],
        "answer": "Teachers can access teaching resources, course materials, and academic documents from the staff document library.",
        "audience": ["teacher"],
        "confidence": "medium"
    },
    {
        "id": "kb004",
        "title": "Administrative Policy",
        "category": "Administration",
        "keywords": ["policy", "procedure", "admin", "administrative"],
        "answer": "Administrators can access internal policies and administrative procedures from the administration section.",
        "audience": ["admin"],
        "confidence": "medium"
    },
    {
        "id": "kb005",
        "title": "Appointment Booking",
        "category": "Support Services",
        "keywords": ["appointment", "advisor", "meeting", "book"],
        "answer": "Users can book an appointment by opening the Appointment Booking page and completing the request form.",
        "audience": ["student", "teacher", "admin"],
        "confidence": "high"
    }
]

documents = [
    {
        "id": "doc001",
        "title": "Exam Retake Form",
        "category": "Academic",
        "summary": "Official form for students requesting an exam retake.",
        "type": "Form",
        "audience": ["student"]
    },
    {
        "id": "doc002",
        "title": "Class Schedule Guide",
        "category": "Student Services",
        "summary": "Guide explaining how students can access and understand their class schedule.",
        "type": "Guide",
        "audience": ["student"]
    },
    {
        "id": "doc003",
        "title": "Teaching Resource Guide",
        "category": "Teacher Resources",
        "summary": "Guide for teachers to access course materials and academic resources.",
        "type": "Guide",
        "audience": ["teacher"]
    },
    {
        "id": "doc004",
        "title": "Administrative Procedure Manual",
        "category": "Administration",
        "summary": "Internal manual for administrative procedures and policies.",
        "type": "Manual",
        "audience": ["admin"]
    }
]

db.users.delete_many({})
db.knowledge_base.delete_many({})
db.documents.delete_many({})
db.appointments.delete_many({})
db.conversations.delete_many({})

db.users.insert_many(users)
db.knowledge_base.insert_many(knowledge_base)
db.documents.insert_many(documents)

print("MongoDB database seeded successfully!")
print("Database: agora_chatbot_db")
print("Collections: users, knowledge_base, documents, appointments, conversations")