# Agora Assistant Chatbot – System Architecture

## Overview

The Agora Assistant Chatbot is a Python-based Flask web application designed to support students, teachers, and administrators through an intelligent campus assistant platform.

The application provides authentication, role-based access, AI-powered chatbot responses, document search, appointment booking, conversation history, a modern campus portal interface, and an embedded chatbot widget. The system uses MongoDB Atlas for cloud-based data storage and Groq AI for natural language response generation.

This architecture represents the Python-based equivalent version of the main Assistant Chatbot project and follows the same functional objectives while using Python technologies.

---

## Architecture Objective

The main objective of the architecture is to provide a modular, scalable, and maintainable structure for the Agora Assistant Chatbot.

The architecture supports:

* Secure user authentication
* Role-based information access
* AI-powered question answering
* MongoDB-based data storage
* Embedded chatbot functionality
* Document and service discovery
* Appointment request handling
* Conversation tracking
* Deployment readiness

---

## High-Level System Architecture

```text
User Browser
↓
Flask Web Application
↓
Authentication and Session Layer
↓
Portal / Dashboard / Module Pages
↓
Service Layer
↓
MongoDB Atlas Retrieval
↓
Groq AI Response Generation
↓
Response Returned to User
↓
Conversation Stored in MongoDB
```

---

## Main Architecture Layers

The system follows a layered architecture:

```text
1. Presentation Layer
2. Application Layer
3. Service Layer
4. Artificial Intelligence Layer
5. Data Layer
6. Deployment Layer
```

---

## 1. Presentation Layer

The presentation layer contains the user interface of the application.

### Technologies

* HTML5
* CSS3
* JavaScript
* Jinja2 Templates

### Responsibilities

* Display application pages
* Render user-specific content
* Submit forms
* Display chatbot conversations
* Show document cards
* Display appointment forms
* Provide navigation between modules
* Support embedded chatbot interaction

### Main Pages

```text
login.html
base.html
dashboard.html
demo_site.html
chat.html
documents.html
appointments.html
history.html
404.html
500.html
```

### Static Resources

```text
static/style.css
static/widget/widget.css
static/widget/widget.js
```

---

## 2. Application Layer

The application layer is handled by Flask and is responsible for routing, authentication, session management, and page rendering.

### Technology

```text
Python Flask
```

### Main File

```text
app.py
```

### Responsibilities

* Initialize Flask application
* Manage user sessions
* Handle login and logout
* Protect routes
* Render templates
* Process form submissions
* Provide REST API endpoints
* Connect frontend requests to service logic

### Main Routes

```text
/
 /login
 /dashboard
 /demo-site
 /chat
 /documents
 /appointments
 /history
 /logout
 /health
```

---

## 3. Service Layer

The service layer separates business logic from route handling.

### Service Files

```text
services/ai_service.py
services/chatbot_service.py
```

### ai_service.py

Responsibilities:

* Connect to Groq AI
* Send prompts to the AI model
* Receive generated responses
* Handle AI-related errors

### chatbot_service.py

Responsibilities:

* Process user questions
* Detect casual conversation
* Search MongoDB collections
* Apply role-based filtering
* Select relevant context
* Prepare AI prompt
* Return chatbot answer and source

---

## 4. Artificial Intelligence Layer

The AI layer improves chatbot responses by generating natural language answers from retrieved MongoDB context.

### Provider

```text
Groq API
```

### Model

```text
Llama 3.1 Instant
```

### Responsibilities

* Natural language response generation
* Context interpretation
* User-friendly explanation
* Professional chatbot responses
* Support for institutional question answering

### Chatbot Processing Flow

```text
User Message
↓
Casual Conversation Check
↓
MongoDB Search
↓
Role-Based Filtering
↓
Top Relevant Context Selection
↓
Groq AI Prompt Creation
↓
AI Response Generation
↓
Source Returned
↓
Conversation Saved
```

### Casual Conversation Handling

The chatbot first checks for basic messages such as:

```text
hi
hello
hii
how are you
thanks
bye
who are you
what can you do
```

If the message is casual, the chatbot responds directly without searching MongoDB.

---

## 5. Data Layer

The data layer uses MongoDB Atlas as the central cloud database.

### Database Provider

```text
MongoDB Atlas
```

### Database Name

```text
agora_chatbot_db
```

### Collections

```text
users
knowledge_base
documents
appointments
conversations
website_content
portal_services
portal_departments
```

### Collection Responsibilities

| Collection           | Purpose                                                 |
| -------------------- | ------------------------------------------------------- |
| `users`              | Stores user account information, roles, and departments |
| `knowledge_base`     | Stores chatbot knowledge records                        |
| `documents`          | Stores document metadata and summaries                  |
| `appointments`       | Stores appointment requests                             |
| `conversations`      | Stores chatbot conversation history                     |
| `website_content`    | Stores portal page content used by the chatbot          |
| `portal_services`    | Stores service information                              |
| `portal_departments` | Stores department information                           |

---

## MongoDB Connection Architecture

Database connection is managed through:

```text
mongo_db.py
```

### Responsibilities

* Load environment variables
* Connect to MongoDB Atlas
* Define database object
* Provide access to MongoDB collections

### Connection Flow

```text
Flask Application
↓
mongo_db.py
↓
MongoClient
↓
MongoDB Atlas Cluster
↓
agora_chatbot_db
↓
Application Collections
```

---

## Embedded Chatbot Widget Architecture

The embedded chatbot widget allows users to chat with the assistant directly from the demo portal page.

### Widget Files

```text
static/widget/widget.css
static/widget/widget.js
```

### Widget API Endpoint

```text
POST /api/widget/message
```

### Widget Features

* Floating chatbot button
* Chat popup window
* Quick action buttons
* Casual conversation support
* AI-generated answers
* Source display
* Suggested navigation buttons
* Links to documents, appointments, services, departments, and history

### Widget Flow

```text
User Opens Widget
↓
User Sends Message
↓
JavaScript Sends POST Request
↓
Flask Widget API Receives Message
↓
Chatbot Service Processes Message
↓
MongoDB / Groq AI Used
↓
Answer Returned to Widget
↓
Widget Displays Answer and Suggested Actions
```

---

## REST API Architecture

The application provides API endpoints for frontend-backend communication.

### Implemented API Endpoints

```text
GET  /health
POST /api/chat/message
POST /api/widget/message
GET  /api/chat/history
GET  /api/documents
GET  /api/appointments
```

### API Responsibilities

* Process chatbot messages
* Return chatbot answers
* Store conversation history
* Retrieve documents
* Retrieve appointments
* Verify application health

---

## Authentication and Access Flow

```text
User Opens Application
↓
Login Page
↓
Credentials Submitted
↓
MongoDB User Validation
↓
Session Created
↓
Redirect to Demo Portal
↓
Protected Pages Become Accessible
```

### Protected Pages

```text
/dashboard
/demo-site
/chat
/documents
/appointments
/history
```

---

## Role-Based Access Design

The system supports three main user roles:

```text
Student
Teacher
Administrator
```

Role information is stored in the user session after login.

The chatbot uses the user role to filter MongoDB knowledge records and documents so that users receive content appropriate to their role.

---

## Chatbot Architecture Flow

```text
User Question
↓
Chat Interface or Embedded Widget
↓
POST Request to Flask API
↓
Role Detection from Session
↓
Casual Message Check
↓
MongoDB Collection Search
↓
Knowledge / Document / Website / Service / Department Matching
↓
Top Results Selected
↓
Groq AI Prompt Generated
↓
AI Answer Returned
↓
Conversation Saved in MongoDB
↓
Response Displayed to User
```

---

## Search and Retrieval Architecture

The chatbot searches multiple MongoDB collections:

```text
knowledge_base
documents
website_content
portal_services
portal_departments
```

The matching logic checks fields such as:

* Title
* Category
* Keywords
* Summary
* Content
* Description
* Type

Results are scored and sorted by relevance before being passed to the AI model.

---

## Conversation History Architecture

When a user sends a chatbot message, the system stores the interaction in MongoDB.

### Stored Conversation Data

* User name
* User role
* Question
* Chatbot response
* Source
* Timestamp
* Module source

### Benefits

* Allows users to review previous conversations
* Supports testing and validation
* Provides future analytics possibility
* Improves project completeness

---

## Document Module Architecture

The document module retrieves document records from MongoDB and displays them in a structured grid layout.

### Responsibilities

* Display document cards
* Support keyword search
* Show document category
* Show document type
* Show document summary
* Provide role-aware document visibility

### Document Flow

```text
User Opens Documents Page
↓
Flask Reads Query Parameter
↓
MongoDB Documents Collection Searched
↓
Matching Documents Returned
↓
documents.html Displays Results
```

---

## Appointment Module Architecture

The appointment module allows users to submit appointment requests.

### Responsibilities

* Display appointment form
* Capture appointment details
* Validate form data
* Store request in MongoDB
* Confirm submission to user

### Appointment Flow

```text
User Opens Appointment Page
↓
User Completes Form
↓
Form Submitted to Flask
↓
Appointment Data Validated
↓
Appointment Saved in MongoDB
↓
Confirmation Displayed
```

---

## Error Handling Architecture

The system includes custom error pages:

```text
404.html
500.html
```

### 404 Page

Displayed when a user visits a route that does not exist.

### 500 Page

Displayed when an internal server error occurs.

These pages improve the professional quality of the application and user experience.

---

## Security Architecture

### Current Security Features

* Session-based authentication
* Protected routes
* Role-based filtering
* Environment variable protection
* MongoDB Atlas authentication
* API keys stored outside source code
* `.env` excluded from GitHub
* Custom error pages

### Protected Resources

```text
/dashboard
/demo-site
/chat
/documents
/appointments
/history
/api/*
```

### Future Security Improvements

* Password hashing
* JWT authentication
* Multi-factor authentication
* Audit logging
* Admin permission management
* Stronger form validation

---

## Environment Configuration Architecture

Sensitive configuration values are stored outside the codebase using environment variables.

### Required Variables

```text
MONGO_URI
GROQ_API_KEY
SECRET_KEY
```

### Local Development

Local values are stored in:

```text
.env
```

### Public Example File

Public example values are stored in:

```text
.env.example
```

### Deployment

On Render, environment variables are added through the Render dashboard.

---

## Deployment Architecture

The application is prepared for free deployment using Render.

### Deployment Flow

```text
GitHub Repository
↓
Render Web Service
↓
Build Command
↓
Install Dependencies
↓
Start Command
↓
Gunicorn Runs Flask App
↓
Application Available Through Public URL
```

### Required Deployment Files

```text
requirements.txt
Procfile
runtime.txt
.env.example
.gitignore
README.md
```

### Render Settings

```text
Environment: Python
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
Plan: Free
```

---

## Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Jinja2 Templates

### Backend

* Python
* Flask

### Database

* MongoDB Atlas
* PyMongo

### Artificial Intelligence

* Groq API
* Llama 3.1 Instant

### Production Server

* Gunicorn

### Deployment

* Render
* GitHub

### Development Tools

* Visual Studio Code
* Git
* GitHub
* Postman
* MongoDB Atlas

---

## Sprint-Based Architecture Evolution

| Sprint   | Architecture Status                                                       |
| -------- | ------------------------------------------------------------------------- |
| Sprint 1 | Project scope and initial planning                                        |
| Sprint 2 | Flask foundation and basic page structure                                 |
| Sprint 3 | MVP with login, chatbot, documents, appointments, and history             |
| Sprint 4 | MongoDB Atlas and Groq AI integration                                     |
| Sprint 5 | Embedded chatbot widget, improved UI, testing, and deployment preparation |

---

## Architecture Improvements

Major improvements completed during later development stages:

* Migration from local JSON storage to MongoDB Atlas
* Integration of Groq AI
* Addition of website content retrieval
* Addition of service and department data collections
* Embedded chatbot widget inside the portal
* Action buttons and suggested navigation links
* Casual conversation support
* Improved document grid layout
* Custom 404 and 500 pages
* Deployment preparation using Render

---

## Conclusion

The Agora Assistant Chatbot architecture provides a modular and maintainable foundation for a Python-based intelligent campus assistant platform. The system combines Flask routing, MongoDB Atlas cloud storage, Groq AI response generation, role-based filtering, document search, appointment handling, conversation history, and embedded chatbot functionality.

This architecture supports local development, project demonstration, future expansion, and free deployment through Render while maintaining clear separation between presentation, application logic, service processing, AI integration, and data storage.
