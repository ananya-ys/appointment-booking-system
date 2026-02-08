from fastapi import FastAPI
from app.core.config import settings
from app.api.appt import router as appointments_router

app = FastAPI(title="Appointment Booking System")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "environment": settings.ENV
    }
from app.api.users import router as users_router

app.include_router(users_router)
app.include_router(appointments_router)
