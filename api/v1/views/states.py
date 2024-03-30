#!/usr/bin/python3
"""States endpoint"""

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"])
def get_states():
    """Get all states"""
    states = [state.to_dict() for state in storage.all("State").values()]
    return jsonify(states), 200


@app_views.route("/states/<string:state_id>", methods=["GET"])
def get_state(state_id):
    """Get a specific state by its ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict()), 200


@app_views.route("/states/<string:state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Delete a specific state by its ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"])
def create_state():
    """Create a new state"""
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<string:state_id>", methods=["PUT"])
def update_state(state_id):
    """Update a specific state by its ID"""
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
