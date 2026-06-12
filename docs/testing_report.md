# Testing Report – Sprint 4

## Project Information

Project Name:
Agora Assistant Chatbot – Python Version

Sprint:
Sprint 4 – Advanced Features

Testing Type:
Functional Testing

Environment:

- Python 3.x
- Flask
- MongoDB Atlas
- Groq AI
- Visual Studio Code
- Windows 11

Testing Date:
June 2026

---

# Testing Objective

The objective of Sprint 4 testing was to verify that all major modules of the Agora Assistant Chatbot function correctly after the migration from JSON storage to MongoDB Atlas and the integration of Groq AI.

Testing focused on:

- Authentication
- Chatbot Functionality
- Role-Based Filtering
- Document Search
- Appointment Management
- Conversation History
- API Endpoints
- MongoDB Integration
- AI Response Generation
- Error Handling

---

# Authentication Testing

## Test Case 1

Test Description:
Student Login

Input:

Email:
etudiant@college.local

Password:
Agora2026!

Expected Result:

Student successfully logs into the application and is redirected to the dashboard.

Actual Result:

Login successful.

Status:

PASS

---

## Test Case 2

Test Description:
Teacher Login

Input:

Email:
enseignant@college.local

Password:
Agora2026!

Expected Result:

Teacher successfully logs into the application.

Actual Result:

Login successful.

Status:

PASS

---

## Test Case 3

Test Description:
Administrator Login

Input:

Email:
admin@college.local

Password:
Agora2026!

Expected Result:

Administrator successfully logs into the application.

Actual Result:

Login successful.

Status:

PASS

---

## Test Case 4

Test Description:
Invalid Credentials

Input:

Incorrect email and password

Expected Result:

System displays login error message.

Actual Result:

Error message displayed correctly.

Status:

PASS

---

## Test Case 5

Test Description:
Logout Functionality

Expected Result:

User session is terminated and redirected to login page.

Actual Result:

Logout successful.

Status:

PASS

---

# Chatbot Testing

## Test Case 6

Test Description:
Student Question

Input:

Where can I see my class schedule?

Expected Result:

Relevant answer returned from knowledge base.

Actual Result:

Correct answer generated.

Status:

PASS

---

## Test Case 7

Test Description:
Course Registration Question

Input:

How do I register for courses?

Expected Result:

Chatbot retrieves course registration information.

Actual Result:

Correct response returned.

Status:

PASS

---

## Test Case 8

Test Description:
Appointment Question

Input:

How do I book an appointment?

Expected Result:

Chatbot provides appointment booking guidance.

Actual Result:

Correct answer generated.

Status:

PASS

---

## Test Case 9

Test Description:
Teacher Attendance Question

User Role:

Teacher

Input:

Where can teachers update attendance?

Expected Result:

Attendance management answer returned.

Actual Result:

Correct answer generated.

Status:

PASS

---

## Test Case 10

Test Description:
Administrative Reports Question

User Role:

Administrator

Input:

Where can administrators see reports?

Expected Result:

Administrative reports answer returned.

Actual Result:

Correct answer generated.

Status:

PASS

---

## Test Case 11

Test Description:
Unknown Question

Input:

Question not present in knowledge base.

Expected Result:

Fallback response displayed.

Actual Result:

Fallback response displayed successfully.

Status:

PASS

---

# Role-Based Access Testing

## Test Case 12

Test Description:
Student attempts to access teacher information.

Expected Result:

Teacher-only information is not accessible.

Actual Result:

Access correctly restricted.

Status:

PASS

---

## Test Case 13

Test Description:
Student attempts to access administrator information.

Expected Result:

Administrator information is hidden.

Actual Result:

Access correctly restricted.

Status:

PASS

---

## Test Case 14

Test Description:
Teacher accesses teacher resources.

Expected Result:

Teacher resources displayed.

Actual Result:

Resources displayed successfully.

Status:

PASS

---

## Test Case 15

Test Description:
Administrator accesses administrator resources.

Expected Result:

Administrative resources displayed.

Actual Result:

Resources displayed successfully.

Status:

PASS

---

# Document Search Testing

## Test Case 16

Test Description:
Search by Title

Input:

registration

Expected Result:

Matching documents displayed.

Actual Result:

Results displayed correctly.

Status:

PASS

---

## Test Case 17

Test Description:
Search by Category

Input:

Academic Services

Expected Result:

Relevant documents returned.

Actual Result:

Correct results displayed.

Status:

PASS

---

## Test Case 18

Test Description:
Search by Summary

Input:

advisor

Expected Result:

Matching documents displayed.

Actual Result:

Search successful.

Status:

PASS

---

## Test Case 19

Test Description:
Role-Based Document Access

Expected Result:

Only authorized documents are displayed.

Actual Result:

Filtering works correctly.

Status:

PASS

---

# Appointment Module Testing

## Test Case 20

Test Description:
Create Appointment Request

Expected Result:

Appointment saved successfully.

Actual Result:

Appointment stored in MongoDB.

Status:

PASS

---

## Test Case 21

Test Description:
Required Field Validation

Expected Result:

Missing required fields trigger validation errors.

Actual Result:

Validation successful.

Status:

PASS

---

## Test Case 22

Test Description:
Appointment Retrieval

Expected Result:

User can view stored appointments.

Actual Result:

Appointments retrieved correctly.

Status:

PASS

---

# Conversation History Testing

## Test Case 23

Test Description:
Conversation Storage

Expected Result:

Chatbot interaction saved in database.

Actual Result:

Conversation saved successfully.

Status:

PASS

---

## Test Case 24

Test Description:
Conversation Retrieval

Expected Result:

User history displayed correctly.

Actual Result:

History loaded successfully.

Status:

PASS

---

## Test Case 25

Test Description:
Timestamp Storage

Expected Result:

Timestamp saved with each conversation.

Actual Result:

Timestamp stored correctly.

Status:

PASS

---

# API Endpoint Testing

## Test Case 26

Endpoint:

GET /health

Expected Result:

Application health information returned.

Actual Result:

Health endpoint working.

Status:

PASS

---

## Test Case 27

Endpoint:

POST /api/chat/message

Expected Result:

Chat response returned.

Actual Result:

Response generated successfully.

Status:

PASS

---

## Test Case 28

Endpoint:

GET /api/chat/history

Expected Result:

Conversation history returned.

Actual Result:

History returned successfully.

Status:

PASS

---

## Test Case 29

Endpoint:

GET /api/documents

Expected Result:

Document list returned.

Actual Result:

Documents returned successfully.

Status:

PASS

---

## Test Case 30

Endpoint:

GET /api/appointments

Expected Result:

Appointment list returned.

Actual Result:

Appointments returned successfully.

Status:

PASS

---

# MongoDB Integration Testing

## Test Case 31

Test Description:
MongoDB Connection

Expected Result:

Application connects successfully to MongoDB Atlas.

Actual Result:

Connection established successfully.

Status:

PASS

---

## Test Case 32

Test Description:
MongoDB Read Operations

Expected Result:

Data retrieved correctly.

Actual Result:

Data retrieved successfully.

Status:

PASS

---

## Test Case 33

Test Description:
MongoDB Write Operations

Expected Result:

Data stored successfully.

Actual Result:

Data written successfully.

Status:

PASS

---

# Groq AI Integration Testing

## Test Case 34

Test Description:
AI Response Generation

Expected Result:

Groq generates natural language responses.

Actual Result:

Responses generated successfully.

Status:

PASS

---

## Test Case 35

Test Description:
Knowledge Base + AI Integration

Expected Result:

Knowledge base context is used when generating responses.

Actual Result:

Responses generated using knowledge context.

Status:

PASS

---

# Error Handling Testing

## Test Case 36

Test Description:
404 Page

Expected Result:

Custom 404 page displayed.

Actual Result:

404 page displayed successfully.

Status:

PASS

---

## Test Case 37

Test Description:
500 Error Handling

Expected Result:

Custom error message displayed.

Actual Result:

Error handler working correctly.

Status:

PASS

---

# Overall Results

Total Test Cases Executed:

37

Passed:

37

Failed:

0

Success Rate:

100%

---

# Testing Summary

All Sprint 4 modules were tested successfully.

Verified Features:

✓ Authentication

✓ Role-Based Access Control

✓ Chatbot Functionality

✓ Groq AI Integration

✓ MongoDB Atlas Integration

✓ Document Search

✓ Appointment Management

✓ Conversation History

✓ API Endpoints

✓ Error Handling

✓ Expanded Knowledge Base

✓ Advanced Sample Data

No critical defects were identified during testing.

---

# Conclusion

Sprint 4 testing confirmed that all major application features operate correctly and meet the functional requirements defined for the advanced feature phase. The migration to MongoDB Atlas and the integration of Groq AI were successfully validated, resulting in a stable and scalable chatbot platform ready for future enhancements.