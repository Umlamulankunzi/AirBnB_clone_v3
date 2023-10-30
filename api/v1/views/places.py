#!/usr/bin/python3
"""Creates a view for City objects"""

from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views
from flask import abort, request, jsonify


# API ROUTE: '/cities/<city_id>/places'       method: GET
# GET ALL reviews
@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """Get all the places associated with City instance with id==city_id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [
        place.to_dict() for place in storage.all(Place).values()
        if place.city_id == city_id]
    return jsonify(places), 200


# API ROUTE: '/places/<place_id>'          method: GET
# GET ONE place
@app_views.route('/places/<place_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Get place instance were place.id==place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict()), 200


# API ROUTE: '/places/<place_id>'          method: DELETE
# DELETE place
@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes place instance with id==place_id from storage"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


# API ROUTE: '/cities/<city_id>/places'          method: POST
# CREATE place
@app_views.route('/cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def add_place(city_id):
    """Add new place instance associated to City instance

    with city.id==city_id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()

    if 'user_id' not in data:
        abort(400, "Missing user_id")

    user_id = data['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if 'name' not in data:
        abort(400, "Missing name")

    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


# API ROUTE: '/places/<place_id>'          method: PUT
# UPDATE place
@app_views.route('/places/<place_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Update place instance with placeinstance id equal to place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    ignore_keys = ('id', 'user_id', 'city_id', 'created_at', 'updated_at')
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


# API ROUTE: '/places_search'          method: POST
# SEARCH place
@app_views.route('/places_search',
                 methods=['POST'],
                 strict_slashes=False)
def places_search():
    """
    Retrieve place objects based on the JSON in the body
    of the request
    """

    data = request.get(silent=True)

    if data is None:
        abort(400, "Not a JSON")

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])
    places = set()

    # if states & cities empty get all Place objects
    if not len(states) + len(cities):
        places.update(storage.all(Place).values())
        if len(amenities) == 0:
            response = [place.to_dict() for place in places]
            return jsonify(response)
    else:
        for state_id in states:
            state = storage.get(State, state_id)
            if state is None:
                abort(404)
            for city in state.cities:
                places.update(city.places)

        for city_id in cities:
            city = storage.get(City, city_id)
            if city is None:
                abort(404)
            places.update(city.places)

    if len(amenities) == 0:
        response = [place.to_dict() for place in places]
        return jsonify(response)
    # Filter results:
    am_filter = [
        storage.get(Amenity, amenity_id) for amenity_id in amenities
        if storage.get(Amenity, amenity_id) is not None]
    results = set()

    for place in places:
        if len(set(am_filter).intersection(set(place.amenities))):
            try:
                del place.amenities
            except AttributeError:
                pass
            results.add(place)
    return jsonify([place.to_dict() for place in results])
