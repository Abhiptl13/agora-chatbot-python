# Agora Assistant Chatbot – Chatbot Flow

## Overview

This document explains how the Agora Assistant Chatbot processes user messages and generates responses.

The current chatbot flow is more advanced than the earlier MVP version. Instead of using only local JSON files, the chatbot now uses MongoDB Atlas collections, role-based filtering, Groq AI response generation, casual conversation handling, conversation history storage, and an embedded chatbot widget inside the AI Campus Portal.

---

## Purpose

The purpose of the chatbot is to help users access College Lasalle-style information quickly through natural language conversation.

The chatbot can assist with:

* Casual greetings
* Portal navigation
* Document search
* Appointment booking
* Student services
* Academic departments
* Knowledge-base questions
* Role-based information
* Conversation history tracking

---

## Chatbot Access Points

The chatbot can be accessed from two main places.

### 1. Full AI Assistant Page

Route:

```text
/chat
```

This page provides the full chatbot interface for longer conversations and testing.

---

### 2. Embedded Chatbot Widget

Route:

```text
/demo-site
```

The embedded chatbot widget appears as a floating chatbot button inside the AI Campus Portal.

The widget allows users to ask questions without leaving the portal page.

---

## High-Level Chatbot Flow

```text
User Login
↓
AI Campus Portal or Chat Page
↓
User Enters Message
↓
Frontend Sends Request
↓
Flask API Receives Request
↓
User Role Retrieved from Session
↓
Casual Conversation Check
↓
MongoDB Search
↓
Relevant Results Selected
↓
Groq AI Generates Response
↓
Conversation Saved in MongoDB
↓
Response Returned to Frontend
↓
Answer Displayed to User
```

---

## Full AI Assistant Flow

The full AI Assistant page uses the following endpoint:

```text
POST /api/chat/message
```

### Process

```text
User Opens /chat
↓
User Types Question
↓
User Clicks Send
↓
JavaScript Sends POST Request
↓
Flask Receives Message
↓
Current User Role is Read from Session
↓
chatbot_service.py Processes Question
↓
Answer and Source are Returned
↓
Conversation is Saved
↓
Frontend Displays Response
```

---

## Embedded Chatbot Widget Flow

The embedded chatbot widget uses the following endpoint:

```text
POST /api/widget/message
```

### Process

```text
User Opens /demo-site
↓
User Clicks Floating Chatbot Button
↓
Widget Window Opens
↓
User Types Message or Clicks Quick Action
↓
widget.js Sends POST Request
↓
Flask Receives Message
↓
chatbot_service.py Processes Question
↓
Answer and Source are Returned
↓
Widget Displays Response
↓
Widget Shows Suggested Action Buttons
```

---

## Casual Conversation Flow

Before searching MongoDB, the chatbot checks whether the message is a casual conversation message.

### Examples

```text
hi
hii
hello
hey
how are you
thanks
bye
who are you
what can you do
```

### Flow

```text
User Message
↓
Normalize Text
↓
Check Casual Message List
↓
Match Found?
↓
Yes → Return Casual Response
No → Continue to MongoDB Search
```

### Example

**User Question:**

```text
hii
```

**Response:**

```text
Hi! How are you? I’m Agora Assistant. I can help you with documents, appointments, services, departments, and portal information.
```

**Source:**

```text
General Conversation
```

This improves user experience because the chatbot can respond naturally before handling institutional questions.

---

## MongoDB Search Flow

If the message is not casual, the chatbot searches MongoDB Atlas.

The chatbot searches these collections:

```text
knowledge_base
documents
website_content
portal_services
portal_departments
```

### Search Fields

The chatbot checks fields such as:

* Title
* Category
* Keywords
* Answer
* Summary
* Content
* Description
* Type

### Flow

```text
User Question
↓
Convert Question to Lowercase
↓
Search Knowledge Base
↓
Search Documents
↓
Search Website Content
↓
Search Portal Services
↓
Search Portal Departments
↓
Calculate Relevance Score
↓
Sort Results by Score
↓
Select Top Results
```

---

## Role-Based Filtering Flow

The chatbot uses the logged-in user’s role to filter information.

Supported roles:

```text
student
teacher
administrator
```

### Role-Based Flow

```text
User Logs In
↓
Role Stored in Session
↓
User Sends Question
↓
Chatbot Reads Role from Session
↓
MongoDB Records Checked Against Audience Field
↓
Only Allowed Records are Used
```

This prevents users from receiving information that is not intended for their role.

---

## AI Response Generation Flow

After relevant MongoDB results are found, the chatbot builds context and sends it to Groq AI.

### Provider

```text
Groq API
```

### Model

```text
Llama 3.1 Instant
```

### Flow

```text
Top MongoDB Results
↓
Context Created
↓
Prompt Built
↓
Groq AI Receives Prompt
↓
AI Generates Natural Language Answer
↓
Answer Returned to Flask
↓
Answer Sent to Frontend
```

---

## Response Source Flow

Each chatbot response includes a source.

Example sources:

```text
General Conversation
Document Center
Appointment Services
Portal Services
Portal Department
Knowledge Base
Fallback
```

The source helps users understand where the answer came from.

---

## Conversation Storage Flow

After the chatbot returns a response, the conversation is saved in MongoDB Atlas.

Collection:

```text
conversations
```

Stored data:

* User email
* User name
* User role
* Question
* Answer
* Source
* Timestamp
* Module source

### Flow

```text
Chatbot Response Generated
↓
Conversation Data Created
↓
Saved in MongoDB Conversations Collection
↓
Displayed Later on History Page
```

---

## Suggested Action Button Flow

The embedded chatbot widget can show suggested action buttons based on the source or answer.

Examples:

* Open Appointment Page
* Open Document Center
* Open Services
* Open Departments
* Open History
* Go to Portal Home

### Flow

```text
Chatbot Response Received
↓
widget.js Checks Source / Answer / Question
↓
Action Buttons Generated
↓
User Clicks Suggested Action
↓
Correct Page or Section Opens
```

This makes the chatbot feel more interactive and useful inside the portal.

---

## Example 1 – Appointment Question

**User Question:**

```text
How can I book an appointment?
```

**Processing:**

```text
Message is not casual
↓
MongoDB collections searched
↓
Appointment-related records matched
↓
Groq AI generates response
↓
Source returned
↓
Suggested appointment action displayed
```

**Example Response:**

```text
You can book an appointment through the Appointment Services page. Select the appointment type, choose an advisor or department, pick a date and time, and submit your request.
```

**Source:**

```text
Appointment Services
```

---

## Example 2 – Document Question

**User Question:**

```text
What documents are available?
```

**Processing:**

```text
Message is not casual
↓
Documents and website content are searched
↓
Document-related records matched
↓
AI response generated
↓
Source returned
```

**Example Response:**

```text
You can access academic guides, student forms, course registration documents, advisor booking guides, and institutional resources through the Document Center.
```

**Source:**

```text
Document Center
```

---

## Example 3 – Department Question

**User Question:**

```text
What departments are available?
```

**Processing:**

```text
Message is not casual
↓
Portal department collection is searched
↓
Department records are matched
↓
AI response generated
↓
Suggested department action displayed
```

**Example Response:**

```text
The portal includes departments such as Computer Science, Business Administration, Design and Digital Arts, Marketing and Commerce, Social Sciences, and General Education.
```

**Source:**

```text
Portal Department
```

---

## Example 4 – Fallback Question

**User Question:**

```text
Where can I park my spaceship?
```

**Processing:**

```text
No casual response matched
↓
No MongoDB result found
↓
Fallback response returned
```

**Example Response:**

```text
I could not find information related to your question. You can try asking about services, documents, appointments, departments, registration, support, or chatbot features.
```

**Source:**

```text
Fallback
```

---

## Chatbot Service Files

The chatbot logic is mainly handled by:

```text
services/chatbot_service.py
```

This file manages:

* Casual conversation detection
* MongoDB searching
* Role filtering
* Relevance scoring
* Context generation
* AI prompt preparation
* Response source selection

AI generation is handled by:

```text
services/ai_service.py
```

This file manages:

* Groq API communication
* AI response generation
* AI error handling

---

## Improvement from Earlier MVP Flow

Earlier MVP flow:

```text
User Question
↓
Load local JSON file
↓
Search keywords
↓
Return static answer
↓
Save to local JSON history
```

Current advanced flow:

```text
User Question
↓
Casual conversation check
↓
Search MongoDB Atlas collections
↓
Apply role filtering
↓
Build AI context
↓
Generate answer using Groq AI
↓
Return source
↓
Show suggested action buttons
↓
Save conversation to MongoDB
```

---

## Current Capabilities

The chatbot currently supports:

* Casual greetings
* Institutional questions
* Role-based answers
* Document-related questions
* Appointment-related questions
* Service-related questions
* Department-related questions
* Source display
* Suggested action buttons
* Conversation history storage
* Embedded widget interaction

---

## Future Improvements

Possible future improvements include:

* Semantic search
* Vector database integration
* Multi-turn conversation memory
* Multilingual support
* More advanced intent detection
* User-specific recommendations
* Admin knowledge-base management
* Voice input support
* Better analytics dashboard
* File upload and document content extraction

---

## Conclusion

The Agora Assistant Chatbot now follows an advanced chatbot flow that combines casual conversation handling, MongoDB Atlas retrieval, role-based filtering, Groq AI response generation, source tracking, suggested action buttons, and conversation history storage.

This flow makes the chatbot more interactive, realistic, and suitable for a campus portal environment compared to the earlier local JSON-based MVP version.
