from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base

# Define the database URL (Update with actual credentials)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/mydb"
# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create an async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# Dependency to get the async database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
