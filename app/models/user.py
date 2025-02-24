from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.models.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'ride_demo'}

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
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

    rides = relationship("Ride", back_populates="user")
