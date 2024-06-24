#!/usr/bin/python3
"""
Class City
"""

from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """City CLass"""

    __tablename__ = "city"

    if getenv("CALEN_STORAGE_TYPE") == "db":
        name = Column(String(60), nullable=False)
        neighborhoods = relationship("Neighborhood", back_populates="city",
                                     cascade="all, delete")

    if getenv("CALEN_STORAGE_TYPE") != "db":
        name = ""
        neighborhoods = []
