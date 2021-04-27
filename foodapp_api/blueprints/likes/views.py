from app import app
from flask import Blueprint, Flask, jsonify, request
from models.like import Like
from models.user import User
from models.chef import Chef

likes_api_blueprint = Blueprint('likes_api', __name__)

# POST /likes/new
@likes_api_blueprint.route('/new', methods=["POST"])
def new_like():
    user_id = request.json.get("user_id", None)
    existing_user = User.get_or_none(User.id == user_id)
    chef_id = request.json.get("chef_id", None)
    existing_chef = Chef.get_or_none(Chef.id == chef_id)
    existing_like = Like.get_or_none(Like.user_id==user_id, Like.chef_id==chef_id)
    
    if existing_user == None:
        return jsonify({
            "message": "User does not exist",
            "status" : "failed"
        }), 400
    if existing_chef == None:
        return jsonify({
            "message": "Chef does not exist",
            "status" : "failed"
        }), 400
    if existing_user and existing_chef:
        if existing_like:
            return jsonify({
                "message": "User already liked this chef",
                "status" : "failed"
            }), 400
        else:
            new_like = Like(user=user_id, chef=chef_id)
            if new_like.save():
                return jsonify({
                    "message": "Liked successfully",
                    "status": "Success"
                })


# GET /likes/<chef_id> - Return list of likes for a chef
@likes_api_blueprint.route('/<chef_id>', methods=["GET"])
def likes(chef_id):
    likes = Like.select().where(Like.chef_id == chef_id).count()
    no_like= {
        "no_of_likes": likes,
        "chef_id":chef_id
    }
    return jsonify(no_like)


# Delete likes
@likes_api_blueprint.route('/delete/<like_id>', methods=["DELETE"])
def delete(like_id):
    existing_like = Like.get_or_none(Like.id == like_id)
    if existing_like:
        if existing_like.delete_instance():
            return jsonify({
                "message": "successfully deleted",
                "status": "success"
            }), 200
    else:
        return jsonify({
            "message": "this 'like' no longer exist or you might deleted twice",
            "status": "failed"
        }), 400