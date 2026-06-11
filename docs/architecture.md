# System Architecture

## Architecture Overview

The Agora Assistant Chatbot follows a three-layer architecture.

### Presentation Layer

Responsible for user interaction.

Components:
- Login Page
- Dashboard
- Chat Interface
- Document Library
- Appointment Booking
- History Page

Technologies:
- HTML
- CSS
- JavaScript

---

### Application Layer

Responsible for business logic.

Technology:
- Flask

Responsibilities:
- User Authentication
- Session Management
- Chatbot Processing
- Document Search
- Appointment Processing
- History Management

---

### Data Layer

Responsible for storing application data.

Technology:
- JSON Files

Files:
- users.json
- knowledge_base.json
- documents.json
- appointments.json
- conversations.json

---

## Architecture Flow

User
↓
Frontend Interface
↓
Flask Backend
↓
Business Logic
↓
JSON Data Layer
↓
Response Returned
↓
Displayed to User

---

## Future Improvements

- MongoDB Integration
- OpenAI API Integration
- Vector Search
- Secure Authentication
- Cloud Deployment