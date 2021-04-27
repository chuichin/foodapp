import os
from app import app, s3
import boto3, botocore
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
        return jsonify([]), 400

# POST /menu_images/new
@menu_images_api_blueprint.route('/new/<menu_id>', methods=["POST"])
def new_menu_image():  
    if request.files['image']:
        file = request.files.get('image')
        s3.upload_fileobj(
            file,
            "foodapp-new",
            f"menu-images/{file.filename}",
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type
            })
    
    
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

