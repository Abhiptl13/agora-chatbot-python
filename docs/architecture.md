# Agora Assistant Chatbot – System Architecture

## Overview

The Agora Assistant Chatbot is a Flask-based web application designed to assist students, teachers, and administrators through an intelligent intranet assistant.

The application provides authentication, AI-powered chatbot functionality, document search, appointment requests, and conversation history while using MongoDB Atlas for cloud data storage and Groq AI for intelligent response generation.

---

# System Architecture

The system follows a three-layer architecture:

1. Presentation Layer
2. Application Layer
3. Data Layer

---

# Presentation Layer

Technologies:

- HTML5
- CSS3
- JavaScript

Responsibilities:

- User Interface
- Form Submission
- Chat Interface
- Document Search Interface
- Appointment Request Interface
- Conversation History Interface

Pages:

- Login
- Dashboard
- Chatbot
- Documents
- Appointments
- History
- Error Pages

---

# Application Layer

Technology:

- Python Flask

Responsibilities:

- User Authentication
- Session Management
- API Processing
- Business Logic
- Role-Based Access Control
- Chatbot Processing
- MongoDB Communication
- Groq AI Integration

Main Modules:

- Authentication Module
- Chatbot Module
- Document Search Module
- Appointment Module
- History Module
- API Module

---

# Artificial Intelligence Layer

Provider:

Groq API

Model:

Llama 3.1 Instant

Responsibilities:

- Response Generation
- Context Processing
- Natural Language Responses
- Knowledge Enhancement

Workflow:

Knowledge Base Retrieval
↓
Context Selection
↓
Groq AI Processing
↓
Natural Language Response

---

# Database Layer

Provider:

MongoDB Atlas

Database:

agora_chatbot_db

Collections:

- users
- knowledge_base
- documents
- appointments
- conversations

Responsibilities:

- Data Storage
- Data Retrieval
- Search Operations
- Conversation Tracking
- Appointment Management

---

# Application Flow

User
↓
Login
↓
Flask Authentication
↓
MongoDB User Validation
↓
Session Creation
↓
Dashboard
↓
Application Modules
↓
MongoDB / Groq AI
↓
Response Returned

---

# Chatbot Architecture Flow

User Question
↓
Chat Interface
↓
POST /api/chat/message
↓
Flask Backend
↓
Role Detection
↓
MongoDB Knowledge Base Search
↓
Best Match Selection
↓
Groq AI Response Generation
↓
Conversation Saved
↓
Response Returned

---

# Security Architecture

Current Security Features:

- Session Authentication
- Protected Routes
- Role-Based Filtering
- Environment Variables
- MongoDB Atlas Security

Protected Endpoints:

- /dashboard
- /chat
- /documents
- /appointments
- /history
- /api/*

Future Security Improvements:

- JWT Authentication
- Password Hashing
- Multi-Factor Authentication
- Audit Logging

---

# Technology Stack

Frontend

- HTML5
- CSS3
- JavaScript

Backend

- Python
- Flask

Database

- MongoDB Atlas

Artificial Intelligence

- Groq API
- Llama 3.1

Development Tools

- Visual Studio Code
- Git
- GitHub

---

# Sprint 4 Architecture Improvements

| Sprint 3 | Sprint 4 |
|-----------|-----------|
| JSON Storage | MongoDB Atlas |
| Local Responses | Groq AI |
| Basic Matching | Advanced Matching |
| Local Data Files | Cloud Database |
| Basic MVP | Advanced Feature Version |

---

# Conclusion

The Sprint 4 architecture provides a scalable and maintainable foundation for the Agora Assistant Chatbot. The integration of MongoDB Atlas and Groq AI significantly improves application functionality, response quality, and long-term scalability while maintaining a clean Python Flask architecture.