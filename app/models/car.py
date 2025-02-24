from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base
from sqlalchemy.sql import func



class Car(Base):
    __tablename__ = "cars"
    __table_args__ = {'schema': 'ride_demo'}

    car_id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("ride_demo.drivers.driver_id"), nullable=False)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    license_plate = Column(String, unique=True, nullable=False)
    color = Column(String, nullable=False)
    # Using server_default for created_at: the database sets the current time on insertion.
    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )

    # Using server_default and onupdate for updated_at: the database sets the current time on insertion
    # and SQLAlchemy updates this value whenever the record is updated.
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    driver = relationship("Driver", back_populates="cars")
