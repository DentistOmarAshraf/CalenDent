#!/usr/bin/python3
"""
Testing City
"""

import unittest
from models.city import City


class test_city(unittest.TestCase):
    """Testing City"""

    def setUp(self):
        self.first = City()
        self.sec = City()

    def test_city_uuid(self):
        """Testing uuid of instance"""
        self.assertNotEqual(self.first.id, self.sec.id)

    def test_city_inhertance(self):
        """Testing City inherit from BaseModel"""
        self.assertTrue(hasattr(self.first, "id"))
        self.assertTrue(hasattr(self.first, "created_at"))
        self.assertTrue(hasattr(self.first, "updated_at"))

    def test_address_attributes(self):
        """Testing City Attibutes"""
        self.assertTrue(hasattr(self.first, "neighborhood"))
        self.assertTrue(hasattr(self.first, "name"))
