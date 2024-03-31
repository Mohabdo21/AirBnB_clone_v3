#!/usr/bin/python3
"""Place_Amenities Endpoints"""

from os import getenv

from flask import abort, jsonify

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route("/places/<string:place_id>/amenities", methods=["GET"])
def get_amenities(place_id):
    """Get all amenities of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [
            storage.get(Amenity, amenity_id).to_dict()
            for amenity_id in place.amenity_ids
        ]
    return jsonify(amenities), 200


@app_views.route(
    "/places/<string:place_id>/amenities/<string:amenity_id>", methods=["DELETE"]
)
def delete_amenity(place_id, amenity_id):
    """Delete a specific amenity from a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    place.save()
    return jsonify({}), 200


@app_views.route(
    "/places/<string:place_id>/amenities/<string:amenity_id>", methods=["POST"]
)
def link_amenity(place_id, amenity_id):
    """Link an amenity to a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
    place.save()
    return jsonify(amenity.to_dict()), 201
