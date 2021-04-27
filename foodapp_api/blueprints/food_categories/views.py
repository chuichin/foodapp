from app import app
from flask import Blueprint, Flask, jsonify, request
from models.food_category import FoodCategory
from models.chef import Chef

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
    chef = Chef.get_or_none(Chef.id == chef_id)
    if chef:
        food_categories = FoodCategory.select(FoodCategory.chef_id, FoodCategory.category).where(FoodCategory.chef_id == chef_id).distinct()
        if food_categories:
            food_categories = {
                "count": food_categories.count(),
                "chef_id": chef_id,
                "food_category": [each.category for each in food_categories]
            }
            return jsonify(food_categories), 200
        else:
            return jsonify({"message": "No records for this chef or in the list yet"}), 400
    else:
        return jsonify(message="This chef does not exist", status="failed"), 400

# GET /food_categories/?category=xxx
@food_categories_api_blueprint.route('/', methods=["GET"])
def chef_results():
    category = request.args.get("category", None)
    if category:
        results_list = FoodCategory.select().where(FoodCategory.category == category)
        if results_list:
            results = [{
                "status": "success",
                "category": category,
                "no_of_results": results_list.count(),
                "chef_id" : [ each.chef_id for each in results_list]
                    }]
            return jsonify(results), 200
        else:
            return jsonify([]), 200


# DELETE /food_categories/delete/<food_category_id>
@food_categories_api_blueprint.route('/delete/<food_category_id>', methods=["DELETE"])
def delete(food_category_id):
    existing_record = FoodCategory.get_or_none(FoodCategory.id == food_category_id )
    if existing_record:
        if existing_record.delete_instance():
            return jsonify({
                "message": "Deleted this food category",
                "food_category_id": food_category_id,
                "status": "success"
            }), 200
    else:
        return jsonify({
            "message": "This record does not exist",
            "status": "failed"
        }), 400