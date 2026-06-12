# Sprint 5 Test Results and Validation Report

## Project Information

Project Name:
Agora Assistant Chatbot – Python Equivalent Version

Sprint:
Sprint 5 – Testing, Security, and Stabilization

Student:
Abhi Patel

Technology Stack:

- Python
- Flask
- MongoDB Atlas
- Groq AI (Llama 3.1)
- HTML
- CSS
- JavaScript

Testing Period:
June 2026

---

# Introduction

Sprint 5 focused on validating the stability, reliability, security, and overall functionality of the Agora Assistant Chatbot. Unlike previous sprints, which primarily concentrated on development and feature implementation, Sprint 5 emphasized testing existing functionality, identifying defects, applying fixes, verifying security practices, and ensuring that the Python version remains aligned with the objectives of the main project.

The goal of Sprint 5 was to confirm that all major modules operate correctly under normal usage conditions and that the application is ready for final review and demonstration.

---

# Testing Objectives

The primary objectives of Sprint 5 testing were:

- Verify authentication and user access controls.
- Validate chatbot functionality and response quality.
- Confirm role-based filtering behavior.
- Test document search capabilities.
- Verify appointment request processing.
- Confirm conversation history tracking.
- Validate MongoDB Atlas integration.
- Verify Groq AI integration.
- Test API endpoints.
- Review security practices.
- Identify and fix critical bugs.
- Ensure overall application stability.

---

# Testing Environment

Hardware:

- Windows Laptop

Operating System:

- Windows 11

Development Environment:

- Visual Studio Code

Backend Framework:

- Flask

Database:

- MongoDB Atlas

Artificial Intelligence Provider:

- Groq API

AI Model:

- Llama 3.1 Instant

Browser Used:

- Google Chrome

Version Tested:

- Sprint 5 Stable Build

---

# Testing Methodology

Testing was performed using a combination of manual validation, functional testing, integration testing, and user flow testing.

Each module was tested independently before performing complete end-to-end workflow testing.

The testing process consisted of:

1. Feature Validation
2. Security Verification
3. Data Validation
4. API Testing
5. User Flow Testing
6. Bug Verification
7. Stability Review

All test cases were executed using realistic application scenarios to simulate actual user behavior.

---

# Authentication Testing

Authentication is responsible for controlling access to protected resources and ensuring that users can only access information appropriate to their assigned role.

## Student Login Testing

Objective:

Verify that student users can successfully authenticate and access student resources.

Procedure:

1. Open login page.
2. Enter valid student credentials.
3. Submit login form.
4. Verify dashboard access.

Expected Result:

Student should successfully access the dashboard.

Actual Result:

Authentication completed successfully and the dashboard loaded correctly.

Status:

PASS

---

## Teacher Login Testing

Objective:

Verify teacher authentication.

Actual Result:

Teacher account successfully authenticated and gained access to teacher resources.

Status:

PASS

---

## Administrator Login Testing

Objective:

Verify administrator authentication.

Actual Result:

Administrator account successfully authenticated and accessed administrative resources.

Status:

PASS

---

## Invalid Credential Testing

Objective:

Verify that incorrect credentials are rejected.

Actual Result:

Application displayed an authentication error message and denied access.

Status:

PASS

---

## Logout Testing

Objective:

Verify session destruction and access revocation.

Actual Result:

User session was removed and access to protected routes was blocked.

Status:

PASS

---

# Chatbot Testing

The chatbot is the primary feature of the application and required extensive validation.

Testing focused on response quality, role filtering, fallback handling, and AI integration.

---

## Student Question Testing

Example Question:

Where can I see my class schedule?

Expected Result:

Relevant information returned from the knowledge base.

Actual Result:

Correct response generated and displayed.

Status:

PASS

---

## Teacher Question Testing

Example Question:

Where can teachers update attendance?

Expected Result:

Teacher-specific information returned.

Actual Result:

Relevant teacher response generated.

Status:

PASS

---

## Administrator Question Testing

Example Question:

Where can administrators access reports?

Expected Result:

Administrative report information returned.

Actual Result:

Correct administrative response displayed.

Status:

PASS

---

## AI Response Quality Testing

Objective:

Verify that Groq AI generates readable and contextual responses.

Observation:

Responses were significantly more natural and user-friendly than static knowledge-base answers.

Status:

PASS

---

## Fallback Response Testing

Objective:

Verify application behavior when no relevant knowledge record exists.

Actual Result:

Fallback response displayed correctly.

Status:

PASS

---

# Role-Based Access Control Testing

Role filtering is one of the most important project requirements.

Testing verified that users only receive information appropriate to their role.

---

## Student Restriction Testing

Objective:

Ensure students cannot access teacher-only information.

Result:

Teacher content was hidden successfully.

Status:

PASS

---

## Teacher Restriction Testing

Objective:

Ensure teachers cannot access administrator-only content.

Result:

Administrator content remained inaccessible.

Status:

PASS

---

## Administrator Access Testing

Objective:

Verify administrator access to administrative information.

Result:

Administrative content displayed successfully.

Status:

PASS

---

# Document Search Testing

Document search functionality was tested using multiple search scenarios.

---

## Search by Title

Result:

Matching documents returned successfully.

Status:

PASS

---

## Search by Category

Result:

Relevant documents displayed correctly.

Status:

PASS

---

## Search by Summary

Result:

Matching results returned successfully.

Status:

PASS

---

## Empty Search Query

Result:

Available documents displayed correctly.

Status:

PASS

---

## Invalid Search Query

Result:

No errors occurred and empty results were handled correctly.

Status:

PASS

---

# Appointment Management Testing

The appointment module was tested to verify form validation and MongoDB storage.

---

## Appointment Creation

Result:

Appointment request stored successfully.

Status:

PASS

---

## Required Field Validation

Result:

Validation prevented incomplete submissions.

Status:

PASS

---

## Appointment Retrieval

Result:

Stored appointments displayed successfully.

Status:

PASS

---

# Conversation History Testing

The conversation history module was tested to ensure that user interactions are properly tracked.

---

## Conversation Storage

Result:

Conversations stored successfully in MongoDB.

Status:

PASS

---

## Conversation Retrieval

Result:

Conversation history displayed correctly.

Status:

PASS

---

## Timestamp Validation

Result:

Every conversation record contained a timestamp.

Status:

PASS

---

# MongoDB Atlas Integration Testing

MongoDB Atlas serves as the primary data storage solution.

---

## Connection Validation

Result:

Connection established successfully.

Status:

PASS

---

## Read Operations

Result:

Knowledge base, documents, users, appointments, and conversations retrieved successfully.

Status:

PASS

---

## Write Operations

Result:

Appointments and conversation history stored correctly.

Status:

PASS

---

## Collection Verification

Verified Collections:

- users
- knowledge_base
- documents
- appointments
- conversations

Status:

PASS

---

# Groq AI Integration Testing

The Groq API was tested to verify response generation.

---

## API Connectivity

Result:

API connection established successfully.

Status:

PASS

---

## Context-Based Responses

Result:

AI successfully generated responses using MongoDB knowledge-base context.

Status:

PASS

---

## Response Quality

Result:

Responses were clear, readable, and contextually appropriate.

Status:

PASS

---

# API Endpoint Testing

The following endpoints were tested:

GET /health

PASS

POST /api/chat/message

PASS

GET /api/chat/history

PASS

GET /api/documents

PASS

GET /api/appointments

PASS

All endpoints returned valid responses and handled errors correctly.

---

# Security Verification

Security testing focused on protecting sensitive credentials and restricting unauthorized access.

---

## Environment Variable Validation

Verified:

- MONGO_URI stored in .env
- GROQ_API_KEY stored in .env

Result:

PASS

---

## GitHub Security Verification

Verified:

- .env excluded through .gitignore
- No credentials uploaded to GitHub

Result:

PASS

---

## Protected Route Verification

Verified:

- Dashboard
- Chat
- Documents
- Appointments
- History

All protected resources required authentication.

Result:

PASS

---

# User Interface Testing

The frontend user flow was tested from login through chatbot interaction.

Verified:

- Login Flow
- Navigation Menu
- Chat Interface
- Document Search Interface
- Appointment Form
- History Page

Result:

PASS

---

# Bug Fixes Applied During Sprint 5

Several issues were identified and corrected during testing.

Issue 1:

Chatbot messages could not be submitted using the Enter key.

Fix:

Added keyboard event listener.

Status:

Resolved

---

Issue 2:

MongoDB Atlas IP restrictions prevented external testing.

Fix:

Updated Atlas Network Access configuration.

Status:

Resolved

---

Issue 3:

Chat responses appeared visually compressed.

Fix:

Updated CSS formatting and line spacing.

Status:

Resolved

---

Issue 4:

Empty appointment fields required stronger validation.

Fix:

Improved form validation checks.

Status:

Resolved

---

# Overall Test Results

Total Test Areas:

10

Total Individual Test Cases:

37

Passed:

37

Failed:

0

Success Rate:

100%

---

# Final Assessment

All major application components were tested successfully.

Validated Areas:

✓ Authentication

✓ Role-Based Access Control

✓ Chatbot Functionality

✓ Groq AI Integration

✓ MongoDB Atlas Integration

✓ Document Search

✓ Appointment Management

✓ Conversation History

✓ API Endpoints

✓ Security Controls

✓ User Interface Stability

No critical defects remain open.

---

# Conclusion

Sprint 5 testing confirmed that the Agora Assistant Chatbot Python Version is stable, secure, and fully functional. The application successfully satisfies the project requirements through authentication, AI-assisted chatbot functionality, document search, appointment management, conversation tracking, role-based filtering, cloud database integration, and API support. All critical functionality has been validated and the project is ready for final review, demonstration, and presentation.