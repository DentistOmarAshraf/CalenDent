#!/usr/bin/python3
"""
BaseModel
"""

import uuid
import models
from os import getenv
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime


if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """BaseModel for all CalenDent Models"""

    if models.storage_t == "db":
        """This will be inhertied by all child classes of BaseModel"""
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

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
                    self.created_at = datetime.strptime(value,
                                                        '%Y-%m-%dT%H:%M:%S.%f')
                    continue
                if key == "updated_at":
                    self.updated_at = datetime.strptime(value,
                                                        '%Y-%m-%dT%H:%M:%S.%f')
                    continue
                if key != "__class__":
                    setattr(self, key, value)

    def __str__(self):
        """String represntaion of instance"""
        dic = self.__dict__.copy()
        if "_sa_instance_state" in dic:
            del (dic["_sa_instance_state"])
        return f"[{self.__class__.__name__}] ({self.id}) {dic}"

    def to_dict(self):
        """making dict of class to saved"""
        obj_info = self.__dict__.copy()
        obj_info["__class__"] = self.__class__.__name__
        obj_info["created_at"] = self.created_at.isoformat()
        obj_info["updated_at"] = self.updated_at.isoformat()
        if "_sa_instance_state" in obj_info:
            del (obj_info["_sa_instance_state"])
        if "_password" in obj_info:
            del (obj_info["_password"])
        return dict(sorted(obj_info.items()))

    def save(self):
        """Using Storage engine to save instance"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """Using Storage engine to delete instance"""
        models.storage.delete(self)
