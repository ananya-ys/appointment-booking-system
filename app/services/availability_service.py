from datetime import datetime
from typing import List, Tuple

from sqlalchemy.orm import Session

from app.models.appointment import Appointment
def filter_conflicting_slots(
    db: Session,
    provider_id: int,
    slots: List[Tuple[datetime, datetime]],
) -> List[Tuple[datetime, datetime]]:
    available_slots = []

    for slot_start, slot_end in slots:
        conflict_exists = (
            db.query(Appointment)
            .filter(
                Appointment.provider_id == provider_id,
                Appointment.start_time < slot_end,
                Appointment.end_time > slot_start,
            )
            .first()
            is not None
        )

        if not conflict_exists:
            available_slots.append((slot_start, slot_end))

    return available_slots

from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session

from app.models.appointment import Appointment, AppointmentStatus
from app.core.config import (
    WORK_START_TIME,
    WORK_END_TIME,
    SLOT_DURATION_MINUTES
)

def get_booked_appointments(
    db: Session,
    provider_id: int,
    day: date
):
    start_of_day = datetime.combine(day, WORK_START_TIME)
    end_of_day = datetime.combine(day, WORK_END_TIME)

    return (
        db.query(Appointment)
        .filter(
            Appointment.provider_id == provider_id,
            Appointment.status == AppointmentStatus.BOOKED,
            Appointment.start_time < end_of_day,
            Appointment.end_time > start_of_day
        )
        .order_by(Appointment.start_time)
        .all()
    )
def get_available_slots(
    db: Session,
    provider_id: int,
    day: date
):
    booked = get_booked_appointments(db, provider_id, day)

    work_start = datetime.combine(day, WORK_START_TIME)
    work_end = datetime.combine(day, WORK_END_TIME)

    slots = []
    current_time = work_start

    for appointment in booked:
        if current_time < appointment.start_time:
            slots.append(
                (current_time, appointment.start_time)
            )

        current_time = max(current_time, appointment.end_time)

    if current_time < work_end:
        slots.append((current_time, work_end))

    return split_into_fixed_slots(slots)

def split_into_fixed_slots(free_ranges):
    slots = []

    for start, end in free_ranges:
        current = start
        while current + timedelta(minutes=SLOT_DURATION_MINUTES) <= end:
            slot_end = current + timedelta(minutes=SLOT_DURATION_MINUTES)
            slots.append((current, slot_end))
            current = slot_end

    return slots