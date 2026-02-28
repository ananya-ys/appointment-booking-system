from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from sqlalchemy.orm import Session
from datetime import date
import json

from app.db.session import get_db
from app.schemas.appointment import AppointmentCreate
from app.services.appt_service import create_appointment
from app.services.availability_service import get_available_slots
from app.core.security import get_current_user
from app.models.user import User
from app.core.limiter import limiter
from app.core.websocket import manager  # ← IMPORTANT: filename must match

router = APIRouter(prefix="/appointments", tags=["appointments"])



@router.post("", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def book_appointment(
    request: Request,
    appointment_data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        appointment = create_appointment(
            db=db,
            customer_id=current_user.id,
            provider_id=appointment_data.provider_id,
            start_time=appointment_data.start_time,
            end_time=appointment_data.end_time,
        )

        
        await manager.broadcast(
            json.dumps(
                {
                    "event": "appointment_booked",
                    "provider_id": appointment.provider_id,
                    "start_time": str(appointment.start_time),
                    "end_time": str(appointment.end_time),
                }
            )
        )

        return appointment

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )



@router.get("/availability")
def get_availability(
    provider_id: int,
    day: date,
    db: Session = Depends(get_db),
):
    slots = get_available_slots(
        db=db,
        provider_id=provider_id,
        day=day,
    )

    return [
        {"start": start, "end": end}
        for start, end in slots
    ]



@router.websocket("/ws/availability")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)