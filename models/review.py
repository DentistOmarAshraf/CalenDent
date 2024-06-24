#!/usr/bin/python3
"""
Review Class
"""

from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Review(BaseModel, Base):
    """review model"""

    __tablename__ = "review"
    if getenv("CALEN_STORAGE_TYPE") == "db":
        text = Column(String(1024), nullable=False)
        stars = Column(Integer, nullable=False)
        user_id = Column(String(60), ForeignKey("user.id"))
        clinic_id = Column(String(60), ForeignKey("clinic.id"))
        user = relationship("User", back_populates="reviews")
        clinic = relationship("Clinic", back_populates="reviews")

    if getenv("CALEN_STORAGE_TYPE") != "db":
        text = ""
