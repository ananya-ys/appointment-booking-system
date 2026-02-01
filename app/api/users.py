from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.services.user_service import create_user
from app.db.session import get_db
from app.schemas.user import UserLogin
from app.core.security import verify_password, create_access_token, get_current_user
from app.models.user import User
from fastapi import HTTPException

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def signup(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(db, user_in)

@router.post("/login")
def login(
    user_in: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == user_in.email).first()

    if not user or not verify_password(user_in.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me")
def read_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role       
    }
