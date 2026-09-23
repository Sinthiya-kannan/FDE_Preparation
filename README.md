# FDE Preparation – FastAPI Backend & AI Security Analysis

## Overview

This project is a backend application developed as part of my Forward Deployed Engineer (FDE) preparation.

The application demonstrates how to:

* Understand and implement client requirements
* Build REST APIs using FastAPI
* Implement authentication and role-based authorization
* Manage customers and users
* Implement invitation and approval workflows
* Integrate PostgreSQL
* Integrate Gemini AI for security analysis
* Containerize the application using Docker
* Use Nginx as a reverse proxy
* Run the application using Docker Compose
* Automate testing and Docker image builds using GitHub Actions

---

## Technology Stack

| Technology     | Purpose                               |
| -------------- | ------------------------------------- |
| Python         | Backend programming                   |
| FastAPI        | REST API framework                    |
| PostgreSQL     | Database                              |
| SQLAlchemy     | ORM                                   |
| Pydantic       | Request/response validation           |
| JWT            | Authentication                        |
| RBAC           | Role-based authorization              |
| Gemini AI      | Security analysis and recommendations |
| Docker         | Application containerization          |
| Docker Compose | Multi-container deployment            |
| Nginx          | Reverse proxy                         |
| Pytest         | Automated testing                     |
| GitHub Actions | CI/CD                                 |
| GitHub         | Source code management                |

---

## Application Architecture

```text
                    Client / Browser
                           |
                           v
                    +-------------+
                    |    Nginx    |
                    |    :80      |
                    +-------------+
                           |
                           v
                    +-------------+
                    |   FastAPI   |
                    |    :8000    |
                    +-------------+
                       /         \
                      /           \
                     v             v
              +-----------+   +-----------+
              | PostgreSQL|   | Gemini AI |
              |   :5432   |   |           |
              +-----------+   +-----------+
```

### Docker Architecture

The application runs using three main containers:

```text
fde-nginx
     |
     v
fde-fastapi
     |
     v
fde-postgres
```

Nginx receives HTTP requests and forwards them to the FastAPI application.

FastAPI communicates with PostgreSQL for application data and with Gemini for AI security analysis.

---

# Features

## 1. Customer Management

The application supports customer/company registration and management.

Example workflow:

```text
Customer Registration
        |
        v
     Pending
      /   \
     /     \
Approved   Rejected
```

Company email/domain validation is used as part of the registration workflow.

---

## 2. User Management

Users can be associated with customers.

The application supports different roles:

* `USER`
* `PRIMARY_USER`
* `ADMIN`

Role-based permissions determine which operations a user can perform.

---

## 3. Authentication

The application uses JWT Bearer authentication.

Authentication flow:

```text
Login
  |
  v
Validate Email + Password
  |
  v
Generate JWT
  |
  v
Client sends:
Authorization: Bearer <token>
  |
  v
FastAPI validates JWT
```

JWT claims contain information such as the authenticated user's identity and role.

The JWT is signed, not encrypted.

---

## 4. Role-Based Authorization

Authorization is implemented using FastAPI dependencies.

Example:

```text
ADMIN
 ├── Approve customer
 ├── Reject customer
 └── Manage users

PRIMARY_USER
 └── Customer-level operations

USER
 └── Permitted user operations
```

Authentication answers:

> Who are you?

Authorization answers:

> What are you allowed to do?

---

# 5. Invitation Workflow

The application supports user invitation and activation.

Example:

```text
Create User
    |
    v
Invitation Created
    |
    v
Invitation Token
    |
    v
User Activates Invitation
    |
    v
User Becomes Active
```

Invitation information includes:

* Invitation ID
* User ID
* UUID token
* Sent date
* Expiration date
* Status
* Active flag

Invitation tokens expire after a configured period.

---

# 6. AI Security Analysis

The application integrates Gemini AI to analyze company security information.

Example input:

```json
{
  "company_name": "ABC Technologies",
  "industry": "Healthcare",
  "employees": 250,
  "security_concerns": [
    "Weak password policy",
    "No MFA",
    "Outdated software"
  ]
}
```

The AI service generates:

* Risk summary
* Security recommendations
* Recommendation priority

Example response structure:

```json
{
  "risk_summary": "The company has several security weaknesses...",
  "recommendations": [
    {
      "recommendation": "Implement multi-factor authentication",
      "priority": "Critical"
    },
    {
      "recommendation": "Improve password policy",
      "priority": "High"
    },
    {
      "recommendation": "Update outdated software",
      "priority": "Medium"
    }
  ]
}
```

### AI Processing Flow

```text
FastAPI
   |
   v
AI Service
   |
   v
Build Prompt
   |
   v
Gemini API
   |
   v
JSON Response
   |
   v
Pydantic Validation
   |
   v
PostgreSQL
```

The AI functionality is separated into an independent service layer so that the business logic is not tightly coupled to the AI provider.

---

# 7. Database

PostgreSQL is used as the application database.

Current main tables include:

```text
customers
users
invitations
ai_analysis
```

SQLAlchemy is used as the ORM.

Database connection configuration is provided through environment variables.

---

# 8. Docker

The application is containerized using Docker.

The Docker image contains:

* Python
* FastAPI
* Application source code
* Required Python dependencies

Example Docker flow:

```text
Dockerfile
    |
    v
docker build
    |
    v
Docker Image
    |
    v
Docker Container
```

Docker Compose is used to run the complete application stack.

---

# 9. Nginx Reverse Proxy

Nginx acts as a reverse proxy.

```text
Browser
   |
   | HTTP :80
   v
Nginx
   |
   | HTTP :8000
   v
FastAPI
```

FastAPI is not directly exposed to the host.

Nginx provides a single entry point for incoming HTTP traffic.

---

# 10. Environment Configuration

Sensitive configuration is not stored in source code.

Examples include:

```text
DATABASE_URL
JWT_SECRET_KEY
GEMINI_API_KEY
```

Local/Docker environment configuration is kept outside the Git repository.

`.env` and `.env.*` files are excluded using `.gitignore` and `.dockerignore`.

Secrets should be provided through secure environment variables or a secrets-management system in production.

---

# 11. Testing

Pytest is used for automated testing.

Run tests locally:

```bash
pytest
```

Example:

```text
1 passed
```

The test suite is also executed through GitHub Actions.

---

# 12. CI/CD

GitHub Actions is configured to automatically run the project checks.

Example pipeline:

```text
Git Push
   |
   v
GitHub Actions
   |
   +----> Install Dependencies
   |
   +----> Start PostgreSQL
   |
   +----> Run Pytest
   |
   +----> Build Docker Image
   |
   +----> Push Docker Image
```

This helps ensure that code changes are tested before the Docker image is published.

---

# 13. Project Structure

```text
FDE_Preparation/
│
├── database/
│   ├── base.py
│   ├── connection.py
│   └── init_db.py
│
├── models/
│   ├── customer.py
│   ├── user.py
│   ├── invitation.py
│   └── ai_analysis.py
│
├── routers/
│   ├── customer.py
│   ├── user.py
│   ├── invitation.py
│   ├── activation.py
│   ├── approval.py
│   ├── rejection.py
│   └── ai_router.py
│
├── schemas/
│   └── ai_schema.py
│
├── services/
│   └── ai_service.py
│
├── tests/
│   └── test_health.py
│
├── nginx/
│   └── nginx.conf
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── main.py
├── .dockerignore
├── .gitignore
└── README.md
```

---

# Running the Application Locally

## 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd FDE_Preparation
```

## 2. Create and activate virtual environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Create the required environment configuration locally.

Example:

```text
DATABASE_URL=<your-database-url>
JWT_SECRET_KEY=<your-jwt-secret>
GEMINI_API_KEY=<your-gemini-api-key>
```

Do not commit these values to GitHub.

## 5. Run the application

```bash
uvicorn main:app --reload
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

# Running with Docker Compose

Make sure the required Docker environment configuration is available.

Then:

```bash
docker compose up -d
```

Check running containers:

```bash
docker compose ps
```

Application:

```text
http://localhost
```

Swagger:

```text
http://localhost/docs
```

Stop the application:

```bash
docker compose down
```

---

# Troubleshooting Approach

For production or deployment issues, the troubleshooting approach is:

```text
Identify the failing API
        |
        v
Check application logs
        |
        v
Check database connectivity
        |
        v
Check environment configuration
        |
        v
Check Docker image/version
        |
        v
Check external services
        |
        v
Fix and test
        |
        v
Deploy
        |
        v
Verify and monitor
```

The goal is to isolate whether the problem is caused by:

* Application code
* Database
* Configuration
* Docker/container
* Nginx
* External API
* Infrastructure

---
# Key User Flow

The overall application flow is:

```text
Customer Registration
        |
        v
Company Email / Domain Validation
        |
        v
Customer Pending
        |
        +----------------+
        |                |
        v                v
    Approved          Rejected
        |
        v
User Creation
        |
        v
Invitation Generated
        |
        v
User Activates Invitation
        |
        v
User Becomes Active
        |
        v
Login
        |
        v
JWT Authentication
        |
        v
Role-Based Authorization
        |
        v
Access Protected APIs
        |
        v
Security Assessment
        |
        v
Gemini AI Analysis
        |
        v
Risk Summary + Recommendations
        |
        v
PostgreSQL
```

---

# API Endpoints

The application exposes REST APIs for customer management, user management, authentication, invitations, approvals, and AI security analysis.

| Method | Endpoint                  | Purpose                            |
| ------ | ------------------------- | ---------------------------------- |
| POST   | `/customers/register`     | Register a customer/company        |
| POST   | `/users/register`         | Create a user                      |
| POST   | `/login`                  | Authenticate user and generate JWT |
| POST   | `/invitations`            | Create user invitation             |
| POST   | `/invitations/activate`   | Activate invitation                |
| POST   | `/customers/{id}/approve` | Approve customer                   |
| POST   | `/customers/{id}/reject`  | Reject customer                    |
| POST   | `/ai/analyze`             | Generate AI security analysis      |
| GET    | `/ai/analyses`            | Retrieve previous AI analyses      |

Swagger UI can be used to test and explore the APIs.

---

# Security

Security considerations implemented in the application include:

* JWT Bearer authentication
* Role-Based Access Control (RBAC)
* Password hashing
* Protected API endpoints
* Invitation token validation
* Invitation token expiration
* Company email/domain validation
* Environment-based secret configuration
* Separation of authentication and authorization

Authentication verifies the identity of the user, while authorization determines whether the authenticated user has permission to perform a particular operation.

Sensitive values such as database credentials, JWT secrets, and Gemini API keys are not stored in source code.

---

# AI Integration Flow

The AI security analysis feature follows this process:

```text
Client Request
      |
      v
FastAPI `/ai/analyze`
      |
      v
Validate Request using Pydantic
      |
      v
AI Service
      |
      v
Build Security Analysis Prompt
      |
      v
Gemini API
      |
      v
Structured JSON Response
      |
      v
Pydantic Response Validation
      |
      v
Store Analysis in PostgreSQL
      |
      v
Return Result to Client
```

The AI service is separated from the API router so that the application can maintain a clean separation between API handling and AI-related business logic.

The stored AI analysis includes:

* Company information
* Industry
* Number of employees
* Security concerns
* Risk summary
* Security recommendations
* Recommendation priority
* Analysis creation time

---

# Deployment Architecture

The application is designed to run as a multi-container application using Docker Compose.

```text
                    Client / Browser
                           |
                           v
                    +-------------+
                    |    Nginx    |
                    |     :80     |
                    +-------------+
                           |
                           v
                    +-------------+
                    |   FastAPI   |
                    |    :8000    |
                    +-------------+
                       /       \
                      /         \
                     v           v
              +-----------+   +-----------+
              | PostgreSQL|   | Gemini AI |
              |   :5432   |   |   API     |
              +-----------+   +-----------+
```

Docker Compose manages the application containers and their communication.

The PostgreSQL container provides persistent database storage through a Docker volume.

Nginx acts as the public entry point and forwards requests to the FastAPI container.

---

# Testing and CI/CD Flow

The project uses Pytest for automated testing and GitHub Actions for CI/CD.

```text
Developer
    |
    v
Git Push
    |
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    +----> Install Dependencies
    |
    +----> Start PostgreSQL
    |
    +----> Run Pytest
    |
    +----> Build Docker Image
    |
    +----> Push Docker Image
    |
    v
Docker Image
```

This provides an automated process for validating code changes and publishing the Docker image.

---

# Production Troubleshooting Scenarios

The project also focuses on practical production troubleshooting.

### API returns 401

Check:

```text
JWT token
    |
    v
Token presence
    |
    v
Token validity
    |
    v
Authentication
```

A `401 Unauthorized` response generally indicates that authentication is missing or invalid.

### API returns 403

Check:

```text
Authenticated User
        |
        v
User Role
        |
        v
Required Permission
```

A `403 Forbidden` response indicates that the user is authenticated but does not have the required permission.

### API returns 500

Check:

```text
API Status
    |
    v
Application Logs
    |
    v
Python / Import Errors
    |
    v
Database Connectivity
    |
    v
Environment Variables
    |
    v
Docker Container
    |
    v
External API
```

### API is slow

Possible areas to investigate:

* Application logs
* Database query performance
* Unnecessary database fields being retrieved
* Number of database queries
* External API response time
* Gemini API response time
* Nginx configuration
* Container resource usage

The goal is to identify the actual bottleneck before making changes.

---

# FDE Skills Demonstrated

This project demonstrates practical skills relevant to a Forward Deployed Engineer role:

* Client requirement analysis
* REST API development
* FastAPI backend development
* PostgreSQL database design
* SQLAlchemy ORM
* Authentication and JWT
* Role-Based Access Control
* API security
* User and customer workflows
* Third-party API integration
* Gemini AI / LLM integration
* Docker containerization
* Docker Compose
* Nginx reverse proxy
* Git and GitHub
* GitHub Actions CI/CD
* Automated testing with Pytest
* Production troubleshooting
* Performance troubleshooting
* Environment and secret management
* Deployment and operational thinking
* Debugging across application, database, container, and external services


# FDE Learning Goals

This project is designed to demonstrate practical FDE skills:

* Requirement analysis
* Backend API development
* Authentication and authorization
* Database design
* API integration
* AI/LLM integration
* Docker deployment
* Reverse proxy configuration
* CI/CD
* Troubleshooting
* Production-oriented thinking

---

## Author

**Sinthiya K**

Backend Developer | Python | FastAPI | PostgreSQL | Docker | API Development
