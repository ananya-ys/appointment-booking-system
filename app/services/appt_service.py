from sqlalchemy.orm import Session
from datetime import timedelta
from app.models.appointment import Appointment, AppointmentStatus
from app.models.availability import Availability
import logging

logger = logging.getLogger(__name__)


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

    # Validate time order
    if end_time <= start_time:
        raise ValueError("End time must be after start time")

    # Check overlap
    if has_overlapping_appointment(
        db=db,
        provider_id=provider_id,
        start_time=start_time,
        end_time=end_time
    ):
        logger.warning(
            f"Overlap detected for provider_id={provider_id}, "
            f"start={start_time}, end={end_time}"
        )
        raise ValueError("Time slot already booked")

    # Create appointment
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

    logger.info(
        f"Appointment created: customer_id={customer_id}, "
        f"provider_id={provider_id}, start={start_time}, end={end_time}"
    )

    return appointment