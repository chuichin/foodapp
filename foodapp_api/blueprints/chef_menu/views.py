from app import app
from flask import Blueprint, Flask, jsonify, request
from models.chef_menu import ChefMenu
from models.chef import Chef
from models.food_category import FoodCategory
import json
import datetime

chef_menu_api_blueprint = Blueprint('chef_menu_api', __name__)

# chef submit/creates new menu
@chef_menu_api_blueprint.route('/<chef_id>/new', methods=["POST"])
def new_menu(chef_id):
    chef = Chef.get_or_none(Chef.id== chef_id)
    if chef:
        food_category = request.json.get('food_category', None)
        appetiser = request.json.get('appetiser', None)
        main = request.json.get('main', None)
        starter = request.json.get('starter', None)
        dessert = request.json.get('dessert', None)
        description = request.json.get('description', None)
        create_menu = ChefMenu(chef=chef_id, food_category=food_category, appetiser=appetiser, main=main, starter=starter, dessert=dessert, description=description)
        if create_menu.save():
            return jsonify({
                "message":"Successfully created new menu",
                "menu":{
                    "id":create_menu.id,
                    "chef": create_menu.chef_id,
                    "food_category": create_menu.food_category,
                    "appetiser" : create_menu.appetiser,
                    "main": create_menu.main,
                    "starter": create_menu.starter,
                    "dessert": create_menu.dessert,
                    "description": create_menu.description
                }   
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


# return all Menus 
@chef_menu_api_blueprint.route('/', methods=["GET"])
def all_menus():
    chef_menus = ChefMenu.select()
    if chef_menus:
        chef_menus = {
            "_status": "success",
            "_count": chef_menus.count(),
            "results": [{
                "id":menu.id,
                "chef": menu.chef_id,
                "food_category_id": menu.food_category,
                "appetiser" : menu.appetiser,
                "main": menu.main,
                "starter": menu.starter,
                "dessert": menu.dessert,
                "description": menu.description
            } for menu in chef_menus]}
        return jsonify(chef_menus), 200
    else:
        return jsonify({"results": []}), 200


# return all Menus for one chef
@chef_menu_api_blueprint.route('/chef/<chef_id>', methods=["GET"])
def menu(chef_id):
    menus = ChefMenu.select().where(ChefMenu.chef_id == chef_id)
    if menus:
        menus = {
            "message": "successful",
            "count": menus.count(),
            "results": [{
                "id":menu.id,
                "chef": menu.chef_id,
                "food_category": menu.food_category,
                "appetiser" : menu.appetiser,
                "main": menu.main,
                "starter": menu.starter,
                "dessert": menu.dessert,
                "description": menu.description
            } for menu in menus]
        }
        return jsonify(menus), 200
    else:
        return jsonify({"results": []}), 200
    
# Return one specific menu
@chef_menu_api_blueprint.route('/<menu_id>', methods=["GET"])
def specific_menu(menu_id):
    menu = ChefMenu.get_or_none(ChefMenu.id==menu_id)
    if menu:
        return jsonify({
            "menu_id": menu_id,
            "results": {
                "chef_id": menu.chef_id,
                "food_category": menu.food_category,
                "appetiser": menu.appetiser,
                "main": menu.main,
                "starter": menu.starter,
                "dessert": menu.dessert,
                "description": menu.description
            }
        }), 200
    else:
        return jsonify({
            "message": "This menu doesn't exist",
            "status": "failed"
        }),400

# GET /menus/chef/<chef_id>/<food_category>
@chef_menu_api_blueprint.route('/chef/<chef_id>/<food_category>', methods=["GET"])
def chef_category_menu(chef_id, food_category):
    chef = Chef.get_or_none(Chef.id == chef_id)
    if chef==None:
        return jsonify({"message": "This chef does not exist", "status": "failed"}), 400
    else: 
        menu = ChefMenu.get_or_none(ChefMenu.chef_id == chef_id, ChefMenu.food_category == food_category)
        if menu:
            return jsonify({
                "menu_id": menu.id,
                "results": {
                    "chef_id": menu.chef_id,
                    "food_category": menu.food_category,
                    "appetiser": menu.appetiser,
                    "main": menu.main,
                    "starter": menu.starter,
                    "dessert": menu.dessert,
                    "description": menu.description
                }
            }), 200
        else:
            existing_food_category = FoodCategory.get_or_none(FoodCategory.chef_id == chef_id, FoodCategory.category == food_category)
            if existing_food_category:
                return jsonify({"results": []}), 400
            else: 
                return jsonify(message="This chef does not have this food category yet, create one first", status="Failed"), 400



# Update
@chef_menu_api_blueprint.route('/update/<menu_id>', methods=["PUT"])
def update(menu_id):
    menu = ChefMenu.get_or_none(ChefMenu.id==menu_id)
    params = request.get_json()
    if menu and params:
        params.update({'updated_at': datetime.datetime.now()})
        for each in params:
            update = ChefMenu.update(params).where(ChefMenu.id == menu_id)
        if update.execute():
            return jsonify({
                "message": "Successfully updated", 
                "menu_id": menu.id,
                "updated_at": menu.updated_at,
                "updated_column": [each for each in params]
            })
        else:
            return jsonify({
                "message": "Unable to update, please try again",
                "status": "failed"
            }), 400
    elif menu == None:
        return jsonify({
            "message": "This menu doesn't exist",
            "status": "failed"
        }),400
    elif params == None:
        return jsonify({
            "message": "No fields are passed",
            "status": "failed"
        }), 400




# DELETE /menus/delete/<menu_id>
@chef_menu_api_blueprint.route('/delete/<menu_id>', methods = ["DELETE"])
def delete(menu_id):
    menu = ChefMenu.get_or_none(ChefMenu.id == menu_id)
    if menu:
        if menu.delete_instance():
            return jsonify({"message": "Successfully deleted", "menu_id": menu_id, "status": "success"}), 200
        else:
            return jsonify({"message": "Unable to delete", "status": "failed"}), 400
    else: 
        return jsonify({"message": "Unable to find this menu", "status": "failed"}), 400

