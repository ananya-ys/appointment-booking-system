from datetime import datetime, date, time, timedelta
from typing import List, Tuple
def generate_slots(
    target_date: date,
    start_time: time,
    end_time: time,
    slot_duration_minutes: int,
) -> List[Tuple[datetime, datetime]]:
    slots = []

    current_start = datetime.combine(target_date, start_time)
    end_boundary = datetime.combine(target_date, end_time)

    slot_duration = timedelta(minutes=slot_duration_minutes)

    while current_start + slot_duration <= end_boundary:
        current_end = current_start + slot_duration
        slots.append((current_start, current_end))
        current_start = current_end

    return slots
