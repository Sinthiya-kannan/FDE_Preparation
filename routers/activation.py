from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from services.activation import activate_user


router = APIRouter(
    tags=["Activation"]
)


@router.get("/activate")
def activate(
    token: str,
    db: Session = Depends(get_db)
):
    return activate_user(token, db)