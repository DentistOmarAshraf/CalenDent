#!/usr/bin/python3
"""Neighborhood Model"""


from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Neighborhood(BaseModel, Base):
    """Class Neighborhood"""

    __tablename__ = "neighborhood"

    if getenv("CALEN_STORAGE_TYPE") == "db":
        name = Column(String(60), nullable=False)
        city_id = Column(String(60), ForeignKey("city.id"))
        city = relationship("City", back_populates="neighborhoods")
        addresses = relationship("Address", back_populates="neighborhood",
                                 cascade="all, delete")
        clinics = relationship("Clinic", back_populates="neighborhood",
                               cascade="all, delete")

    if getenv("CALEN_STORAGE_TYPE") != "db":
        name = ""
        city = ""
