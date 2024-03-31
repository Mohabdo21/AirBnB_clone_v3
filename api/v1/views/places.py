#!/usr/bin/python3
"""Places endpoint"""

from flask import abort, jsonify, make_response, request

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


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """
    Retrieves all Place objects depending on
    the JSON in the body of the request
    """
    if request.content_type != "application/json":
        abort(400, "Not a JSON")

    data = request.get_json()

    if not data:
        abort(400, "Not a JSON")

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    if not any([states, cities, amenities]):
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    list_places = get_places_by_states(states)
    list_places += get_places_by_cities(cities, list_places)
    list_places = filter_places_by_amenities(amenities, list_places)

    return jsonify([place.to_dict() for place in list_places])


def get_places_by_states(state_ids):
    states = [storage.get(State, s_id) for s_id in state_ids]
    places = []
    for state in states:
        if state:
            for city in state.cities:
                places.extend(city.places)
    return places


def get_places_by_cities(city_ids, existing_places):
    cities = [storage.get(City, c_id) for c_id in city_ids]
    places = []
    for city in cities:
        if city:
            for place in city.places:
                if place not in existing_places:
                    places.append(place)
    return places


def filter_places_by_amenities(amenity_ids, places):
    if not amenity_ids:
        return places

    amenities = [storage.get(Amenity, a_id) for a_id in amenity_ids]
    return [
            place for place in places if all(
                am in place.amenities for am in amenities
                )
            ]
