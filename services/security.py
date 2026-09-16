from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from database.connection import get_db
from models.user import User
from services.auth import SECRET_KEY, ALGORITHM


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")
        email = payload.get("email")

        if not user_id or not email:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return {
            "user_id": int(user_id),
            "email": email
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


def require_role(required_role: str):

    def role_checker(
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        user = (
            db.query(User)
            .filter(User.user_id == current_user["user_id"])
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        if user.role != required_role:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to perform this action"
            )

        return current_user

    return role_checker


def require_same_customer(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user_db = (
        db.query(User)
        .filter(User.user_id == current_user["user_id"])
        .first()
    )

    target_user = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )

    if not current_user_db:
        raise HTTPException(
            status_code=404,
            detail="Current user not found"
        )

    if not target_user:
        raise HTTPException(
            status_code=404,
            detail="Target user not found"
        )

    if current_user_db.role != "PRIMARY_USER":
        raise HTTPException(
            status_code=403,
            detail="Only PRIMARY_USER can perform this action"
        )

    if current_user_db.customer_id != target_user.customer_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot manage users from another customer"
        )

    return {
        "current_user_id": current_user_db.user_id,
        "target_user_id": target_user.user_id,
        "customer_id": current_user_db.customer_id
    }