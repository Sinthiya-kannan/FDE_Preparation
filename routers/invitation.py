from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from services.invitation import create_invitation


router = APIRouter(
    prefix="/invitations",
    tags=["Invitations"]
)


@router.post("/create")
def create(
    user_id: int,
    db: Session = Depends(get_db)
):
    return create_invitation(user_id, db)