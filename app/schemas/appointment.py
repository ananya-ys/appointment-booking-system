from datetime import datetime
from pydantic import BaseModel
class AppointmentCreate(BaseModel):
    provider_id: int
    start_time: datetime
    end_time: datetime
class AppointmentOut(BaseModel):
    id: int
    provider_id: int
    customer_id: int
    start_time: datetime
    end_time: datetime
    status: str

    class Config:
        from_attributes = True
