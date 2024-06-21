#!/usr/bin/python3
"""
Testing Service
"""

import unittest
from models.service import Service


class test_service(unittest.TestCase):
    """Testing Service"""

    def setUp(self):
        self.first = Service()
        self.sec = Service()

    def test_service_uuid(self):
        """Testing uuid of instance"""
        self.assertNotEqual(self.first.id, self.sec.id)

    def test_service_inhertance(self):
        """Testing Service inherit from BaseModel"""
        self.assertTrue(hasattr(self.first, "id"))
        self.assertTrue(hasattr(self.first, "created_at"))
        self.assertTrue(hasattr(self.first, "updated_at"))

    def test_Serivce_attributes(self):
        """Testing Service Attibutes"""
        self.assertTrue(hasattr(self.first, "name"))
        self.assertTrue(hasattr(self.first, "duration"))
        self.assertTrue(hasattr(self.first, "price"))
