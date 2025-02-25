from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.service.driver import register_driver as register_driver_service
from app.schemas.driver import DriverCreate, DriverResponse

router = APIRouter()

@router.post("/drivers/register", response_model=DriverResponse)
async def register_driver(driver_data: DriverCreate, db: AsyncSession = Depends(get_db)):
    return await register_driver_service(driver_data, db)
