from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from database.base import Base


class Invitation(Base):
    __tablename__ = "invitations"

    invitation_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )
    token = Column(String, nullable=False, unique=True)
    status = Column(String, nullable=False)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    accepted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)