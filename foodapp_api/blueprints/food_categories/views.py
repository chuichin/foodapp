from app import app
from flask import Blueprint, Flask, jsonify, request
from models.food_category import FoodCategory

food_categories_api_blueprint = Blueprint("food_category_api", __name__)

# GET /food_categories
@food_categories_api_blueprint.route('/', methods=["GET"])
def index():
    food_categories = FoodCategory.select()
    food_categories = [{
        "id": each.id,
        "category": each.category,
        "chef": each.chef
    } for each in food_categories]
    return jsonify(food_categories)