import os
from app import app, s3
from models.menu_image import MenuImage
from flask import Flask, request, jsonify, Blueprint

menu_images_api_blueprint = Blueprint('menu_images_api', __name__)

# GET /menu_images - Return list of menu images
@menu_images_api_blueprint.route('/<chef_id>', methods=["GET"])
def index(chef_id):
    menu_images = MenuImage.select().where(MenuImage.chef_id == chef_id)
    if menu_images:
        menu_images = [{
            "menu_images_id" : each.id,
            "chef" : each.chef_id, 
            "image_url": each.image_url
        } for each in menu_images]
        return jsonify(menu_images), 200
    else:
        return jsonify({
            "message": "No images for this chef, or chef doesnt exist",
            "status": "failed"
        }), 400

# POST /menu_images/new
@menu_images_api_blueprint.route('/new', methods=["POST"])
def new_menu_image():
    chef_id = request.json.get('chef', None)
    image_url = request.json.get('image_url', None)
    if chef_id and image_url:
        new = MenuImage(chef=chef_id, image_url=image_url)
        if new.save():
            return jsonify({
                "message": "Successully posted new image",
                "status": "success"
            }), 200
    else:
        return jsonify({
            "message": "Missing chef id or image url",
            "status": "failed"
        }), 400
  