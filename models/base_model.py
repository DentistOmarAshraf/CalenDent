#!/usr/bin/python3
"""
BaseModel
"""

import uuid
import models
from datetime import datetime


class BaseModel:
    """BaseModel for all CalenDent Models"""

    def __init__(self, *args, **kwargs):
        """Constructor Instance"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                if key == "id":
                    self.id = value
                    continue
                if key == "created_at":
                    self.created_at = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                    continue
                if key == "updated_at":
                    self.updated_at = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                    continue
                if key != "__class__":
                    setattr(self, key, value)

    def __str__(self):
        """String represntaion of instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def to_dict(self):
        """making dict of class to saved"""
        obj_info = self.__dict__.copy()
        obj_info["__class__"] = self.__class__.__name__
        obj_info["created_at"] = self.created_at.isoformat()
        obj_info["updated_at"] = self.updated_at.isoformat()
        return obj_info

    def save(self):
        """Using Storage engine to save instance"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """Using Storage engine to delete instance"""
        models.storage.delete(self)