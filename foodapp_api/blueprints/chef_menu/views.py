from app import app
from flask import Blueprint, Flask, jsonify, request
from models.chef_menu import ChefMenu

chef_menu_api_blueprint = Blueprint('chef_menu_api', __name__)

@chef_menu_api_blueprint.route('/', methods=["GET"])
def chef_menu():
    chef_menus = ChefMenu.select()
    chef_menus = [{
        "id" = menu.id,
        "food_category_id" = menu.food_category_id,
        "menu" = menu.menu
    } for menu in chef_menus]
    return jsonify(chef_menus)
