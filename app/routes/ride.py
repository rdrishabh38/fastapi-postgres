from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.service.ride import book_ride, complete_ride
from app.schemas.ride import RideCreate, RideResponse

router = APIRouter()

@router.post("/book", response_model=RideResponse)
async def book_ride_endpoint(ride_data: RideCreate, db: AsyncSession = Depends(get_db)):
    return await book_ride(ride_data, db)

@router.post("/{ride_id}/complete", response_model=RideResponse)
async def complete_ride_endpoint(ride_id: int, db: AsyncSession = Depends(get_db)):
    return await complete_ride(ride_id, db)
