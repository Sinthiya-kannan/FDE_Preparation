from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.customer import Customer


def approve_customer(
    customer_id: int,
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

    if customer.status == "APPROVED":
        raise HTTPException(
            status_code=400,
            detail="Customer is already approved"
        )

    if customer.status == "REJECTED":
        raise HTTPException(
            status_code=400,
            detail="Rejected customer cannot be approved"
        )

    customer.status = "APPROVED"
    customer.rejection_reason = None

    db.commit()
    db.refresh(customer)

    return {
        "message": "Customer approved successfully",
        "customer_id": customer.customer_id,
        "customer_name": customer.customer_name,
        "status": customer.status
    }