from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.service.car import register_car, get_car_by_id, get_car_by_license, get_cars_by_driver
from app.schemas.car import CarCreate, CarResponse

router = APIRouter()

@router.post("/cars/register", response_model=CarResponse)
async def register_car_endpoint(car_data: CarCreate, db: AsyncSession = Depends(get_db)):
    return await register_car(car_data, db)

@router.get("/cars/{car_id}", response_model=CarResponse)
async def get_car_by_id_endpoint(car_id: int, db: AsyncSession = Depends(get_db)):
    return await get_car_by_id(car_id, db)

@router.get("/cars/by-license", response_model=CarResponse)
async def get_car_by_license_endpoint(license_plate: str = Query(...), db: AsyncSession = Depends(get_db)):
    return await get_car_by_license(license_plate, db)

@router.get("/cars/by-driver/{driver_id}", response_model=List[CarResponse])
async def get_cars_by_driver_endpoint(driver_id: int, db: AsyncSession = Depends(get_db)):
    return await get_cars_by_driver(driver_id, db)