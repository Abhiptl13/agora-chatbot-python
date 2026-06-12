# Agora Assistant Chatbot – Python Intelligent Assistant Platform

## Project Overview

The Agora Assistant Chatbot is a modern web-based intelligent assistant designed to support students, teachers, and administrators within the Collège Agora intranet environment.

The platform provides secure authentication, role-based access control, AI-powered assistance, document discovery, appointment management, conversation tracking, and cloud-based data storage. The objective of the system is to centralize access to institutional information while improving communication and user experience through intelligent automation.

This project serves as the Python equivalent implementation of the main Assistant Chatbot project and follows the same objectives, sprint planning methodology, architecture principles, and functional requirements while being fully developed using Python technologies.

---

# Project Objectives

The primary objectives of the project are:

- Provide a centralized intelligent assistant for institutional support.
- Improve access to academic and administrative information.
- Enable role-based access for students, teachers, and administrators.
- Simplify document discovery and information retrieval.
- Support appointment scheduling and tracking.
- Maintain conversation history for future reference.
- Demonstrate cloud database integration and AI-assisted responses.
- Implement a scalable architecture suitable for future enhancements.

---

# Sprint Status

## Sprint 1 – Project Planning

Completed

Deliverables:

- Project scope definition
- Requirements gathering
- Initial architecture planning
- Technology selection
- Sprint planning

---

## Sprint 2 – Foundation Development

Completed

Deliverables:

- Flask project setup
- Initial user interface
- Authentication planning
- Knowledge base structure
- Core application architecture

---

## Sprint 3 – MVP Development

Completed

Deliverables:

- Login system
- Dashboard
- Chatbot interface
- Document library
- Appointment booking
- Conversation history
- JSON-based storage
- Initial testing

---

## Sprint 4 – Advanced Features

Completed

Deliverables:

- MongoDB Atlas integration
- Groq AI integration
- Role-based filtering
- Enhanced chatbot logic
- Expanded knowledge base
- Advanced documentation
- API improvements
- Improved testing coverage
- Cloud-based architecture

---

# Core Features

## Authentication and Access Control

The system includes a secure authentication mechanism designed to protect application resources and ensure users only access information appropriate to their role.

Features:

- User Login
- Session Management
- Protected Routes
- Logout Functionality
- Role-Based Authorization

Supported Roles:

### Student

Access to:

- Student resources
- Academic information
- Document library
- Appointment requests
- Personal conversation history

### Teacher

Access to:

- Teacher resources
- Attendance information
- Academic support resources
- Document library
- Personal conversation history

### Administrator

Access to:

- Administrative resources
- Reports and statistics
- Internal documentation
- Appointment management information
- Personal conversation history

---

## AI-Powered Assistant

The chatbot serves as the core feature of the platform.

The assistant combines knowledge-base retrieval with artificial intelligence to provide accurate and user-friendly responses.

Capabilities:

- Institutional Question Answering
- Knowledge Base Retrieval
- Context-Aware Responses
- Source Identification
- Fallback Handling
- Role-Based Information Filtering

Artificial Intelligence Provider:

Groq API

Model:

Llama 3.1 Instant

Response Workflow:

User Question
↓
Knowledge Base Search
↓
Role Validation
↓
Context Selection
↓
Groq AI Processing
↓
Response Generation
↓
Conversation Storage

---

## Document Library

The document library allows users to discover institutional documents through an integrated search system.

Features:

- Document Search
- Category Search
- Summary Search
- Role-Based Visibility
- MongoDB-Powered Retrieval

Document Types:

- Guides
- Policies
- Procedures
- Administrative Documents
- Academic Resources

---

## Appointment Management

The appointment module enables users to submit and track appointment requests.

Features:

- Appointment Creation
- Advisor Selection
- Appointment Type Selection
- Date Selection
- Time Selection
- Notes Support
- Status Tracking

Supported Appointment Types:

- Academic Support
- Administrative Assistance
- Student Services
- Program Consultation

---

## Conversation History

The platform maintains a complete history of user interactions.

Stored Information:

- User Information
- User Role
- Question
- Response
- Source
- Timestamp

Benefits:

- Activity Tracking
- Information Review
- Future Analytics Support
- Improved User Experience

---

# REST API Layer

The application provides REST API endpoints for communication between the frontend and backend.

Implemented Endpoints:

GET /health

POST /api/chat/message

GET /api/chat/history

GET /api/documents

GET /api/appointments

These endpoints support both current functionality and future integrations.

---

# Technology Stack

## Frontend Technologies

- HTML5
- CSS3
- JavaScript

Responsibilities:

- User Interface
- Form Handling
- Chat Interface
- Search Interface
- User Interaction

---

## Backend Technologies

- Python
- Flask

Responsibilities:

- Business Logic
- Authentication
- API Processing
- Session Management
- AI Integration
- Database Communication

---

## Database Technologies

- MongoDB Atlas

Responsibilities:

- User Management
- Knowledge Base Storage
- Document Storage
- Appointment Storage
- Conversation Storage

---

## Artificial Intelligence Technologies

- Groq API
- Llama 3.1 Instant

Responsibilities:

- Response Generation
- Context Enhancement
- Natural Language Processing
- Intelligent Assistance

---

## Development Tools

- Visual Studio Code
- Git
- GitHub
- MongoDB Atlas
- Postman
- Python Virtual Environment

---

# Dependencies

## Introduction

The Agora Assistant Chatbot relies on several third-party Python libraries to support web application development, database communication, artificial intelligence integration, environment variable management, and API processing.

These dependencies are maintained through the `requirements.txt` file, ensuring that every developer, evaluator, or reviewer can install the exact versions required to run the application successfully.

Using a centralized dependency management approach improves reproducibility, simplifies project setup, and reduces compatibility issues across different environments.

---

## Installing Dependencies

After creating and activating the virtual environment, install all required packages using:

```bash
pip install -r requirements.txt
```

This command automatically installs every library required by the application.

---

## Core Dependencies

### Flask

Purpose:

Provides the primary backend framework used to build the web application.

Responsibilities:

- Routing
- Session Management
- Authentication
- Template Rendering
- API Endpoint Handling
- Request Processing

---

### PyMongo

Purpose:

Provides communication between the Flask application and MongoDB Atlas.

Responsibilities:

- Database Connectivity
- Collection Access
- Data Retrieval
- Data Storage
- Query Execution

---

### Python-Dotenv

Purpose:

Loads environment variables from the `.env` file.

Responsibilities:

- Configuration Management
- Credential Loading
- Environment Separation
- Secure Secret Storage

---

### Groq

Purpose:

Provides access to Groq AI services and large language models.

Responsibilities:

- AI Response Generation
- Prompt Processing
- Context Enhancement
- Natural Language Generation

---

## Dependency Verification

After installation, verify that all packages have been installed correctly:

```bash
pip list
```

The installed package list should include the required project dependencies.

---

## Summary

The Agora Assistant Chatbot utilizes a carefully selected set of Python libraries to support web development, cloud database integration, artificial intelligence capabilities, and secure configuration management. These dependencies form the technical foundation of the platform and enable the successful execution of all implemented features.



# Installation Guide

## Introduction

This section provides detailed instructions for setting up and running the Agora Assistant Chatbot in a local development environment.

The application is built using Python and Flask, utilizes MongoDB Atlas as a cloud-based database solution, and integrates Groq AI to generate intelligent chatbot responses. Following the steps outlined below will ensure that all required dependencies, services, and configurations are installed correctly before launching the application.

The installation process has been designed to be straightforward and reproducible, allowing developers, evaluators, and project reviewers to deploy the application consistently across different environments.

---

## System Requirements

Before installing the project, ensure that the following software and services are available on the target system.

### Required Software

* Python 3.10 or later
* Git
* Visual Studio Code (recommended)
* MongoDB Atlas Account
* Groq AI Account
* Modern Web Browser (Google Chrome, Microsoft Edge, Firefox)

### Recommended Knowledge

Although not required, basic familiarity with the following technologies may simplify the installation process:

* Python Programming
* Flask Framework
* MongoDB
* REST APIs
* Environment Variables

---

## Repository Setup

The first step is obtaining the project source code.

Clone the GitHub repository to the local machine:

```bash
git clone <repository-url>
```

Navigate to the project directory:

```bash
cd agora_chatbot_python
```

This directory contains the complete source code, templates, static resources, service modules, configuration files, and project documentation required to run the application.

---

## Virtual Environment Configuration

Python virtual environments provide isolated dependency management and help prevent conflicts with globally installed packages.

Create a virtual environment:

```bash
python -m venv venv
```

Once created, activate the environment.

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Successful activation will display the environment name in the terminal prompt.

Example:

```text
(venv)
```

All subsequent package installations should be performed while the virtual environment is active.

---

## Dependency Installation

After activating the virtual environment, install all required project dependencies.

```bash
pip install -r requirements.txt
```

The requirements file contains all libraries necessary for application execution, database communication, AI integration, and environment configuration.

Installation may take several minutes depending on internet speed and system performance.

---

## Configuration Preparation

Before running the application, database and AI credentials must be configured through environment variables.

A dedicated `.env` file should be created in the project root directory. This file stores sensitive credentials and configuration values that should never be committed to source control.

Additional setup details for MongoDB Atlas and Groq AI are provided in the following sections of this document.

---

## Verification

After installation is completed successfully, verify the environment by executing:

```bash
pip list
```

The required project dependencies should appear in the installed package list.

The application is now ready for environment variable configuration, database setup, and execution.

---

## Installation Summary

The installation process consists of the following stages:

1. Install required software.
2. Clone the repository.
3. Create a virtual environment.
4. Activate the virtual environment.
5. Install project dependencies.
6. Configure environment variables.
7. Configure MongoDB Atlas.
8. Configure Groq AI.
9. Launch the Flask application.

Completing these steps prepares the Agora Assistant Chatbot for local development, testing, demonstration, and evaluation.

# Dependencies

## Introduction

The Agora Assistant Chatbot relies on several third-party Python libraries to support web application development, database communication, artificial intelligence integration, environment variable management, and API processing.

These dependencies are maintained through the `requirements.txt` file, ensuring that every developer, evaluator, or reviewer can install the exact versions required to run the application successfully.

Using a centralized dependency management approach improves reproducibility, simplifies project setup, and reduces compatibility issues across different environments.

---

## Installing Dependencies

After creating and activating the virtual environment, install all required packages using:

```bash
pip install -r requirements.txt
```

This command automatically installs every library required by the application.

---

## Core Dependencies

### Flask

Purpose:

Provides the primary backend framework used to build the web application.

Responsibilities:

- Routing
- Session Management
- Authentication
- Template Rendering
- API Endpoint Handling
- Request Processing

---

### PyMongo

Purpose:

Provides communication between the Flask application and MongoDB Atlas.

Responsibilities:

- Database Connectivity
- Collection Access
- Data Retrieval
- Data Storage
- Query Execution

---

### Python-Dotenv

Purpose:

Loads environment variables from the `.env` file.

Responsibilities:

- Configuration Management
- Credential Loading
- Environment Separation
- Secure Secret Storage

---

### Groq

Purpose:

Provides access to Groq AI services and large language models.

Responsibilities:

- AI Response Generation
- Prompt Processing
- Context Enhancement
- Natural Language Generation

---

## Dependency Verification

After installation, verify that all packages have been installed correctly:

```bash
pip list
```

The installed package list should include the required project dependencies.

---

## Summary

The Agora Assistant Chatbot utilizes a carefully selected set of Python libraries to support web development, cloud database integration, artificial intelligence capabilities, and secure configuration management. These dependencies form the technical foundation of the platform and enable the successful execution of all implemented features.


# Environment Variables

## Introduction

The Agora Assistant Chatbot utilizes environment variables to securely store sensitive configuration information that should not be hardcoded within the application source code.

Environment variables provide a secure and maintainable approach for managing credentials, API keys, database connection strings, and deployment-specific settings. By separating configuration from application logic, the system becomes easier to manage, more secure, and better suited for deployment across different environments.

This project uses a dedicated `.env` file to store all confidential information required by the application.

---

## Purpose of Environment Variables

Environment variables are used to:

* Protect sensitive credentials
* Prevent accidental exposure of secrets
* Simplify configuration management
* Support multiple deployment environments
* Improve application security
* Follow modern development best practices

Without environment variables, sensitive information such as database credentials and API keys would need to be stored directly in the source code, which creates significant security risks.

---

## Creating the Environment File

A file named:

```text
.env
```

must be created in the root directory of the project.

Example project structure:

```text
agora_chatbot_python/
│
├── .env
├── app.py
├── mongo_db.py
├── requirements.txt
│
├── services/
├── templates/
├── static/
├── docs/
└── data/
```

The `.env` file is automatically loaded by the application during startup using the Python dotenv library.

---

## Required Environment Variables

The current version of the application requires the following environment variables.

### MongoDB Atlas Connection String

```env
MONGO_URI=your_mongodb_connection_string
```

Purpose:

This variable stores the MongoDB Atlas connection string used to establish communication between the Flask application and the cloud database.

Responsibilities:

* Database authentication
* Collection access
* Data retrieval
* Data storage
* Cloud connectivity

Example:

```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

---

### Groq API Key

```env
GROQ_API_KEY=your_groq_api_key
```

Purpose:

This variable stores the API key used to authenticate requests to the Groq AI platform.

Responsibilities:

* AI authentication
* Response generation
* Context processing
* Natural language generation

Example:

```env
GROQ_API_KEY=gsk_example_api_key
```

---

## Example Environment File

The completed `.env` file should resemble the following structure:

```env
MONGO_URI=mongodb+srv://your_connection_string
GROQ_API_KEY=your_groq_api_key
```

Actual credentials should never be shared publicly.

---

## Loading Environment Variables

The application loads environment variables automatically during startup using the dotenv library.

Example implementation:

```python
from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
groq_api_key = os.getenv("GROQ_API_KEY")
```

This approach ensures that sensitive credentials remain outside the application source code.

---

## Security Considerations

Environment variables contain sensitive information and must be protected carefully.

Recommended practices include:

* Never commit `.env` files to GitHub.
* Never share credentials publicly.
* Restrict database access when possible.
* Rotate API keys periodically.
* Use different credentials for development and production environments.

Failure to protect environment variables may result in unauthorized database access or misuse of external AI services.

---

## GitHub Protection

The project includes a `.gitignore` configuration that excludes the `.env` file from version control.

Example:

```text
.env
venv/
__pycache__/
```

This ensures that sensitive credentials are never uploaded to the repository.

---

## Verification

To verify successful configuration:

1. Start the Flask application.
2. Confirm MongoDB Atlas connects successfully.
3. Confirm Groq AI generates chatbot responses.
4. Verify no authentication or connection errors appear in the console.

Successful execution confirms that environment variables have been configured correctly.

---

## Summary

Environment variables provide the foundation for secure configuration management within the Agora Assistant Chatbot. By storing database credentials and AI service keys outside the source code, the application maintains a higher level of security, portability, and maintainability while supporting cloud database integration and AI-powered functionality.

# MongoDB Atlas Setup

## Introduction

MongoDB Atlas serves as the primary cloud database platform for the Agora Assistant Chatbot. The database is responsible for storing and managing all application data, including user accounts, chatbot knowledge records, documents, appointments, and conversation history.

Migrating from local JSON storage to MongoDB Atlas was one of the major improvements introduced during Sprint 4. This transition significantly improved scalability, maintainability, data organization, and overall application architecture.

MongoDB Atlas provides a fully managed cloud database solution, allowing the application to securely store and retrieve information from any authorized environment while maintaining high availability and centralized data management.

---

## Purpose of MongoDB Atlas

The database plays a critical role within the system architecture.

Primary responsibilities include:

* User management
* Knowledge base storage
* Document storage
* Appointment management
* Conversation tracking
* Data persistence
* Role-based information retrieval

Without MongoDB Atlas, the application would be limited to local file storage and would not provide centralized cloud-based data management.

---

## Creating a MongoDB Atlas Account

The first step is creating a MongoDB Atlas account.

Steps:

1. Visit the MongoDB Atlas website.
2. Create an account.
3. Create a new project.
4. Create a new cluster.
5. Configure database access.
6. Configure network access.

A free cluster is sufficient for development, testing, demonstration, and project evaluation purposes.

---

## Cluster Configuration

A dedicated cluster should be created to host the Agora Assistant Chatbot database.

Recommended Configuration:

Cluster Type:

* Shared Cluster (Free Tier)

Cloud Provider:

* AWS

Region:

* Closest available region

Cluster Name:

```text
AgoraCluster
```

Once deployment is completed, the cluster becomes available for database creation and connection.

---

## Database User Configuration

After creating the cluster, a database user must be configured.

Steps:

1. Open Database Access.
2. Create a database user.
3. Assign a username.
4. Assign a secure password.
5. Grant Read and Write permissions.

Example:

```text
Username: agora_admin
Password: ********
```

This user account will be used by the Flask application to authenticate with MongoDB Atlas.

---

## Network Access Configuration

MongoDB Atlas restricts access to authorized IP addresses.

To allow application access:

1. Open Network Access.
2. Select Add IP Address.
3. Add the required IP address.

For project evaluation purposes:

```text
0.0.0.0/0
```

may be temporarily used to allow external access.

For production environments, only trusted IP addresses should be authorized.

---

## Obtaining the Connection String

After the cluster has been configured:

1. Open the Cluster.
2. Select Connect.
3. Choose Drivers.
4. Select Python.
5. Copy the generated connection string.

Example:

```text
mongodb+srv://username:password@cluster.mongodb.net/
```

The connection string contains the information required for the application to establish communication with MongoDB Atlas.

---

## Environment Variable Configuration

The MongoDB connection string should never be hardcoded directly into the application.

Instead, store the connection string within the `.env` file.

Example:

```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

This approach improves security and simplifies configuration management.

---

## Database Structure

The Agora Assistant Chatbot utilizes a database named:

```text
agora_chatbot_db
```

The database contains several collections that support the application's functionality.

---

## Users Collection

Purpose:

Stores application user accounts.

Example Data:

* Name
* Email
* Password
* Role
* Department

Responsibilities:

* Authentication
* User identification
* Role management

---

## Knowledge Base Collection

Purpose:

Stores chatbot knowledge records.

Example Data:

* Title
* Category
* Keywords
* Answer
* Audience

Responsibilities:

* Chatbot retrieval
* Knowledge matching
* Role-based information filtering

---

## Documents Collection

Purpose:

Stores document metadata available through the document library.

Example Data:

* Title
* Category
* Summary
* Type
* Audience

Responsibilities:

* Document discovery
* Search functionality
* Role filtering

---

## Appointments Collection

Purpose:

Stores appointment requests submitted through the platform.

Example Data:

* User
* Appointment Type
* Advisor
* Date
* Time
* Status

Responsibilities:

* Appointment management
* Request tracking
* Future workflow support

---

## Conversations Collection

Purpose:

Stores chatbot conversation history.

Example Data:

* User
* Question
* Response
* Source
* Timestamp

Responsibilities:

* History tracking
* Activity monitoring
* Future analytics support

---

## MongoDB Integration Architecture

Application Flow:

```text
User
↓
Flask Application
↓
MongoDB Driver (PyMongo)
↓
MongoDB Atlas
↓
Collections
↓
Application Response
```

This architecture enables centralized cloud-based data storage and retrieval.

---

## Connection Verification

After configuring MongoDB Atlas, verify connectivity by executing a connection test.

Expected Result:

```text
MongoDB Connected Successfully!
```

Successful connection confirms that:

* Credentials are valid.
* Network access is configured correctly.
* The application can communicate with the cloud database.

---

## Advantages of MongoDB Atlas

The migration to MongoDB Atlas introduced several advantages.

### Scalability

Supports future application growth without requiring significant architecture changes.

### Centralized Storage

All application data is stored within a single cloud-hosted database.

### Flexibility

Document-based storage allows rapid schema evolution.

### Reliability

Managed infrastructure provides high availability and automatic maintenance.

### Security

Supports authentication, access control, encrypted connections, and network restrictions.

---

## MongoDB Usage Within This Project

MongoDB Atlas is used throughout the application for:

* Authentication data
* Chatbot knowledge retrieval
* Document search
* Appointment storage
* Conversation tracking

As a result, MongoDB serves as the central data layer of the Agora Assistant Chatbot architecture.

---

## Summary

MongoDB Atlas provides the cloud database foundation for the Agora Assistant Chatbot. Through centralized storage, flexible document management, role-based data retrieval, and scalable architecture, the database enables the application to support authentication, intelligent chatbot functionality, document management, appointment processing, and conversation history tracking while maintaining reliability, security, and future growth potential.

# Groq AI Setup

## Introduction

Artificial Intelligence is one of the core components of the Agora Assistant Chatbot. While the knowledge base provides structured institutional information, the integration of Groq AI enhances the quality of responses by generating more natural, conversational, and context-aware answers.

The AI layer transforms static knowledge-base content into intelligent responses that are easier for users to understand and interact with. This creates a significantly better user experience compared to traditional rule-based chatbot systems.

The current implementation uses the Groq API together with the Llama 3.1 Instant model to generate responses based on knowledge retrieved from MongoDB Atlas.

---

## Purpose of Groq AI Integration

The primary objective of integrating Groq AI is to improve the chatbot's ability to communicate information effectively.

Key responsibilities include:

* Response generation
* Natural language processing
* Context enhancement
* Improved readability
* Conversational interaction
* Knowledge interpretation
* User assistance

Without AI integration, the chatbot would simply return raw knowledge-base responses, resulting in a less engaging user experience.

---

## Why Groq AI Was Selected

Several AI providers were evaluated during the development process.

Groq AI was selected because it provides:

* Fast response generation
* High-quality language models
* Simple API integration
* Reliable performance
* Developer-friendly implementation
* Cost-effective access for educational projects

The service integrates easily with Python applications and supports modern large language models capable of producing professional and contextually relevant responses.

---

## AI Model Used

Current Model:

```text
Llama 3.1 Instant
```

Model Provider:

```text
Groq
```

Purpose:

* Question answering
* Context interpretation
* Response enhancement
* Natural language generation

The selected model provides an excellent balance between response quality and speed, making it well suited for real-time chatbot interactions.

---

## Creating a Groq Account

To use Groq AI, a Groq account must be created.

Steps:

1. Create a Groq account.
2. Access the Groq Developer Console.
3. Generate a new API key.
4. Copy the generated key.
5. Store the key securely.

The API key is required for authenticating requests sent from the Flask application.

---

## API Key Configuration

The API key should never be hardcoded into the application source code.

Instead, it should be stored inside the `.env` file.

Example:

```env
GROQ_API_KEY=your_groq_api_key
```

This approach improves security and simplifies configuration management.

---

## Environment Variable Loading

The application loads the Groq API key automatically during startup.

Example:

```python
from dotenv import load_dotenv
import os

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
```

This ensures that sensitive credentials remain outside the source code.

---

## AI Service Architecture

The AI integration is implemented through a dedicated service layer.

File:

```text
services/ai_service.py
```

Responsibilities:

* API communication
* Prompt construction
* Response generation
* Error handling
* AI request processing

This separation improves maintainability and supports future AI model upgrades.

---

## Chatbot Processing Workflow

The chatbot follows a multi-stage workflow before generating a response.

### Step 1 – User Question

The user submits a question through the chatbot interface.

Example:

```text
How can I book an academic advisor appointment?
```

---

### Step 2 – Knowledge Base Search

The application searches MongoDB Atlas for relevant knowledge records.

Matching criteria include:

* Keywords
* Titles
* Categories
* Audience roles

---

### Step 3 – Role Validation

The system verifies whether the current user has permission to access the requested information.

Supported Roles:

* Student
* Teacher
* Administrator

Only authorized content is considered.

---

### Step 4 – Context Selection

The most relevant knowledge record is selected.

Example Context:

```text
Students can book an academic advisor appointment using the Appointment Booking page.
```

---

### Step 5 – Prompt Generation

A structured prompt is created and sent to Groq AI.

Example Structure:

```text
Context:
[Knowledge Base Information]

User Question:
[User Question]

Provide a helpful response.
```

This ensures that Groq AI generates responses grounded in institutional information.

---

### Step 6 – AI Response Generation

Groq AI processes the prompt and generates a natural-language response.

Example:

```text
You can schedule an academic advisor appointment through the Appointment Booking section of the Agora portal. After selecting your preferred advisor, choose a suitable date and time before submitting your request.
```

---

### Step 7 – Conversation Storage

The generated response is saved in MongoDB Atlas.

Stored Information:

* User
* Question
* Response
* Source
* Timestamp

This supports conversation history functionality.

---

## AI Response Advantages

The integration of Groq AI provides several advantages.

### Improved Readability

Responses are easier to understand than raw database entries.

### Better User Experience

Users interact with a conversational assistant rather than a static FAQ system.

### Context Awareness

Responses are generated using knowledge retrieved from MongoDB Atlas.

### Scalability

Future knowledge records can be added without redesigning the chatbot architecture.

---

## Error Handling

The AI integration includes fallback handling to ensure reliability.

If AI generation fails:

1. The application attempts to use local knowledge-base information.
2. A fallback response is displayed.
3. The application continues operating without interruption.

This prevents AI service outages from affecting the overall usability of the system.

---

## Security Considerations

Several security practices were implemented.

### API Key Protection

The Groq API key is stored within environment variables.

### Source Code Protection

No credentials are hardcoded within the repository.

### GitHub Protection

The `.env` file is excluded through `.gitignore`.

### Controlled Access

Only the backend communicates directly with the Groq API.

These measures reduce the risk of credential exposure.

---

## Future AI Enhancements

Potential future improvements include:

* Advanced prompt engineering
* Multi-turn conversation support
* Semantic search integration
* Vector database integration
* Personalized responses
* Fine-tuned institutional assistants
* Multi-language support
* Retrieval-Augmented Generation (RAG)

These enhancements would further improve chatbot intelligence and response quality.

---

## Benefits to the Project

The addition of Groq AI transformed the chatbot from a simple knowledge retrieval system into a more advanced intelligent assistant.

Major benefits include:

* Natural language interaction
* Improved response quality
* Enhanced user experience
* Better contextual understanding
* More professional demonstrations
* Greater scalability for future development

---

## Summary

The integration of Groq AI represents a major enhancement to the Agora Assistant Chatbot architecture. By combining MongoDB-based knowledge retrieval with AI-powered response generation, the system delivers accurate, contextual, and user-friendly answers while maintaining security, scalability, and maintainability. The Groq AI layer significantly improves the overall effectiveness of the platform and provides a strong foundation for future intelligent assistant development.


# Running the Application

## Introduction

After completing the installation process, configuring environment variables, setting up MongoDB Atlas, and configuring Groq AI, the Agora Assistant Chatbot is ready to be executed.

The application is built using the Flask web framework and runs as a local web server during development and testing. Once started, users can access the platform through a web browser and interact with all implemented features, including authentication, AI-powered assistance, document search, appointment management, and conversation history tracking.

This section explains how to launch, verify, and test the application successfully.

---

## Pre-Execution Checklist

Before starting the application, verify the following requirements:

### Installation Completed

Confirm that all project dependencies have been installed successfully.

```bash
pip install -r requirements.txt
```

---

### Virtual Environment Activated

The Python virtual environment should be active.

Example:

```text
(venv)
```

Running the application without activating the virtual environment may result in missing dependency errors.

---

### Environment Variables Configured

Verify that the `.env` file exists and contains valid credentials.

Required Variables:

```env
MONGO_URI=your_mongodb_connection_string
GROQ_API_KEY=your_groq_api_key
```

---

### MongoDB Atlas Accessible

Verify that:

* Database credentials are valid
* Network access is configured
* Cluster is active

---

### Groq API Configured

Verify that:

* API key is valid
* API key is stored in `.env`
* Internet connectivity is available

---

## Starting the Application

The Flask server can be started using the following command:

```bash
python app.py
```

---

## Expected Startup Output

If the application starts successfully, the terminal should display output similar to:

```text
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000
```

This indicates that:

* Flask is running correctly
* Backend services are active
* Database configuration has loaded successfully
* Application routes are available

---

## Accessing the Application

Open a web browser and navigate to:

```text
http://127.0.0.1:5000
```

The login page should appear.

---

## Authentication Testing

Once the application loads, users can authenticate using available accounts.

Supported Roles:

### Student

Access to:

* Chatbot
* Documents
* Appointments
* Conversation History

---

### Teacher

Access to:

* Teacher Resources
* Attendance Information
* Documents
* Chatbot
* History

---

### Administrator

Access to:

* Administrative Information
* Reports
* Documents
* Chatbot
* History

---

## Verifying Application Functionality

After login, the following modules should be tested to confirm successful execution.

---

### Dashboard

Verify that:

* Dashboard loads successfully
* Navigation menu is visible
* User information displays correctly

Expected Result:

Dashboard accessible without errors.

---

### Chatbot

Verify that:

* Questions can be submitted
* Responses are generated
* Source information is displayed

Example Questions:

```text
How can I register for courses?
```

```text
Where can teachers update attendance?
```

Expected Result:

AI-generated response displayed successfully.

---

### Document Library

Verify that:

* Documents are visible
* Search functionality works
* Results are filtered correctly

Expected Result:

Relevant documents returned successfully.

---

### Appointment Management

Verify that:

* Appointment form loads
* Validation works
* Requests can be submitted

Expected Result:

Appointment stored successfully.

---

### Conversation History

Verify that:

* Previous conversations appear
* Timestamps display correctly
* User-specific history is shown

Expected Result:

Conversation history retrieved successfully.

---

## API Verification

The application exposes several REST API endpoints.

These endpoints can be tested using a browser, Postman, or developer tools.

---

### Health Endpoint

```text
GET /health
```

Expected Result:

```json
{
  "status": "running",
  "project": "Agora Assistant Chatbot - Python Version"
}
```

---

### Chat Endpoint

```text
POST /api/chat/message
```

Expected Result:

Returns chatbot response data.

---

### History Endpoint

```text
GET /api/chat/history
```

Expected Result:

Returns conversation history.

---

### Documents Endpoint

```text
GET /api/documents
```

Expected Result:

Returns available documents.

---

### Appointments Endpoint

```text
GET /api/appointments
```

Expected Result:

Returns user appointment records.

---

## Common Startup Issues

### MongoDB Connection Error

Possible Causes:

* Invalid connection string
* Network access restrictions
* Database user credentials incorrect

Resolution:

Verify:

* MONGO_URI
* Atlas Network Access
* Database user configuration

---

### Groq API Error

Possible Causes:

* Invalid API key
* Expired credentials
* Internet connectivity issues

Resolution:

Verify:

* GROQ_API_KEY
* Account status
* API key configuration

---

### Missing Module Error

Possible Causes:

Required dependency not installed.

Resolution:

Run:

```bash
pip install -r requirements.txt
```

---

### Environment Variable Error

Possible Causes:

Missing `.env` file.

Resolution:

Create and configure the `.env` file correctly.

---

## Stopping the Application

To stop the Flask server:

Press:

```text
CTRL + C
```

The application will shut down safely.

---

## Execution Summary

Successful execution confirms:

✓ Flask application is running

✓ MongoDB Atlas is connected

✓ Groq AI integration is active

✓ Authentication functions correctly

✓ Chatbot responses are generated

✓ Documents can be retrieved

✓ Appointments can be created

✓ Conversation history is stored

✓ API endpoints are operational

---

## Conclusion

The Agora Assistant Chatbot can be launched using a simple Flask execution command and accessed through a standard web browser. Successful startup confirms that all core components—including MongoDB Atlas integration, Groq AI connectivity, authentication, chatbot functionality, document management, appointment processing, and conversation tracking—are operating correctly. This execution process supports development, testing, demonstration, and final project evaluation activities.


# Project Folder Structure

## Introduction

The Agora Assistant Chatbot follows a modular and organized project structure designed to improve maintainability, scalability, readability, and future development. The architecture separates application logic, presentation components, service layers, configuration files, documentation, and static resources into dedicated directories.

This approach simplifies development and testing while allowing new features to be integrated without significantly affecting existing functionality.

The structure also follows common Flask application development practices and supports future expansion into larger-scale deployments.

---

## Project Structure Overview

```text
agora_chatbot_python/
│
├── app.py
├── mongo_db.py
├── seed_data.py
├── requirements.txt
├── .env
├── .gitignore
│
├── services/
│   ├── ai_service.py
│   └── chatbot_service.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── chat.html
│   ├── documents.html
│   ├── appointments.html
│   ├── history.html
│   ├── 404.html
│   └── 500.html
│
├── static/
│   └── style.css
│
├── docs/
│
└── data/
```

---

# Root Directory Files

The root directory contains the primary application files responsible for execution, configuration, and database connectivity.

---

## app.py

Purpose:

Main application entry point.

Responsibilities:

* Flask initialization
* Route registration
* Session management
* Authentication
* API endpoint handling
* Business logic coordination
* Frontend rendering

This file acts as the central controller of the application and coordinates communication between all major components.

---

## mongo_db.py

Purpose:

MongoDB Atlas connection management.

Responsibilities:

* Establish database connection
* Load environment variables
* Initialize MongoDB client
* Provide collection access

Collections Managed:

* users
* knowledge_base
* documents
* appointments
* conversations

This file serves as the application's database access layer.

---

## seed_data.py

Purpose:

Database initialization and sample data population.

Responsibilities:

* Insert initial records
* Populate knowledge base
* Populate documents
* Create sample users
* Create sample appointments

This file simplifies testing and demonstration activities by ensuring the database contains meaningful content.

---

## requirements.txt

Purpose:

Dependency management.

Responsibilities:

* Define project packages
* Support environment setup
* Simplify installation

Typical Dependencies:

* Flask
* pymongo
* python-dotenv
* groq

This file enables reproducible project installation across different environments.

---

## .env

Purpose:

Secure storage of configuration values and credentials.

Contains:

* MongoDB connection string
* Groq API key

Important:

This file should never be uploaded to GitHub.

---

## .gitignore

Purpose:

Exclude sensitive or unnecessary files from source control.

Protected Resources:

* .env
* Virtual environments
* Cache files
* Temporary files

This file supports secure repository management.

---

# Services Directory

The services directory contains business logic and external service integrations.

Structure:

```text
services/
├── ai_service.py
└── chatbot_service.py
```

---

## ai_service.py

Purpose:

Groq AI integration layer.

Responsibilities:

* API communication
* Prompt generation
* Response processing
* Error handling

This module isolates AI-related functionality from the rest of the application.

Benefits:

* Improved maintainability
* Easier testing
* Future AI model replacement

---

## chatbot_service.py

Purpose:

Chatbot processing logic.

Responsibilities:

* Knowledge base retrieval
* Role filtering
* Context selection
* AI request preparation
* Response generation workflow

This file represents the intelligence layer of the chatbot system.

---

# Templates Directory

The templates directory contains all frontend HTML pages rendered by Flask.

Structure:

```text
templates/
```

The application uses server-side rendering to dynamically generate user interfaces.

---

## base.html

Purpose:

Master template shared by all pages.

Responsibilities:

* Layout structure
* Navigation
* Shared styling
* Page inheritance

This file promotes consistency across the user interface.

---

## login.html

Purpose:

User authentication interface.

Responsibilities:

* Credential submission
* Login validation
* Authentication entry point

---

## dashboard.html

Purpose:

Application landing page after authentication.

Responsibilities:

* Navigation
* User information
* Module access

---

## chat.html

Purpose:

Chatbot interaction interface.

Responsibilities:

* User questions
* AI responses
* Source display
* Message submission

This page represents the primary user-facing feature of the application.

---

## documents.html

Purpose:

Document discovery interface.

Responsibilities:

* Search functionality
* Role filtering
* Document presentation

---

## appointments.html

Purpose:

Appointment request interface.

Responsibilities:

* Form submission
* Appointment creation
* Validation

---

## history.html

Purpose:

Conversation history display.

Responsibilities:

* Conversation tracking
* Response review
* Timestamp display

---

## 404.html

Purpose:

Custom page-not-found interface.

Displayed when:

* Invalid URLs are requested

---

## 500.html

Purpose:

Custom server error interface.

Displayed when:

* Internal server errors occur

---

# Static Directory

The static directory contains frontend resources used throughout the application.

Structure:

```text
static/
└── style.css
```

---

## style.css

Purpose:

Application styling.

Responsibilities:

* Layout design
* Chat interface styling
* Form styling
* Navigation styling
* Responsive appearance

This file controls the visual presentation of the platform.

---

# Documentation Directory

The docs directory contains all project documentation generated throughout development.

Structure:

```text
docs/
```

Examples:

* architecture.md
* mongodb_architecture.md
* data_structure.md
* api_examples.md
* test_plan.md
* testing_report.md
* sprint4_summary.md
* sprint5_test_results.md
* sprint5_bug_list.md
* python_demo_notes.md
* limitations_future_improvements.md

Purpose:

* Project validation
* Technical documentation
* Sprint reporting
* Testing evidence
* Future development planning

---

# Data Directory

The data directory stores local resources, backup files, and development assets used during implementation.

Structure:

```text
data/
```

Purpose:

* Temporary storage
* Local datasets
* Development resources
* Backup content

While MongoDB Atlas is the primary storage solution, this directory remains useful for development and testing purposes.

---

# Architectural Benefits

The current project structure provides several advantages.

### Modularity

Application components are separated logically.

### Maintainability

Individual modules can be updated independently.

### Scalability

New features can be integrated with minimal disruption.

### Reusability

Services and templates can be reused throughout the application.

### Professional Development Practices

The structure aligns with modern Flask application design principles.

---

# Summary

The Agora Assistant Chatbot utilizes a structured and modular architecture that separates business logic, database connectivity, user interfaces, AI integration, configuration management, and documentation into dedicated components. This organization improves maintainability, supports future scalability, and provides a professional foundation for continued development and deployment.

    
# Database Architecture

Database:

agora_chatbot_db

Collections:

- users
- knowledge_base
- documents
- appointments
- conversations

Advantages:

- Cloud-Based Storage
- Improved Scalability
- Centralized Data Management
- Flexible Schema Design
- Enhanced Performance

---

# System Architecture

User
↓
Web Interface
↓
Flask Application
↓
Authentication Layer
↓
Business Logic Layer
↓
MongoDB Atlas
↓
Groq AI
↓
Response Returned

---

# Security Features

Implemented Security Controls:

- Session Authentication
- Protected Routes
- Role-Based Access Control
- Environment Variable Protection
- MongoDB Atlas Security

Protected Resources:

- Dashboard
- Chat
- Documents
- Appointments
- History
- API Endpoints

Future Security Enhancements:

- Password Hashing
- JWT Authentication
- Multi-Factor Authentication
- Audit Logging

---

# Documentation

Comprehensive project documentation is available within the docs directory.

Available Documentation:

- Architecture Documentation
- MongoDB Architecture Documentation
- Data Structure Documentation
- API Documentation
- Test Plan
- Testing Report
- Sprint 4 Summary
- Python Version Mapping

---

# Testing Coverage

Completed Testing Areas:

✓ Authentication

✓ Chatbot Functionality

✓ Role-Based Access Control

✓ Document Search

✓ Appointment Management

✓ Conversation History

✓ API Endpoints

✓ MongoDB Integration

✓ Groq AI Integration

✓ Error Handling

---

# Sprint 4 Achievements

Major accomplishments completed during Sprint 4 include:

- Migration from JSON files to MongoDB Atlas
- Integration of Groq AI
- Advanced chatbot response generation
- Role-based information filtering
- Expanded knowledge base
- Improved document search
- Enhanced appointment management
- Expanded testing coverage
- Professional technical documentation

---

# Future Roadmap

Planned future enhancements include:

- JWT Authentication
- Password Hashing
- Email Notifications
- Appointment Status Management
- Administrative Dashboard
- Advanced Search Algorithms
- Analytics Dashboard
- Vector Database Integration
- Multi-Factor Authentication
- AI Knowledge Expansion

---

# Conclusion

The Agora Assistant Chatbot demonstrates a complete Python-based intelligent assistant platform capable of supporting students, teachers, and administrators through secure authentication, cloud database integration, AI-powered assistance, document management, appointment scheduling, and conversation tracking.

The successful completion of Sprint 4 transformed the project from a minimum viable product into a significantly more advanced and scalable application architecture. Through the integration of MongoDB Atlas and Groq AI, the platform now provides a realistic foundation for future institutional chatbot solutions and continued development.