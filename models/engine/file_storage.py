#!/usr/bin/python3
"""
FileStorage Model
"""
from models.base_model import BaseModel
from models.user import User
from models.address import Address
from models.city import City
from models.neighborhood import Neighborhood
from models.review import Review
from models.clinic import Clinic
from models.reservation import Reservation
from models.service import Service
from models.role import Role
import json


class FileStorage:
    """FileStorage Module"""
    __file_path = 'file.json'
    __object = {}

    def new(self, obj):
        """Add new instance to FileStorage.__object"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        val = obj
        FileStorage.__object[key] = val

    def all(self):
        """Return Data reloaded from JSON"""
        return FileStorage.__object

    def save(self):
        """Save data in __object into JSON file"""
        obj_to_save = {}
        for key, value in FileStorage.__object.items():
            obj_to_save[key] = value.to_dict()

        with open(FileStorage.__file_path, "w+") as f:
            json.dump(obj_to_save, f, indent=4)

    def reload(self):
        """Reload from JSON and save in __object"""
        classes = {"BaseModel": BaseModel, "User": User, "Address": Address,
                   "City": City, "Review": Review, "Clinic": Clinic,
                   "Reservation": Reservation, "Service": Service,
                   "Role": Role, "Neighborhood": Neighborhood}
        try:
            with open(FileStorage.__file_path, "r") as f:
                reloaded = json.load(f)
                for key, value in reloaded.items():
                    the_instance = classes[value["__class__"]](**value)
                    FileStorage.__object[key] = the_instance
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete Instance from file.json and from __object"""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in FileStorage.__object:
                del (FileStorage.__object[key])
                FileStorage.save(self)

    def close(self):
        """for reloading"""
        self.reload()
