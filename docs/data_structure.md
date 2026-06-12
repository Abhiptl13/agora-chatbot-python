# Data Structure – Sprint 4

## Overview

The Agora Assistant Chatbot uses MongoDB Atlas as its primary data storage solution. The database is organized into collections that support authentication, chatbot knowledge retrieval, document management, appointment requests, and conversation history.

The data structure was redesigned during Sprint 4 to improve scalability, maintainability, and support cloud-based storage.

---

# Database

Database Name:

agora_chatbot_db

Collections:

- users
- knowledge_base
- documents
- appointments
- conversations

---

# users Collection

## Purpose

Stores user account information and role assignments.

## Fields

| Field | Type | Description |
|---------|---------|-------------|
| id | String | Unique user identifier |
| name | String | User full name |
| email | String | Login email |
| password | String | User password |
| role | String | User role |
| department | String | User department |

## Example

```json
{
  "id": "u001",
  "name": "Student User",
  "email": "etudiant@college.local",
  "password": "Agora2026!",
  "role": "student",
  "department": "Student Services"
}
```

---

# knowledge_base Collection

## Purpose

Stores chatbot knowledge records used to answer user questions.

## Fields

| Field | Type | Description |
|---------|---------|-------------|
| id | String | Knowledge record ID |
| title | String | Topic title |
| category | String | Knowledge category |
| keywords | Array | Search keywords |
| answer | String | Knowledge answer |
| audience | Array | Allowed user roles |
| confidence | String | Confidence level |

## Example

```json
{
  "id": "kb001",
  "title": "Class Schedule",
  "category": "Academic Services",
  "keywords": [
    "schedule",
    "class",
    "timetable"
  ],
  "answer": "Students can view their class schedule from the Agora dashboard.",
  "audience": [
    "student"
  ],
  "confidence": "high"
}
```

---

# documents Collection

## Purpose

Stores searchable document metadata.

## Fields

| Field | Type | Description |
|---------|---------|-------------|
| id | String | Document ID |
| title | String | Document title |
| category | String | Document category |
| summary | String | Document summary |
| type | String | Document type |
| audience | Array | Allowed user roles |

## Example

```json
{
  "id": "doc001",
  "title": "Course Registration Guide",
  "category": "Academic Services",
  "summary": "Guide explaining course registration.",
  "type": "Guide",
  "audience": [
    "student"
  ]
}
```

---

# appointments Collection

## Purpose

Stores appointment requests submitted by users.

## Fields

| Field | Type | Description |
|---------|---------|-------------|
| user | String | User email |
| role | String | User role |
| name | String | User name |
| appointment_type | String | Appointment category |
| advisor | String | Selected advisor |
| date | String | Appointment date |
| time | String | Appointment time |
| notes | String | Additional notes |
| status | String | Request status |
| created_at | String | Creation timestamp |

## Example

```json
{
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
```

---

# conversations Collection

## Purpose

Stores chatbot interaction history.

## Fields

| Field | Type | Description |
|---------|---------|-------------|
| user | String | User email |
| name | String | User name |
| role | String | User role |
| question | String | User question |
| answer | String | Chatbot answer |
| source | String | Knowledge source |
| timestamp | String | Interaction timestamp |

## Example

```json
{
  "user": "etudiant@college.local",
  "name": "Student User",
  "role": "student",
  "question": "Where can I see my class schedule?",
  "answer": "Students can view their class schedule from the dashboard.",
  "source": "Class Schedule",
  "timestamp": "2026-06-11 14:30:00"
}
```

---

# Relationships Between Collections

users
↓
appointments

users
↓
conversations

knowledge_base
↓
chatbot responses

documents
↓
document search

---

# Role-Based Access Structure

Supported Roles:

- student
- teacher
- admin

Role filtering is applied to:

- Knowledge Base Records
- Documents
- Chatbot Responses
- API Responses

This ensures users only access information relevant to their responsibilities.

---

# Data Flow

User Action
↓
Flask Backend
↓
MongoDB Collection
↓
Data Processing
↓
Role Filtering
↓
Response Returned

---

# Sprint 4 Improvements

Major improvements introduced in Sprint 4:

- Migration from JSON files to MongoDB Atlas
- Structured collections
- Cloud-based storage
- Improved search capability
- Expanded sample data
- Support for AI integration
- Improved scalability

---

# Conclusion

The Sprint 4 data structure provides a scalable and organized foundation for the Agora Assistant Chatbot. The use of MongoDB collections improves performance, maintainability, and supports future application growth while enabling advanced features such as AI integration, conversation tracking, appointment management, and role-based access control.