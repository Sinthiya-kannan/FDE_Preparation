from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from services.approval import approve_customer
from services.security import require_role


router = APIRouter(
    prefix="/customers",
    tags=["Customer Approval"]
)


@router.put("/{customer_id}/approve")
def approve(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("ADMIN"))
):
    return approve_customer(customer_id, db)