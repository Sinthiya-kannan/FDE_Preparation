from pydantic import BaseModel, EmailStr


class CustomerRegistration(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    website: str

class CustomerUpdate(BaseModel):
    customer_name: str
    website: str | None = None