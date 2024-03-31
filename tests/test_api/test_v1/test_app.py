import os
import unittest
from flask import Flask
from api.v1.app import app
from api.v1.views import app_views
from models import storage
from sqlalchemy.exc import InvalidRequestError


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_status(self):
        response = self.app.get('/api/v1/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "OK"})

    def test_404(self):
        response = self.app.get('/api/v1/nonexistent_route')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Not found"})

    def test_blueprint_registration(self):
        self.assertIn('app_views', self.app.application.blueprints)

    def test_tear_down(self):
        with self.app.application.app_context():
            storage.close()
            self.assertTrue(storage.is_closed)


if __name__ == "__main__":
    unittest.main()
