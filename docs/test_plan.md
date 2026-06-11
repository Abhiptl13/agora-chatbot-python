# Sprint 3 MVP Test Plan

## Purpose

Verify that all Sprint 3 MVP features work correctly.

---

## Login Tests

Test 1:
Student Login

Expected:
Dashboard opens successfully.

Status:
Pass

---

Test 2:
Teacher Login

Expected:
Dashboard opens successfully.

Status:
Pass

---

Test 3:
Admin Login

Expected:
Dashboard opens successfully.

Status:
Pass

---

Test 4:
Invalid Credentials

Expected:
Error message displayed.

Status:
Pass

---

## Chatbot Tests

Test 5:
Known Question

Input:
Where can I see my class schedule?

Expected:
Knowledge base answer returned.

Status:
Pass

---

Test 6:
Unknown Question

Input:
Random unsupported question

Expected:
Fallback response returned.

Status:
Pass

---

## History Tests

Test 7:
Conversation Saved

Expected:
Question and answer stored in conversations.json

Status:
Pass

---

## Document Tests

Test 8:
Document Search

Expected:
Matching documents displayed.

Status:
Pass

---

## Appointment Tests

Test 9:
Appointment Submission

Expected:
Appointment stored in appointments.json

Status:
Pass

---

## API Tests

Test 10:
POST /api/chat/message

Expected:
JSON response returned.

Status:
Pass

---

Test 11:
GET /api/chat/history

Expected:
History JSON returned.

Status:
Pass