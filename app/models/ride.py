from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography
from datetime import datetime
from app.models.base import Base


class Ride(Base):
    __tablename__ = "rides"

    ride_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.driver_id"), nullable=False)
    pickup_location = Column(Geography(geometry_type="POINT", srid=4326), nullable=False)
    dropoff_location = Column(Geography(geometry_type="POINT", srid=4326), nullable=False)
    status = Column(String, nullable=False)
    fare = Column(Numeric, nullable=False)
    distance = Column(Numeric, nullable=False)
    started_at = Column(TIMESTAMP, nullable=True)
    completed_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="rides")
    driver = relationship("Driver", back_populates="rides")
