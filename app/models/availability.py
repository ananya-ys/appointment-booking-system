from sqlalchemy import Column, Integer, Boolean, ForeignKey, Time
from sqlalchemy.orm import relationship

from app.db.session import Base
class Availability(Base):
    __tablename__ = "availabilities"

    id = Column(Integer, primary_key=True, index=True)

    provider_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    slot_duration_minutes = Column(Integer, nullable=False)

    is_active = Column(Boolean, nullable=False, default=True)

    provider = relationship(
        "User",
        foreign_keys=[provider_id]
    )
