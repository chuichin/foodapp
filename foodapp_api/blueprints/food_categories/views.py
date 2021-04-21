from app import app
from flask import Blueprint, Flask, jsonify, request
from models.food_category import FoodCategory

food_categories_api_blueprint = Blueprint("food_category_api", __name__)



# POST /food_categories/new
@food_categories_api_blueprint.route('/new/<chef_id>', methods=["POST"])
def new(chef_id):
    category = request.json.get('category', None)
    existing_record = FoodCategory.get_or_none(FoodCategory.chef_id == chef_id, FoodCategory.category == category)
    if existing_record:
        return jsonify({
            "message": "This food category for this chef already exist",
            "category": category,
            "chef": chef_id
        }), 400
    else:
        new = FoodCategory(chef=chef_id, category=category)
        if new.save():
            return jsonify({
                "message": "Successfully create new category record",
                "chef_id": chef_id,
                "category": category,
                "status":"Success"
            }), 200
        else: 
            return jsonify({
                "message":"Error in creating new category record"
            }), 400

# GET /food_categories/<chef_id>
@food_categories_api_blueprint.route('/<chef_id>', methods=["GET"])
def index(chef_id):
    food_categories = FoodCategory.select(FoodCategory.chef_id, FoodCategory.category).where(FoodCategory.chef_id == chef_id).distinct()
    if food_categories:
        food_categories = [{
            "food_category": each.category,
            "chef": each.chef_id
        } for each in food_categories]
        return jsonify(food_categories), 200
    else:
        return jsonify({"message": "No records for this chef or in the list yet"})
    
# GET /food_categories/chefs
@food_categories_api_blueprint.route('/chefs', methods=["GET"])
def chefs():
    category = 
    chefs_list = FoodCategory.select(FoodCategory.chef_id).where().distinct()