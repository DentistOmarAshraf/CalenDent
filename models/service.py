#!/usr/bin/python3
"""
Service Class
"""

from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship


clinic_service = Table("clinic_service", Base.metadata,
        Column("clinic_id", ForeignKey("clinic.id"), primary_key=True),
        Column("service_id", ForeignKey("service.id"), primary_key=True))


class Service(BaseModel, Base):
    """Service Model"""
    __tablename__ = "service"

    if getenv("CALEN_STORAGE_TYPE") == "db":
        name = Column(String(60), nullable=False)
        clinics = relationship("Clinic", secondary="clinic_service",
                               back_populates="services")

    if getenv("CALEN_STORAGE_TYPE") != "db":
        name = ""
        duration = ""
        price = ""
