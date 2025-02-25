from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.car import Car
from app.schemas.car import CarCreate

async def register_car(car_data: CarCreate, db: AsyncSession) -> Car:
    # Check if a car with the same license plate already exists
    result = await db.execute(select(Car).where(Car.license_plate == car_data.license_plate))
    existing_car = result.scalars().first()
    if existing_car:
        raise HTTPException(status_code=400, detail="Car with this license plate already exists")

    new_car = Car(
        driver_id=car_data.driver_id,
        make=car_data.make,
        model=car_data.model,
        year=car_data.year,
        license_plate=car_data.license_plate,
        color=car_data.color
    )
    db.add(new_car)
    await db.commit()
    await db.refresh(new_car)
    return new_car

async def get_car_by_id(car_id: int, db: AsyncSession) -> Car:
    result = await db.execute(select(Car).where(Car.car_id == car_id))
    car = result.scalars().first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

async def get_car_by_license(license_plate: str, db: AsyncSession) -> Car:
    result = await db.execute(select(Car).where(Car.license_plate == license_plate))
    car = result.scalars().first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

async def get_cars_by_driver(driver_id: int, db: AsyncSession) -> List[Car]:
    result = await db.execute(select(Car).where(Car.driver_id == driver_id))
    cars = result.scalars().all()
    if not cars:
        raise HTTPException(status_code=404, detail="No cars found for this driver")
    return cars
