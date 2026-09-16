from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.customer import Customer
from models.user import User
from schemas.customer import CustomerRegistration, CustomerUpdate


def register_customer(
    customer: CustomerRegistration,
    db: Session
):
    # Check duplicate domain
    existing_customer = (
        db.query(Customer)
        .filter(Customer.domain == customer.domain)
        .first()
    )

    if existing_customer:
        raise HTTPException(
            status_code=400,
            detail=f"Customer with domain {customer.domain} already exists"
        )

    new_customer = Customer(
        customer_name=f"{customer.first_name} {customer.last_name}",
        domain=customer.domain,
        website=str(customer.website) if customer.website else None,
        status="PENDING"
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return {
        "message": "Customer registration successful",
        "customer_id": new_customer.customer_id,
        "customer_name": new_customer.customer_name,
        "domain": new_customer.domain,
        "website": new_customer.website,
        "status": new_customer.status
    }


def get_customer(
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

    return {
        "customer_id": customer.customer_id,
        "customer_name": customer.customer_name,
        "domain": customer.domain,
        "website": customer.website,
        "status": customer.status,
        "rejection_reason": customer.rejection_reason,
        "created_at": customer.created_at
    }

def get_all_customers(db: Session):
    customers = (
        db.query(Customer)
        .order_by(Customer.customer_id)
        .all()
    )

    return [
        {
            "customer_id": customer.customer_id,
            "customer_name": customer.customer_name,
            "domain": customer.domain,
            "website": customer.website,
            "status": customer.status,
            "rejection_reason": customer.rejection_reason,
            "created_at": customer.created_at
        }
        for customer in customers
    ]

def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
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

    customer.customer_name = customer_data.customer_name

    if customer_data.website is not None:
        customer.website = customer_data.website

    db.commit()
    db.refresh(customer)

    return {
        "message": "Customer updated successfully",
        "customer_id": customer.customer_id,
        "customer_name": customer.customer_name,
        "domain": customer.domain,
        "website": customer.website,
        "status": customer.status
    }

def delete_customer(
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

    if customer.status == "INACTIVE":
        raise HTTPException(
            status_code=400,
            detail="Customer is already inactive"
        )

    # Deactivate customer
    customer.status = "INACTIVE"

    # Deactivate all users belonging to this customer
    db.query(User).filter(
        User.customer_id == customer_id
    ).update(
        {"status": "INACTIVE"},
        synchronize_session=False
    )

    # Commit both changes together
    db.commit()
    db.refresh(customer)

    return {
        "message": "Customer deactivated successfully",
        "customer_id": customer.customer_id,
        "customer_name": customer.customer_name,
        "status": customer.status
    }