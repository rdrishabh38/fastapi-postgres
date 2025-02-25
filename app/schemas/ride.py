from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RideCreate(BaseModel):
    user_id: int
    pickup_location: str  # e.g., "POINT(-73.935242 40.730610)"
    dropoff_location: str # e.g., "POINT(-73.985428 40.748817)"
    # Distance and fare will be calculated server-side

class RideResponse(BaseModel):
    ride_id: int
    user_id: int
    driver_id: int
    pickup_location: str
    dropoff_location: str
    status: str
    fare: float
    distance: float
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
