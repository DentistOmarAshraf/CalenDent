#!/usr/bin/python3
"""
Testing Clinic
"""

import unittest
from models.clinic import Clinic


class test_clinic(unittest.TestCase):
    """Testing Clinic"""

    def setUp(self):
        self.first = Clinic()
        self.sec = Clinic()

    def test_clinic_uuid(self):
        """Testing uuid of instance"""
        self.assertNotEqual(self.first.id, self.sec.id)

    def test_clinic_inhertance(self):
        """Testing clinic inherit from BaseModel"""
        self.assertTrue(hasattr(self.first, "id"))
        self.assertTrue(hasattr(self.first, "created_at"))
        self.assertTrue(hasattr(self.first, "updated_at"))

    def test_clinic_attributes(self):
        """Testing Address Attibutes"""
        self.assertTrue(hasattr(self.first, "name"))
        self.assertTrue(hasattr(self.first, "avalibality"))
