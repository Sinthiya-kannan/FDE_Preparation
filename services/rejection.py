from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.customer import Customer


def reject_customer(
    customer_id: int,
    rejection_reason: str,
    db: Session
):
    customer = (
        db.query(Customer)
        .filter(Customer.customer_id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if customer.status == "REJECTED":
        raise HTTPException(
            status_code=400,
            detail="Customer is already rejected"
        )

    if customer.status == "APPROVED":
        raise HTTPException(
            status_code=400,
            detail="Approved customer cannot be rejected"
        )
    if customer.status == "INACTIVE":
        raise HTTPException(
            status_code=400,
            detail="Inactive customer cannot be rejected"
        )

    customer.status = "REJECTED"
    customer.rejection_reason = rejection_reason

    db.commit()
    db.refresh(customer)

    return {
        "message": "Customer rejected successfully",
        "customer_id": customer.customer_id,
        "customer_name": customer.customer_name,
        "status": customer.status,
        "rejection_reason": customer.rejection_reason
    }