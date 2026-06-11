from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["agora_chatbot_db"]

knowledge_base = [
    {
        "id": "kb006",
        "title": "Course Registration",
        "category": "Academic Services",
        "keywords": ["registration", "course", "enroll", "classes"],
        "answer": "Students can complete course registration through the Agora intranet registration section.",
        "audience": ["student"],
        "confidence": "high"
    },
    {
        "id": "kb007",
        "title": "Tuition Payment",
        "category": "Finance",
        "keywords": ["tuition", "payment", "fees", "invoice"],
        "answer": "Students can view tuition fees and payment deadlines through the finance section of the student portal.",
        "audience": ["student"],
        "confidence": "high"
    },
    {
        "id": "kb008",
        "title": "Academic Advisor Appointment",
        "category": "Student Support",
        "keywords": ["advisor", "appointment", "academic support", "meeting"],
        "answer": "Students can book an academic advisor appointment using the Appointment Booking page.",
        "audience": ["student"],
        "confidence": "high"
    },
    {
        "id": "kb009",
        "title": "Classroom Change",
        "category": "Schedule",
        "keywords": ["classroom", "room", "change", "location"],
        "answer": "Students and teachers can check classroom changes from the schedule updates section.",
        "audience": ["student", "teacher"],
        "confidence": "medium"
    },
    {
        "id": "kb010",
        "title": "Assignment Submission",
        "category": "Academic",
        "keywords": ["assignment", "submit", "deadline", "homework"],
        "answer": "Students should submit assignments through the assigned course platform before the deadline.",
        "audience": ["student"],
        "confidence": "high"
    },
    {
        "id": "kb011",
        "title": "Teacher Attendance Review",
        "category": "Teacher Resources",
        "keywords": ["attendance", "student attendance", "absence"],
        "answer": "Teachers can review and update student attendance records through the teacher dashboard.",
        "audience": ["teacher"],
        "confidence": "medium"
    },
    {
        "id": "kb012",
        "title": "Student Follow-Up",
        "category": "Teacher Resources",
        "keywords": ["follow-up", "student support", "academic warning"],
        "answer": "Teachers can submit student follow-up notes through the academic support process.",
        "audience": ["teacher"],
        "confidence": "medium"
    },
    {
        "id": "kb013",
        "title": "Administrative Reports",
        "category": "Administration",
        "keywords": ["report", "admin report", "statistics"],
        "answer": "Administrators can access internal reports from the administration dashboard.",
        "audience": ["admin"],
        "confidence": "medium"
    },
    {
        "id": "kb014",
        "title": "Document Access",
        "category": "Document Library",
        "keywords": ["document", "form", "library", "download"],
        "answer": "Users can search available documents from the Document Library based on their role.",
        "audience": ["student", "teacher", "admin"],
        "confidence": "high"
    },
    {
        "id": "kb015",
        "title": "Technical Support",
        "category": "Support",
        "keywords": ["technical", "support", "login problem", "help"],
        "answer": "Users experiencing technical issues should contact technical support or administration.",
        "audience": ["student", "teacher", "admin"],
        "confidence": "medium"
    },
    {
        "id": "kb016",
        "title": "Attendance Management",
        "category": "Teacher Resources",
        "keywords": [
            "attendance",
            "update attendance",
            "teacher attendance",
            "student attendance",
            "attendance records"
       ],
       "answer": "Teachers can update and review attendance records through the teacher dashboard.",
       "audience": ["teacher"],
       "confidence": "high"
    },
    {
         "id": "kb017",
         "title": "Administrative Reports",
         "category": "Administration",
         "keywords": [
             "admin reports",
             "reports",
             "statistics",
             "administrative reports",
             "dashboard reports"
         ],
         "answer": "Administrators can access reports and statistics from the administration dashboard.",
         "audience": ["admin"],
         "confidence": "high"
    }
]

documents = [
    {
        "id": "doc005",
        "title": "Course Registration Guide",
        "category": "Academic Services",
        "summary": "Guide explaining how students can register for courses through the Agora portal.",
        "type": "Guide",
        "audience": ["student"]
    },
    {
        "id": "doc006",
        "title": "Tuition Payment Instructions",
        "category": "Finance",
        "summary": "Instructions for checking tuition fees, invoices, and payment deadlines.",
        "type": "Guide",
        "audience": ["student"]
    },
    {
        "id": "doc007",
        "title": "Academic Advisor Booking Guide",
        "category": "Student Support",
        "summary": "Guide for booking academic advisor appointments.",
        "type": "Guide",
        "audience": ["student"]
    },
    {
        "id": "doc008",
        "title": "Assignment Submission Policy",
        "category": "Academic",
        "summary": "Policy explaining assignment submission rules and deadline expectations.",
        "type": "Policy",
        "audience": ["student", "teacher"]
    },
    {
        "id": "doc009",
        "title": "Teacher Attendance Manual",
        "category": "Teacher Resources",
        "summary": "Manual for teachers to manage student attendance records.",
        "type": "Manual",
        "audience": ["teacher"]
    },
    {
        "id": "doc010",
        "title": "Student Follow-Up Procedure",
        "category": "Teacher Resources",
        "summary": "Procedure for submitting academic follow-up notes for students.",
        "type": "Procedure",
        "audience": ["teacher"]
    },
    {
        "id": "doc011",
        "title": "Administrative Reports Guide",
        "category": "Administration",
        "summary": "Guide for administrators to access reports and internal statistics.",
        "type": "Guide",
        "audience": ["admin"]
    },
    {
        "id": "doc012",
        "title": "Internal Policy Manual",
        "category": "Administration",
        "summary": "Internal administrative policy reference document.",
        "type": "Manual",
        "audience": ["admin"]
    },
    {
        "id": "doc013",
        "title": "Technical Support Contact Guide",
        "category": "Support",
        "summary": "Contact information and process for technical support requests.",
        "type": "Guide",
        "audience": ["student", "teacher", "admin"]
    },
    {
        "id": "doc014",
        "title": "Appointment Request Process",
        "category": "Support Services",
        "summary": "Guide explaining how users can request and track appointments.",
        "type": "Guide",
        "audience": ["student", "teacher", "admin"]
    }
]

users_extra = [
    {
        "id": "u004",
        "name": "Academic Advisor",
        "email": "advisor@college.local",
        "password": "Agora2026!",
        "role": "admin",
        "department": "Student Support"
    },
    {
        "id": "u005",
        "name": "Program Coordinator",
        "email": "coordinator@college.local",
        "password": "Agora2026!",
        "role": "teacher",
        "department": "Academic Coordination"
    }
]

appointments_sample = [
    {
        "user": "etudiant@college.local",
        "role": "student",
        "name": "Student User",
        "appointment_type": "Academic Support",
        "advisor": "Dr. Sarah Johnson",
        "date": "2026-06-20",
        "time": "10:00",
        "notes": "Need help understanding course registration.",
        "status": "Pending",
        "created_at": "2026-06-11 12:00:00"
    },
    {
        "user": "enseignant@college.local",
        "role": "teacher",
        "name": "Teacher User",
        "appointment_type": "Administrative Help",
        "advisor": "Ms. Emily Rodriguez",
        "date": "2026-06-21",
        "time": "14:00",
        "notes": "Need clarification about attendance report process.",
        "status": "Pending",
        "created_at": "2026-06-11 12:10:00"
    }
]

# Insert only if IDs/emails do not already exist
for item in knowledge_base:
    db.knowledge_base.update_one(
        {"id": item["id"]},
        {"$set": item},
        upsert=True
    )

for item in documents:
    db.documents.update_one(
        {"id": item["id"]},
        {"$set": item},
        upsert=True
    )

for item in users_extra:
    db.users.update_one(
        {"email": item["email"]},
        {"$set": item},
        upsert=True
    )

for item in appointments_sample:
    db.appointments.insert_one(item)

print("Sprint 4 richer data inserted successfully.")
print("Added/updated:")
print("- 10 knowledge base records")
print("- 10 document records")
print("- 2 extra users")
print("- 2 sample appointments")