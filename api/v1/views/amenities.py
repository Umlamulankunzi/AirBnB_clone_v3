#!/usr/bin/python3
"""Amenity API views module"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


# API ROUTE: '/amenities'       method: GET
# GET ALL amenities
@app_views.route(
    '/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """Retrieve all amenities"""
    _amenities = [
        amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(_amenities), 200


# API ROUTE: '/amenities'       method: GET
# GET ONE amenity
@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Get amenity object with id equal to amenity_id

    Return 404 if not found"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict()), 200


# API ROUTE: '/amenities/amenity_id'       method: DELETE
# DELETE amenity
@app_views.route('/amenities/<string:amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete an amenity object with id equal to amenity_id

    Return 404 if not found"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


# API ROUTE: '/amenities'       method: POST
# CREATE amenity
@app_views.route('/amenities',
                 methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """Creates a new amenity or return 404 if not found"""
    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    if 'name' not in data:
        abort(400, "Missing name")
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


# API ROUTE: '/amenities/amenity_id'       method: PUT
# UPDATE amenity
@app_views.route('/amenities/<string:amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id: str = None):
    """Update an amenity given its id or return 404 if not found"""
    if not request.is_json:
        abort(400, "Not a JSON")

    ignore_keys = ('id', 'updated_at', 'created_at')
    data = request.get_json()
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
