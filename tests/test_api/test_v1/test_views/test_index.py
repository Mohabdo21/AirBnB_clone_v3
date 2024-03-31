#!/usr/bin/python3
"""Test Module for index view"""
import unittest

from flask import json

from api.v1.app import app
from api.v1.views.index import MODEL_CLASSES


class TestIndex(unittest.TestCase):
    """Test Class for index view"""

    def setUp(self):
        """Configure the app"""
        self.app = app.test_client()
        self.app.testing = True

    def test_status(self):
        """Test status route"""
        response = self.app.get("/api/v1/status")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "OK"})

    def test_get_storage_stats(self):
        """Test stats route"""
        response = self.app.get("/api/v1/stats")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertEqual(set(data.keys()), set(MODEL_CLASSES.keys()))
        for key, value in data.items():
            self.assertIsInstance(value, int)
            self.assertGreaterEqual(value, 0)


if __name__ == "__main__":
    unittest.main()
