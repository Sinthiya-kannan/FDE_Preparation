from pydantic import BaseModel


class RejectionRequest(BaseModel):
    rejection_reason: str