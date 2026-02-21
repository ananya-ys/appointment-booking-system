from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, date
from fastapi import Request
from app.db.session import get_db
from app.schemas.appointment import AppointmentCreate, AppointmentOut
from app.services.appt_service import create_appointment
from app.core.security import get_current_user
from app.models.appointment import Appointment, AppointmentStatus
from app.services.availability_service import get_available_slots
from app.core.security import get_current_user
from app.models.user import User
from app.core.limiter import limiter

router = APIRouter(prefix="/appointments", tags=["appointments"])
@router.post("", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
def book_appointment(
    request: Request,
    appointment_data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_appointment(
            db=db,
            customer_id=current_user.id,
            provider_id=appointment_data.provider_id,
            start_time=appointment_data.start_time,
            end_time=appointment_data.end_time,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
@router.get("/availability")
def get_availability(
    provider_id: int,
    day: date,
    db: Session = Depends(get_db)
):
    slots = get_available_slots(
        db=db,
        provider_id=provider_id,
        day=day
    )

    return [
        {"start": start, "end": end}
        for start, end in slots
    ]