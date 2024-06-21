#!/usr/bin/python3
"""
Testing Neighborhood model
"""

import unittest
from models.neighborhood import Neighborhood


class test_neighborhood(unittest.TestCase):
    """Testing Neighborhood"""

    def setUp(self):
        self.first = Neighborhood()
        self.sec = Neighborhood()

    def test_address_uuid(self):
        """Testing uuid of instance"""
        self.assertNotEqual(self.first.id, self.sec.id)

    def test_address_inhertance(self):
        """Testing Neighborhood inherit from BaseModel"""
        self.assertTrue(hasattr(self.first, "id"))
        self.assertTrue(hasattr(self.first, "created_at"))
        self.assertTrue(hasattr(self.first, "updated_at"))

    def test_address_attributes(self):
        """Testing Neighborhood Attibutes"""
        self.assertTrue(hasattr(self.first, "name"))
