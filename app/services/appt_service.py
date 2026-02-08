from sqlalchemy.orm import Session
from datetime import timedelta

from app.models.appointment import Appointment,AppointmentStatus
from app.models.availability import Availability
def create_appointment(
    db: Session,
    customer_id: int,
    provider_id: int,
    start_time,
    end_time,
):
    # 1. Fetch active availability
    availability = (
        db.query(Availability)
        .filter(
            Availability.provider_id == provider_id,
            Availability.is_active == True,
        )
        .first()
    )

    if not availability:
        raise ValueError("Provider is not available")
    # 2. Check slot duration
    duration = end_time - start_time
    if duration != timedelta(minutes=availability.slot_duration_minutes):
        raise ValueError("Invalid slot duration")
    # 3. Check availability window
    if not (
        availability.start_time <= start_time.time()
        and end_time.time() <= availability.end_time
    ):
        raise ValueError("Time outside availability window")
    # 4. Conflict check
    conflict = (
        db.query(Appointment)
        .filter(
            Appointment.provider_id == provider_id,
            Appointment.start_time < end_time,
            Appointment.end_time > start_time,
        )
        .first()
    )

    if conflict:
        raise ValueError("Slot already booked")
    # 5. Create appointment
    appointment = Appointment(
        customer_id=customer_id,
        provider_id=provider_id,
        start_time=start_time,
        end_time=end_time,
        status="booked",
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment

def has_overlapping_appointment(
    db: Session,
    provider_id: int,
    start_time,
    end_time
) -> bool:
    """
    Returns True if the provider already has a BOOKED
    appointment overlapping the given time range.
    """

    conflict = (
        db.query(Appointment)
        .filter(
            Appointment.provider_id == provider_id,
            Appointment.status == AppointmentStatus.BOOKED,
            Appointment.start_time < end_time,
            Appointment.end_time > start_time
        )
        .first()
    )

    return conflict is not None

def create_appointment(
    db: Session,
    customer_id: int,
    provider_id: int,
    start_time,
    end_time
) -> Appointment:
    """
    Creates an appointment only if the time slot is valid
    and no overlap exists.
    """

    if end_time <= start_time:
        raise ValueError("End time must be after start time")

    if has_overlapping_appointment(
        db=db,
        provider_id=provider_id,
        start_time=start_time,
        end_time=end_time
    ):
        raise ValueError("Time slot already booked")

    appointment = Appointment(
        customer_id=customer_id,
        provider_id=provider_id,
        start_time=start_time,
        end_time=end_time,
        status=AppointmentStatus.BOOKED
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment