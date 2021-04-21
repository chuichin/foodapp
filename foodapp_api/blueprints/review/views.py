from app import app
from flask import Blueprint, Flask, jsonify, request
from models.review import Review

reviews_api_blueprint = Blueprint('reviews_api', __name__)

# GET /reviews - Return all reviews
@reviews_api_blueprint.route('/', methods=["GET"])
def index():
    reviews = Review.select()
    if reviews:
        review = [{
            "id": review.id,
            "user_id": review.user_id,
            "chef_id" : review.chef_id,
            "comment" : review.comment,
            "rating" : review.rating
        } for review in reviews]
        return jsonify(review)
    else: 
        return jsonify({
            "message": "No reviews yet", 
            "status": "failed"
        }), 400

# GET /reviews/chef/<chef_id> - Return ALL reviews for a specific chef
@reviews_api_blueprint.route('/chef/<chef_id>', methods=["GET"])
def review_chef(chef_id):
    reviews = Review.select().where(Review.chef == chef_id)
    if reviews:
        review = [{
            "count": reviews.count(),
            "chef_reviews": [{
                "id": review.id,
                "user_id": review.user_id,
                "chef_id" : review.chef_id,
                "comment" : review.comment,
                "rating" : review.rating
                } for review in reviews]}]
        return jsonify(review)
    else: 
        return jsonify({
            "message": "No reviews for this chef", 
            "status": "failed"
        }), 400


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
        }), 
        
# to add validation for create new post?

        