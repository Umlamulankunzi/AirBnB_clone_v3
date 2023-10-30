#!/usr/bin/python3

"""
Create a route '/status' on the object app_views
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

models = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'users': User,
        'states': State
        }


@app_views.route("/status",
                 methods=["GET"],
                 strict_slashes=False)
def api_status():
    """Returns status of RESTful API"""
    response = {"status": "OK"}
    return jsonify(response)


@app_views.route("/stats", methods=["GET"])
def get_stats():
    """Get statistics of each object type"""
    statistics = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }
    return jsonify(statistics)
