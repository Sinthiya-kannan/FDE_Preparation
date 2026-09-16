from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.user import UserRegistration, LoginRequest
from services.user import register_user, get_user
from services.auth import login_user
from services.security import require_same_customer


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/register")
def register(
    user: UserRegistration,
    db: Session = Depends(get_db)
):
    return register_user(user, db)


@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    return login_user(
        request.email,
        request.password,
        db
    )


@router.get("/{user_id}")
def get_user_details(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_user(user_id, db)


@router.put("/{user_id}/manage")
def manage_user(
    user_id: int,
    current_user: dict = Depends(require_same_customer)
):
    return {
        "message": "User management authorized",
        "current_user_id": current_user["current_user_id"],
        "target_user_id": current_user["target_user_id"],
        "customer_id": current_user["customer_id"]
    }