#!/usr/bin/python3
"""City API views module"""

from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import abort, request, jsonify



# API ROUTE: '/states/<state_id>/cities'       method: GET
# GET ALL cities
@app_views.route('/states/<state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    """gets all cities where city.state.id == state_id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [
        city.to_dict() for city in storage.all(City).values()
        if city.state_id == state_id]
    return jsonify(cities), 200


# API ROUTE: '/cities/<city_id>'       method: GET
# GET ONE city
@app_views.route('/cities/<city_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """gets city instance were city.id==city_id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict()), 200


# API ROUTE: '/cities/<city_id>'       method: DELETE
# DELETE city
@app_views.route('/cities/<city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes city instance from storage"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


# API ROUTE: '/states/<state_id>/cities'       method: POST
# POST city
@app_views.route('states/<state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Create new city into storage using POST method"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    if "name" not in data:
        abort(400, "Missing name")

    data["state_id"] = state_id
    city = City(**data)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


# API ROUTE: '/states/<state_id>/cities'       method: PUT
# UPDATE city
@app_views.route("/cities/<city_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    """Update a city instance"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    ignore_keys = ('id', 'state_id', 'created_at', 'updated_at')
    data = request.get_json()

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
