#!/usr/bin/python3

"""
Create a route '/status' on the object app_views
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=["GET"])
def api_status():
    """Returns status of RESTful API"""
    response = {"status": "OK"}
    return jsonify(response)

@app_views.route("/stats", methods=["GET"])
def get_stats():
    """Get statistics of each object type"""
    statistics = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("Amenity"),
        "places": storage.count("Amenity"),
        "reviews": storage.count("Amenity"),
        "states": storage.count("Amenity"),
        "users": storage.count("Amenity"),
    }
    return jsonify(statistics)
