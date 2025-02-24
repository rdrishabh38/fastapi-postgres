from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.user import UserCreate, UserResponse
from service.user import register_user
from service.user import get_user_by_email, get_user_by_phone

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user_route(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Delegate the business logic to the service layer
    return await register_user(user_data, db)

@router.get("/by-email", response_model=UserResponse)
async def get_user_by_email_endpoint(email: str = Query(...), db: AsyncSession = Depends(get_db)):
    return await get_user_by_email(email, db)

@router.get("/by-phone", response_model=UserResponse)
async def get_user_by_phone_endpoint(phone_number: str = Query(...), db: AsyncSession = Depends(get_db)):
    return await get_user_by_phone(phone_number, db)
