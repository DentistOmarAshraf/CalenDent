#!/usr/bin/python3
"""
Testing User
"""

import unittest
from models.user import User


class test_user(unittest.TestCase):
    """Testing User"""

    def setUp(self):
        self.first = User()
        self.sec = User()

    def test_user_uuid(self):
        """Testing uuid of instance"""
        self.assertNotEqual(self.first.id, self.sec.id)

    def test_user_inhertance(self):
        """Testing User inherit from BaseModel"""
        self.assertTrue(hasattr(self.first, "id"))
        self.assertTrue(hasattr(self.first, "created_at"))
        self.assertTrue(hasattr(self.first, "updated_at"))

    def test_user_attributes(self):
        """Testing User Attibutes"""
        self.assertTrue(hasattr(self.first, "email"))
        self.assertTrue(hasattr(self.first, "password"))
        self.assertTrue(hasattr(self.first, "first_name"))
        self.assertTrue(hasattr(self.first, "last_name"))
