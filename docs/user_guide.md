# Agora Assistant Chatbot – User Guide

## Overview

This user guide explains how to use the Agora Assistant Chatbot application. The system is a Python-based Flask web application that provides an intelligent campus assistant for students, teachers, and administrators.

Users can log in, access the AI campus portal, use the embedded chatbot widget, ask questions through the full AI Assistant page, search documents, book appointments, and review previous chatbot conversations.

---

## Starting the Application Locally

Open a terminal inside the project folder.

Run the application:

```bash
python app.py
```

Open a browser and visit:

```text
http://127.0.0.1:5000
```

The login page should appear.

---

## Accessing the Deployed Application

After deployment, the application can be accessed through the Render live URL.

Example:

```text
https://agora-chatbot-python.onrender.com
```

Note:

On the free Render plan, the application may take extra time to load after inactivity because free services may sleep.

---

## Demo Accounts

Use one of the following accounts to test the system.

### Student Account

```text
Email: etudiant@college.local
Password: Agora2026!
```

### Teacher Account

```text
Email: enseignant@college.local
Password: Agora2026!
```

### Administrator Account

```text
Email: admin@college.local
Password: Agora2026!
```

---

## Login Process

1. Open the application.
2. Enter a demo email address.
3. Enter the password.
4. Click **Login**.
5. After successful login, the system redirects the user to the AI Campus Portal.

If login fails, verify that the email and password are entered correctly.

---

## AI Campus Portal

After login, users are redirected to:

```text
/demo-site
```

The AI Campus Portal is the main landing page of the application.

The portal includes:

* Navigation bar
* User profile information
* Dashboard link
* Department section
* Document section
* Service section
* Full AI Assistant link
* Embedded chatbot widget
* Logout button

Users can use this page to quickly access the main features of the system.

---

## Using the Embedded Chatbot Widget

The embedded chatbot widget appears as a floating chatbot button on the AI Campus Portal.

### Steps

1. Open the AI Campus Portal.
2. Click the floating chatbot button.
3. Type a message or select a quick action.
4. Review the chatbot response.
5. Use suggested action buttons when available.

### Example Casual Messages

```text
hii
hello
how are you
thanks
bye
who are you
what can you do
```

### Example Portal Questions

```text
How can I book an appointment?
What documents are available?
What services are available?
What departments are available?
Where can I get student support?
```

The chatbot can provide answers with source information and navigation suggestions.

---

## Using the Full AI Assistant Page

The full chatbot page is available from:

```text
/chat
```

### Steps

1. Click **AI Assistant** in the navigation bar.
2. Type a question in the chat input.
3. Click **Send**.
4. Review the AI-generated answer.
5. Check the source shown below the response.

The full AI Assistant page is useful for longer conversations and direct chatbot testing.

---

## Using the Document Center

The document page is available from:

```text
/documents
```

### Steps

1. Click **Documents** in the navigation bar.
2. Enter a keyword in the search box.
3. Click **Search**.
4. Review matching document cards.
5. Use category links to filter results.

### Example Search Keywords

```text
registration
forms
advisor
schedule
academic
student services
administration
```

The Document Center retrieves document information from MongoDB Atlas and displays the results in a structured card layout.

---

## Booking an Appointment

The appointment page is available from:

```text
/appointments
```

### Steps

1. Click **Appointments** in the navigation bar.
2. Select the appointment type.
3. Select an advisor or service department.
4. Choose a date.
5. Choose a time.
6. Add notes if needed.
7. Submit the request.

After submission, the appointment request is saved in MongoDB Atlas.

### Appointment Examples

* Academic advising
* Registrar support
* Student services support
* IT support
* Program consultation

---

## Viewing Conversation History

The history page is available from:

```text
/history
```

### Steps

1. Click **History** in the navigation bar.
2. Review previous chatbot questions.
3. Review chatbot answers.
4. Check source information and timestamps.

The conversation history helps users review previous interactions with the assistant.

---

## Using the Dashboard

The dashboard is available from:

```text
/dashboard
```

The dashboard provides quick access to:

* AI Campus Portal
* AI Assistant
* Documents
* Appointments
* Conversation History
* User role information
* System feature overview

---

## Using the Navigation Bar

The navigation bar provides access to the main modules:

```text
Portal
Dashboard
AI Assistant
Documents
Appointments
History
Logout
```

Users can move between pages using these links.

---

## Logging Out

To end the current session:

1. Click **Logout** in the navigation bar.
2. The session will end.
3. The user will be redirected to the login page.

Logging out is recommended after finishing work, especially on shared computers.

---

## Common User Issues

### Login Does Not Work

Check:

* Email is entered correctly.
* Password is entered correctly.
* MongoDB Atlas is connected.
* Demo users exist in the database.

---

### Chatbot Does Not Respond

Check:

* Groq API key is configured.
* MongoDB Atlas is connected.
* Internet connection is available.
* Flask server is running.

---

### Documents Do Not Appear

Check:

* MongoDB documents collection contains data.
* User role has permission to view documents.
* Search keyword is not too specific.

---

### Appointment Does Not Submit

Check:

* All required fields are completed.
* Flask server is running.
* MongoDB Atlas is connected.

---

### Live Deployment Loads Slowly

If using Render Free Plan, the application may sleep after inactivity. Wait for the first request to wake the service.

---

## User Testing Checklist

Use the following checklist to verify the application:

```text
Login page opens
Student account login works
Teacher account login works
Admin account login works
Portal page opens after login
Embedded chatbot opens
Chatbot replies to casual messages
Chatbot answers portal questions
AI Assistant page works
Documents page opens
Document search works
Appointments page opens
Appointment form submits
History page displays conversations
Dashboard opens
Logout works
```

---

## Summary

The Agora Assistant Chatbot provides a centralized intelligent campus assistant experience. Users can access institutional support through the AI Campus Portal, embedded chatbot widget, AI Assistant page, Document Center, Appointment system, and Conversation History page. The system is designed to improve access to information while demonstrating a Python-based intelligent assistant architecture using Flask, MongoDB Atlas, and Groq AI.
