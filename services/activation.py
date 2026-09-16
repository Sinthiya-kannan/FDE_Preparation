from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.user import User
from models.invitation import Invitation


def activate_user(
    token: str,
    db: Session
):
    # Find invitation
    invitation = (
        db.query(Invitation)
        .filter(Invitation.token == token)
        .first()
    )

    if not invitation:
        raise HTTPException(
            status_code=404,
            detail="Invalid invitation token"
        )

    # Already accepted
    if invitation.status == "ACCEPTED":
        raise HTTPException(
            status_code=400,
            detail="Invitation has already been accepted"
        )

    # Check expiry
    now = datetime.now(timezone.utc)

    expires_at = invitation.expires_at

    # PostgreSQL should return a timezone-aware datetime.
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at <= now:
        invitation.status = "EXPIRED"
        db.commit()

        raise HTTPException(
            status_code=400,
            detail="Invitation has expired"
        )

    # Find user
    user = (
        db.query(User)
        .filter(User.user_id == invitation.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Activate user
    user.status = "ACTIVE"

    # Accept invitation
    invitation.status = "ACCEPTED"
    invitation.accepted_at = now

    db.commit()

    return {
        "message": "User activated successfully",
        "user_id": user.user_id,
        "invitation_status": invitation.status,
        "user_status": user.status
    }