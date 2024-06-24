#!/usr/bin/python3
"""
Address Model
"""

from os import getenv
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Address(BaseModel, Base):
    """Address Model"""

    __tablename__ = "address"

    if getenv("CALEN_STORAGE_TYPE") == "db":
        text_address = Column(String(1024), nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        neighborhood_id = Column(String(60), ForeignKey("neighborhood.id"))
        neighborhood = relationship("Neighborhood", back_populates="addresses")
        users = relationship("User", back_populates="address")
        clinics = relationship("Clinic", back_populates="address",
                               cascade="all, delete")

    if getenv("CALEN_STORAGE_TYPE") != "db":
        text_address = ""
        city = ""
        neighborhood = ""
        location = []
