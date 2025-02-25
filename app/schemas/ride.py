from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from geoalchemy2.shape import to_shape

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

    @validator("pickup_location", pre=True, always=True)
    def convert_pickup_location(cls, v):
        # If v is not a string, assume it's a geometry object and convert to WKT.
        if not isinstance(v, str):
            try:
                return to_shape(v).wkt
            except Exception as e:
                raise ValueError(f"Error converting pickup_location to WKT: {e}")
        return v

    @validator("dropoff_location", pre=True, always=True)
    def convert_dropoff_location(cls, v):
        # If v is not a string, assume it's a geometry object and convert to WKT.
        if not isinstance(v, str):
            try:
                return to_shape(v).wkt
            except Exception as e:
                raise ValueError(f"Error converting dropoff_location to WKT: {e}")
        return v

    class Config:
        orm_mode = True
