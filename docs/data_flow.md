# Backend Data Flow

## Login Flow

User Enters Credentials
↓
POST /login
↓
users.json
↓
Validate Email and Password
↓
Create Session
↓
Redirect to Dashboard

---

## Chat Flow

User Types Question
↓
Frontend Chat Interface
↓
POST /api/chat/message
↓
Flask Backend
↓
Read User Role
↓
Load knowledge_base.json
↓
Search Matching Keywords
↓
Generate Response
↓
Save Conversation
↓
Update conversations.json
↓
Return Response
↓
Display Response

---

## History Flow

User Opens History Page
↓
Read conversations.json
↓
Filter by Logged-In User
↓
Display User Conversations

---

## Document Search Flow

User Enters Search Query
↓
documents.json
↓
Filter by Role
↓
Search Matching Documents
↓
Display Results

---

## Appointment Flow

User Completes Appointment Form
↓
POST /appointments
↓
appointments.json
↓
Save Appointment Request
↓
Return Confirmation Message