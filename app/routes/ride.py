from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.service.ride import book_ride
from app.schemas.ride import RideCreate, RideResponse

router = APIRouter()

@router.post("/book", response_model=RideResponse)
async def book_ride_endpoint(ride_data: RideCreate, db: AsyncSession = Depends(get_db)):
    return await book_ride(ride_data, db)
