# Sprint 4 Test Plan

## Overview

The purpose of this test plan is to verify that all major components of the Agora Assistant Chatbot function correctly after the Sprint 4 enhancements.

Sprint 4 introduced:

- MongoDB Atlas integration
- Groq AI integration
- Role-based filtering
- Expanded document search
- Appointment management
- Conversation history
- Improved API routes
- Enhanced error handling

This test plan defines the tests required to validate each feature.

---

# Testing Scope

The following modules are included in Sprint 4 testing:

1. Authentication Module
2. Chatbot Module
3. Role-Based Access Control
4. Document Search Module
5. Appointment Management Module
6. Conversation History Module
7. API Layer
8. MongoDB Integration
9. Groq AI Integration
10. Error Handling

---

# Testing Environment

Operating System:

Windows 11

Development Environment:

Visual Studio Code

Backend:

Python Flask

Database:

MongoDB Atlas

Artificial Intelligence:

Groq API (Llama 3.1)

Browser:

Google Chrome

---

# Authentication Testing

## Test Case AUTH-01

Feature:

Student Login

Test Steps:

1. Open login page.
2. Enter student credentials.
3. Click Sign In.

Expected Result:

Student is redirected to dashboard.

Priority:

High

---

## Test Case AUTH-02

Feature:

Teacher Login

Test Steps:

1. Open login page.
2. Enter teacher credentials.
3. Click Sign In.

Expected Result:

Teacher is redirected to dashboard.

Priority:

High

---

## Test Case AUTH-03

Feature:

Administrator Login

Test Steps:

1. Open login page.
2. Enter administrator credentials.
3. Click Sign In.

Expected Result:

Administrator is redirected to dashboard.

Priority:

High

---

## Test Case AUTH-04

Feature:

Invalid Login

Test Steps:

1. Enter incorrect credentials.
2. Submit form.

Expected Result:

Error message displayed.

Priority:

High

---

## Test Case AUTH-05

Feature:

Logout

Test Steps:

1. Login successfully.
2. Click Logout.

Expected Result:

Session destroyed and login page displayed.

Priority:

High

---

# Chatbot Testing

## Test Case CHAT-01

Feature:

Knowledge Base Question

Input:

Where can I see my class schedule?

Expected Result:

Relevant answer returned.

Priority:

High

---

## Test Case CHAT-02

Feature:

Course Registration Question

Input:

How do I register for courses?

Expected Result:

Course registration answer returned.

Priority:

High

---

## Test Case CHAT-03

Feature:

Appointment Question

Input:

How do I book an appointment?

Expected Result:

Appointment guidance returned.

Priority:

High

---

## Test Case CHAT-04

Feature:

Teacher Question

Role:

Teacher

Input:

Where can teachers update attendance?

Expected Result:

Teacher attendance information returned.

Priority:

High

---

## Test Case CHAT-05

Feature:

Administrator Question

Role:

Administrator

Input:

Where can administrators see reports?

Expected Result:

Administrative reports information returned.

Priority:

High

---

## Test Case CHAT-06

Feature:

Fallback Response

Input:

Unknown question

Expected Result:

Fallback response displayed.

Priority:

Medium

---

# Role-Based Access Testing

## Test Case ROLE-01

Feature:

Student Access Restriction

Test Steps:

1. Login as student.
2. Request teacher-only information.

Expected Result:

Access denied through role filtering.

Priority:

High

---

## Test Case ROLE-02

Feature:

Administrator Information Restriction

Test Steps:

1. Login as student.
2. Request administrator-only information.

Expected Result:

Information not returned.

Priority:

High

---

## Test Case ROLE-03

Feature:

Teacher Resource Access

Test Steps:

1. Login as teacher.
2. Access teacher resources.

Expected Result:

Resources displayed successfully.

Priority:

High

---

# Document Search Testing

## Test Case DOC-01

Feature:

Search by Title

Input:

registration

Expected Result:

Matching documents returned.

Priority:

High

---

## Test Case DOC-02

Feature:

Search by Category

Input:

Academic Services

Expected Result:

Matching documents displayed.

Priority:

Medium

---

## Test Case DOC-03

Feature:

Search by Summary

Input:

advisor

Expected Result:

Matching documents displayed.

Priority:

Medium

---

## Test Case DOC-04

Feature:

Role-Based Document Access

Expected Result:

Users only see documents assigned to their role.

Priority:

High

---

# Appointment Testing

## Test Case APP-01

Feature:

Create Appointment

Test Steps:

1. Open appointment page.
2. Complete form.
3. Submit request.

Expected Result:

Appointment stored in MongoDB.

Priority:

High

---

## Test Case APP-02

Feature:

Required Field Validation

Test Steps:

1. Leave required fields blank.
2. Submit form.

Expected Result:

Validation message displayed.

Priority:

High

---

## Test Case APP-03

Feature:

Appointment Retrieval

Expected Result:

Appointments displayed correctly.

Priority:

Medium

---

# Conversation History Testing

## Test Case HIS-01

Feature:

Conversation Saving

Expected Result:

Conversation stored in MongoDB.

Priority:

High

---

## Test Case HIS-02

Feature:

Conversation Display

Expected Result:

History page displays stored conversations.

Priority:

High

---

## Test Case HIS-03

Feature:

Timestamp Storage

Expected Result:

Timestamp saved with each conversation.

Priority:

Medium

---

# API Testing

## Test Case API-01

Endpoint:

GET /health

Expected Result:

Application health status returned.

Priority:

High

---

## Test Case API-02

Endpoint:

POST /api/chat/message

Expected Result:

Chat response returned successfully.

Priority:

High

---

## Test Case API-03

Endpoint:

GET /api/chat/history

Expected Result:

Conversation history returned.

Priority:

High

---

## Test Case API-04

Endpoint:

GET /api/documents

Expected Result:

Documents returned successfully.

Priority:

High

---

## Test Case API-05

Endpoint:

GET /api/appointments

Expected Result:

Appointments returned successfully.

Priority:

High

---

# MongoDB Testing

## Test Case DB-01

Feature:

Database Connection

Expected Result:

MongoDB Atlas connection established.

Priority:

Critical

---

## Test Case DB-02

Feature:

Read Operations

Expected Result:

Data retrieved successfully.

Priority:

Critical

---

## Test Case DB-03

Feature:

Write Operations

Expected Result:

Data stored successfully.

Priority:

Critical

---

# Groq AI Testing

## Test Case AI-01

Feature:

Response Generation

Expected Result:

Groq AI generates readable responses.

Priority:

Critical

---

## Test Case AI-02

Feature:

Knowledge Base Context Usage

Expected Result:

AI uses MongoDB knowledge records as context.

Priority:

Critical

---

# Error Handling Testing

## Test Case ERR-01

Feature:

404 Page

Expected Result:

Custom 404 page displayed.

Priority:

Medium

---

## Test Case ERR-02

Feature:

500 Error Handling

Expected Result:

Custom 500 page displayed.

Priority:

Medium

---

# Acceptance Criteria

Sprint 4 will be considered successful if:

- All authentication tests pass.
- All chatbot tests pass.
- Role-based filtering works correctly.
- Document search works correctly.
- Appointment requests are stored successfully.
- Conversation history is saved and displayed.
- API endpoints function correctly.
- MongoDB integration is stable.
- Groq AI generates responses successfully.
- No critical defects remain open.

---

# Conclusion

This test plan provides a structured approach for validating all Sprint 4 functionality. Successful completion of these tests confirms that the Agora Assistant Chatbot meets the requirements for authentication, AI integration, cloud database storage, document search, appointment management, conversation history, API functionality, and role-based access control.