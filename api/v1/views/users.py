#!/usr/bin/python3
"""User RESTFul API module"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


# API ROUTE: '/users'                method=GET
# GET ALL users
@app_views.route('/users',
                 methods=['GET'],
                 strict_slashes=False)
def get_all_users():
    """Get all users"""
    response = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(response), 200


# API ROUTE: '/users/<user_id>'      method=GET
# GET ONE user
@app_views.route('/users/<user_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Get user with supplied user_id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict()), 200


# API ROUTE: '/users/<user_id>'      method=DELETE
# DELETE user
@app_views.route('/users/<user_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes user with given user_id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


# API ROUTE: '/users'        method=POST
# CREATE user
@app_views.route('/users',
                 methods=['POST'],
                 strict_slashes=False)
def create_user():
    """Create new User and save to storage"""
    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")
    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


# API ROUTE: '/users/<user_id>'      method=PUT
# GET ONE users
@app_views.route('/users/<user_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Update user instance with given user_id"""
    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    ignore_keys = ('id', 'updated_at', 'created_at', 'email')
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
