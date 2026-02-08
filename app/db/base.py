from app.db.session import Base

# Import all models so Alembic can detect them
from app.models.user import User
from app.models.appointment import Appointment
from app.models.availability import Availability
