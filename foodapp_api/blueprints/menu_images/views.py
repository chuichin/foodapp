import os
from app import app, s3
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
    if request.file['image_url']:
        file = request.file.get('image_url')
        s3.upload_fileobj(
            file,
            # need to set .env
            os.getenv("S3_BUCKET"),
            file.filename,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type
            })
            # need to set .env
        chef_id = request.json.get('chef', None)
        image_url = f"https://{os.getenv('S3_BUCKET')}.s3-ap-southeast-1.amazonaws.com/{file.filename}"
        new = MenuImage(chef=chef_id, image_url=image_url)
        if new.save():
            return jsonify({
                "message": "successully posted new image",
                "status": "success"
            })
    