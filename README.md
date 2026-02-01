# Appointment Booking System — Backend

A production-grade backend for an appointment booking system built using FastAPI, designed with clean architecture, secure authentication, and extensibility in mind.

This project focuses on building strong backend foundations that can later support complex booking logic, real-time features, and intelligent scheduling.

---

## Features (Phase 1)

- User signup with secure password hashing (bcrypt)
- Login with JWT-based authentication
- JWT-protected routes using Bearer tokens
- Role-based user model (customer / provider / admin)
- Clean separation of concerns (routes, services, core, models, schemas)
- Health check endpoint for system monitoring

---

## Tech Stack

- FastAPI  
- PostgreSQL  
- SQLAlchemy ORM  
- Pydantic  
- JWT Authentication (python-jose)  
- Uvicorn  

---

## Authentication Flow

1. User signs up with name, email, and password  
2. Password is hashed using bcrypt before storing in the database  
3. User logs in using email and password  
4. On successful login, a JWT access token is issued  
5. Protected routes require the token to be sent via:  

   Authorization: Bearer <access_token>

6. The token is validated, decoded, and the authenticated user is injected into the request context  

---

## Project Structure

app/  
├── api/        # Route definitions  
├── core/       # Security and authentication logic  
├── db/         # Database session and setup  
├── models/     # SQLAlchemy models  
├── schemas/    # Pydantic schemas  
├── services/   # Business logic  
└── main.py     # Application entry point  

---

## Running Locally

### Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the server

```bash
uvicorn app.main:app --reload
```

### Open API documentation

http://127.0.0.1:8000/docs

---

## Health Check

Endpoint:

GET /health

Response:

```json
{
  "status": "ok"
}
```

---

## Roadmap

- Phase 2: Appointment booking and availability management  
- Phase 3: Reliability, security hardening, and deployment  
- Phase 4+: Real-time updates and intelligent scheduling  

---

## Notes

This project is developed incrementally in clearly defined phases to mirror real-world backend engineering workflows and production system design.
