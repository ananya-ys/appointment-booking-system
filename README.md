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

## Features (Phase 2 – Core Appointment Booking)

Phase 2 implements the core business logic of the appointment booking system and is fully verified end-to-end.

### Key Capabilities

- Appointment booking between customers and providers
- Time-interval based appointments (start_time / end_time)
- Overlap prevention to avoid double booking
- Appointment lifecycle management:
  - booked
  - cancelled
  - completed
- Derived availability calculation (no pre-created slots)
- Secure, JWT-protected appointment APIs
- Clean service-layer business logic
- Swagger-verified workflows

### Core Appointment Endpoints

- POST /appointments – Book an appointment
- POST /appointments/{id}/cancel – Cancel an appointment
- GET /appointments/availability – Fetch provider availability for a given date

### Verification

- Booking removes the slot from availability
- Cancelling an appointment restores availability
- Overlapping bookings are rejected
- All flows tested and verified via Swagger UI

### Status

✅ Phase 2 completed and verified

---

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Pydantic
- JWT Authentication (python-jose)
- Alembic (database migrations)
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
├── api/
│   ├── appt.py        # Appointment routes
│   └── users.py       # User & auth routes
├── core/
│   ├── config.py
│   └── security.py    # JWT auth & role checks
├── db/
│   └── session.py
├── models/
│   ├── user.py
│   └── appointment.py
├── schemas/
│   └── ...
├── services/
│   ├── appointments.py
│   └── availability_service.py
├── main.py

---

## Running Locally

### Create and activate virtual environment

python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

### Install dependencies

pip install -r requirements.txt

### Start the server

uvicorn app.main:app --reload

### Open API documentation

http://127.0.0.1:8000/docs

---

## Health Check

Endpoint:

GET /health

Response:

{
  "status": "ok"
}

---

## Roadmap

- Phase 3: Reliability, security hardening, and cloud deployment
- WOW Features:
  - Real-time availability updates
  - Smart slot ranking (rule-based → ML-driven)
- Level 2: Intelligent scheduling and ML-powered optimization engine

---

## Notes

This project is developed incrementally in clearly defined phases to mirror real-world backend engineering workflows and production system design.