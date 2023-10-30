#!/usr/bin/python3
"""
Create new view for state objects
"""

from flask import abort, jsonify, request
from models.state import State
from api.v1.views import app_views
from models import storage


# API ROUTE: /states                GET
@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """Get list of all state objects"""
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)

# API ROUTE: /states/<state_id>     GET
@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_one_state(state_id):
    """Get state object with state.id==state_id"""
    state = storage.get(State, state_id)
    return jsonify(state.to_dict()) if state else abort(404)

# API ROUTE: /states/<state_id>     DELETE
@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """Delete state object with state.id==state_id"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    abort(404)

# API ROUTE: /states         POST
@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Create new state object"""
    data = request.get_json()
    if not data:
        # return 400 if request data type not json
        abort(400, "Not a JSON")
    if "name" not in data:
        # return 400 if key 'name' not in data
        abort(400, "Missing name")

    state = State(**data)
    state.save()

    # return created state & status code 201
    return jsonify(state.to_dict()), 201

@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """update a State instance"""
    # get state object with state.id==state_id from storage
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            # Return Error 400: if type request data not json
            abort(400, "Not a Json")

        # Get json data from the request
        data = request.get_json()
        ignore_keys = ["id", "created_at", "updated_at"]

        # update attributes of state object
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)

        # Save the updated state object to staorage
        state.save()
        return jsonify(state.to_dict()), 200

    else:
        # Return Error 404: if state object not found
        abort(404)

@app_views.errorhandler(404)
def not_found(error):
    """Handles Resource Not Found Error: 404"""
    response = {"error": "Not found"}
    return jsonify(response), 404

@app_views.errorhandler(400)
def bad_request(error):
    """Handles Bad Request Error: 400"""
    response = {"error": "Not found"}
    return jsonify(response), 404
