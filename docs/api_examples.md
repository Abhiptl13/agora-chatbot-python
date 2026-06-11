# API Request and Response Examples

## Login Request

Endpoint:
POST /login

Purpose:
Authenticate a user.

Request:

{
  "email": "etudiant@college.local",
  "password": "Agora2026!"
}

Response:

{
  "status": "success",
  "role": "student"
}

---

## Chat Message Request

Endpoint:
POST /api/chat/message

Request:

{
  "question": "Where can I see my class schedule?"
}

Response:

{
  "question": "Where can I see my class schedule?",
  "answer": "Students can view their class schedule from the Agora intranet dashboard under the Schedule section.",
  "source": "Class Schedule",
  "matched": true
}

---

## Chat History Request

Endpoint:
GET /api/chat/history

Response:

[
  {
    "user": "etudiant@college.local",
    "role": "student",
    "question": "Where can I see my class schedule?",
    "answer": "Students can view their class schedule from the Agora intranet dashboard.",
    "source": "Class Schedule",
    "timestamp": "2026-06-11 12:00:00"
  }
]

---

## Document Search Request

Endpoint:
GET /api/documents?q=schedule

Response:

[
  {
    "title": "Class Schedule Guide",
    "category": "Student Services",
    "type": "Guide"
  }
]

---

## Appointment Request

Endpoint:
POST /appointments

Request:

{
  "name": "Student User",
  "appointment_type": "Academic Support",
  "advisor": "Dr. Sarah Johnson",
  "date": "2026-06-15",
  "time": "10:00",
  "notes": "Need help with schedule."
}

Response:

{
  "message": "Appointment request submitted successfully."
}