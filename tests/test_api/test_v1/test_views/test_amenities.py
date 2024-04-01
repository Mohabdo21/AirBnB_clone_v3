#!/usr/bin/python3
"""Test for Amenity view"""
import json
import unittest

from api.v1.app import app
from models import storage, storage_t
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """Test Class for amenity view"""

    def setUp(self):
        """Configure the app"""
        self.app = app.test_client()
        self.app.testing = True
        self.amenity = Amenity(name="Test Amenity")
        storage.new(self.amenity)
        storage.save()

    def tearDown(self):
        """Tear down test environment"""
        if storage_t == "db":
            storage.rollback()
        else:
            storage.reload()

    def test_get_amenities(self):
        """Test GET all amenities"""
        response = self.app.get("/api/v1/amenities")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_amenity(self):
        """Test GET a specific amenity by its ID"""
        amenity = Amenity(name="Test Amenity")
        storage.new(amenity)
        storage.save()
        if storage_t == "db":
            storage.reload()
        response = self.app.get(f"/api/v1/amenities/{self.amenity.id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["id"], self.amenity.id)

    def test_delete_amenity(self):
        """Test DELETE a specific amenity by its ID"""
        response = self.app.delete(f"/api/v1/amenities/{self.amenity.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {})

    def test_create_amenity(self):
        """Test POST to create an amenity"""
        response = self.app.post(
                "/api/v1/amenities",
                json={"name": "New Amenity"}
                )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["name"], "New Amenity")

    def test_update_amenity(self):
        """Test PUT to update an amenity"""
        response = self.app.put(
            f"/api/v1/amenities/{self.amenity.id}",
            json={"name": "Updated Amenity"}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["name"], "Updated Amenity")


if __name__ == "__main__":
    unittest.main()
