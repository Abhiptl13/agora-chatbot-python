# Agora Assistant Chatbot – API Examples

## Overview

This document explains the main API routes used in the Agora Assistant Chatbot Python-based Flask application.

The current version uses:

* Flask for backend routing
* MongoDB Atlas for cloud data storage
* Groq AI for chatbot response generation
* Session authentication for protected access
* Role-based filtering for chatbot and document results
* Embedded chatbot widget API support
* Conversation history storage

---

## Authentication Note

Most API routes require the user to be logged in.

If a user tries to access a protected API without logging in, the system may return:

```json
{
  "error": "Unauthorized"
}
```

Status Code:

```text
401
```

Protected API behavior depends on the route and session validation logic in `app.py`.

---

# 1. Health Check API

## Endpoint

```text
GET /health
```

## Purpose

Checks if the Flask application is running.

## Example Response

```json
{
  "status": "running",
  "project": "Agora Assistant Chatbot - Python Version"
}
```

## Expected Result

The route confirms that the backend server is active.

---

# 2. Chat Message API

## Endpoint

```text
POST /api/chat/message
```

## Purpose

Receives a user question from the full AI Assistant page, processes the question through the chatbot service, returns an AI-generated response, and stores the conversation in MongoDB Atlas.

## Request Example

```json
{
  "message": "How can I book an appointment?"
}
```

## Response Example

```json
{
  "answer": "You can book an appointment through the Appointment Services page. Select the type of appointment, choose an advisor or department, pick a date and time, and submit your request.",
  "source": "Appointment Services"
}
```

## Processing Flow

```text
User Question
↓
POST /api/chat/message
↓
Flask Backend
↓
Session Role Detection
↓
Casual Conversation Check
↓
MongoDB Search
↓
Groq AI Response Generation
↓
Conversation Saved
↓
Response Returned
```

## Empty Message Error Example

If the message is empty:

```json
{
  "error": "Message cannot be empty."
}
```

Status Code:

```text
400
```

---

# 3. Embedded Widget Chat API

## Endpoint

```text
POST /api/widget/message
```

## Purpose

Receives a user question from the embedded chatbot widget inside the AI Campus Portal and returns a chatbot response.

This endpoint supports the floating chatbot widget on:

```text
/demo-site
```

## Request Example

```json
{
  "message": "What documents are available?"
}
```

## Response Example

```json
{
  "answer": "You can search academic documents, student forms, course registration guides, advisor booking guides, and institutional resources through the Document Center.",
  "source": "Document Center"
}
```

## Widget Features Supported

* Casual conversation
* Portal question answering
* Document guidance
* Appointment guidance
* Service information
* Department information
* Source display
* Suggested action buttons from frontend JavaScript

---

# 4. Casual Conversation Examples

The chatbot can respond to basic casual messages before searching MongoDB.

## Example Request

```json
{
  "message": "hii"
}
```

## Example Response

```json
{
  "answer": "Hi! How are you? I’m Agora Assistant. I can help you with documents, appointments, services, departments, and portal information.",
  "source": "General Conversation"
}
```

## Supported Casual Inputs

```text
hi
hii
hello
hey
how are you
thanks
bye
who are you
what can you do
```

---

# 5. Chat History API

## Endpoint

```text
GET /api/chat/history
```

## Purpose

Returns the logged-in user’s chatbot conversation history from MongoDB Atlas.

## Example Response

```json
[
  {
    "user": "etudiant@college.local",
    "name": "Student User",
    "role": "student",
    "question": "How can I book an appointment?",
    "answer": "You can book an appointment through the Appointment Services page.",
    "source": "Appointment Services",
    "timestamp": "2026-06-11 14:30:00"
  }
]
```

## Expected Result

Only conversation records belonging to the current logged-in user should be displayed or returned.

---

# 6. Documents API

## Endpoint

```text
GET /api/documents
```

## Purpose

Returns documents available to the logged-in user based on role and optional search keywords.

## Example Response

```json
[
  {
    "id": "doc001",
    "title": "Course Registration Guide",
    "category": "Academic Services",
    "summary": "Guide explaining course registration and enrollment support.",
    "type": "Guide",
    "audience": ["student"]
  }
]
```

---

# 7. Documents Search API

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

The API can search:

* title
* category
* summary
* type

---

# 8. Appointments API – GET

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
    "user": "etudiant@college.local",
    "role": "student",
    "name": "Student User",
    "appointment_type": "Academic Support",
    "advisor": "Academic Advisor",
    "date": "2026-06-20",
    "time": "10:00",
    "notes": "Need help with course registration.",
    "status": "Pending",
    "created_at": "2026-06-11 12:00:00"
  }
]
```

---

# 9. Appointments API – POST

## Endpoint

```text
POST /api/appointments
```

## Purpose

Creates a new appointment request and stores it in MongoDB Atlas.

## Request Example

```json
{
  "appointment_type": "Academic Support",
  "advisor": "Academic Advisor",
  "date": "2026-06-20",
  "time": "10:00",
  "notes": "Need help understanding course registration."
}
```

## Response Example

```json
{
  "message": "Appointment request submitted successfully."
}
```

Status Code:

```text
201
```

---

# 10. Appointment Validation Error

## Example

If required fields are missing:

```json
{
  "error": "Missing required fields"
}
```

Status Code:

```text
400
```

---

# 11. Role-Based API Behavior

The API uses the logged-in user’s role to filter information.

## Student Access

A student can access:

* Student documents
* Student chatbot answers
* Their own appointment requests
* Their own conversation history

## Teacher Access

A teacher can access:

* Teacher resources
* Teacher knowledge-base answers
* Their own appointment requests
* Their own conversation history

## Administrator Access

An administrator can access:

* Administrative documents
* Administrative chatbot answers
* Their own appointment requests
* Their own conversation history

---

# 12. Chatbot Retrieval Collections

The chatbot searches multiple MongoDB collections:

```text
knowledge_base
documents
website_content
portal_services
portal_departments
```

## Search Purpose

| Collection           | Purpose                       |
| -------------------- | ----------------------------- |
| `knowledge_base`     | Institutional chatbot answers |
| `documents`          | Document-related information  |
| `website_content`    | Portal website content        |
| `portal_services`    | Service information           |
| `portal_departments` | Department information        |

---

# 13. Chatbot Response Source

Each chatbot response includes a source.

## Example

```json
{
  "answer": "You can access document resources through the Document Center.",
  "source": "Document Center"
}
```

The source helps users understand where the response came from.

---

# 14. API Testing with Postman

Example Postman test for chatbot:

```text
Method: POST
URL: http://127.0.0.1:5000/api/chat/message
Body Type: JSON
```

Body:

```json
{
  "message": "What services are available?"
}
```

Expected result:

```json
{
  "answer": "The portal provides access to services such as appointments, document search, academic support, and student service information.",
  "source": "Portal Services"
}
```

---

# 15. API Testing Locally

Run the application:

```bash
python app.py
```

Open local server:

```text
http://127.0.0.1:5000
```

Test the health endpoint:

```text
http://127.0.0.1:5000/health
```

---

# 16. Deployment API Testing

After deployment on Render, replace the local URL with the deployed URL.

Example:

```text
https://agora-chatbot-python.onrender.com/health
```

Example deployed chatbot endpoint:

```text
https://agora-chatbot-python.onrender.com/api/chat/message
```

---

# 17. Error Handling

## Unauthorized Access

```json
{
  "error": "Unauthorized"
}
```

Status Code:

```text
401
```

## Empty Message

```json
{
  "error": "Message cannot be empty."
}
```

Status Code:

```text
400
```

## Server Error

If an unexpected error occurs, the application uses custom error handling and the `500.html` page for server-side errors.

---

# 18. Current API Improvements

Compared to the earlier MVP version, the current API layer includes:

* MongoDB Atlas data retrieval
* MongoDB Atlas data insertion
* Groq AI response generation
* Embedded chatbot widget endpoint
* Casual conversation support
* Website content retrieval
* Portal services retrieval
* Portal departments retrieval
* Protected API routes
* Role-based filtering
* Improved response structure
* Error handling
* Deployment readiness

---

# Conclusion

The API layer connects the frontend interface, embedded chatbot widget, Flask backend, MongoDB Atlas database, and Groq AI service. These APIs support authentication-based access, chatbot responses, document search, appointment requests, conversation history, health checks, and deployment verification.

The updated API structure makes the Agora Assistant Chatbot more complete, interactive, and suitable for final demonstration and deployment.
