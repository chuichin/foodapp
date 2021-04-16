from app import app
from flask import Blueprint, Flask, jsonify, request
from models.like import Like

likes_api_blueprint = Blueprint('likes_api', __name__)

# GET /likes/<chef_id> - Return list of likes for a chef
@likes_api_blueprint.route('/<chef_id>', methods=["GET"])
def likes(chef_id):
    likes = Like.select().where(Like.chef == chef_id)
    likes = [{
        "id" = like.id,
        "user_id" = like.user,
        "chef_id" = like.chef
    } for like in likes]
    return jsonify(likes)

# POST /likes/new
@likes_api_blueprint.route('/new', methods=["POST"])
def new_like():
    user = request.json.get("user_id", None)
    chef = request.json.get("chef_id", None)
    new_like = Like(user=user, chef=chef)
    if new_like:
        return jsonify({
            "message": "Liked successfully",
            "status": "Success"
        })
