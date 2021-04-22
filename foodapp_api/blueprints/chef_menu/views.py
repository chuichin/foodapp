from app import app
from flask import Blueprint, Flask, jsonify, request
from models.chef_menu import ChefMenu
from models.chef import Chef

chef_menu_api_blueprint = Blueprint('chef_menu_api', __name__)

# return all Menus 
@chef_menu_api_blueprint.route('/', methods=["GET"])
def all_menus():
    chef_menus = ChefMenu.select()
    if chef_menus:
        chef_menus = [{
            "id":menu.id,
            "food_category_id": menu.food_category_id,
            "menu" : menu.menu,
            "chef": menu.chef_id
        } for menu in chef_menus]
        return jsonify(chef_menus)
    else:
        return jsonify({
            "message":"There are no menus yet",
            "status": "failed"
        }), 400

# return all Menus for one chef
@chef_menu_api_blueprint.route('/<chef_id>', methods=["GET"])
def menu(chef_id):
    menus = ChefMenu.select().where(ChefMenu.chef_id == chef_id)
    if menus:
        menus = [{
            "food_category": each.food_category,
            "chef": each.chef_id,
            "menu" : each.menu
        } for each in menus]
        return jsonify(menus), 200
    else:
        return jsonify({"message": "No records for this chef or in the list yet"}), 400
    

# chef submit/creates new menu
@chef_menu_api_blueprint.route('/<chef_id>/new', methods=["POST"])
def new_menu(chef_id):
    chef = Chef.get_or_none(Chef.id== chef_id)
    if chef:
        food_category = request.json.get('food_category', None)
        menu = request.json.get('menu', None)
        create_menu = ChefMenu(chef=chef_id, food_category=food_category, menu=menu)
        if create_menu.save():
            return jsonify({
                "message":"Successfully created new menu",
                "menu": menu,
                "food_category": food_category,
                "chef_id": chef_id
            }), 200
        else:
            return jsonify({
                "message": "Unable to create new menu",
                "status": "failed"
            }), 400
    else:
        return jsonify({
            "message":"This chef does not exist",
            "status":"failed"
        }), 400
