#!/usr/bin/python3
"""Creates a view for Review objects"""

from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from flask import abort, request, jsonify


# API ROUTE: /places/<place_id>/reviews'       method: GET
# GET ALL reviews
@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """Get all reviews associated with the Place instance with id==place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [
        review.to_dict() for review in storage.all(Review).values()
        if review.place_id == place_id]
    return jsonify(reviews), 200


# API ROUTE: '/reviews/<review_id>'       method: GET
# GET review
@app_views.route('/reviews/<review_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Get review were review.id==review_id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict()), 200


# API ROUTE: '/reviews/<review_id>'       method: DELETE
# DELETE review
@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review from storage"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


# API ROUTE: '/places/<place_id>/reviews'       method: POST
# POST review
@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create Review instance, link it to Place instance with id==place_id

    Then save Review instance to storage"""
    place = storage.get(Place, place_id)
    if not place:
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

    if 'text' not in data:
        abort(400, "Missing text")

    data['place_id'] = place_id
    review = Review(**data)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


# API ROUTE: '/reviews/<review_id>'       method: PUT
# UPDATE review
@app_views.route('/reviews/<review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update a Review instance saving changes to storage"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    data = request.get_json()
    ignore_keys = ('id', 'user_id', 'place_id', 'created_at', 'updated_at')
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
