from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.rejection import RejectionRequest
from services.rejection import reject_customer
from services.security import require_role


router = APIRouter(
    prefix="/customers",
    tags=["Customer Rejection"]
)


@router.put("/{customer_id}/reject")
def reject(
    customer_id: int,
    request: RejectionRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("ADMIN"))
):
    return reject_customer(
        customer_id,
        request.rejection_reason,
        db
    )