from app import app
from flask import Blueprint, Flask, jsonify, request
from models.review import Review

reviews_api_blueprint = Blueprint('reviews_api', __name__)

# GET /reviews - Return all reviews
@reviews_api_blueprint.route('/', methods=["GET"])
def index():
    reviews = Review.select()
    review = [{
        "id" = review.id,
        "user_id" = review.user,
        "chef_id" = review.chef,
        "comment" = review.comment,
        "rating" = review.rating
    } for review in reviews]
    return jsonify(review)

# GET /reviews/chef/<chef_id> - Return ALL reviews for a specific chef
@reviews_api_blueprint.route('/chef/<chef_id>', methods=["GET"])
def review_chef(chef_id):
    reviews = Review.select().where(Review.chef == chef_id)
    review = [{
        "id" = review.id,
        "user_id" = review.user,
        "chef_id" = review.chef,
        "comment" = review.comment,
        "rating" = review.rating
    } for review in reviews]
    return jsonify(review)

# POST /reviews/new
@reviews_api_blueprint.route('/new', methods=["POST"])
def review_new():
    user = request.json.get("user", None)
    chef = request.json.get("chef", None)
    comment = request.json.get("comment", None)
    rating = request.json.get("rating", None)   
    review = Review(user=user, chef=chef, comment=comment, rating=rating)
    if review.save():
        return jsonify({
            "message": "successfully submitted a review",
            "status": "success"
        })
    else:
        return jsonify({
            "message": "failed to submit a review",
            "status": "failed"
        }), 400

        