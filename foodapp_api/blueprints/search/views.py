# Note: this is for Filter search
# Still under testing

from app import app
from flask import Blueprint, Flask, jsonify, request
from models.booking import Booking
from models.food_category import FoodCategory

search_api_blueprint = Blueprint('searches_api', __name__)

incomes = [
  { 'description': 'salary', 'amount': 5000 }
]

# Random filter /api/v1/searches
# @search_api_blueprint.route('/', methods=["POST"])


@search_api_blueprint.route('/incomes/test', methods=['POST'])
def test():
    category = request.args.get('category')
    return jsonify(category)
    # category = request.args.get('category')
    # chef_id = request.args.get('chef_id')
    # if category:
    #     x = FoodCategory.category.in_([category])
    # if chef_id:
    #     y = FoodCategory.chef_id.in_([chef_id])
    # results = FoodCategory.select().where(x,y)
    # return jsonify([{"chef":each.chef_id, "category":each.category} for each in results])


@search_api_blueprint.route('/incomes/hello', methods=['POST'])
def add_income():
  incomes.append(request.get_json())
  return jsonify(incomes)

