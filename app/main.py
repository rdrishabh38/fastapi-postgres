from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from routes.user import router as user_router

app = FastAPI()

# Database configuration
DATABASE_URL = "postgresql://user:password@postgres_db:5432/mydb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Test endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Include user registration routes
app.include_router(user_router, prefix="/users", tags=["Users"])