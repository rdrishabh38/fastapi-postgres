from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db


from routes.user import router as user_router
from routes.driver import router as driver_router
from routes.car import router as car_router
from routes.ride import router as ride_router


app = FastAPI()

# Database configuration
DATABASE_URL = "postgresql://user:password@postgres_db:5432/mydb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Test endpoint
@app.get("/health", tags=["health"])
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        if result.scalar() != 1:
            raise HTTPException(status_code=500, detail="Database check failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
    return {"status": "ok"}

# Include user registration routes
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(driver_router, prefix="/drivers", tags=["Drivers"])
app.include_router(car_router, prefix="/cars", tags=["Cars"])
app.include_router(prefix="/rides", tags=["Rides"])
