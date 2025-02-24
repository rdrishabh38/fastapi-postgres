from sqlalchemy import Column, Integer, String, Boolean, Numeric, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base
from sqlalchemy.sql import func



class Driver(Base):
    __tablename__ = "drivers"
    __table_args__ = {'schema': 'ride_demo'}

    driver_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    driver_license = Column(String, unique=True, nullable=False)
    is_available = Column(Boolean, default=True)
    rating = Column(Numeric, nullable=True)
    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    rides = relationship("Ride", back_populates="driver")
    cars = relationship("Car", back_populates="driver", lazy="joined")
