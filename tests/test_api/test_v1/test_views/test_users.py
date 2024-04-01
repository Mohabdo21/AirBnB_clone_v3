#!/usr/bin/python3
"""Test for User view"""
import json
import unittest

from api.v1.app import app
from models import storage, storage_t
from models.user import User


class TestUser(unittest.TestCase):
    """Test Class for user view"""

    def setUp(self):
        """Configure the app"""
        self.app = app.test_client()
        self.app.testing = True
        self.user = User(email="test@test.com", password="test")
        storage.new(self.user)
        storage.save()

    def tearDown(self):
        """Tear down test environment"""
        if storage_t == "db":
            storage.rollback()
        else:
            storage.reload()

    def test_get_users(self):
        """Test GET all users"""
        response = self.app.get("/api/v1/users")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_user(self):
        """Test GET a specific user by its ID"""
        user = User(email="test@test.com", password="test")
        storage.new(user)
        storage.save()
        if storage_t == "db":
            storage.reload()
        response = self.app.get(f"/api/v1/users/{self.user.id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["id"], self.user.id)

    def test_delete_user(self):
        """Test DELETE a specific user by its ID"""
        response = self.app.delete(f"/api/v1/users/{self.user.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {})

    def test_create_user(self):
        """Test POST to create a user"""
        response = self.app.post(
            "/api/v1/users", json={"email": "new@test.com", "password": "new"}
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["email"], "new@test.com")

    def test_update_user(self):
        """Test PUT to update a user"""
        user = User(email="test@test.com", password="test")
        storage.new(user)
        storage.save()
        if storage_t == "db":
            storage.reload()
        response = self.app.put(
            f"/api/v1/users/{self.user.id}", json={"password": "updated"}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["id"], self.user.id)


if __name__ == "__main__":
    unittest.main()
