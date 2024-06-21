#!/usr/bin/python3
"""
Testing Review model
"""

import unittest
from models.review import Review


class test_review(unittest.TestCase):
    """Testing Review"""

    def setUp(self):
        self.first = Review()
        self.sec = Review()

    def test_review_uuid(self):
        """Testing uuid of instance"""
        self.assertNotEqual(self.first.id, self.sec.id)

    def test_review_inhertance(self):
        """Testing Review inherit from BaseModel"""
        self.assertTrue(hasattr(self.first, "id"))
        self.assertTrue(hasattr(self.first, "created_at"))
        self.assertTrue(hasattr(self.first, "updated_at"))

    def test_review_attributes(self):
        """Testing Review Attibutes"""
        self.assertTrue(hasattr(self.first, "text"))
