from sqlalchemy import Column, Integer, String, Boolean, Numeric, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base


class Driver(Base):
    __tablename__ = "drivers"

    driver_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    driver_license = Column(String, unique=True, nullable=False)
    is_available = Column(Boolean, default=True)
    rating = Column(Numeric, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    rides = relationship("Ride", back_populates="driver")
    cars = relationship("Car", back_populates="driver")
