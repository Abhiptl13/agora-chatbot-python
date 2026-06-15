# Deployment Notes

## Project Name

Agora Assistant Chatbot – Python Intelligent Campus Assistant

---

## Deployment Objective

The objective of deployment is to make the Agora Assistant Chatbot accessible online through a public URL. The application is currently designed as a Python-based Flask web application with MongoDB Atlas integration, Groq AI integration, authentication, chatbot functionality, document management, appointment booking, conversation history, and an embedded chatbot widget.

The deployment process allows the project to be demonstrated outside the local development environment.

---

## Recommended Deployment Platform

The recommended deployment platform for this project is:

```text
Render
```

Render is suitable for this project because it supports Python web services and can run Flask applications using Gunicorn.

---

## Deployment Type

The application should be deployed as:

```text
Web Service
```

The application is not a static website because it requires:

* Python backend execution
* Flask routing
* MongoDB Atlas database connection
* Groq AI API communication
* Session-based authentication
* Dynamic pages and API endpoints

---

## Deployment Architecture

```text
User Browser
↓
Render Web Service
↓
Gunicorn Server
↓
Flask Application
↓
MongoDB Atlas
↓
Groq AI API
↓
Response Returned to User
```

---

## Deployment Stack

### Application Framework

```text
Python Flask
```

### Production Server

```text
Gunicorn
```

### Database

```text
MongoDB Atlas
```

### AI Provider

```text
Groq API
```

### Version Control

```text
GitHub
```

### Hosting Platform

```text
Render Free Plan
```

---

## Required Deployment Files

Before deployment, the project root should contain the following files:

```text
requirements.txt
Procfile
runtime.txt
.env.example
.gitignore
README.md
```

---

## requirements.txt

The `requirements.txt` file defines the Python dependencies required by the project.

Recommended content:

```txt
Flask==3.1.3
pymongo==4.17.0
python-dotenv==1.2.2
groq
gunicorn
requests==2.34.2
dnspython==2.8.0
Werkzeug==3.1.8
Jinja2==3.1.6
```

Important packages:

* `Flask` runs the web application.
* `pymongo` connects the application to MongoDB Atlas.
* `python-dotenv` loads local environment variables.
* `groq` connects the application to the Groq AI API.
* `gunicorn` runs the Flask application in deployment.
* `dnspython` supports MongoDB Atlas connection strings.

---

## Procfile

The `Procfile` tells Render how to start the Flask application.

File name:

```text
Procfile
```

Content:

```text
web: gunicorn app:app
```

Explanation:

* `web` tells Render this is a web service.
* `gunicorn` starts the production server.
* `app:app` means Render should look for the Flask object named `app` inside `app.py`.

---

## runtime.txt

The `runtime.txt` file defines the Python version used during deployment.

File name:

```text
runtime.txt
```

Content:

```text
python-3.11.9
```

---

## .env.example

The `.env.example` file documents the required environment variables without exposing real credentials.

File name:

```text
.env.example
```

Content:

```env
MONGO_URI=your_mongodb_atlas_connection_string
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key
```

Important:

The `.env.example` file is safe to upload to GitHub because it does not contain real credentials.

---

## .env File

The real `.env` file is used only for local development.

Example:

```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
GROQ_API_KEY=your_real_groq_api_key
SECRET_KEY=your_real_secret_key
```

Important:

The `.env` file must never be uploaded to GitHub.

---

## .gitignore

The `.gitignore` file prevents sensitive and unnecessary files from being uploaded to GitHub.

Recommended content:

```gitignore
.env
venv/
__pycache__/
*.pyc
instance/
.pytest_cache/
.DS_Store
*.log
```

---

## Render Environment Variables

In Render, the following environment variables must be added manually:

```text
MONGO_URI
GROQ_API_KEY
SECRET_KEY
```

These values replace the local `.env` file during deployment.

---

## Render Deployment Settings

Recommended Render settings:

```text
Environment: Python
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
Plan: Free
```

---

## GitHub Preparation

Before deployment, the project should be pushed to GitHub.

Commands:

```bash
git status
git add .
git commit -m "Prepare project for deployment"
git push origin main
```

After pushing, Render can connect directly to the GitHub repository.

---

## MongoDB Atlas Deployment Configuration

MongoDB Atlas must allow the deployed Render application to connect to the database.

For project demo and testing, MongoDB Atlas Network Access can temporarily allow:

```text
0.0.0.0/0
```

This allows access from external deployment services.

Important:

For production use, database access should be restricted to trusted IP addresses only.

---

## Local Testing Before Deployment

Before deploying, the application should be tested locally.

Run:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

Test the following:

```text
Login page
Demo portal page
Embedded chatbot widget
Dashboard
Chat page
Document page
Appointment page
History page
404 page
500 page
MongoDB connection
Groq AI response
```

---

## Deployment Testing After Render

After deployment, Render will provide a public application URL.

Example:

```text
https://agora-chatbot-python.onrender.com
```

After deployment, test:

```text
Live URL opens
Login works
Portal redirects correctly
Chatbot widget opens
Chatbot answers casual messages
Chatbot answers institutional questions
Documents load
Appointments submit
History loads
API endpoints respond
```

---

## API Endpoints to Verify

### Health Check

```text
GET /health
```

Expected result:

```json
{
  "status": "running",
  "project": "Agora Assistant Chatbot - Python Version"
}
```

### Chatbot API

```text
POST /api/chat/message
```

### Embedded Widget API

```text
POST /api/widget/message
```

### Documents API

```text
GET /api/documents
```

### Appointments API

```text
GET /api/appointments
```

### History API

```text
GET /api/chat/history
```

---

## Free Deployment Limitation

When using the Render Free Plan, the web service may sleep after a period of inactivity. Because of this, the first request after inactivity may take longer to load.

This is acceptable for a student project, internship demonstration, and portfolio deployment.

---

## Security Considerations

The following security practices should be followed during deployment:

* Do not upload `.env` to GitHub.
* Store real credentials only in Render environment variables.
* Use `.env.example` only for documentation.
* Keep MongoDB Atlas credentials private.
* Keep Groq API keys private.
* Avoid hardcoding secrets inside source code.
* Restrict MongoDB network access in production.
* Use stronger password handling in future versions.

---

## Deployment Checklist

```text
README.md updated
requirements.txt updated
Procfile created
runtime.txt created
.env.example created
.gitignore updated
.env removed from GitHub tracking
MongoDB Atlas configured
Groq API key available
Project tested locally
Project pushed to GitHub
Render web service created
Render environment variables added
Live URL tested
README live link updated
```

---

## Common Deployment Issues

### Application Fails to Start

Possible causes:

* Missing `gunicorn`
* Incorrect `Procfile`
* Incorrect start command
* Missing dependencies

Solution:

Verify:

```text
requirements.txt
Procfile
Render start command
```

---

### MongoDB Connection Error

Possible causes:

* Incorrect MongoDB URI
* MongoDB network access blocked
* Wrong database username or password

Solution:

Verify:

```text
MONGO_URI
MongoDB Atlas Network Access
MongoDB Database User
```

---

### Groq API Error

Possible causes:

* Missing Groq API key
* Invalid API key
* API key not added to Render

Solution:

Verify:

```text
GROQ_API_KEY
Render Environment Variables
```

---

### Static Files Not Loading

Possible causes:

* Incorrect folder structure
* Incorrect static file paths

Solution:

Verify:

```text
static/style.css
static/widget/widget.css
static/widget/widget.js
```

---

## Final Deployment Outcome

After deployment, the project will be accessible through a public Render URL. The deployed application will demonstrate:

* Python Flask backend
* MongoDB Atlas cloud database
* Groq AI chatbot responses
* Embedded chatbot widget
* Role-based portal access
* Document search
* Appointment booking
* Conversation history
* Professional UI design

---

## Conclusion

The Agora Assistant Chatbot is deployment-ready once the required configuration files, environment variables, GitHub repository, and Render web service are correctly prepared. Deployment allows the Python-based intelligent assistant platform to be demonstrated publicly and supports final internship presentation, project evaluation, and portfolio use.
