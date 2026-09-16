from pydantic import BaseModel, EmailStr, Field


class UserRegistration(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    customer_id: int
    password: str = Field(min_length=8, max_length=72)

class LoginRequest(BaseModel):
    email: EmailStr
    password:str = Field(min_length=8, max_length=72)