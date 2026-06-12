# MongoDB Architecture – Sprint 4

## Overview

The Agora Assistant Chatbot uses MongoDB Atlas as its primary cloud database platform. MongoDB replaces the JSON-based storage system used during Sprint 3 and provides a scalable, centralized, and flexible data management solution.

The database stores user accounts, chatbot knowledge records, document metadata, appointment requests, and conversation history. This improves the project from a simple local MVP into a more realistic cloud-connected web application.

---

## Database Platform

Database Type:
NoSQL Document Database

Provider:
MongoDB Atlas

Deployment:
Cloud Hosted Free Cluster

Database Name:
agora_chatbot_db

Connection Method:
MongoClient(MONGO_URI)

Environment Variable Used:
MONGO_URI

---

## Reason for Using MongoDB

MongoDB was selected for Sprint 4 because the project required more advanced data management than local JSON files.

In Sprint 3, JSON files were enough for a basic MVP. However, Sprint 4 required advanced features such as document search, appointment requests, role-based filtering, conversation history, and improved data structure. MongoDB provides a better solution for these requirements because it stores data in flexible document format and supports cloud-based access.

---

## Collections Used

The database contains the following collections:

1. users
2. knowledge_base
3. documents
4. appointments
5. conversations

Each collection supports a major feature of the chatbot system.

---

## users Collection

Purpose:

The users collection stores account information for students, teachers, and administrators.

Example Structure:

{
  "id": "u001",
  "name": "Student User",
  "email": "etudiant@college.local",
  "password": "Agora2026!",
  "role": "student",
  "department": "Student Services"
}

Main Responsibilities:

- Store user login information
- Identify user roles
- Support role-based access
- Support session-based authentication

User roles include:

- student
- teacher
- admin

---

## knowledge_base Collection

Purpose:

The knowledge_base collection stores the information used by the chatbot to answer user questions.

Example Structure:

{
  "id": "kb001",
  "title": "Class Schedule",
  "category": "Student Services",
  "keywords": ["schedule", "class", "timetable"],
  "answer": "Students can view their class schedule from the Agora intranet dashboard.",
  "audience": ["student"],
  "confidence": "high"
}

Main Responsibilities:

- Store chatbot knowledge
- Support keyword matching
- Provide context to the Groq AI model
- Filter answers based on user role
- Return relevant source information

The audience field is important because it controls which role can access a specific answer.

Example:

- student can access student services
- teacher can access teaching resources
- admin can access administrative information

---

## documents Collection

Purpose:

The documents collection stores searchable document metadata.

Example Structure:

{
  "id": "doc001",
  "title": "Course Registration Guide",
  "category": "Academic Services",
  "summary": "Guide explaining how students can register for courses.",
  "type": "Guide",
  "audience": ["student"]
}

Main Responsibilities:

- Store document information
- Support search by title, category, summary, and type
- Display documents based on user role
- Support the document library module

This allows each user type to only view the documents relevant to their role.

---

## appointments Collection

Purpose:

The appointments collection stores appointment requests submitted by users.

Example Structure:

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

Main Responsibilities:

- Store appointment requests
- Track appointment status
- Store selected advisor
- Store appointment date and time
- Support future appointment management features

---

## conversations Collection

Purpose:

The conversations collection stores chatbot interaction history.

Example Structure:

{
  "user": "etudiant@college.local",
  "name": "Student User",
  "role": "student",
  "question": "Where can I see my class schedule?",
  "answer": "Students can view their class schedule from the Agora dashboard.",
  "source": "Class Schedule",
  "timestamp": "2026-06-11 14:30:00"
}

Main Responsibilities:

- Store user questions
- Store chatbot responses
- Store source used
- Store timestamp
- Allow users to review previous conversations

---

## Database Flow

User logs in
↓
Flask validates user from MongoDB users collection
↓
Session is created
↓
User opens chatbot, documents, appointments, or history
↓
Flask queries the correct MongoDB collection
↓
Data is filtered by role
↓
Response is returned to the frontend

---

## Chatbot Data Flow

User asks a question
↓
Question is sent to /api/chat/message
↓
Flask reads the user role from session
↓
MongoDB knowledge_base collection is searched
↓
Best matching knowledge entry is selected
↓
Groq AI generates a cleaner answer using the selected context
↓
Answer is returned to the chat interface
↓
Conversation is saved in MongoDB conversations collection

---

## Security Notes

Current Security Controls:

- MongoDB connection string stored in .env
- .env file ignored using .gitignore
- Protected routes using session checking
- Role-based data filtering
- API access requires login

Current Limitations:

- Passwords are stored as plain text for demo purposes
- JWT authentication is not implemented yet
- Advanced permission management is not implemented yet

Future Improvements:

- Password hashing
- JWT authentication
- Admin dashboard for user management
- Appointment status updates
- Audit logs

---

## Sprint 3 vs Sprint 4 Database Comparison

| Area | Sprint 3 | Sprint 4 |
|---|---|---|
| Storage | JSON files | MongoDB Atlas |
| Location | Local project folder | Cloud database |
| Scalability | Limited | Improved |
| Search | Basic file search | MongoDB query search |
| History | JSON file | MongoDB collection |
| Appointments | JSON file | MongoDB collection |
| Maintenance | Manual file editing | Collection-based management |

---

## Conclusion

MongoDB Atlas significantly improves the backend structure of the Agora Assistant Chatbot. It supports advanced Sprint 4 features such as role-based filtering, document search, appointment requests, conversation history, and scalable data storage. This upgrade makes the Python version more professional and closer to a real-world web application.