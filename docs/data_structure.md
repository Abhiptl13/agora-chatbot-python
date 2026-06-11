# Data Structure Documentation

## users.json

Purpose:
Stores application users.

Fields:
- id
- name
- email
- password
- role
- department

Example:

{
  "id": "u001",
  "name": "Student User",
  "email": "etudiant@college.local",
  "password": "Agora2026!",
  "role": "student",
  "department": "Student Services"
}

---

## knowledge_base.json

Purpose:
Stores chatbot knowledge.

Fields:
- id
- title
- category
- keywords
- answer
- audience
- confidence

---

## documents.json

Purpose:
Stores document information.

Fields:
- id
- title
- category
- summary
- type
- audience

---

## conversations.json

Purpose:
Stores chatbot history.

Fields:
- user
- name
- role
- question
- answer
- source
- timestamp

---

## appointments.json

Purpose:
Stores appointment requests.

Fields:
- user
- role
- name
- appointment_type
- advisor
- date
- time
- notes
- status
- created_at