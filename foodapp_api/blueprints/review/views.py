from app import app
from flask import Blueprint, Flask, jsonify, request
from models.review import Review
from models.user import User
from models.chef import Chef
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt_header

reviews_api_blueprint = Blueprint('reviews_api', __name__)

jwt = JWTManager(app) 


# POST /reviews/new
@reviews_api_blueprint.route('/new', methods=["POST"])
@jwt_required()
def review_new():
    user = User.get_or_none(User.email == get_jwt_identity())

    if request.is_json:
        chef_id = request.json.get("chef", None)
        comment = request.json.get("comment", None)
        rating = request.json.get("rating", None)   

        existing_chef = Chef.get_or_none(Chef.id == chef_id)

        if existing_chef:
            review = Review(user=user.id, chef=existing_chef.id, comment=comment, rating=rating)
            if review.save():
                return jsonify({
                    "message": "successfully submitted a review",
                    "status": "success"
                }), 200
        elif existing_chef==None:
            return jsonify(message ="Chef does not exist", status="failed"), 400
    else:
        return jsonify(message="Nothing is passed"), 400
                

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
@reviews_api_blueprint.route('/<chef_id>', methods=["GET"])
def review_chef(chef_id):
    existing_chef = Chef.get_or_none(Chef.id == chef_id)
    if existing_chef:
        reviews = Review.select().where(Review.chef == chef_id)
        if reviews:
            review = {
                "count": reviews.count(),
                "chef_reviews": [{
                    "id": review.id,
                    "user_id": review.user_id,
                    "chef_id" : review.chef_id,
                    "comment" : review.comment,
                    "rating" : review.rating
                    } for review in reviews]}
            return jsonify(review), 200
        else: 
            return jsonify([]), 200
    else:
        return jsonify(message="This chef does not exist", status="Failed"), 400



# DELETE /reviews/delete/<review_id>
@reviews_api_blueprint.route("/delete/<review_id>", methods=["DELETE"])
def delete(review_id):
    existing_review = Review.get_or_none(Review.id == review_id)
    if existing_review:
        if existing_review.delete_instance():
            return jsonify({
                "message": "Successfully delete a reivew",
                "status": "success"
            }), 200
    else:
        return jsonify({
            "message": "This review no longer exist or did not exist at all",
            "status": "failed"
        }), 400