from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.user import User
from models.invitation import Invitation


def create_invitation(
    user_id: int,
    db: Session
):
    # Find user
    user = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # User should be active only after invitation acceptance,
    # so prevent unnecessary duplicate active invitations.
    if user.status == "ACTIVE":
        raise HTTPException(
            status_code=400,
            detail="User is already active"
        )

    # Check for an existing active SENT invitation
    existing_invitation = (
        db.query(Invitation)
        .filter(
            Invitation.user_id == user_id,
            Invitation.status == "SENT"
        )
        .first()
    )

    if existing_invitation:
        raise HTTPException(
            status_code=400,
            detail="An active invitation already exists for this user"
        )

    token = str(uuid4())

    sent_at = datetime.now(timezone.utc)
    expires_at = sent_at + timedelta(days=7)

    invitation = Invitation(
        user_id=user.user_id,
        token=token,
        status="SENT",
        sent_at=sent_at,
        expires_at=expires_at
    )

    db.add(invitation)
    db.commit()
    db.refresh(invitation)

    activation_url = (
        f"http://127.0.0.1:8000/activate?token={token}"
    )

    return {
        "message": "Invitation created successfully",
        "invitation_id": invitation.invitation_id,
        "user_id": user.user_id,
        "email": user.email,
        "status": invitation.status,
        "expires_at": invitation.expires_at,
        "activation_url": activation_url
    }