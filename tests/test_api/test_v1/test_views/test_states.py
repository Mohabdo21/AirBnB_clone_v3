#!/usr/bin/python3
"""Test for State view"""
import unittest

from flask import json

from api.v1.app import app
from models import storage, storage_t
from models.state import State


class TestStates(unittest.TestCase):
    """Test Class for states view"""

    def setUp(self):
        """Configure the app"""
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        """Tear down test environment"""
        if storage_t == "db":
            storage.rollback()
        else:
            storage.reload()

    def test_get_states(self):
        """Test GET all states"""
        response = self.app.get("/api/v1/states")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        for state in data:
            self.assertIsInstance(state, dict)

    def test_get_state(self):
        """Test GET a specific state"""
        state = State(name="Test State")
        storage.new(state)
        storage.save()
        storage.reload()
        response = self.app.get(f"/api/v1/states/{state.id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertEqual(data["id"], state.id)

    def test_delete_state(self):
        """Test DELETE a specific state"""
        state = State(name="Test State")
        storage.new(state)
        storage.save()
        response = self.app.delete(f"/api/v1/states/{state.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {})

    def test_create_state(self):
        """Test POST to create a state"""
        response = self.app.post("/api/v1/states", json={"name": "New State"})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertEqual(data["name"], "New State")

    def test_update_state(self):
        """Test PUT to update a state"""
        state = State(name="Test State")
        storage.new(state)
        storage.save()
        response = self.app.put(
            f"/api/v1/states/{state.id}", json={"name": "Updated State"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertEqual(data["name"], "Updated State")


if __name__ == "__main__":
    unittest.main()
