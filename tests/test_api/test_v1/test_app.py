#!/usr/bin/python3
"""Test Module for Flask app"""

import os
import unittest

from flask import Flask

from api.v1.app import app
from api.v1.views import app_views
from models import storage


class TestApp(unittest.TestCase):
    """Test Class for Flask app"""

    def setUp(self):
        """Configure the app"""
        self.app = app.test_client()
        self.app.testing = True

    def test_status(self):
        """Test status"""
        response = self.app.get("/api/v1/status")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "OK"})

    def test_404(self):
        """Test Error handling"""
        response = self.app.get("/api/v1/nonexistent_route")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Not found"})

    def test_blueprint_registration(self):
        """Check Blueprint"""
        self.assertIn("app_views", self.app.application.blueprints)

    def test_tear_down(self):
        """Test teardown"""
        with self.app.application.app_context():
            storage.close()
            self.assertTrue(storage.is_closed)


if __name__ == "__main__":
    unittest.main()
