#!/usr/bin/python3
"""
Testing Address
"""

import unittest
from models.address import Address


class test_address(unittest.TestCase):
    """Testing Address"""

    def setUp(self):
        self.first = Address()
        self.sec = Address()

    def test_address_uuid(self):
        """Testing uuid of instance"""
        self.assertNotEqual(self.first.id, self.sec.id)

    def test_address_inhertance(self):
        """Testing Address inherit from BaseModel"""
        self.assertTrue(hasattr(self.first, "id"))
        self.assertTrue(hasattr(self.first, "created_at"))
        self.assertTrue(hasattr(self.first, "updated_at"))

    def test_address_attributes(self):
        """Testing Address Attibutes"""
        self.assertTrue(hasattr(self.first, "text_address"))
        self.assertTrue(hasattr(self.first, "city"))
        self.assertTrue(hasattr(self.first, "neighborhood"))
        self.assertTrue(hasattr(self.first, "location"))
