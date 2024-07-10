#!/usr/bin/python3
"""
Reservation Class
"""

from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Time, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
import enum


class Status(enum.Enum):
    """User reservation status"""
    CONFIRMED = "confirmed"
    DECLINED = "declined"
    WAITING = "waiting"


class Reservation(BaseModel, Base):
    """reservation module"""

    __tablename__ = "reservation"

    if getenv("CALEN_STORAGE_TYPE") == "db":
        phone = Column(String(60), nullable=False)
        appointment = Column(Time, nullable=False)
        status = Column(Enum(Status), nullable=False)
        clinic_id = Column(String(60), ForeignKey("clinic.id"))
        user_id = Column(String(60), ForeignKey("user.id"))
        clinic = relationship("Clinic", back_populates="reservations")
        user = relationship("User", back_populates="reservations")

    if getenv("CALEN_STORAGE_TYPE") != "db":
        appointment = ""
        status = ""
