from app import app
from models.menu_image import MenuImage
from flask import Flask, request, jsonify, Blueprint

menu_images_api_blueprint = Blueprint('menu_images_api', __name__)

# GET /menu_images - Return list of menu images
@menu_images_api_blueprint.route('/', methods=["GET"])
def index():
    menu_images = MenuImage.select()
    menu_images = [{
        "id" : each.id,
        "chef" : each.chef, 
        "image_url": each.image_url
    } for each in menu_images]

# POST /menu_images/new
@menu_images_api_blueprint.route('/new', methods=["POST"])
def new_menu_image():
    chef_id = request.json.get('chef', None)
    image_url = request.json.get('image_url', None)
    new = MenuImage(chef=chef_id, image_url=image_url)
    if new.save():
        return jsonify({
            "message": "successully posted new image",
            "status": "success"
        })