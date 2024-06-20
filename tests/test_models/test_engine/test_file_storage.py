#!/usr/bin/python3
"""
FileStorage Test
"""

import unittest
from models.base_model import BaseModel
from models import storage
import os


class test_fileStorage(unittest.TestCase):
    """Testing FileStorage"""

    def setUp(self):
        self.first = BaseModel()
        self.first.save()
        self.sec = BaseModel()
        self.sec.save()

    @classmethod
    def tearDownClass(self):
        os.remove("file.json")

    def test_all_method(self):
        """test the return data from FileStorage"""
        name = f"{self.first.__class__.__name__}.{self.first.id}"
        to_comp = storage.all()[name]
        self.assertEqual(self.first, to_comp)

    def test_all_data_type(self):
        """testing data type returned from all is dict"""
        self.assertIsInstance(storage.all(), dict)

    def test_created_file(self):
        """testing if file Storage create file.json successfully"""
        self.assertTrue(os.path.isfile("file.json"))

    def test_delete(self):
        name = f"{self.sec.__class__.__name__}.{self.sec.id}"
        self.sec.delete()
        self.assertTrue(name not in storage.all().keys())
