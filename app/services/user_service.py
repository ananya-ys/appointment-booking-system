from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password


def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Business logic to create a new user.
    """
    # 1. Hash the password
    hashed_password = hash_password(user_in.password)

    # 2. Create DB model
    user = User(
        name=user_in.name,
        email=user_in.email,
        password_hash=hashed_password,
    )

    # 3. Persist to database
    db.add(user)
    db.commit()
    db.refresh(user)

    return user
    