from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.service.driver import register_driver as register_driver_service
from app.schemas.driver import DriverCreate, DriverResponse
from app.service.driver import get_driver_by_email, get_driver_by_phone
from loguru import logger

router = APIRouter()

@router.post("/register", response_model=DriverResponse)
async def register_driver(driver_data: DriverCreate, db: AsyncSession = Depends(get_db)):
    return await register_driver_service(driver_data, db)

@router.get("/by-email", response_model=DriverResponse)
async def get_driver_by_email_endpoint(email: str = Query(...), db: AsyncSession = Depends(get_db)):
    return await get_driver_by_email(email, db)

@router.get("/by-phone", response_model=DriverResponse)
async def get_driver_by_phone_endpoint(phone_number: str = Query(...), db: AsyncSession = Depends(get_db)):
    return await get_driver_by_phone(phone_number, db)
