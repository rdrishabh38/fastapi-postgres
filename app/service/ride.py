import random
import math
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.ride import Ride
from app.models.driver import Driver
from app.schemas.ride import RideCreate


def parse_point(point_str: str):
    """
    Parse a WKT point string (e.g., "POINT(-73.935242 40.730610)")
    and return a tuple (lon, lat) as floats.
    """
    point_str = point_str.strip()
    if point_str.startswith("POINT(") and point_str.endswith(")"):
        coords_str = point_str[6:-1]  # Remove "POINT(" and ")"
        parts = coords_str.split()
        if len(parts) == 2:
            try:
                lon, lat = float(parts[0]), float(parts[1])
                return lon, lat
            except ValueError:
                pass
    raise ValueError("Invalid point format. Expected format: 'POINT(lon lat)'.")


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great-circle distance between two points on the Earth using the haversine formula.
    Returns the distance in kilometers.
    """
    R = 6371  # Earth radius in kilometers
    dlon = math.radians(lon2 - lon1)
    dlat = math.radians(lat2 - lat1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return R * c


async def get_available_driver(db: AsyncSession) -> Driver:
    result = await db.execute(select(Driver).where(Driver.is_available == True))
    driver = result.scalars().first()
    if not driver:
        raise HTTPException(status_code=404, detail="No available driver found")
    return driver


async def book_ride(ride_data: RideCreate, db: AsyncSession) -> Ride:
    # Select an available driver
    driver = await get_available_driver(db)

    # Optionally mark the driver as unavailable
    driver.is_available = False
    db.add(driver)

    # Calculate the distance based on pickup and dropoff locations
    try:
        lon1, lat1 = parse_point(ride_data.pickup_location)
        lon2, lat2 = parse_point(ride_data.dropoff_location)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    computed_distance = haversine(lon1, lat1, lon2, lat2)

    # Generate a random pricing multiplier between 1 and 5
    random_pricing = random.uniform(1, 5)
    computed_fare = computed_distance * random_pricing

    new_ride = Ride(
        user_id=ride_data.user_id,
        driver_id=driver.driver_id,
        pickup_location=ride_data.pickup_location,
        dropoff_location=ride_data.dropoff_location,
        fare=computed_fare,
        distance=computed_distance,
        status="booked"
    )
    db.add(new_ride)
    await db.commit()
    await db.refresh(new_ride)
    return new_ride
