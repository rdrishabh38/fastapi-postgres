from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from passlib.context import CryptContext

from models.user import User
from schemas.user import UserCreate

# Setup for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def register_user(user_data: UserCreate, db: AsyncSession):
    # Check if email or phone number already exists
    result = await db.execute(
        select(User).where(
            (User.email == user_data.email) | (User.phone_number == user_data.phone_number)
        )
    )
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email or phone number already registered")

    # Create new user instance
    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        name=user_data.name,
        phone_number=user_data.phone_number
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user
