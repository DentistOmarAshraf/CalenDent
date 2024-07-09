#!/usr/bin/python3
"""
Reservation Class
"""

from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Time, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class Reservation(BaseModel, Base):
    """reservation module"""

    __tablename__ = "reservation"

    if getenv("CALEN_STORAGE_TYPE") == "db":
        phone = Column(String(60), nullable=False)
        appointment = Column(Time, nullable=False)
        confirmed = Column(Boolean, default=False)
        clinic_id = Column(String(60), ForeignKey("clinic.id"))
        user_id = Column(String(60), ForeignKey("user.id"))
        clinic = relationship("Clinic", back_populates="reservations")
        user = relationship("User", back_populates="reservations")

    if getenv("CALEN_STORAGE_TYPE") != "db":
        appointment = ""
        status = ""
