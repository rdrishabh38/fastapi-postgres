from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    phone_number: str


class UserResponse(BaseModel):
    user_id: int
    email: EmailStr
    name: str
    phone_number: str

    class Config:
        from_attributes = True
