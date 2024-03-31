#!/usr/bin/python3
"""Places endpoint"""

from flask import abort, jsonify, make_response, request
import logging
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity


@app_views.route("/cities/<string:city_id>/places", methods=["GET"])
def get_places(city_id):
    """Get all places of a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places), 200


@app_views.route("/places/<string:place_id>", methods=["GET"])
def get_place(place_id):
    """Get a specific place by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route("/places/<string:place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Delete a specific place by its ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<string:city_id>/places", methods=["POST"])
def create_place(city_id):
    """Create a new place"""
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    if "name" not in data:
        abort(400, "Missing name")
    data["city_id"] = city_id
    place = Place(**data)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<string:place_id>", methods=["PUT"])
def update_place(place_id):
    """Update a specific place by its ID"""
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/api/v1/places_search", methods=["POST"])
def search_places():
    """Search for places based on the JSON in the request body"""
    if request.content_type != "application/json":
        abort(400, "Not a JSON")
    if not request.is_json:
        abort(400, "Not a JSON")
    data = request.get_json()
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenity_ids = data.get('amenities', [])
    if not states and not cities and not amenity_ids:
        places = [place.to_dict() for place in storage.all(Place).values()]
    else:
        places = []
        if states:
            for state_id in states:
                state = storage.get(State, state_id)
                if state:
                    for city in state.cities:
                        for place in city.places:
                            if place not in places:
                                places.append(place)
        if cities:
            for city_id in cities:
                city = storage.get(City, city_id)
                if city:
                    for place in city.places:
                        if place not in places:
                            places.append(place)
        if amenity_ids:
            amenities = [
                    storage.get(
                        Amenity, amenity_id
                        ) for amenity_id in amenity_ids
                    ]
            places = [
                    place for place in places
                    if all(amenity in place.amenities for amenity in amenities)
                    ]
    return jsonify([place.to_dict() for place in places]), 200
