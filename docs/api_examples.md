# API Examples – Sprint 4

## Overview

This document explains the main API routes used in the Agora Assistant Chatbot Python version after the Sprint 4 upgrade.

The Sprint 4 version uses:

- Flask for backend routes
- MongoDB Atlas for data storage
- Groq AI for chatbot response generation
- Session authentication for protected access
- Role-based filtering for documents and chatbot answers

---

# Authentication Note

Most API routes require the user to be logged in.

If a user tries to access a protected API without logging in, the system returns:

```json
{
  "error": "Unauthorized"
}
```

Status Code:

```text
401
```

---

# 1. Health Check API

## Endpoint

```text
GET /health
```

## Purpose

Checks if the Flask application is running and confirms the active database and AI provider.

## Example Response

```json
{
  "status": "running",
  "project": "Agora Assistant Chatbot - Python Version",
  "database": "MongoDB Atlas",
  "ai_provider": "Groq API"
}
```

## Expected Result

The route confirms that the application is active and connected to Sprint 4 services.

---

# 2. Chat Message API

## Endpoint

```text
POST /api/chat/message
```

## Purpose

Receives a user question, searches MongoDB knowledge base records, applies role-based filtering, sends context to Groq AI, returns a generated answer, and saves the conversation in MongoDB.

## Request Example

```json
{
  "question": "Where can I see my class schedule?"
}
```

## Response Example

```json
{
  "question": "Where can I see my class schedule?",
  "answer": "You can view your class schedule from the Agora intranet dashboard under the Schedule section.",
  "source": "Class Schedule",
  "matched": true
}
```

## Processing Flow

User Question
↓
Flask API
↓
Role Detection
↓
MongoDB Knowledge Base Search
↓
Groq AI Response Generation
↓
Conversation Saved
↓
Response Returned

## Error Example

If the question is empty:

```json
{
  "error": "Question cannot be empty."
}
```

Status Code:

```text
400
```

---

# 3. Chat History API

## Endpoint

```text
GET /api/chat/history
```

## Purpose

Returns the logged-in user's conversation history from MongoDB.

## Example Response

```json
[
  {
    "_id": "665f0e234b1a2c7f00000001",
    "user": "etudiant@college.local",
    "name": "Student User",
    "role": "student",
    "question": "Where can I see my class schedule?",
    "answer": "You can view your class schedule from the Agora intranet dashboard.",
    "source": "Class Schedule",
    "timestamp": "2026-06-11 14:30:00"
  }
]
```

## Expected Result

Only conversations belonging to the logged-in user are returned.

---

# 4. Documents API

## Endpoint

```text
GET /api/documents
```

## Purpose

Returns documents available to the logged-in user's role.

## Example Response

```json
[
  {
    "_id": "665f0e234b1a2c7f00000002",
    "id": "doc001",
    "title": "Course Registration Guide",
    "category": "Academic Services",
    "summary": "Guide explaining course registration.",
    "type": "Guide",
    "audience": ["student"]
  }
]
```

---

# 5. Documents Search API

## Endpoint

```text
GET /api/documents?q=registration
```

## Purpose

Searches documents by title, category, summary, and type while applying role-based filtering.

## Example Response

```json
[
  {
    "id": "doc005",
    "title": "Course Registration Guide",
    "category": "Academic Services",
    "summary": "Guide explaining how students can register for courses through the Agora portal.",
    "type": "Guide",
    "audience": ["student"]
  }
]
```

## Search Fields

The API searches:

- title
- category
- summary
- type

---

# 6. Appointments API – GET

## Endpoint

```text
GET /api/appointments
```

## Purpose

Returns appointment requests belonging to the logged-in user.

## Example Response

```json
[
  {
    "_id": "665f0e234b1a2c7f00000003",
    "user": "etudiant@college.local",
    "role": "student",
    "name": "Student User",
    "appointment_type": "Academic Support",
    "advisor": "Dr. Sarah Johnson",
    "date": "2026-06-20",
    "time": "10:00",
    "notes": "Need help with course registration.",
    "status": "Pending",
    "created_at": "2026-06-11 12:00:00"
  }
]
```

---

# 7. Appointments API – POST

## Endpoint

```text
POST /api/appointments
```

## Purpose

Creates a new appointment request and stores it in MongoDB.

## Request Example

```json
{
  "name": "Student User",
  "appointment_type": "Academic Support",
  "advisor": "Dr. Sarah Johnson",
  "date": "2026-06-20",
  "time": "10:00",
  "notes": "Need help understanding course registration."
}
```

## Response Example

```json
{
  "message": "Appointment request submitted successfully.",
  "appointment": {
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
  }
}
```

Status Code:

```text
201
```

---

# 8. Appointment Validation Error

## Example

If required fields are missing:

```json
{
  "error": "Missing required fields",
  "missing_fields": [
    "advisor",
    "date"
  ]
}
```

Status Code:

```text
400
```

---

# 9. Role-Based API Behavior

The API respects user roles.

Example:

A student can access:

- Student documents
- Student chatbot answers
- Their own appointments
- Their own conversation history

A teacher can access:

- Teacher resources
- Teacher knowledge base answers
- Their own conversations
- Their own appointments

An administrator can access:

- Administrative documents
- Administrative chatbot answers
- Their own conversations
- Their own appointments

---

# 10. Sprint 4 API Improvements

Compared to Sprint 3, the Sprint 4 API layer includes:

- MongoDB data retrieval
- MongoDB data insertion
- Groq AI response generation
- Improved validation
- Protected API routes
- Role-based filtering
- Better response structure
- Error handling

---

# Conclusion

The Sprint 4 API layer provides the main connection between the frontend, MongoDB database, and Groq AI service. The APIs support authentication, chatbot responses, document search, appointment requests, conversation history, and health checks while maintaining protected access through session authentication.