#!/usr/bin/python3
"""
Testing BaseModel
"""

import os
import shutil
import unittest
from models.base_model import BaseModel
from datetime import datetime


class test_basemodel(unittest.TestCase):
    """Testing BaseModel"""

    def setUp(self):
        """Setting up models"""
        self.keyValue = {"id": "1",
                         "created_at": datetime.now().isoformat(),
                         "updated_at": datetime.now().isoformat()}
        self.first = BaseModel()
        self.sec = BaseModel()
        self.third = BaseModel(**(self.keyValue))

    @classmethod
    def tearDownClass(self):
        """Removing __pycahce__"""
        try:
            shutil.rmtree("models/__pycache__")
        except Exception as e:
            print(e)

    def test_type_of_instance(self):
        """type of instance"""
        self.assertIsInstance(self.first, BaseModel)
        self.assertIsInstance(self.sec, BaseModel)

    def test_uuid_exists(self):
        """UUID exists in class"""
        self.assertEqual(hasattr(self.first, "id"), True)
        self.assertEqual(hasattr(self.sec, "id"), True)

    def test_uuid_unique(self):
        """UUID is unique and not repated"""
        self.assertNotEqual(self.first.id, self.sec.id)

    def test_created_at_exists(self):
        """created_at exists in class"""
        self.assertEqual(hasattr(self.first, "created_at"), True)
        self.assertEqual(hasattr(self.sec, "created_at"), True)

    def test_create_at_unique(self):
        """created_at is unique and not repated"""
        self.assertNotEqual(self.first.created_at, self.sec.created_at)

    def test_updated_at_exists(self):
        """updated_at exists in class"""
        self.assertEqual(hasattr(self.first, "updated_at"), True)
        self.assertEqual(hasattr(self.sec, "updated_at"), True)

    def test_updated_at_unique(self):
        """updated_at unique and not repated"""
        self.assertNotEqual(self.first.updated_at, self.sec.updated_at)

    def test_str_value(self):
        """__str__() value return"""
        to_comp = "[{}] ({}) {}".format(self.first.__class__.__name__,
                                        self.first.id, self.first.__dict__)
        self.assertEqual(self.first.__str__(), to_comp)

    def test_to_dict(self):
        """to_dict() return correct value"""
        to_comp = self.first.__dict__.copy()
        to_comp["__class__"] = self.first.__class__.__name__
        to_comp["created_at"] = self.first.created_at.isoformat()
        to_comp["updated_at"] = self.first.updated_at.isoformat()

        self.assertEqual(self.first.to_dict(), to_comp)

    def test_constructor_with_args(self):
        """testing kwargs in construction"""
        self.assertEqual(self.third.id, self.keyValue["id"])
        self.assertEqual(self.third.created_at.isoformat(),
                         self.keyValue["created_at"])
        self.assertEqual(self.third.updated_at.isoformat(),
                         self.keyValue["updated_at"])
