import os
from app import app, s3
import boto3, botocore
from models.menu_image import MenuImage
from models.chef_menu import ChefMenu
from models.chef import Chef

from flask import Flask, request, jsonify, Blueprint
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt_header


menu_images_api_blueprint = Blueprint('menu_images_api', __name__)



# POST /menu_images/new
@menu_images_api_blueprint.route('/new/<chef_menu_id>', methods=["POST"])
@jwt_required()
def new_menu_image(chef_menu_id): 
    existing_chef = Chef.get_or_none(Chef.email == get_jwt_identity())
    if existing_chef:
        image_path = request.json.get("image_url", None)
        # breakpoint()
        new_menu_image = MenuImage(chef=existing_chef.id, chef_menu=chef_menu_id, image_path=image_path)
        if new_menu_image.save():
            return jsonify({
                "message": "Successfully posted this menu's image",
                "chef_id": new_menu_image.chef_id,
                "menu_id": new_menu_image.chef_menu_id,
                "image_path": new_menu_image.image_path,
            }), 200


# GET /menu_images - Return list of menu images
@menu_images_api_blueprint.route('/<chef_menu_id>', methods=["GET"])
def index(chef_menu_id):
    menu_images = MenuImage.select().where(MenuImage.chef_menu == chef_menu_id)
    if menu_images:
        menu_images = [{
            "menu_images_id" : each.id,
            "chef" : each.chef_id, 
            "menu_id": each.chef_menu_id,
            "image_path": each.image_path
        } for each in menu_images]
        return jsonify(menu_images), 200
    else:
        return jsonify([]), 200

# UPDATE /menu_images
@menu_images_api_blueprint.route("/update/<chef_menu_image_id>", methods=["PUT"])
@jwt_required()
def update_image(chef_menu_image_id):
    if get_jwt_header()['type'] == "Chef":
        chef = Chef.get_or_none(Chef.email == get_jwt_identity())
        if request.content_length == 0:
            return jsonify(message="No images passed", status="failed"), 400
        elif request.files['menu_image']:
            file = request.files.get('menu_image')
            menu_image = MenuImage.get(MenuImage.chef == chef.id)
            s3.upload_fileobj(
                file,
                "foodapp-new",
                f"menus/{menu_image.chef_id}/{file.filename}",
                ExtraArgs={
                    "ACL": "public-read",
                    "ContentType": file.content_type
                }
            )
            update = MenuImage.update({MenuImage.image_path:f"https://foodapp-new.s3-ap-southeast-1.amazonaws.com/menus/{menu_image.chef_id}/{file.filename}"}).where(MenuImage.id == chef_menu_image_id).execute()
            updated_image = MenuImage.get(MenuImage.id == chef_menu_image_id)
            return jsonify({
                "message": "Successfully updated menu image",
                "menu_image_id": updated_image.id,
                "image": updated_image.image_path,
                "chef_id": updated_image.chef_id
            }), 200
    else:
        return jsonify(message="You are not logged in as Chef"), 400
   
    
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
