from app import app
from flask import Blueprint, Flask, jsonify, request
from models.review import Review
from models.user import User
from models.chef import Chef

reviews_api_blueprint = Blueprint('reviews_api', __name__)

# POST /reviews/new
@reviews_api_blueprint.route('/new', methods=["POST"])
def review_new():
    user_id = request.json.get("user", None)
    chef_id = request.json.get("chef", None)
    comment = request.json.get("comment", None)
    rating = request.json.get("rating", None)   

    if user_id and chef_id:
        existing_user = User.get_or_none(User.id == user_id)
        existing_chef = Chef.get_or_none(Chef.id == chef_id)
        if existing_user and existing_chef:
            review = Review(user=user_id, chef=chef_id, comment=comment, rating=rating)
            if review.save():
                return jsonify({
                    "message": "successfully submitted a review",
                    "status": "success"
                }), 200
            else:
                return jsonify({
                    "message": "failed to submit a review",
                    "status": "failed"
                }), 400
        
        elif existing_user== None:
            return jsonify(message ="User does not exist", status="failed"), 400
        
        elif existing_chef==None:
            return jsonify(message ="Chef does not exist", status="failed"), 400

                

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
            return jsonify({
                "message": "No reviews for this chef", 
                "status": "failed"
            }), 400
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