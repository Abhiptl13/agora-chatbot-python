# Chatbot Flow

## Purpose

This document explains how the chatbot processes user requests and generates responses.

## Chatbot Process Flow

User Login
↓
Dashboard
↓
Open Chat Interface
↓
Enter Question
↓
Click Send Button
↓
Frontend Sends Request
↓
POST /api/chat/message
↓
Flask Backend Receives Request
↓
Read User Role from Session
↓
Load knowledge_base.json
↓
Search Matching Keywords
↓
Answer Found?
↓
Yes → Return Knowledge Base Answer
No → Return Local Fallback Response
↓
Save Conversation to conversations.json
↓
Display Response in Chat Window

## Example

Question:
Where can I see my class schedule?

Matched Source:
Class Schedule

Response:
Students can view their class schedule from the Agora intranet dashboard under the Schedule section.

## Fallback Example

Question:
Where can I park my spaceship?

Response:
Sorry, I could not find this information in the local knowledge base. Please contact administration for more help.

## Future Improvements

- NLP Processing
- Semantic Search
- OpenAI Integration
- Context-Aware Responses
- Multi-language Support