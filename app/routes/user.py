from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.user import UserCreate, UserResponse
from service.user import register_user
from service.user import get_user_by_email, get_user_by_phone
from loguru import logger

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user_route(request: Request, user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Bind additional context (e.g., user email) to the logger
    request_logger = request.state.logger.bind(email=user_data.email, phone_number=user_data.phone_number)
    request_logger.info("Registering new user")
    # Delegate the business logic to the service layer
    new_user =  await register_user(user_data, db)
    request_logger.info("User registered", user_id=new_user.user_id, email=new_user.email,
                        phone_number=new_user.phone_number)
    return new_user

@router.get("/by-email", response_model=UserResponse)
async def get_user_by_email_endpoint(request: Request, email: str = Query(...), db: AsyncSession = Depends(get_db)):
    request_logger = request.state.logger.bind(email=email)
    user_by_email = await get_user_by_email(email, db)
    request_logger.info("User Fetched", email=user_by_email.email)
    return user_by_email

@router.get("/by-phone", response_model=UserResponse)
async def get_user_by_phone_endpoint(request: Request, phone_number: str = Query(...), db: AsyncSession = Depends(get_db)):
    request_logger = request.state.logger.bind(phone_number=phone_number)
    user_by_phone_number = await get_user_by_phone(phone_number, db)
    request_logger.info("User Fetched", phone_number=user_by_phone_number.phone_number)
    return user_by_phone_number
