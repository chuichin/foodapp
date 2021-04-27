import os
from app import app, s3
import boto3, botocore
from models.menu_image import MenuImage
from models.chef_menu import ChefMenu

from flask import Flask, request, jsonify, Blueprint

menu_images_api_blueprint = Blueprint('menu_images_api', __name__)

# GET /menu_images - Return list of menu images
@menu_images_api_blueprint.route('/<chef_menu_id>', methods=["GET"])
def index(chef_menu_id):
    menu_images = MenuImage.select().where(MenuImage.chef_menu_id == chef_menu_id)
    if menu_images:
        menu_images = [{
            "menu_images_id" : each.id,
            "chef" : each.chef_id, 
            "menu_id": each.chef_menu_id,
            "image_url": each.image_url
        } for each in menu_images]
        return jsonify(menu_images), 200
    else:
        return jsonify([]), 200

# POST /menu_images/new
@menu_images_api_blueprint.route('/new/<chef_menu_id>', methods=["POST"])
def new_menu_image(chef_menu_id): 
    if request.content_length == 0:
            return jsonify(message="No images passed", status="failed"), 400
    elif request.files['menu_image']:
        file = request.files.get('menu_image')
        s3.upload_fileobj(
            file,
            "foodapp-new",
            f"menus/{chef_menu_id}/{file.filename}",
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type
            }
        )
        existing_chef = ChefMenu.get_or_none(ChefMenu.id == chef_menu_id)
        new_menu_image = MenuImage(chef=existing_chef.chef_id, chef_menu=chef_menu_id, image_path=f"https://foodapp-new.s3-ap-southeast-1.amazonaws.com/menus/{chef_menu_id}/{file.filename}")
        if new_menu_image.save(): 
            new_menu_image = MenuImage.get_or_none(MenuImage.chef_menu == chef_menu_id)
            return jsonify({
                "message": "Successfully posted this menu's image",
                "chef_id": new_menu_image.chef_id,
                "menu_id": new_menu_image.chef_menu_id,
                "image": new_menu_image.image_path,
            }), 200 
    
    
    
# DELETE /menu_images/delete/<menu_images_id>
@menu_images_api_blueprint.route('/delete/<menu_image_id>', methods=["DELETE"])
def delete(menu_image_id):
    menu_image = MenuImage.get_or_none(MenuImage.id == menu_image_id)
    if menu_image:
        if menu_image.delete_instance():
            return jsonify({
                "message": "Successfully deleted this image",
                "menu_image_id": menu_image_id,
                "status": "Success"
            }), 200
    else:
        return jsonify({
            "message": "This image does not exist",
            "status": "Failed"
        }), 400
