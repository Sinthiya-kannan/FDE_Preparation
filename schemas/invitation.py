from pydantic import BaseModel


class InvitationCreate(BaseModel):
    user_id: int