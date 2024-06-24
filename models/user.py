#!/usr/bin/python3
"""
User Class
"""

from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
import hashlib


class RoleType(enum.Enum):
    """Type of USER"""
    USER = "user"
    DOCTOR = "doctor"


class User(BaseModel, Base):
    """User Class"""

    __tablename__ = "user"

    if getenv("CALEN_STORAGE_TYPE") == "db":
        email = Column(String(60), nullable=False)
        __password = Column('password', String(60), nullable=False)
        first_name = Column(String(60))
        last_name = Column(String(60))
        address_id = Column(String(60), ForeignKey("address.id"))
        address = relationship("Address", back_populates="users",
                               cascade="all, delete")
        role = Column(Enum(RoleType))
        clinics = relationship("Clinic", back_populates="user",
                               cascade="all, delete")
        reservations = relationship("Reservation", back_populates="user",
                                    cascade="all, delete")
        reviews = relationship("Review", back_populates="user",
                               cascade="all, delete")

    if getenv("CALEN_STORAGE_TYPE") != "db":
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, passwd):
        self.__password = hashlib.md5(passwd.encode()).hexdigest()
