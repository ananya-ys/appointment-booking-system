from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings
# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # logs SQL (good for learning)
)
# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
# Base class for all SQLAlchemy models
Base = declarative_base()
from sqlalchemy.orm import Session
from typing import Generator
# Dependency for getting DB session in FastAPI routes
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
