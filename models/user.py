#!/usr/bin/python3
"""
User Class
"""

from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
import bcrypt


class RoleType(enum.Enum):
    """Type of USER"""
    USER = "user"
    DOCTOR = "doctor"


class User(BaseModel, Base):
    """User Class"""

    __tablename__ = "user"

    if getenv("CALEN_STORAGE_TYPE") == "db":
        email = Column(String(60), nullable=False, unique=True)
        _password = Column('password', String(128), nullable=False)
        username = Column(String(128), nullable=False)
        first_name = Column(String(60))
        last_name = Column(String(60))
        address_id = Column(String(60), ForeignKey("address.id"))
        address = relationship("Address", back_populates="users",
                               cascade="all, delete")
        role = Column(Enum(RoleType), nullable=False)
        clinics = relationship("Clinic", back_populates="user",
                               cascade="all, delete")
        reservations = relationship("Reservation", back_populates="user",
                                    cascade="all, delete")
        reviews = relationship("Review", back_populates="user",
                               cascade="all, delete")

    if getenv("CALEN_STORAGE_TYPE") != "db":
        email = ""
        _password = ""
        first_name = ""
        last_name = ""

    @property
    def password(self):
        raise AttributeError("password is NOT READABLE")

    @password.setter
    def password(self, passwd):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(passwd.encode('utf-8'), salt)
        self._password = hashed.decode('utf-8')

    def verify_password(self, password):
        """Check Password"""
        return bcrypt.checkpw(password.encode('utf-8'),
                              self._password.encode('utf-8'))
