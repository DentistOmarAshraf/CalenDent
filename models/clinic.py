#!/usr/bin/python3
"""
Clinic Model
"""

from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Time, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import time


class Clinic(BaseModel, Base):
    """Clinic Module"""
    __tablename__ = "clinic"

    if getenv("CALEN_STORAGE_TYPE") == "db":
        name = Column(String(60), nullable=False)
        opening_time = Column(Time, default=time(17, 0))
        closing_time = Column(Time, default=time(22, 0))
        visit_price = Column(Float, default=200.00)
        user_id = Column(String(60), ForeignKey("user.id"))
        address_id = Column(String(60), ForeignKey("address.id"))
        user = relationship("User", back_populates="clinics")
        address = relationship("Address", back_populates="clinics")
        services = relationship("Service", secondary="clinic_service",
                                back_populates="clinics")
        reservations = relationship("Reservation", back_populates="clinic",
                                    cascade="all, delete")
        reviews = relationship("Review", back_populates="clinic",
                               cascade="all, delete")

    if getenv("CALEN_STORAGE_TYPE") != "db":
        name = ""
        avalibality = ""
