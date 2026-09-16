from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from database.base import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    domain = Column(String, nullable=False, unique=True)
    website = Column(String, nullable=True)
    status = Column(String, nullable=False, default="PENDING")
    rejection_reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)