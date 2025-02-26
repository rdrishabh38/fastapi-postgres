from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db
from app.middleware_logger import RequestIDMiddleware
from loguru import logger
import app.logging_config  # This will run the logger configuration
import starlette.requests

from routes.user import router as user_router
from routes.driver import router as driver_router
from routes.car import router as car_router
from routes.ride import router as ride_router


app = FastAPI()

# Add the middleware to capture request IDs and other context
app.add_middleware(RequestIDMiddleware)

# Database configuration
DATABASE_URL = "postgresql://user:password@postgres_db:5432/mydb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Test endpoint

# Example of using the bound logger from middleware, if available
# Otherwise, fallback to global logger
# In an actual endpoint, you could use: request.state.logger.info(...)
# For now, we use the global logger.
@app.get("/health", tags=["health"])
async def health_check(db: AsyncSession = Depends(get_db)):
    logger.info("Health check endpoint called")
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
app.include_router(ride_router, prefix="/rides", tags=["Rides"])
