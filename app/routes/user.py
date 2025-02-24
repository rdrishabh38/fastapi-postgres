from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.user import UserCreate, UserResponse
from service.user import register_user as register_user_service

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user_route(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Delegate the business logic to the service layer
    return await register_user_service(user_data, db)
