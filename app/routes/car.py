from typing import List
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.service.car import register_car, get_car_by_id, get_car_by_license, get_cars_by_driver
from app.schemas.car import CarCreate, CarResponse
from loguru import logger

router = APIRouter()

@router.post("/register", response_model=CarResponse)
async def register_car_endpoint(request: Request, car_data: CarCreate, db: AsyncSession = Depends(get_db)):
    return await register_car(car_data, db)

@router.get("/{car_id}", response_model=CarResponse)
async def get_car_by_id_endpoint(request: Request, car_id: int, db: AsyncSession = Depends(get_db)):
    return await get_car_by_id(car_id, db)

@router.get("/by-license/{license_plate}", response_model=CarResponse)
async def get_car_by_license_endpoint(request: Request, license_plate: str, db: AsyncSession = Depends(get_db)):
    return await get_car_by_license(license_plate, db)

@router.get("/by-driver/{driver_id}", response_model=List[CarResponse])
async def get_cars_by_driver_endpoint(request: Request, driver_id: int, db: AsyncSession = Depends(get_db)):
    return await get_cars_by_driver(driver_id, db)