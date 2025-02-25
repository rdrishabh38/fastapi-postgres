from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.driver import Driver
from app.schemas.driver import DriverCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def register_driver(driver_data: DriverCreate, db: AsyncSession) -> Driver:
    # Check if a driver with the given email, phone number, or license exists
    result = await db.execute(
        select(Driver).where(
            (Driver.email == driver_data.email) |
            (Driver.phone_number == driver_data.phone_number) |
            (Driver.driver_license == driver_data.driver_license)
        )
    )
    existing_driver = result.scalars().first()
    if existing_driver:
        raise HTTPException(status_code=400, detail="Driver with given details already exists")

    # Create a new driver record
    new_driver = Driver(
        email=driver_data.email,
        hashed_password=hash_password(driver_data.password),
        name=driver_data.name,
        phone_number=driver_data.phone_number,
        driver_license=driver_data.driver_license
    )

    db.add(new_driver)
    await db.commit()
    await db.refresh(new_driver)
    return new_driver
