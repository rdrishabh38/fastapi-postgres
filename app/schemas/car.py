from pydantic import BaseModel
from datetime import datetime

class CarCreate(BaseModel):
    driver_id: int
    make: str
    model: str
    year: int
    license_plate: str
    color: str

class CarResponse(BaseModel):
    car_id: int
    driver_id: int
    make: str
    model: str
    year: int
    license_plate: str
    color: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
