# Agora Assistant Chatbot – Python Intelligent Campus Assistant

A Python-based Flask web application that provides an intelligent AI-powered assistant for a College Lasalle-style intranet portal. The system supports authentication, role-based access, MongoDB Atlas cloud storage, MongoDB GridFS PDF storage, Groq AI response generation, MongoDB Atlas Vector Search, appointment booking, document management, conversation history, and an embedded chatbot widget inside a modern campus portal website.

---

## Live Deployment

The project is deployed on Render and can be accessed here:

```text
https://agora-chatbot-python.onrender.com
```

Login page:

```text
https://agora-chatbot-python.onrender.com/login
```

---

## Project Overview

The **Agora Assistant Chatbot** is a Python-based intelligent assistant platform designed to help students, teachers, and administrators access institutional information quickly through a centralized portal.

This project was developed as the **Python-based equivalent version** of the main Assistant Chatbot project. It follows the same functional objectives, sprint-based development process, architecture principles, and feature requirements while being implemented using Python technologies.

The platform includes a modern portal interface where users can browse services, documents, departments, appointments, and chatbot support. The embedded chatbot can answer casual greetings and institutional questions using MongoDB-based retrieval, MongoDB Atlas Vector Search, and AI-generated responses through the Groq API.

---

## Screenshots

Screenshots are included to demonstrate the final working system.

> Save your screenshots inside this folder:

```text
docs/screenshots/
```

Recommended screenshot files:

```text
docs/screenshots/login.png
docs/screenshots/demo-portal.png
docs/screenshots/dashboard.png
docs/screenshots/chatbot-page.png
docs/screenshots/chatbot-widget.png
docs/screenshots/document-center.png
docs/screenshots/pdf-preview.png
docs/screenshots/appointments.png
docs/screenshots/admin-appointments.png
docs/screenshots/conversation-history.png
docs/screenshots/mongodb-collections.png
docs/screenshots/vector-search-indexes.png
docs/screenshots/render-deployment.png
```

### Login Page

![Login Page](docs/screenshots/login.png)

### Demo Portal

![Demo Portal](docs/screenshots/demo-portal.png)

### Dashboard

![Dashboard](docs/screenshots/dashboard.png)

### Chatbot Page

![Chatbot Page](docs/screenshots/chatbot-page.png)

### Embedded Chatbot Widget

![Embedded Chatbot Widget](docs/screenshots/chatbot-widget.png)

### Document Center

![Document Center](docs/screenshots/document-center.png)

### PDF Preview

![PDF Preview](docs/screenshots/pdf-preview.png)

### Appointment Page

![Appointment Page](docs/screenshots/appointments.png)

### Admin Appointment Management

![Admin Appointment Management](docs/screenshots/admin-appointments.png)

### Conversation History

![Conversation History](docs/screenshots/conversation-history.png)

### MongoDB Collections

![MongoDB Collections](docs/screenshots/mongodb-collections.png)

### MongoDB Atlas Vector Search Indexes

![MongoDB Atlas Vector Search Indexes](docs/screenshots/vector-search-indexes.png)

### Render Deployment

![Render Deployment](docs/screenshots/render-deployment.png)

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
* Role-based access control
* Secure password verification
* Automatic password upgrade from plain text to hashed password when needed

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
* MongoDB Atlas Vector Search
* MongoDB regex fallback search
* Knowledge base retrieval
* Website content search
* Document and PDF content search
* Department search
* Service search
* Source display
* Fallback response handling
* Casual conversation support
* Strict guardrails to prevent hallucinated answers

If the database context does not contain the answer, the chatbot is instructed to reply:

```text
I cannot find this information in the database.
```

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
Which courses are offered?
How can students register for courses?
Where can I get student support?
What services are available?
```

---

## MongoDB Atlas Vector Search

MongoDB Atlas Vector Search is implemented for semantic chatbot retrieval.

Vector Search is enabled on:

```text
knowledge_base
documents
website_content
```

The system uses the SentenceTransformers model:

```text
all-MiniLM-L6-v2
```

Embedding dimensions:

```text
384
```

Vector Search index name:

```text
vector_index
```

Vector Search index JSON:

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 384,
      "similarity": "cosine"
    }
  ]
}
```

The chatbot search order is:

```text
1. MongoDB Atlas Vector Search
2. MongoDB regex fallback search
3. Groq AI response generation using only retrieved database context
```

This improves semantic retrieval and allows the chatbot to understand meaning, not only exact keywords.

---

## Chatbot Retrieval Fixes

Several important chatbot retrieval issues were fixed during development.

### 1. Inverted Search Logic

Old issue:

```text
The chatbot checked whether a full document title existed inside the short user question.
```

Fix:

```text
The question is now tokenized, and meaningful words are compared against searchable database fields.
```

---

### 2. Naive Non-Tokenized Scoring

Old issue:

```text
Raw string matching caused poor results when the user used different wording.
```

Fix:

```text
Tokenized scoring, stop-word filtering, plural handling, and weighted field scoring were added.
```

---

### 3. Brute Force Database Scanning

Old issue:

```text
The chatbot loaded entire MongoDB collections into memory for every message request.
```

Fix:

```text
MongoDB-side filtering and Vector Search are now used to reduce unnecessary memory usage.
```

---

### 4. Context Field Mismatch

Old issue:

```text
The chatbot expected only the answer field, but imported records often used text, summary, content, description, or content_text.
```

Fix:

```text
The chatbot now checks multiple fields:
answer, text, summary, content, description, and content_text.
```

---

### 5. LLM Guardrails

Old issue:

```text
The AI could generate unsupported answers when the retrieved context was empty.
```

Fix:

```text
The Groq prompt now strictly tells the model to use only database context and not guess.
```

---

## Embedded Chatbot Widget

The project includes a floating chatbot widget inside the demo portal website.

Widget features:

* Floating chatbot button
* Chat window inside the portal page
* Quick action buttons
* Chatbot responses with source information
* Suggested navigation buttons
* Links to documents, appointments, services, departments, and history

---

## Document Center and PDF Storage

The document center allows users to view, search, preview, and download institutional resources.

Implemented features:

* Role-based document visibility
* Search by title, category, type, summary, file name, and extracted PDF text
* Document cards
* Category sidebar
* MongoDB-powered document retrieval
* PDF upload for teachers and administrators
* PDF preview
* PDF download
* PDF text extraction using `pypdf`
* PDF storage using MongoDB GridFS
* Vector embedding generation for uploaded documents
* Orphan GridFS cleanup if document metadata insertion fails

PDF metadata is stored in:

```text
documents
```

PDF file bytes are stored in:

```text
document_files.files
document_files.chunks
```

Document examples:

* Student forms
* Course registration guide
* Advisor booking guide
* Academic resources
* Administrative documents
* Student service documents

---

## Appointment Management

The appointment module allows users to submit appointment requests.

Implemented features:

* Appointment booking form
* Advisor selection
* Appointment type selection
* Date selection
* Time selection
* Notes field
* MongoDB appointment storage
* Pending appointment status
* Admin appointment review
* Admin approval or rejection workflow

Supported appointment types:

* Academic advising
* Administrative support
* Student services
* Program consultation
* Technical support

Important note:

```text
The application saves appointment requests as Pending. Email confirmation is not currently implemented.
```

The chatbot is instructed not to promise email notifications or automatic confirmations.

---

## Conversation History

The platform stores user chatbot interactions in MongoDB Atlas.

Stored information:

* User name
* User email
* User role
* Question
* AI response
* Source
* Module
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
POST /api/appointments
POST /api/admin/appointments/<appointment_id>/status
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
* Werkzeug Security
* pypdf

### Database and Storage

* MongoDB Atlas
* PyMongo
* MongoDB GridFS

### Artificial Intelligence and Search

* Groq API
* Llama 3.1 Instant model
* SentenceTransformers
* all-MiniLM-L6-v2
* MongoDB Atlas Vector Search
* MongoDB regex fallback search

### Deployment

* Render
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
MongoDB Atlas Vector Search
↓
MongoDB Regex Fallback
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
Question Tokenization
↓
Vector Search on MongoDB Atlas
↓
Regex Fallback Search
↓
Role-Based Filtering
↓
Relevant Context Selection
↓
Strict Groq Prompt Processing
↓
AI Response Generation
↓
Source Returned
↓
Conversation Saved
```

The chatbot first checks whether the message is a basic casual message such as `hi`, `hello`, `how are you`, or `thanks`. If not, it searches MongoDB collections for relevant institutional information and generates an answer using Groq AI.

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
document_files.files
document_files.chunks
```

| Collection              | Purpose                                                      |
| ----------------------- | ------------------------------------------------------------ |
| `users`                 | Stores user accounts, roles, departments, and passwords      |
| `knowledge_base`        | Stores chatbot knowledge records                             |
| `documents`             | Stores document metadata, extracted PDF text, and embeddings |
| `appointments`          | Stores appointment requests                                  |
| `conversations`         | Stores chatbot interaction history                           |
| `website_content`       | Stores portal page information                               |
| `portal_services`       | Stores service information                                   |
| `portal_departments`    | Stores department information                                |
| `document_files.files`  | Stores GridFS PDF file metadata                              |
| `document_files.chunks` | Stores GridFS PDF file chunks                                |

Vector Search indexes are created on:

```text
knowledge_base
documents
website_content
```

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
├── README.md
│
├── services/
│   ├── ai_service.py
│   ├── chatbot_service.py
│   └── vector_embedding_service.py
│
├── scripts/
│   ├── backfill_embeddings.py
│   ├── check_embeddings.py
│   └── test_vector_search.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── demo_site.html
│   ├── chat.html
│   ├── documents.html
│   ├── appointments.html
│   ├── admin_appointments.html
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
└── docs/
    └── screenshots/
        ├── login.png
        ├── demo-portal.png
        ├── dashboard.png
        ├── chatbot-page.png
        ├── chatbot-widget.png
        ├── document-center.png
        ├── pdf-preview.png
        ├── appointments.png
        ├── admin-appointments.png
        ├── conversation-history.png
        ├── mongodb-collections.png
        ├── vector-search-indexes.png
        └── render-deployment.png
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

### Final Enhancement – Retrieval Optimization and Vector Search

Completed:

* Fixed inverted chatbot search logic
* Added tokenized scoring
* Added MongoDB regex filtering
* Removed inefficient full collection scan from chatbot search
* Added multi-field context extraction
* Added strict Groq guardrails
* Added MongoDB GridFS PDF storage
* Added PDF text extraction
* Added embedding generation
* Added embedding backfill script
* Added MongoDB Atlas Vector Search indexes
* Integrated Vector Search into chatbot response flow
* Added regex fallback for reliability

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
MONGO_DB_NAME=agora_chatbot_db
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
SECRET_KEY=your_secret_key
FLASK_DEBUG=0
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

Required variables:

```env
MONGO_URI=your_mongodb_connection_string
MONGO_DB_NAME=agora_chatbot_db
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
SECRET_KEY=your_secret_key
FLASK_DEBUG=0
```

Recommended public example file:

```text
.env.example
```

Example `.env.example` content:

```env
MONGO_URI=your_mongodb_atlas_connection_string
MONGO_DB_NAME=agora_chatbot_db
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
SECRET_KEY=your_secret_key
FLASK_DEBUG=0
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
pypdf
sentence-transformers
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
MONGO_DB_NAME
GROQ_API_KEY
GROQ_MODEL
SECRET_KEY
FLASK_DEBUG
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

## MongoDB Atlas Vector Search Setup

Create a Vector Search index named:

```text
vector_index
```

Create it on these collections:

```text
knowledge_base
documents
website_content
```

Use this JSON:

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 384,
      "similarity": "cosine"
    }
  ]
}
```

After creating the indexes, wait until each index status shows:

```text
READY
```

or:

```text
ACTIVE
```

---

## Embedding Scripts

### Backfill Existing Records

Run:

```bash
python scripts/backfill_embeddings.py
```

This adds embeddings to existing MongoDB records.

### Check Embeddings

Run:

```bash
python scripts/check_embeddings.py
```

This verifies how many records have embeddings.

### Test Vector Search

Run:

```bash
python scripts/test_vector_search.py
```

Example successful result:

```text
Testing Vector Search on: knowledge_base
Title: Course Registration
Score: 0.7449570894241333
```

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
  "project": "Agora Assistant Chatbot - Python Version",
  "database": "MongoDB Atlas",
  "file_storage": "MongoDB GridFS",
  "ai_provider": "Groq API",
  "vector_search_ready": true
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
  "message": "Which courses are offered?"
}
```

Expected response:

```json
{
  "question": "Which courses are offered?",
  "answer": "Students can complete course registration through the Agora intranet registration section.",
  "source": "Course Registration",
  "matched": true
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
  "message": "How can I book an appointment?"
}
```

Expected response:

```json
{
  "question": "How can I book an appointment?",
  "answer": "You can book an appointment through the appointment page.",
  "source": "Academic Advisor Booking Guide",
  "matched": true,
  "module": "embedded_widget"
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
Chatbot uses Vector Search results
Chatbot fallback works
Chatbot action buttons work
Dashboard opens
Documents page layout works
Document search works
PDF upload works
PDF preview works
PDF download works
Appointment page works
Appointment form submits
Admin appointment page opens
Admin can approve appointment
Admin can reject appointment
History page displays conversations
404 page works
500 page exists
API health endpoint works
MongoDB connection works
GridFS file storage works
Groq AI response works
Vector Search indexes are READY
Render deployment works
Screenshots are added to docs/screenshots
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
* Password hashing with Werkzeug
* Automatic password upgrade for old plain-text demo passwords
* Custom error pages
* File upload restricted to PDFs
* Maximum upload size limit
* Secure filename handling

Future security improvements:

* CSRF protection
* Multi-factor authentication
* Audit logs
* More advanced role permissions
* Stronger PDF content validation

---

## Known Limitations

Current limitations:

* Email confirmations for appointments are not implemented.
* Public self-registration is not enabled.
* Admin-created or seeded accounts are required.
* Free Render deployment may sleep after inactivity.
* MongoDB Atlas M0 free cluster has Search/Vector index limits.
* Some collections may use regex fallback if Vector Search index slots are unavailable.
* Scanned image-only PDFs may not be searchable unless OCR is added in the future.

---

## Future Improvements

Planned improvements:

* Email notifications for appointments
* OCR for scanned PDFs
* Admin user-management page
* CSRF protection
* Audit logs
* Advanced analytics dashboard
* Multilingual chatbot support
* User profile management
* Vector Search indexes for all searchable collections after MongoDB upgrade
* More advanced AI prompt monitoring and evaluation

---

## Project Status

```text
Development: Completed
Testing: Completed
Vector Search: Completed
PDF Upload and GridFS Storage: Completed
Render Deployment: Completed
Final Documentation: Completed
```

---

## Author

```text
Abhi Ketankumar Patel
Student ID: 2431401
Internship Project – LCI LX Studio Inc.
Python-Based Equivalent Version
College Lasalle – AI and ML Internship Project
```

---

## Conclusion

The Agora Assistant Chatbot demonstrates a complete Python-based intelligent assistant platform for a College Lasalle-style intranet environment. The project combines Flask backend development, MongoDB Atlas cloud storage, MongoDB GridFS PDF storage, Groq AI response generation, MongoDB Atlas Vector Search, role-based access, document search, appointment management, embedded chatbot functionality, and professional user interface design.

The final system provides a strong foundation for a realistic institutional assistant and can be expanded in the future with email notifications, OCR, multilingual support, analytics, and advanced administrative features.
