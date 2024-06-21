#!/usr/bin/python3
"""
Test Address
"""

import unittest
from models.reservation import Reservation


class test_reservation(unittest.TestCase):
    """Testing class reservation"""

    def setUp(self):
        """Setting up classes for tests"""
        self.first = Reservation()
        self.sec = Reservation()

    def test_reservation_uuid(self):
        """compare uuid"""
        self.assertNotEqual(self.first.id, self.sec.id)

    def test_reservation_inhertance(self):
        """Testing reservation inherit from BaseModel"""
        self.assertTrue(hasattr(self.first, "id"))
        self.assertTrue(hasattr(self.first, "created_at"))
        self.assertTrue(hasattr(self.first, "updated_at"))

    def test_attributes(self):
        """Testing attributes"""
        self.assertTrue(hasattr(self.first, "appointment"))
        self.assertTrue(hasattr(self.first, "status"))
