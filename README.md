# Agora Assistant Chatbot – Python Intelligent Campus Assistant

A Python-based Flask web application that provides an intelligent AI-powered assistant for a College Agora-style intranet portal. The system supports authentication, role-based access, MongoDB Atlas cloud storage, Groq AI response generation, document search, appointment booking, conversation history, and an embedded chatbot widget inside a modern campus portal website.

---

## Project Overview

The **Agora Assistant Chatbot** is a Python-based intelligent assistant platform designed to help students, teachers, and administrators access institutional information quickly through a centralized portal.

This project was developed as the **Python-based equivalent version** of the main Assistant Chatbot project. It follows the same functional objectives, sprint-based development process, architecture principles, and feature requirements while being implemented using Python technologies.

The platform includes a modern portal interface where users can browse services, documents, departments, appointments, and chatbot support. The embedded chatbot can answer both casual greetings and institutional questions using MongoDB-based knowledge retrieval combined with AI-generated responses.

---
## Live Deployment

The project is deployed on Render and can be accessed here:

https://agora-chatbot-python.onrender.com

```

---

## Key Features

### AI Campus Portal

* Modern portal website after login
* Embedded chatbot widget
* Department section
* Document section
* Service section
* Quick access buttons
* Responsive layout
* Navigation to dashboard, chatbot, documents, appointments, and history

---

### Authentication System

The system includes a login mechanism to protect application pages and allow users to access information based on their role.

Implemented features:

* User login
* Session-based authentication
* Protected routes
* Logout functionality
* Role-based user information

Supported roles:

* Student
* Teacher
* Administrator

---

### AI Chatbot

The chatbot is the main intelligent feature of the platform. It retrieves relevant information from MongoDB Atlas and uses Groq AI to generate clear and professional answers.

Implemented capabilities:

* Groq AI integration
* Llama 3.1 Instant response generation
* MongoDB knowledge-base retrieval
* Website content search
* Document search
* Department search
* Service search
* Source display
* Fallback response handling
* Basic casual conversation support

Example casual questions:

```text
hii
hello
how are you
thanks
bye
who are you
what can you do
```

Example portal questions:

```text
How can I book an appointment?
What documents are available?
What services are available?
What departments are available?
Where can I get student support?
```

---

### Embedded Chatbot Widget

The project includes a floating chatbot widget inside the demo portal website.

Widget features:

* Floating chatbot button
* Chat window inside the portal page
* Quick action buttons
* Chatbot responses with source information
* Suggested navigation buttons
* Links to documents, appointments, services, departments, and history

---

### Document Library

The document library allows users to view and search institutional resources.

Implemented features:

* Role-based document visibility
* Search by title, category, type, and summary
* Document cards
* Category sidebar
* MongoDB-powered document retrieval
* Improved responsive layout

Document examples:

* Student forms
* Course registration guide
* Advisor booking guide
* Academic resources
* Administrative documents
* Student service documents

---

### Appointment Management

The appointment module allows users to submit appointment requests.

Implemented features:

* Appointment booking form
* Advisor selection
* Appointment type selection
* Date selection
* Time selection
* Notes field
* MongoDB appointment storage

Supported appointment types:

* Academic advising
* Administrative support
* Student services
* Program consultation
* Technical support

---

### Conversation History

The platform stores user chatbot interactions in MongoDB Atlas.

Stored information:

* User name
* User role
* Question
* AI response
* Source
* Timestamp

Benefits:

* User activity tracking
* Previous response review
* Future analytics support
* Improved user experience

---

## REST API Endpoints

The application includes REST API endpoints used by the chatbot, widget, documents, appointments, and history modules.

Implemented endpoints:

```text
GET  /health
POST /api/chat/message
POST /api/widget/message
GET  /api/chat/history
GET  /api/documents
GET  /api/appointments
```

---

## Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Jinja2 templates

### Backend

* Python
* Flask

### Database

* MongoDB Atlas
* PyMongo

### Artificial Intelligence

* Groq API
* Llama 3.1 Instant model

### Deployment

* Render Free Plan
* Gunicorn
* GitHub

### Development Tools

* Visual Studio Code
* Git
* GitHub
* MongoDB Atlas
* Postman
* Python virtual environment

---

## System Architecture

```text
User
↓
Flask Web Interface
↓
Authentication Layer
↓
Portal / Dashboard / Chatbot Pages
↓
Chatbot Service Layer
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

## Chatbot Workflow

```text
User Question
↓
Casual Conversation Check
↓
MongoDB Search
↓
Role-Based Filtering
↓
Relevant Context Selection
↓
Groq AI Prompt Processing
↓
AI Response Generation
↓
Source Returned
↓
Conversation Saved
```

The chatbot first checks whether the message is a basic casual message such as "hi", "hello", "how are you", or "thanks". If not, it searches MongoDB collections for relevant institutional information and generates an answer using Groq AI.

---

## MongoDB Database Structure

Database name:

```text
agora_chatbot_db
```

Collections used:

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

| Collection           | Purpose                                      |
| -------------------- | -------------------------------------------- |
| `users`              | Stores user accounts, roles, and departments |
| `knowledge_base`     | Stores chatbot knowledge records             |
| `documents`          | Stores document metadata                     |
| `appointments`       | Stores appointment requests                  |
| `conversations`      | Stores chatbot interaction history           |
| `website_content`    | Stores portal page information               |
| `portal_services`    | Stores service information                   |
| `portal_departments` | Stores department information                |

---

## Project Folder Structure

```text
agora_chatbot_python/
│
├── app.py
├── mongo_db.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── .env.example
├── .gitignore
│
├── services/
│   ├── ai_service.py
│   └── chatbot_service.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── demo_site.html
│   ├── chat.html
│   ├── documents.html
│   ├── appointments.html
│   ├── history.html
│   ├── 404.html
│   └── 500.html
│
├── static/
│   ├── style.css
│   └── widget/
│       ├── widget.css
│       └── widget.js
│
├── docs/
│
└── data/
```

---

## Sprint Progress

### Sprint 1 – Planning

Completed:

* Project scope definition
* Requirement analysis
* Initial architecture planning
* Team role understanding
* Technology selection

---

### Sprint 2 – Foundation Development

Completed:

* Flask project setup
* Initial templates
* Login planning
* Knowledge-base structure
* Basic project architecture
* Initial documentation

---

### Sprint 3 – MVP Development

Completed:

* Login system
* Dashboard
* Chatbot page
* Document library
* Appointment form
* Conversation history
* Initial local data handling
* Manual testing

---

### Sprint 4 – Advanced Features

Completed:

* MongoDB Atlas integration
* Groq AI integration
* Role-based chatbot retrieval
* Advanced chatbot service layer
* API improvements
* Expanded data collections
* Professional portal UI
* Website content retrieval

---

### Sprint 5 – Testing and Stabilization

Completed:

* UI improvement
* Embedded chatbot widget
* Custom error pages
* Document layout fix
* Casual conversation handling
* Chatbot action buttons
* Testing and bug fixes
* Deployment preparation

---

## Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/Abhiptl13/agora-chatbot-python.git
```

```bash
cd agora-chatbot-python
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment.

Windows:

```bash
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create Environment File

Create a file named:

```text
.env
```

Add the following values:

```env
MONGO_URI=your_mongodb_atlas_connection_string
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key
```

Important:

```text
Do not upload .env to GitHub.
```

---

### 5. Run the Application

```bash
python app.py
```

Open in browser:

```text
http://127.0.0.1:5000
```

---

## Environment Variables

The project uses environment variables to protect sensitive credentials.

Required variables:

```env
MONGO_URI=your_mongodb_connection_string
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key
```

Recommended public example file:

```text
.env.example
```

Example `.env.example` content:

```env
MONGO_URI=your_mongodb_atlas_connection_string
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key
```

---

## Deployment Preparation

Before deploying, make sure these files exist in the project root:

```text
requirements.txt
Procfile
runtime.txt
.gitignore
.env.example
```

---

## requirements.txt

Recommended dependencies:

```txt
Flask
pymongo
python-dotenv
groq
gunicorn
```

---

## Procfile

Create a file named:

```text
Procfile
```

Add:

```text
web: gunicorn app:app
```

---

## runtime.txt

Create a file named:

```text
runtime.txt
```

Add:

```text
python-3.11.9
```

---

## .gitignore

Recommended `.gitignore` content:

```text
.env
venv/
__pycache__/
*.pyc
instance/
.pytest_cache/
.DS_Store
```

---

## Render Deployment Guide

The recommended free deployment platform for this Python-based Flask project is **Render**.

### Deployment Steps

1. Push the project to GitHub.
2. Create a Render account.
3. Select **New Web Service**.
4. Connect the GitHub repository.
5. Select the Agora chatbot repository.
6. Use the following settings:

```text
Environment: Python
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
Plan: Free
```

7. Add environment variables in Render:

```text
MONGO_URI
GROQ_API_KEY
SECRET_KEY
```

8. Deploy the application.

---

## MongoDB Atlas Deployment Setting

For Render to connect with MongoDB Atlas, MongoDB Network Access must allow Render to reach the cluster.

For project demo:

```text
0.0.0.0/0
```

This allows external access for deployment testing.

For production, restrict access to trusted IP addresses only.

---

## API Examples

### Health Check

```http
GET /health
```

Expected response:

```json
{
  "status": "running",
  "project": "Agora Assistant Chatbot - Python Version"
}
```

---

### Chat Message

```http
POST /api/chat/message
```

Example body:

```json
{
  "message": "How can I book an appointment?"
}
```

Expected response:

```json
{
  "answer": "You can book an appointment through the Appointment Services page.",
  "source": "Appointment Services"
}
```

---

### Widget Chat Message

```http
POST /api/widget/message
```

Example body:

```json
{
  "message": "What documents are available?"
}
```

Expected response:

```json
{
  "answer": "You can search academic documents, forms, guides, and support resources through the Document Center.",
  "source": "Document Center"
}
```

---

## Testing Checklist

Before final submission or deployment, test the following:

```text
Login page loads
Login redirects to /demo-site
Demo portal opens correctly
Embedded chatbot opens
Chatbot answers casual messages
Chatbot answers institutional questions
Chatbot action buttons work
Dashboard opens
Documents page layout works
Document search works
Appointment page works
Appointment form submits
History page displays conversations
404 page works
500 page exists
API health endpoint works
MongoDB connection works
Groq AI response works
```

---

## Security Features

Implemented security features:

* Session-based authentication
* Protected routes
* Role-based content filtering
* Environment variable protection
* MongoDB Atlas authentication
* API keys stored outside source code
* `.env` excluded from GitHub
* Custom error pages

Future security improvements:

* Password hashing
* JWT authentication
* Multi-factor authentication
* Audit logs
* More advanced role permissions

---

## Known Limitations

Current limitations:

* Password handling is basic for demonstration purposes
* Appointment approval workflow is not fully automated
* Document files are represented mainly as metadata
* Chatbot uses keyword scoring instead of vector search
* Admin analytics dashboard is not fully implemented
* Free Render deployment may sleep after inactivity

---

## Future Improvements

Planned improvements:

* Password hashing with Werkzeug
* Admin dashboard
* Appointment approval workflow
* Email notifications
* File upload support
* Semantic search
* Vector database integration
* Multi-turn chatbot memory
* Multilingual chatbot support
* Analytics dashboard
* Improved AI prompt engineering
* User profile management

---

## Screenshots

Add screenshots after final testing.

Recommended screenshots:

```text
Login Page
Demo Portal
Embedded Chatbot
Dashboard
Chatbot Page
Document Center
Appointment Page
Conversation History
MongoDB Collections
Render Deployment
```

Example format:

```markdown
![Login Page](docs/screenshots/login.png)
![Demo Portal](docs/screenshots/demo_portal.png)
![Chatbot Widget](docs/screenshots/chatbot_widget.png)
```

---

## Project Status

```text
Development: Completed
Testing: Completed
Deployment Preparation: In Progress
Final Deployment: Pending
```

---

## Author

```text
Abhi Ketankumar Patel
Student ID: 2431401
Internship Project – LCI LX Studio Inc.
Python-Based Equivalent Version
```

---

## Conclusion

The Agora Assistant Chatbot demonstrates a complete Python-based intelligent assistant platform for a College Agora-style intranet environment. The project combines Flask backend development, MongoDB Atlas cloud storage, Groq AI response generation, role-based access, document search, appointment management, embedded chatbot functionality, and professional user interface design.

The final system provides a strong foundation for a realistic institutional assistant and can be expanded in the future with stronger authentication, semantic search, multilingual support, analytics, and advanced administrative features.
