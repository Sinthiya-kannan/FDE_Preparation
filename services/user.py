from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.user import User
from models.customer import Customer
from schemas.user import UserRegistration

from services.auth import hash_password


def register_user(
    user: UserRegistration,
    db: Session
):
    # Check whether customer exists
    customer = (
        db.query(Customer)
        .filter(Customer.customer_id == user.customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # Check duplicate email
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail=f"User with email {user.email} already exists"
        )

    password_hash = hash_password(user.password)

    new_user = User(
        customer_id=user.customer_id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        password_hash=password_hash,
        role="USER",
        status="PENDING"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registration successful",
        "user_id": new_user.user_id,
        "customer_id": new_user.customer_id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "status": new_user.status
    }


def get_user(
    user_id: int,
    db: Session
):
    user = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "user_id": user.user_id,
        "customer_id": user.customer_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": user.phone,
        "role": user.role,
        "status": user.status,
        "created_at": user.created_at
    }