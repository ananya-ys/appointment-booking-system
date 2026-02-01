from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title="Appointment Booking System")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "environment": settings.ENV
    }
from app.api.users import router as users_router

app.include_router(users_router)
