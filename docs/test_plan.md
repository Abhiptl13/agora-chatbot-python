# Agora Assistant Chatbot – Test Plan

## Overview

This test plan defines the testing strategy for the Agora Assistant Chatbot Python-based Flask application.

The objective of this test plan is to verify that the application works correctly after the latest development updates, including MongoDB Atlas integration, Groq AI integration, role-based access, embedded chatbot widget, modern portal UI, document search, appointment booking, conversation history, casual conversation handling, custom error pages, and deployment preparation.

---

## Testing Objectives

The main objectives of testing are:

* Verify that authentication works correctly.
* Verify that protected routes cannot be accessed without login.
* Verify that users are redirected to the AI Campus Portal after login.
* Verify that the chatbot responds to casual and institutional questions.
* Verify that chatbot responses use MongoDB and Groq AI correctly.
* Verify that the embedded chatbot widget works inside the portal.
* Verify that document search and layout work correctly.
* Verify that appointment requests are submitted and stored.
* Verify that conversation history is saved and displayed.
* Verify that REST API endpoints return expected responses.
* Verify that MongoDB Atlas integration is stable.
* Verify that error pages display correctly.
* Verify that the application is ready for Render deployment.

---

## Testing Scope

The following modules are included in this test plan:

1. Authentication Module
2. AI Campus Portal
3. Embedded Chatbot Widget
4. Full AI Assistant Page
5. Role-Based Access Control
6. Document Center
7. Appointment Management
8. Conversation History
9. REST API Layer
10. MongoDB Atlas Integration
11. Groq AI Integration
12. Error Handling
13. Deployment Readiness

---

## Testing Environment

| Item                    | Details                        |
| ----------------------- | ------------------------------ |
| Operating System        | Windows 11                     |
| Development Environment | Visual Studio Code             |
| Backend Framework       | Python Flask                   |
| Database                | MongoDB Atlas                  |
| AI Provider             | Groq API                       |
| AI Model                | Llama 3.1 Instant              |
| Browser                 | Google Chrome / Microsoft Edge |
| Local URL               | http://127.0.0.1:5000          |
| Deployment Target       | Render Free Plan               |

---

## Test Data

### Demo Student Account

```text
Email: etudiant@college.local
Password: Agora2026!
```

### Demo Teacher Account

```text
Email: enseignant@college.local
Password: Agora2026!
```

### Demo Administrator Account

```text
Email: admin@college.local
Password: Agora2026!
```

---

## Authentication Testing

### Test Case AUTH-01 – Student Login

**Feature:** Student authentication

**Test Steps:**

1. Open the login page.
2. Enter student email and password.
3. Click Login.

**Expected Result:**

The student is authenticated and redirected to `/demo-site`.

**Priority:** High

---

### Test Case AUTH-02 – Teacher Login

**Feature:** Teacher authentication

**Test Steps:**

1. Open the login page.
2. Enter teacher email and password.
3. Click Login.

**Expected Result:**

The teacher is authenticated and redirected to `/demo-site`.

**Priority:** High

---

### Test Case AUTH-03 – Administrator Login

**Feature:** Administrator authentication

**Test Steps:**

1. Open the login page.
2. Enter administrator email and password.
3. Click Login.

**Expected Result:**

The administrator is authenticated and redirected to `/demo-site`.

**Priority:** High

---

### Test Case AUTH-04 – Invalid Login

**Feature:** Invalid credential handling

**Test Steps:**

1. Open the login page.
2. Enter incorrect credentials.
3. Submit the form.

**Expected Result:**

An error message is displayed and the user remains on the login page.

**Priority:** High

---

### Test Case AUTH-05 – Logout

**Feature:** Session logout

**Test Steps:**

1. Login successfully.
2. Click Logout.

**Expected Result:**

The user session is destroyed and the login page is displayed.

**Priority:** High

---

### Test Case AUTH-06 – Protected Route Access

**Feature:** Route protection

**Test Steps:**

1. Logout from the application.
2. Try to open `/dashboard`, `/chat`, `/documents`, `/appointments`, or `/history`.

**Expected Result:**

The user is redirected to the login page.

**Priority:** High

---

## AI Campus Portal Testing

### Test Case PORTAL-01 – Portal Page Load

**Feature:** Demo portal page

**Test Steps:**

1. Login successfully.
2. Confirm redirect to `/demo-site`.

**Expected Result:**

The AI Campus Portal loads with navigation, user profile, portal sections, and chatbot widget.

**Priority:** High

---

### Test Case PORTAL-02 – Navigation Links

**Feature:** Portal navigation

**Test Steps:**

1. Click Dashboard.
2. Click AI Assistant.
3. Click Documents.
4. Click Appointments.
5. Click History.

**Expected Result:**

Each navigation link opens the correct page.

**Priority:** High

---

### Test Case PORTAL-03 – Portal Section Buttons

**Feature:** Portal interactive links

**Test Steps:**

1. Click Browse Documents.
2. Click Book Appointment.
3. Click Full AI Assistant.
4. Click department cards.
5. Click service cards.

**Expected Result:**

Each button or card navigates to the correct page or section.

**Priority:** Medium

---

## Embedded Chatbot Widget Testing

### Test Case WIDGET-01 – Widget Opens

**Feature:** Embedded chatbot widget

**Test Steps:**

1. Open `/demo-site`.
2. Click the floating chatbot button.

**Expected Result:**

The chatbot widget opens successfully.

**Priority:** High

---

### Test Case WIDGET-02 – Quick Action Buttons

**Feature:** Widget quick actions

**Test Steps:**

1. Open chatbot widget.
2. Click Services, Appointments, Documents, and Departments quick buttons.

**Expected Result:**

The chatbot sends the selected question and returns a relevant answer.

**Priority:** High

---

### Test Case WIDGET-03 – Widget Casual Conversation

**Feature:** Casual conversation handling

**Input Examples:**

```text
hii
hello
how are you
thanks
bye
```

**Expected Result:**

The chatbot responds naturally without requiring MongoDB search.

**Priority:** Medium

---

### Test Case WIDGET-04 – Widget Action Links

**Feature:** Suggested action buttons

**Test Steps:**

1. Ask: “How can I book an appointment?”
2. Review the chatbot response.
3. Click the suggested action button.

**Expected Result:**

The suggested action button opens the correct page or section.

**Priority:** High

---

## Full AI Assistant Testing

### Test Case CHAT-01 – Knowledge Base Question

**Feature:** Knowledge-base response

**Input:**

```text
Where can I see my class schedule?
```

**Expected Result:**

A relevant answer is returned with a source.

**Priority:** High

---

### Test Case CHAT-02 – Course Registration Question

**Feature:** Academic information retrieval

**Input:**

```text
How do I register for courses?
```

**Expected Result:**

The chatbot returns course registration guidance.

**Priority:** High

---

### Test Case CHAT-03 – Appointment Question

**Feature:** Appointment guidance

**Input:**

```text
How do I book an appointment?
```

**Expected Result:**

The chatbot explains how to book an appointment and provides a relevant source.

**Priority:** High

---

### Test Case CHAT-04 – Services Question

**Feature:** Portal service retrieval

**Input:**

```text
What services are available?
```

**Expected Result:**

The chatbot returns information about available portal services.

**Priority:** High

---

### Test Case CHAT-05 – Department Question

**Feature:** Department retrieval

**Input:**

```text
What departments are available?
```

**Expected Result:**

The chatbot returns department-related information.

**Priority:** High

---

### Test Case CHAT-06 – Fallback Response

**Feature:** Unknown question handling

**Input:**

```text
What is the weather on Mars today?
```

**Expected Result:**

The chatbot returns a fallback response without breaking the application.

**Priority:** Medium

---

## Role-Based Access Testing

### Test Case ROLE-01 – Student Role Filtering

**Feature:** Student access control

**Test Steps:**

1. Login as a student.
2. Ask for teacher-only information.

**Expected Result:**

Teacher-only information is not returned if it is restricted by role.

**Priority:** High

---

### Test Case ROLE-02 – Teacher Role Access

**Feature:** Teacher content access

**Test Steps:**

1. Login as a teacher.
2. Ask a teacher-related question.

**Expected Result:**

Teacher-related content is returned successfully.

**Priority:** High

---

### Test Case ROLE-03 – Administrator Role Access

**Feature:** Administrator content access

**Test Steps:**

1. Login as administrator.
2. Ask an administrator-related question.

**Expected Result:**

Administrator-related content is returned successfully.

**Priority:** High

---

## Document Center Testing

### Test Case DOC-01 – Document Page Load

**Feature:** Document Center page

**Test Steps:**

1. Login successfully.
2. Open `/documents`.

**Expected Result:**

The document page loads with sidebar categories and document cards displayed in a grid layout.

**Priority:** High

---

### Test Case DOC-02 – Search by Title

**Input:**

```text
registration
```

**Expected Result:**

Matching registration documents are displayed.

**Priority:** High

---

### Test Case DOC-03 – Search by Category

**Input:**

```text
academic
```

**Expected Result:**

Academic documents are displayed.

**Priority:** Medium

---

### Test Case DOC-04 – Search by Summary

**Input:**

```text
advisor
```

**Expected Result:**

Documents related to advisor support are displayed.

**Priority:** Medium

---

### Test Case DOC-05 – Empty Search Result

**Input:**

```text
unknownrandomkeyword
```

**Expected Result:**

A no-document-found message is displayed.

**Priority:** Medium

---

### Test Case DOC-06 – Document Layout

**Feature:** UI layout validation

**Test Steps:**

1. Open the Documents page.
2. Verify document cards are displayed in rows.

**Expected Result:**

Document cards appear in a clean grid layout and are not pushed to one side.

**Priority:** High

---

## Appointment Testing

### Test Case APP-01 – Appointment Page Load

**Feature:** Appointment page

**Test Steps:**

1. Login successfully.
2. Open `/appointments`.

**Expected Result:**

The appointment booking page loads successfully.

**Priority:** High

---

### Test Case APP-02 – Create Appointment

**Test Steps:**

1. Open the appointment page.
2. Complete the form.
3. Submit the request.

**Expected Result:**

The appointment request is stored in MongoDB.

**Priority:** High

---

### Test Case APP-03 – Required Field Validation

**Test Steps:**

1. Leave required fields blank.
2. Submit the form.

**Expected Result:**

The form prevents submission or displays a validation message.

**Priority:** High

---

## Conversation History Testing

### Test Case HIS-01 – Conversation Saving

**Test Steps:**

1. Ask a chatbot question.
2. Open MongoDB or the History page.

**Expected Result:**

The conversation is saved in MongoDB.

**Priority:** High

---

### Test Case HIS-02 – History Display

**Test Steps:**

1. Open `/history`.

**Expected Result:**

Previous conversations are displayed with question, answer, source, and timestamp.

**Priority:** High

---

### Test Case HIS-03 – User-Specific History

**Test Steps:**

1. Login as different users.
2. Check conversation history.

**Expected Result:**

The history page displays records related to the current user.

**Priority:** Medium

---

## API Testing

### Test Case API-01 – Health Endpoint

**Endpoint:**

```text
GET /health
```

**Expected Result:**

Application health status is returned.

**Priority:** High

---

### Test Case API-02 – Chat Endpoint

**Endpoint:**

```text
POST /api/chat/message
```

**Expected Result:**

A chatbot response is returned successfully.

**Priority:** High

---

### Test Case API-03 – Widget Endpoint

**Endpoint:**

```text
POST /api/widget/message
```

**Expected Result:**

The embedded chatbot widget receives a response successfully.

**Priority:** High

---

### Test Case API-04 – History Endpoint

**Endpoint:**

```text
GET /api/chat/history
```

**Expected Result:**

Conversation history is returned.

**Priority:** High

---

### Test Case API-05 – Documents Endpoint

**Endpoint:**

```text
GET /api/documents
```

**Expected Result:**

Documents are returned successfully.

**Priority:** High

---

### Test Case API-06 – Appointments Endpoint

**Endpoint:**

```text
GET /api/appointments
```

**Expected Result:**

Appointment records are returned successfully.

**Priority:** High

---

## MongoDB Atlas Testing

### Test Case DB-01 – Database Connection

**Feature:** MongoDB connection

**Expected Result:**

MongoDB Atlas connection is established without errors.

**Priority:** Critical

---

### Test Case DB-02 – Read Operations

**Feature:** Data retrieval

**Expected Result:**

Users, documents, knowledge records, services, departments, and conversations are retrieved successfully.

**Priority:** Critical

---

### Test Case DB-03 – Write Operations

**Feature:** Data storage

**Expected Result:**

Appointments and conversations are stored successfully.

**Priority:** Critical

---

### Test Case DB-04 – Additional Collections

**Feature:** Expanded collections

**Expected Result:**

The application can read data from `website_content`, `portal_services`, and `portal_departments`.

**Priority:** High

---

## Groq AI Testing

### Test Case AI-01 – Response Generation

**Feature:** AI response generation

**Expected Result:**

Groq AI generates readable and relevant responses.

**Priority:** Critical

---

### Test Case AI-02 – Context Usage

**Feature:** Context-based response generation

**Expected Result:**

AI responses are generated using MongoDB search results as context.

**Priority:** Critical

---

### Test Case AI-03 – AI Failure Handling

**Feature:** AI error handling

**Expected Result:**

If AI response generation fails, the application returns a safe fallback response instead of crashing.

**Priority:** High

---

## Error Handling Testing

### Test Case ERR-01 – 404 Page

**Feature:** Custom 404 page

**Test Steps:**

1. Open a route that does not exist.

**Expected Result:**

The custom 404 page is displayed.

**Priority:** Medium

---

### Test Case ERR-02 – 500 Page

**Feature:** Custom 500 page

**Expected Result:**

The custom 500 page exists and is available for internal server error handling.

**Priority:** Medium

---

## Deployment Readiness Testing

### Test Case DEPLOY-01 – Requirements File

**Feature:** Deployment dependencies

**Expected Result:**

`requirements.txt` includes all required dependencies including Flask, PyMongo, python-dotenv, Groq, Gunicorn, requests, dnspython, Werkzeug, and Jinja2.

**Priority:** High

---

### Test Case DEPLOY-02 – Procfile

**Feature:** Render start command

**Expected Result:**

`Procfile` exists and contains:

```text
web: gunicorn app:app
```

**Priority:** High

---

### Test Case DEPLOY-03 – runtime.txt

**Feature:** Python runtime

**Expected Result:**

`runtime.txt` exists and specifies a supported Python version.

**Priority:** Medium

---

### Test Case DEPLOY-04 – Environment Variables

**Feature:** Deployment secrets

**Expected Result:**

Required environment variables are documented in `.env.example` and real values are not committed to GitHub.

**Priority:** Critical

---

## Acceptance Criteria

The project will be considered ready for final deployment and demonstration if:

* Login works for student, teacher, and administrator accounts.
* Protected routes require authentication.
* The AI Campus Portal loads successfully.
* The embedded chatbot widget works.
* The chatbot answers casual messages.
* The chatbot answers institutional questions.
* Chatbot responses show source information.
* Document search works correctly.
* Document layout displays properly.
* Appointment requests are saved.
* Conversation history is stored and displayed.
* API endpoints function correctly.
* MongoDB Atlas connection is stable.
* Groq AI response generation works.
* Custom error pages are available.
* Deployment files are ready.
* No critical defects remain open.

---

## Conclusion

This test plan provides a structured approach for validating the Agora Assistant Chatbot before final deployment. The test cases cover authentication, portal navigation, embedded chatbot functionality, AI responses, MongoDB integration, document search, appointment management, conversation history, API endpoints, error handling, and deployment readiness.

Successful completion of this test plan confirms that the Python-based Agora Assistant Chatbot is stable, functional, and prepared for demonstration, evaluation, and free deployment through Render.
