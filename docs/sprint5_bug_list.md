# Sprint 5 Bug List and Resolution Report

## Project Information

**Project Name:** Agora Assistant Chatbot – Python Equivalent Version

**Sprint:** Sprint 5 – Testing, Security, and Stabilization

**Prepared By:** Abhi Patel

**Technology Stack:**

* Python
* Flask
* MongoDB Atlas
* Groq AI (Llama 3.1)
* HTML
* CSS
* JavaScript

**Date:** June 2026

---

# Introduction

Sprint 5 focused on project stabilization, testing, validation, security review, and preparation for final project evaluation. The primary objective of this phase was to identify functional issues, validate system behavior, verify integrations, improve user experience, and ensure that the Python version remained aligned with the objectives of the main Assistant Chatbot project.

Throughout the testing process, multiple functional, usability, integration, and security-related issues were reviewed. Identified defects were analyzed, documented, corrected, and re-tested to verify successful resolution.

This report provides a complete overview of the issues discovered during Sprint 5, the corrective actions taken, and the remaining limitations that may be considered future enhancements.

---

# Bug Classification Methodology

The following severity scale was used during testing and validation.

## Critical

A defect that prevents a major system component from functioning or causes complete application failure.

Examples:

* Application crash
* Database connection failure
* Authentication failure

---

## High

A defect that significantly impacts functionality, usability, or project evaluation.

Examples:

* Form validation failure
* Data not being stored correctly
* Unauthorized access to protected resources

---

## Medium

A defect that affects usability, response quality, or user experience but does not prevent core functionality.

Examples:

* Poor formatting
* Incorrect responses
* Navigation inconsistencies

---

## Low

A minor issue that has minimal impact on functionality and can be considered a future enhancement.

Examples:

* Missing optional functionality
* User interface refinements
* Administrative convenience features

---

# Bug 1 – Chatbot Message Submission Using Enter Key

## Severity

Medium

## Module

Chatbot Interface

## Description

During user testing, it was discovered that chatbot messages could only be submitted through the Send button. Pressing the Enter key within the chat input field did not trigger message submission.

This behavior differed from standard chat application expectations and negatively affected user experience.

---

## Impact

* Reduced usability
* Slower user interaction
* Inconsistent chat experience

---

## Root Cause

The message input field lacked a keyboard event listener capable of detecting Enter key presses and triggering message submission.

---

## Resolution

Implemented a JavaScript keydown event listener that detects Enter key events and calls the existing sendMessage() function.

---

## Verification

Successfully verified that users can:

* Type a message
* Press Enter
* Send the message immediately

---

## Status

Resolved

---

# Bug 2 – MongoDB Atlas Connection Restriction

## Severity

High

## Module

Database Connectivity

## Description

External testers were unable to connect to MongoDB Atlas despite using the correct database credentials and environment configuration.

The issue prevented project reviewers from accessing and testing the application.

---

## Impact

* Blocked external evaluation
* Prevented remote testing
* Delayed validation process

---

## Root Cause

MongoDB Atlas Network Access settings only allowed connections from the developer's whitelisted IP address.

---

## Resolution

Updated MongoDB Atlas Network Access configuration to temporarily allow project evaluation access.

---

## Verification

External connectivity was successfully tested and confirmed.

---

## Status

Resolved

---

# Bug 3 – Chat Response Formatting Issue

## Severity

Medium

## Module

User Interface

## Description

Long chatbot responses appeared visually compressed and difficult to read.

Spacing and line breaks were not preserved correctly.

---

## Impact

* Reduced readability
* Poor user experience
* Difficult interpretation of long responses

---

## Root Cause

The CSS styling for chatbot messages did not preserve whitespace formatting.

---

## Resolution

Updated CSS configuration to improve spacing and preserve line breaks.

### Applied Styling

```css
.bot-message {
    white-space: pre-line;
    line-height: 1.6;
}
```

---

## Verification

Responses now display with improved readability and visual consistency.

---

## Status

Resolved

---

# Bug 4 – Appointment Form Validation Weakness

## Severity

High

## Module

Appointment Management

## Description

The appointment request form initially allowed submission attempts with incomplete information.

Incomplete requests could reduce data quality and generate invalid records.

---

## Impact

* Invalid records
* Poor user guidance
* Reduced data integrity

---

## Root Cause

Required field validation was insufficient.

---

## Resolution

Enhanced validation for:

* Name
* Appointment Type
* Advisor
* Date
* Time

---

## Verification

Application correctly prevents incomplete submissions and displays validation messages.

---

## Status

Resolved

---

# Bug 5 – Knowledge Base Matching Accuracy

## Severity

Medium

## Module

Chatbot Logic

## Description

Several valid questions produced fallback responses even when relevant knowledge existed within the database.

---

## Impact

* Reduced chatbot accuracy
* Increased fallback responses
* Lower confidence in chatbot reliability

---

## Root Cause

Keyword matching logic was overly restrictive and lacked sufficient keyword coverage.

---

## Resolution

Improvements included:

* Expanded keyword sets
* Additional knowledge records
* Enhanced context selection logic
* Improved matching criteria

---

## Verification

Previously failing questions successfully returned relevant responses.

---

## Status

Resolved

---

# Bug 6 – Missing Administrative Knowledge Records

## Severity

Medium

## Module

Knowledge Base

## Description

Administrative questions related to reports, statistics, and management functions returned fallback responses.

---

## Impact

Administrator users could not obtain appropriate responses.

---

## Root Cause

Administrative content had not yet been added to the knowledge base.

---

## Resolution

Added new records covering:

* Administrative Reports
* Attendance Management
* Administrative Services
* Internal Resources

---

## Verification

Administrative questions now return relevant responses.

---

## Status

Resolved

---

# Bug 7 – Static Response Limitation

## Severity

Medium

## Module

Artificial Intelligence

## Description

The initial chatbot implementation relied exclusively on static knowledge-base responses.

Although technically functional, responses often appeared repetitive and lacked conversational quality.

---

## Impact

* Reduced user engagement
* Robotic responses
* Limited response flexibility

---

## Root Cause

No AI enhancement layer existed.

---

## Resolution

Integrated Groq AI using the Llama 3.1 Instant model.

Implemented context-driven prompt generation using MongoDB knowledge records.

---

## Verification

Responses became:

* More natural
* More conversational
* More context aware
* Easier to understand

---

## Status

Resolved

---

# Bug 8 – Appointment Approval Workflow Not Implemented

## Severity

Low

## Module

Appointment Management

## Description

Users can successfully create appointment requests; however, administrators currently do not have a dedicated interface for reviewing, approving, rejecting, or updating appointment requests.

---

## Impact

The limitation does not affect appointment creation or storage but limits administrative workflow management.

---

## Root Cause

The project scope prioritized appointment request creation rather than complete appointment lifecycle management.

---

## Recommended Solution

Develop an administrative dashboard supporting:

* Appointment review
* Appointment approval
* Appointment rejection
* Status updates
* Administrative notes

---

## Verification

Appointment creation and storage work correctly.

Administrative workflow management remains unavailable.

---

## Status

Open – Future Enhancement

---

# Security Issues Reviewed

## Environment Variable Protection

### Risk

Sensitive credentials exposed in source code.

### Resolution

Moved all credentials to environment variables.

Protected values include:

* MONGO_URI
* GROQ_API_KEY

### Status

Resolved

---

## GitHub Credential Exposure

### Risk

Sensitive information accidentally committed to source control.

### Resolution

Configured `.gitignore` to exclude:

* .env
* Virtual environments
* Cache files
* Temporary files

### Status

Resolved

---

## Unauthorized Route Access

### Risk

Unauthenticated users accessing protected resources.

### Resolution

Implemented authentication validation for:

* Dashboard
* Chat
* Documents
* Appointments
* History
* API Endpoints

### Status

Resolved

---

# Remaining Known Limitations

The following limitations do not impact required project functionality but should be considered future improvements.

## Password Security

Current implementation stores passwords in plain text for demonstration purposes.

Recommended Improvement:

Implement bcrypt password hashing.

Priority:

Future Enhancement

---

## Authentication Model

Current implementation uses session-based authentication.

Recommended Improvement:

Implement JWT authentication for production deployment.

Priority:

Future Enhancement

---

## Search Intelligence

Current implementation relies on keyword matching.

Recommended Improvement:

Implement semantic search using embeddings or vector databases.

Priority:

Future Enhancement

---

## Administrative Appointment Management

Appointment approval and rejection functionality is not yet implemented.

Recommended Improvement:

Administrative appointment dashboard.

Priority:

Future Enhancement

---

# Sprint 5 Bug Summary

## Total Issues Identified

8

## Critical Issues

0

## High Severity Issues

2

## Medium Severity Issues

5

## Low Severity Issues

1

## Resolved Issues

7

## Open Issues

1

## Resolution Rate

87.5%

---

# Quality Assessment

Application Stability:

Excellent

Authentication:

Verified

MongoDB Integration:

Verified

Groq AI Integration:

Verified

Role-Based Access Control:

Verified

Document Search:

Verified

Appointment Management:

Verified

Conversation History:

Verified

API Functionality:

Verified

Security Review:

Passed

Readiness for Demonstration:

Ready

---

# Conclusion

Sprint 5 testing successfully identified, documented, and resolved the majority of issues discovered during validation of the Agora Assistant Chatbot. All core modules, including authentication, chatbot processing, MongoDB Atlas integration, Groq AI integration, document search, appointment management, role-based filtering, conversation history, and API functionality, were thoroughly tested and validated.

A single non-critical enhancement remains related to administrative appointment approval workflow management. This limitation does not impact the required project objectives and has been documented for future development.

Overall, the application is considered stable, secure, well-documented, and ready for final review, demonstration, and project presentation.
