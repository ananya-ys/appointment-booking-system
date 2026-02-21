from fastapi import FastAPI
from app.core.config import settings
from app.api.appt import router as appointments_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse
from app.core.limiter import limiter

app = FastAPI(title="Appointment Booking System")

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Slow down."},
    )
if settings.ENV == "development":
    origins = ["*"]  # allow everything locally
else:
    origins = ["https://your-frontend-domain.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "environment": settings.ENV
    }
from app.api.users import router as users_router

app.include_router(users_router)
app.include_router(appointments_router)
