from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.customer import CustomerRegistration, CustomerUpdate
from services.customer import delete_customer, get_all_customers, register_customer, get_customer, update_customer


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post("/register")
def register(
    customer: CustomerRegistration,
    db: Session = Depends(get_db)
):
    return register_customer(customer, db)


@router.get("/{customer_id}")
def get_customer_details(
    customer_id: int,
    db: Session = Depends(get_db)
):
    return get_customer(customer_id, db)

@router.get("/")
def get_all(
    db: Session = Depends(get_db)
):
    return get_all_customers(db)

@router.put("/{customer_id}")
def update(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db)
):
    return update_customer(
        customer_id,
        customer_data,
        db
    )

@router.delete("/{customer_id}")
def delete(
    customer_id: int,
    db: Session = Depends(get_db)
):
    return delete_customer(
        customer_id,
        db
    )