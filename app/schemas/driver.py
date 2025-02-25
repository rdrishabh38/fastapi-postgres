from pydantic import BaseModel, EmailStr
from typing import Optional

class DriverCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    phone_number: str
    driver_license: str

class DriverResponse(BaseModel):
    driver_id: int
    email: EmailStr
    name: str
    phone_number: str
    driver_license: str
    is_available: bool
    rating: Optional[float] = None

    class Config:
        orm_mode = True
