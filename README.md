# Appointment Booking System — Production Backend (Level 1)

A production-ready backend for a role-aware appointment booking system built using FastAPI, PostgreSQL, and SQLAlchemy.

This project focuses on backend engineering fundamentals: authentication, secure API design, booking conflict resolution, availability calculation, rate limiting, WebSocket updates, and real-world production deployment.

Deployed in production using Render + Supabase (PostgreSQL).

---

## Overview

This system allows customers to book appointments with providers while ensuring:

- Secure JWT-based authentication
- Role-aware user model
- Conflict-free booking logic
- Dynamic availability calculation
- Rate-limited endpoints
- Real-time availability notifications via WebSockets
- Production deployment with environment configuration

This is not a basic CRUD app — it simulates real backend system design.

---

## Architecture

Clean separation of concerns:

app/
├── api/            # Route definitions  
├── core/           # Security, config, rate limiter, websocket manager  
├── db/             # Database session setup  
├── models/         # SQLAlchemy models  
├── schemas/        # Pydantic request/response schemas  
├── services/       # Business logic layer  
└── main.py         # Application entry point  

---

## Authentication System

### Features

- Secure password hashing (bcrypt via passlib)
- JWT token generation (python-jose)
- Token validation via dependency injection
- Protected routes using OAuth2PasswordBearer
- Role stored per user (customer / provider / admin)

### Flow

1. User signs up  
2. Password is hashed before storage  
3. User logs in with email + password  
4. JWT token is issued  
5. Token must be sent as:

Authorization: Bearer <access_token>

6. Token is decoded and user injected into request context  

---

## Appointment System (Core Logic)

### Booking Logic Includes:

- Time interval-based appointments
- Overlap detection (no double booking)
- Status lifecycle:
  - BOOKED
  - CANCELLED
  - COMPLETED
- Availability derived dynamically (not pre-generated slots)
- Slot validation based on provider configuration

### Conflict Prevention

Booking is rejected if:

- End time ≤ Start time
- Slot overlaps with existing BOOKED appointment
- Time outside provider availability window

---

## Real-Time Availability

WebSocket endpoint:

/appointments/ws/availability

When a booking is created:
- Connected clients receive "availability_updated"
- Clients can re-fetch updated slots

This simulates real-time system behavior.

---

## Rate Limiting

Implemented using SlowAPI.

Example:
10 requests per minute

Prevents abuse and simulates production-grade API control.

---

## Production Deployment

### Hosted On

- Render (Backend service)
- Supabase PostgreSQL (Managed database)

### Environment Variables Required

DATABASE_URL  
SECRET_KEY  
ENV=production  

All sensitive data is handled via environment configuration.

---

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Alembic (migrations)
- JWT (python-jose)
- Passlib (bcrypt)
- SlowAPI (rate limiting)
- WebSockets
- Render (deployment)
- Supabase (database)

---

## Verified Production Tests

- Signup works
- Login issues valid JWT
- /users/me protected via JWT
- Booking creates appointment
- Duplicate booking rejected
- Availability updates after booking
- Rate limiting returns 429
- WebSocket connection broadcasts update
- Production deployment stable

---

## Running Locally

### Create virtual environment

python -m venv venv  
venv\Scripts\activate   # Windows  
source venv/bin/activate  # macOS/Linux  

### Install dependencies

pip install -r requirements.txt  

### Run server

uvicorn app.main:app --reload  

### Open docs

http://127.0.0.1:8000/docs  

---

## Future Extensions

- Strict route-level role enforcement (RBAC)
- Appointment cancellation endpoint expansion
- Provider dashboard endpoints
- Redis-based distributed rate limiting
- Dockerization
- Horizontal scaling
- ML-driven smart slot ranking (Level 2 project)

---

## Project Status

Level 1 — Completed and Production Deployed

This project establishes strong backend engineering fundamentals and serves as the foundation for more advanced real-time and ML-driven systems in future project levels.

---

## Author

Backend-focused system built as part of a structured multi-level engineering project ladder.