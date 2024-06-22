#!/usr/bin/python3
"""
Testing Role
"""

import unittest
from models.role import Role


class test_Role(unittest.TestCase):
    """Testing Role"""

    def setUp(self):
        self.first = Role()
        self.sec = Role()

    def test_role_uuid(self):
        """Testing uuid of instance"""
        self.assertNotEqual(self.first.id, self.sec.id)

    def test_role_inhertance(self):
        """Testing Role inherit from BaseModel"""
        self.assertTrue(hasattr(self.first, "id"))
        self.assertTrue(hasattr(self.first, "created_at"))
        self.assertTrue(hasattr(self.first, "updated_at"))

    def test_role_attributes(self):
        """Testing Role Attibutes"""
        self.assertTrue(hasattr(self.first, "name"))
