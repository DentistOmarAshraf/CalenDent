#!/usr/bin/python3
"""
Address Model
"""

from models.base_model import BaseModel

class Address(BaseModel):
    """Address Model"""
    text_address = ""
    city = ""
    neighborhood = ""
    location = []
